from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RequestType(str, Enum):
    REFUND = "refund"
    ORDER_STATUS = "order_status"
    ADDRESS_CHANGE = "address_change"
    UNKNOWN = "unknown"

class AnalyseRequest(BaseModel):
    customer_message: str
    model: str
    temperature: float

class AnalyseResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_type: RequestType
    order_id: str | None
    reason: str | None
    summary: str = Field(min_length=1)


class AnalyseResponse(BaseModel):
    analysed_response: AnalyseResult
    missing_fields: list[str]
