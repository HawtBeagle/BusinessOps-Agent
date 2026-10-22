# A deadline limits waiting, not an already-running worker

`ToolsExecutor.execute_with_timeout` wraps a synchronous registered handler with `asyncio.to_thread` and `asyncio.timeout`. It checks registry membership and argument shape before invoking the handler with application-supplied customer context.

An expired deadline raises `ToolExecutionTimeoutError("TOOL_TIMEOUT")`. It does not forcibly terminate an already-running synchronous worker, undo side effects, confirm failure or retry the call. A handler's own TimeoutError is preserved when the wrapper's deadline did not expire.

The published settings default is five seconds, but the executor takes an explicit `timeout_seconds` argument: callers must pass their selected timeout. The tests use shorter controlled deadlines rather than waiting five seconds per test.

```bash
uv sync --frozen
uv run python -m pytest tests/test_tool_executor_standalone.py -q
```

The synchronized worker test verifies that the timeout is observed while the worker is still waiting, the handler is called once, and it can finish after the test releases it. Other tests cover argument validation, unknown tools, application context, worker-thread execution and preserving a handler's own timeout. No model or external service is called.

For an operation such as ticket creation, an unknown outcome should not be described as confirmed success or confirmed non-execution. Retrying a write safely requires an appropriate service contract, such as idempotency and operation-status tracking. Neither is implemented by this wrapper.

This snapshot publishes the standalone executor and its errors, not the full registry wiring, HTTP route, model-facing timeout observation, production authentication, ticket service, or ownership checks. Customer context is passed to the handler; the handler remains responsible for domain authorization.
