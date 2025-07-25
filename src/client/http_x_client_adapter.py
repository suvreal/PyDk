import httpx
from typing import Any, Optional

from src.client.http_client_interface import HTTPClientInterface


class HTTPXClientAdapter(HTTPClientInterface):
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.aclose()

    async def post(
        self,
        url: str,
        data: Optional[dict[Any, Any]] = None,
        headers: Optional[dict[Any, Any]] = None,
    ) -> dict[str, Any]:
        response = await self.client.post(url, json=data, headers=headers)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}

    async def get(
        self,
        url: str,
        params: Optional[dict[Any, Any]] = None,
        headers: Optional[dict[Any, Any]] = None,
    ) -> dict[str, Any]:
        response = await self.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}

    async def put(
        self,
        url: str,
        data: Optional[dict[Any, Any]] = None,
        headers: Optional[dict[Any, Any]] = None,
    ) -> dict[str, Any]:
        response = await self.client.put(url, json=data, headers=headers)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}

    async def patch(
        self,
        url: str,
        data: Optional[dict[Any, Any]] = None,
        headers: Optional[dict[Any, Any]] = None,
    ) -> dict[str, Any]:
        response = await self.client.patch(url, json=data, headers=headers)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}

    async def delete(
        self,
        url: str,
        params: Optional[dict[Any, Any]] = None,
        headers: Optional[dict[Any, Any]] = None,
    ) -> dict[str, Any]:
        response = await self.client.delete(url, params=params, headers=headers)
        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}

    async def aclose(self) -> None:
        await self.client.aclose()
