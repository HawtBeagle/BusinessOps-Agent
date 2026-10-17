from enum import Enum
from typing import Any

from pydantic import BaseModel, computed_field, Field


class Role(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
    TOOL = "tool"

class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any]

class LLMMessage(BaseModel):
    role: Role
    content: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_name: str | None = None

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]

class LLMRequest(BaseModel):
    model: str | None
    messages: list[LLMMessage]
    temperature: float | None
    provider: str | None = "real"
    output_schema: dict[str, Any] | None = None
    tools: list[ToolDefinition] | None = None


class LLMResponse(BaseModel):
    model: str | None
    provider: str | None
    content: str | None
    input_tokens: int | None = 0
    output_tokens: int | None = 0
    latency_ms: float = 0
    finish_reason: str | None
    tool_calls: list[ToolCall] = Field(default_factory=list)

    @computed_field
    @property
    def total_tokens(self) -> int:
        return (self.input_tokens or 0) + (self.output_tokens or 0)
