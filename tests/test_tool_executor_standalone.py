import asyncio
import threading
from unittest.mock import Mock

import pytest
from pydantic import BaseModel, ConfigDict, Field

from app.core.exceptions import (
    InvalidToolArgumentsError, ToolExecutionTimeoutError, UnknownToolError,
)
from app.tools.tools_executor import ToolsExecutor


class LookupInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    order_id: str = Field(min_length=1)


def executor_for(handler):
    return ToolsExecutor({"lookup": {"input_schema": LookupInput, "handler": handler}})


def test_valid_arguments_and_application_context_reach_handler():
    handler = Mock(return_value="processing")
    result = executor_for(handler).execute("lookup", {"order_id": "ORD-1"}, "customer-1")
    assert result == "processing"
    handler.assert_called_once_with(LookupInput(order_id="ORD-1"), "customer-1")


def test_unknown_tool_never_executes_handler():
    handler = Mock()
    with pytest.raises(UnknownToolError):
        executor_for(handler).execute("unregistered", {}, "customer-1")
    handler.assert_not_called()


@pytest.mark.parametrize("arguments", [{}, {"order_id": None}, {"order_id": "   "}])
def test_invalid_arguments_never_execute_handler(arguments):
    handler = Mock()
    with pytest.raises(InvalidToolArgumentsError):
        executor_for(handler).execute("lookup", arguments, "customer-1")
    handler.assert_not_called()


def test_async_wrapper_runs_handler_on_another_thread():
    main_thread = threading.get_ident()
    handler = Mock(side_effect=lambda request, customer: threading.get_ident())
    worker_thread = asyncio.run(executor_for(handler).execute_with_timeout(
        "lookup", {"order_id": "ORD-1"}, "customer-1", 1,
    ))
    assert worker_thread != main_thread
    handler.assert_called_once()


def test_timeout_stops_waiting_but_worker_can_finish_without_retry():
    started = threading.Event()
    release = threading.Event()
    finished = threading.Event()

    def slow_handler(request, customer):
        started.set()
        try:
            release.wait(timeout=5)
            return "completed"
        finally:
            finished.set()

    handler = Mock(side_effect=slow_handler)

    async def scenario():
        try:
            with pytest.raises(ToolExecutionTimeoutError, match="TOOL_TIMEOUT"):
                await executor_for(handler).execute_with_timeout(
                    "lookup", {"order_id": "ORD-1"}, "customer-1", 0.1,
                )
            assert started.is_set()
            assert not finished.is_set()
            handler.assert_called_once()
        finally:
            release.set()

    asyncio.run(scenario())
    assert finished.is_set()


def test_handler_timeout_is_not_mislabeled_as_executor_deadline():
    original = TimeoutError("Backend-specific timeout")
    handler = Mock(side_effect=original)
    with pytest.raises(TimeoutError) as caught:
        asyncio.run(executor_for(handler).execute_with_timeout(
            "lookup", {"order_id": "ORD-1"}, "customer-1", 1,
        ))
    assert type(caught.value) is TimeoutError
    assert caught.value.args == original.args
    handler.assert_called_once()
