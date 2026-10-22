GET_ORDER_STATUS_TOOL = "get_order_status"
GET_ACCOUNT_TOOL = "get_account"
SEARCH_CATALOG_TOOL = "search_catalog"
CREATE_CRM_CASE_TOOL = "create_crm_case"
INPUT_SCHEMA_KEY = "input_schema"
HANDLER_KEY = "handler"
ORDER_SERVICE_KEY = "order_service"
ACCOUNT_SERVICE_KEY = "account_service"
CATALOG_SERVICE_KEY = "catalog_service"
CRM_CASE_SERVICE_KEY = "crm_case_service"
DESCRIPTION_KEY = "description"
TYPE_KEY = "type"
FUNCTION_KEY = "function"
NAME_KEY = "name"
PARAMETERS_KEY = "parameters"
FUNCTION_TOOL_TYPE = "function"

GET_ORDER_STATUS_DESCRIPTION = (
    "Read the status of an order belonging to the signed-in customer. "
    "Requires the exact order ID; ask the customer if it is missing. "
    "Does not modify, cancel, or refund an order."
)
GET_ACCOUNT_DESCRIPTION = (
    "Read the signed-in customer's account details and support plan. "
    "Takes no arguments; the application supplies the customer identity. "
    "Does not modify the account or plan."
)
SEARCH_CATALOG_DESCRIPTION = (
    "Search the mock public plan catalog for plans supporting at least "
    "minimum_users within max_monthly_price in INR. "
    "Requires both requirements; ask for any missing value. "
    "Returns matching plans or an empty list. Does not purchase or change a plan."
)
CREATE_CRM_CASE_DESCRIPTION = (
    "Create an in-memory support case for the signed-in customer's account "
    "when the customer requests a ticket. Requires a subject and description. "
    "The application resolves account identity; do not supply account or customer IDs. "
    "Creates a record but does not resolve the issue, approve refunds, or change plans. "
    "Report creation only after a successful tool result. "
    'Argument shape: {"request": {"subject": "Delivery question", '
    '"description": "Please help with my delivery."}}. '
    "Place subject and description directly inside request. "
    "CaseDetails is a schema type name, not an argument key; do not add a CaseDetails wrapper. "
    "Use the customer's supplied values, not the example values, and preserve exact text "
    "including punctuation when requested."
)
