class SDKException(Exception):
    """Base exception for the SDK."""


class NetworkError(SDKException):
    """Raised when network issues occur (timeout, connection error)."""


class APIError(SDKException):
    """Raised when API returns an error status."""


class AuthError(APIError):
    """Raised when authentication fails."""


class ParsingError(SDKException):
    """Raised when response cannot be parsed."""
