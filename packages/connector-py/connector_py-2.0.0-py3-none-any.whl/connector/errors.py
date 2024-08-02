from abc import abstractmethod
from enum import StrEnum
from types import FunctionType
from typing import Any, Callable, List, Tuple

from connector.serializers.lumos import ErrorResp


class ErrorCodes(StrEnum):
    """
    Error codes for Lumos connector.
    """

    NOT_FOUND = "not_found"
    INTERNAL_ERROR = "internal_error"
    UNAUTHORIZED = "unauthorized"
    BAD_REQUEST = "bad_request"
    PERMISSION_DENIED = "permission_denied"
    NOT_IMPLEMENTED = "not_implemented"
    UNEXPECTED = "unexpected_error"
    UNSUPPORTED = "unsupported_operation"


ErrorHandler = (
    Callable[
        [Exception, FunctionType, ErrorResp, str | ErrorCodes | None],
        ErrorResp | Any,
    ]
    | None
)
ErrorMap = List[Tuple[Any, ErrorHandler, str | ErrorCodes | None]]


# Custom error
class ConnectorError(Exception):
    """
    Base exception class for Lumos connectors.
    Preferred way to raise exceptions inside the conenctors.
    `raise ConnectorError(message, error_code)`

    message: str (Custom error message)
    error_code: str | ErrorCodes (The actual error code, eg. "internal_error")
    """

    def __init__(self, message: str, error_code: str | ErrorCodes):
        self.error_code = error_code.value if isinstance(error_code, ErrorCodes) else error_code
        self.message = message


class ExceptionHandler:
    """
    Abstract class for handling exceptions.
    """

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def handle(
        e: Exception,
        original_func: FunctionType,
        response: ErrorResp,
        error_code: str | ErrorCodes | None = None,
    ) -> ErrorResp:
        """
        Handle an exception. (ErrorHandler signature typing)

        e: Exception (An exception that was raised)
        original_func: FunctionType (The original method that was called, eg. validate_credentials)
        response: ErrorResp (The output of the connector call)
        error_code: str | ErrorCodes | None (The actual error code, eg. "internal_error")
        """
        return response


class DefaultHandler(ExceptionHandler):
    """
    Default exception handler that handles the basic HTTPX/GQL extraction (etc.) and chains onto the global handler.
    """

    @staticmethod
    def handle(
        e: Exception,
        original_func: FunctionType,
        response: ErrorResp,
        error_code: str | ErrorCodes | None = None,
    ) -> ErrorResp:
        status_code: int | None = None

        # HTTPX HTTP Status code
        if hasattr(e, "response") and hasattr(e.response, "status_code"):
            status_code = e.response.status_code
        # GraphQL error code
        if hasattr(e, "code"):
            status_code = e.code

        # Populating some base info
        response.response.message = e.message if hasattr(e, "message") else str(e)
        response.response.status_code = status_code
        response.response.raised_in = f"{original_func.__module__}:{original_func.__name__}"
        response.response.raised_by = f"{e.__class__.__name__}"

        # ConnectorError already has an error code attached, so we need to chain
        if isinstance(e, ConnectorError):
            response.response.error_code = (
                f"{error_code}.{e.error_code}" if error_code else f"{e.error_code}"
            )
        else:
            # Otherwise, it is an unexpected error from an app_id
            response.response.error_code = (
                f"{error_code}.{ErrorCodes.UNEXPECTED.value}"
                if error_code
                else f"{ErrorCodes.UNEXPECTED.value}"
            )

        return response
