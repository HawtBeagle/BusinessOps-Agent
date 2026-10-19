import pytest
from pydantic import ValidationError

from app.schemas.business_req_resp import AnalyseResult, RequestType
from app.services.business_validation_service import find_missing_business_information

TEST_SUMMARY = "Customer requests a refund."
STATUS_SUMMARY = "Customer asks about their order status."
STATUS_ORDER_ID = "123"
ORDER_ID_FIELD = "order_id"
REASON_FIELD = "reason"
SUMMARY_FIELD = "summary"
EXTRA_FIELD = "extra"
MISSING_ERROR = "missing"
EXTRA_ERROR = "extra_forbidden"
LENGTH_ERROR = "string_too_short"
LOCATION_KEY = "loc"
TYPE_KEY = "type"


@pytest.mark.parametrize("missing_field", [ORDER_ID_FIELD, REASON_FIELD])
def test_omitted_nullable_key_is_rejected(missing_field):
    payload = AnalyseResult(
        request_type=RequestType.REFUND,
        order_id=None,
        reason=None,
        summary=TEST_SUMMARY,
    ).model_dump()
    payload.pop(missing_field)

    with pytest.raises(ValidationError) as exc_info:
        AnalyseResult.model_validate(payload)

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0][LOCATION_KEY] == (missing_field,)
    assert errors[0][TYPE_KEY] == MISSING_ERROR


@pytest.mark.parametrize(
    "order_id, expected_missing",
    [(None, [ORDER_ID_FIELD]), (STATUS_ORDER_ID, [])],
    ids=["missing-order-id", "provided-order-id"],
)
def test_order_status_requires_only_order_id(order_id, expected_missing):
    result = AnalyseResult(
        request_type=RequestType.ORDER_STATUS,
        order_id=order_id,
        reason=None,
        summary=STATUS_SUMMARY,
    )

    assert find_missing_business_information(result) == expected_missing


def test_valid_response_accepted() -> None:
    result = AnalyseResult(
        request_type=RequestType.REFUND,
        order_id="#123",
        reason="Order arrived damaged",
        summary="Customer requests refund because the order arrived damaged",
    )

    assert result.request_type == RequestType.REFUND
    assert result.order_id == "#123"

def test_invalid_requesttype_not_accepted() -> None:
    with pytest.raises(ValidationError):
        result = AnalyseResult(
            request_type="Example",
            order_id="#123",
            reason="Order arrived damaged",
            summary="Customer requests refund because the order arrived damaged",
        )

def test_extra_field_not_accepted() -> None:
    with pytest.raises(ValidationError) as exc_info:
        result = AnalyseResult(
            request_type=RequestType.REFUND,
            order_id="#123",
            reason=None,
            summary=TEST_SUMMARY,
            extra="this is extra field"
        )
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0][LOCATION_KEY] == (EXTRA_FIELD,)
    assert errors[0][TYPE_KEY] == EXTRA_ERROR

def test_summary_improper_field_length_not_accepted() -> None:
    with pytest.raises(ValidationError) as exc_info:
        result = AnalyseResult(
            request_type=RequestType.REFUND,
            order_id=None,
            reason="Order arrived damaged",
            summary="",
        )
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0][LOCATION_KEY] == (SUMMARY_FIELD,)
    assert errors[0][TYPE_KEY] == LENGTH_ERROR


def test_missing_required_fields_not_accepted() -> None:
    with pytest.raises(ValidationError):
        result = AnalyseResult(
            request_type=RequestType.REFUND,
        )

def test_missing_business_information_accepted() -> None:
    result = AnalyseResult(
        request_type=RequestType.REFUND,
        order_id=None,
        reason=None,
        summary="Customer requests refund because the order arrived damaged",
    )

    assert result.order_id is None
    assert result.reason is None


def test_missing_order_id() -> None:
    result = AnalyseResult(
        request_type=RequestType.REFUND,
        order_id=None,
        reason="Order arrived damaged",
        summary="Customer requests refund because the order arrived damaged",
    )

    missing_fields = find_missing_business_information(result)
    assert missing_fields == ["order_id"]

def test_missing_reason() -> None:
    result = AnalyseResult(
        request_type=RequestType.REFUND,
        reason=None,
        order_id="#123",
        summary="Customer requests refund because the order arrived damaged",
    )

    missing_fields = find_missing_business_information(result)
    assert missing_fields == ["reason"]

def test_missing_business_fields() -> None:
    result = AnalyseResult(
        request_type=RequestType.REFUND,
        order_id=None,
        reason=None,
        summary="Customer requests refund because the order arrived damaged",
    )

    missing_fields = find_missing_business_information(result)
    assert missing_fields == ["order_id", "reason"]

def test_business_no_missing_fields() -> None:
    result = AnalyseResult(
        request_type=RequestType.REFUND,
        order_id="#123",
        reason="Order arrived damaged",
        summary="Customer requests refund because the order arrived damaged",
    )

    missing_fields = find_missing_business_information(result)
    assert missing_fields == []


def test_valid_schema_cannot_detect_an_inferred_refund_intent() -> None:
    # The customer only reported damage; this simulated output invents an action.
    # Neither field validation nor presence checks compare it with the message.
    result = AnalyseResult.model_validate_json(
        '{"request_type":"refund","order_id":"123",'
        '"reason":"damaged","summary":"Customer reports order 123 is damaged."}'
    )

    assert result.request_type is RequestType.REFUND
    assert find_missing_business_information(result) == []
