# From a registry entry to a model-facing tool definition

`build_tool_definitions` converts a supplied registry into provider-neutral `ToolDefinition` objects with a name, description and JSON argument schema. The Pydantic input model provides that schema.

The handler stays inside the application. Converting the registry does not execute handlers, authorize actions, look up orders or call a model. The provider-neutral definitions still need an adapter before sending them to a particular model provider.

```bash
uv sync --frozen
uv run python -m pytest tests/test_tool_definitions.py -q
```

The tests use a small local registry to verify the serialized fields, required order ID, lack of handler exposure, empty-registry behaviour and compatibility with the common LLM request. No model or backend service is called.

This incremental publication does not yet contain the application's full registry assembly, execution/ownership checks, model-provider tool adapter or runnable tool-calling endpoint. Those local components will be published separately after isolated verification.
