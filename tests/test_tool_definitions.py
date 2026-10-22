import json

from pydantic import BaseModel, ConfigDict

from app.schemas.common_llm_request_response import LLMRequest, ToolDefinition
from app.tools.tool_definitions import build_tool_definitions


class OrderLookupInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    order_id: str


def test_definitions_contain_name_description_and_argument_schema_only():
    def handler(*args):
        raise AssertionError("Building definitions must not execute a tool")

    registry = {
        "get_order_status": {
            "description": "Read an order status; requires its order ID.",
            "input_schema": OrderLookupInput,
            "handler": handler,
        }
    }

    definitions = build_tool_definitions(registry)

    assert definitions == [ToolDefinition(
        name="get_order_status",
        description=registry["get_order_status"]["description"],
        parameters=OrderLookupInput.model_json_schema(),
    )]
    serialized = definitions[0].model_dump()
    assert set(serialized) == {"name", "description", "parameters"}
    assert serialized["parameters"]["required"] == ["order_id"]
    assert serialized["parameters"]["additionalProperties"] is False
    json.dumps(serialized)
    assert registry["get_order_status"]["handler"] is handler


def test_empty_registry_produces_no_definitions():
    assert build_tool_definitions({}) == []


def test_common_request_accepts_generated_tool_definitions():
    registry = {
        "get_order_status": {
            "description": "Read an order status.",
            "input_schema": OrderLookupInput,
        }
    }
    definitions = build_tool_definitions(registry)

    request = LLMRequest(
        model="test-model", messages=[], temperature=0, tools=definitions,
    )

    assert request.tools == definitions
    assert request.model_dump()["tools"][0]["name"] == "get_order_status"
