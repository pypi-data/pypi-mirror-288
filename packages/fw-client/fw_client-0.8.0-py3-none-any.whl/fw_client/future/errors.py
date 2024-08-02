"""Flywheel client errors."""

from httpx import HTTPStatusError

__all__ = [
    "ClientError",
    "Conflict",
    "ConnectionError",
    "HTTPStatusError",
    "NotFound",
    "ServerError",
]


class ClientError(HTTPStatusError):
    """The server returned a response with a 4xx status code."""


class NotFound(HTTPStatusError):
    """The server returned a response with a 404 status code."""


class Conflict(HTTPStatusError):
    """The server returned a response with a 409 status code."""


class ServerError(HTTPStatusError):
    """The server returned a response with a 5xx status code."""


class ValidationError(Exception):
    """Raised when client configuration is not valid."""


def http_error_str(self) -> str:  # pragma: no cover
    """Return the string representation of an HTTPError."""
    request = self.request or self.response.request
    msg = (
        f"{request.method} {self.response.url} - "
        f"{self.response.status_code} {self.response.reason_phrase}"
    )
    return msg
