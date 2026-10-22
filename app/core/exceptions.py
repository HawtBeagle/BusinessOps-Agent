
class ProviderError(Exception):
    """Exception class to capture provider related errors."""

class ProviderTimeout(ProviderError):
    """The provider timed out or cannot be reached"""

class ProviderUnavailable(ProviderError):
    """The provider is not available or could not be connected"""

class ProviderMalformedResponse(ProviderError):
    """The provider returned malformed response"""



class OrderNotFound(Exception):
    """The order could not be found"""

class UnknownToolError(Exception):
    """The tool could not be found"""


class InvalidToolArgumentsError(Exception):
    """The model's tool arguments failed input-schema validation."""


class AccountNotFoundError(Exception):
    """The authenticated customer's account could not be found."""


TOOL_CALL_LIMIT_EXCEEDED_CODE = "TOOL_CALL_LIMIT_EXCEEDED"


class ToolCallLimitExceededError(Exception):
    """The tool call limit was exceeded."""


TOOL_TIMEOUT_CODE = "TOOL_TIMEOUT"


class ToolExecutionTimeoutError(Exception):
    """The application stopped waiting; the tool outcome may be unknown."""
