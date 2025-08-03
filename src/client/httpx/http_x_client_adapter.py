from src.client.httpx.httpx_error_handler import handle_http_errors
from src.client.httpx.http_client_interface import HTTPClientInterface, HTTPResponse
import httpx
from typing import Optional


class HTTPXClientAdapter(HTTPClientInterface):
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

    @handle_http_errors
    async def post(
        self,
        url: str,
        data: Optional[dict[str, str] | dict[str, str | int | float]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> HTTPResponse:
        response = await self.client.post(url, json=data, headers=headers)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}

    @handle_http_errors
    async def get(
        self,
        url: str,
        params: Optional[dict[str, str] | dict[str, str | int | float]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> HTTPResponse:
        response = await self.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}

    async def aclose(self) -> None:
        await self.client.aclose()
