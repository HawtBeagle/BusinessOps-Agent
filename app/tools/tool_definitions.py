from app.schemas.common_llm_request_response import ToolDefinition
from app.tools.tool_constants import (
    DESCRIPTION_KEY,
    INPUT_SCHEMA_KEY,
)

def build_tool_definitions(registry: dict) -> list[ToolDefinition]:
    tool_definitions = []

    for tool_name, tool in registry.items():
        definition = ToolDefinition(
            name=tool_name,
            description=tool[DESCRIPTION_KEY],
            parameters=tool[INPUT_SCHEMA_KEY].model_json_schema(),
        )

        tool_definitions.append(definition)

    return tool_definitions
