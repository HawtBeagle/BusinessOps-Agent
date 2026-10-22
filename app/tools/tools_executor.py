import asyncio

from pydantic import ValidationError

from app.core.exceptions import (
    UnknownToolError, InvalidToolArgumentsError, ToolExecutionTimeoutError, TOOL_TIMEOUT_CODE,
)

INVALID_TOOL_ARGUMENTS_CODE = "INVALID_TOOL_ARGUMENTS"


class ToolsExecutor:
    def __init__(self, registry: dict):
        self._registry = registry

    async def execute_with_timeout(
        self,
        tool_name: str,
        arguments: dict,
        authenticated_customer_id: str,
        timeout_seconds: float,
    ):
        # A deadline stops waiting, not an already-running synchronous worker.
        deadline = asyncio.timeout(timeout_seconds)
        try:
            async with deadline:
                return await asyncio.to_thread(
                    self.execute,
                    tool_name=tool_name,
                    arguments=arguments,
                    authenticated_customer_id=authenticated_customer_id,
                )
        except TimeoutError as exc:
            if not deadline.expired():
                raise
            raise ToolExecutionTimeoutError(TOOL_TIMEOUT_CODE) from exc

    def execute(self, tool_name: str, arguments: dict, authenticated_customer_id: str):

        tool = self._registry.get(tool_name)
        if tool is None:
            raise UnknownToolError("UNKNOWN_TOOL")

        input_schema = tool["input_schema"]
        try:
            validated_request = input_schema.model_validate(arguments)
        except ValidationError as exc:
            raise InvalidToolArgumentsError(INVALID_TOOL_ARGUMENTS_CODE) from exc

        handler = tool["handler"]

        return handler(
            validated_request,
            authenticated_customer_id,
        )
