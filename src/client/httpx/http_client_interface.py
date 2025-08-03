from abc import ABC, abstractmethod
from typing import Optional, Any, TypedDict


class HTTPResponse(TypedDict):
    status_code: int
    data: Any


class HTTPClientInterface(ABC):
    @abstractmethod
    async def post(
        self,
        url: str,
        data: Optional[dict[str, str] | dict[str, str | int | float]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> HTTPResponse:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        url: str,
        params: Optional[dict[str, str] | dict[str, str | int | float]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> HTTPResponse:
        raise NotImplementedError

    @abstractmethod
    async def aclose(self) -> None:
        raise NotImplementedError
