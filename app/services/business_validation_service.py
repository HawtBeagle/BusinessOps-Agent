from app.schemas.business_req_resp import AnalyseResult, RequestType

ORDER_ID_FIELD = "order_id"
REASON_FIELD = "reason"


def find_missing_business_information(result: AnalyseResult) -> list[str]:

    missing_fields = []

    if result.request_type in (RequestType.REFUND, RequestType.ORDER_STATUS):
        if result.order_id is None:
            missing_fields.append(ORDER_ID_FIELD)

    if result.request_type == RequestType.REFUND:
        if result.reason is None:
            missing_fields.append(REASON_FIELD)

    return missing_fields
