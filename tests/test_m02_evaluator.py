from scripts.evaluate_m02 import check_response
import pytest


def test_wrong_id_is_not_a_pass():
    case = {"request_type": "order_status", "order_id": "00123", "damage": False, "missing_fields": []}
    body = {"analysed_response": {"request_type": "order_status", "order_id": "123", "reason": None, "summary": "Order status"}, "missing_fields": []}
    assert "order_id" in check_response(case, body)


@pytest.mark.parametrize("body", [None, {}, {"analysed_response": "not an object"}])
def test_invalid_schema_is_not_a_pass(body):
    assert check_response({}, body) == ["schema"]


def test_valid_fields_and_missing_information():
    case = {"request_type": "refund", "order_id": None, "damage": True, "missing_fields": ["order_id"]}
    body = {"analysed_response": {"request_type": "refund", "order_id": None, "reason": "damaged", "summary": "Refund requested"}, "missing_fields": ["order_id"]}
    assert check_response(case, body) == []
    body["missing_fields"] = []
    assert check_response(case, body) == ["missing_fields"]
    body["analysed_response"]["reason"] = None
    assert check_response(case, body) == ["reason", "missing_fields"]
