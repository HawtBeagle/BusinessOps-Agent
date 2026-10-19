import json

import pytest
from pydantic import ValidationError

from app.schemas.business_req_resp import AnalyseResult, RequestType


REQUEST_TYPE_FIELD = "request_type"
ORDER_ID_FIELD = "order_id"
REASON_FIELD = "reason"
SUMMARY_FIELD = "summary"
LOCATION_KEY = "loc"
TYPE_KEY = "type"
STRING_TYPE_ERROR = "string_type"
ENUM_ERROR = "enum"
TEST_SUMMARY = "Customer asks about their order."
LEADING_ZERO_ID = "00123"
ALPHANUMERIC_ID = "ORD-ABC-42"


def valid_payload():
    return {
        REQUEST_TYPE_FIELD: RequestType.ORDER_STATUS.value,
        ORDER_ID_FIELD: LEADING_ZERO_ID,
        REASON_FIELD: None,
        SUMMARY_FIELD: TEST_SUMMARY,
    }


@pytest.mark.parametrize(
    ("field", "invalid_value", "expected_error"),
    [
        (ORDER_ID_FIELD, 123, STRING_TYPE_ERROR),
        (REASON_FIELD, {}, STRING_TYPE_ERROR),
        (SUMMARY_FIELD, [], STRING_TYPE_ERROR),
        (REQUEST_TYPE_FIELD, True, ENUM_ERROR),
    ],
    ids=["numeric-order-id", "object-reason", "array-summary", "boolean-request-type"],
)
def test_wrong_json_field_type_is_rejected(field, invalid_value, expected_error):
    payload = valid_payload()
    payload[field] = invalid_value

    # Use the same JSON validation boundary as LLMService, without adding
    # strict=True only in the test and accidentally testing different behavior.
    with pytest.raises(ValidationError) as exc_info:
        AnalyseResult.model_validate_json(json.dumps(payload))

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0][LOCATION_KEY] == (field,)
    assert errors[0][TYPE_KEY] == expected_error


@pytest.mark.parametrize("order_id", [LEADING_ZERO_ID, ALPHANUMERIC_ID, None])
def test_valid_json_enum_strings_and_nullable_fields_are_preserved(order_id):
    payload = valid_payload()
    payload[ORDER_ID_FIELD] = order_id

    result = AnalyseResult.model_validate_json(json.dumps(payload))

    assert result.request_type == RequestType.ORDER_STATUS
    assert result.order_id == order_id
    assert result.reason is None
    assert result.summary == TEST_SUMMARY
