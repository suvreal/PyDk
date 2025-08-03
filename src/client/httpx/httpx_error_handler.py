import functools
import httpx
from src.exceptions.httpx_adapter_client_exceptions import (
    SDKException,
    NetworkError,
    APIError,
)


def handle_http_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timed out: {e}") from e
        except httpx.RequestError as e:
            raise NetworkError(f"Network error occurred: {e}") from e
        except httpx.HTTPStatusError as e:
            raise APIError(f"HTTP error: {e.response.status_code} - {e.response.text}") from e
        except Exception as e:
            raise SDKException(f"Unexpected error: {e}") from e

    return wrapper
