from abc import ABC, abstractmethod


class HTTPClientInterface(ABC):
    @abstractmethod
    async def post(self, url: str, data: dict | None = None, headers: dict | None = None) -> dict:
        raise NotImplementedError("POST method must be implemented by subclass.")

    @abstractmethod
    async def get(self, url: str, params: dict | None = None, headers: dict | None = None) -> dict:
        raise NotImplementedError("GET method must be implemented by subclass.")

    @abstractmethod
    async def put(self, url: str, data: dict | None = None, headers: dict | None = None) -> dict:
        raise NotImplementedError("PUT method must be implemented by subclass.")

    @abstractmethod
    async def patch(self, url: str, data: dict | None = None, headers: dict | None = None) -> dict:
        raise NotImplementedError("PATCH method must be implemented by subclass.")

    @abstractmethod
    async def delete(
        self, url: str, params: dict | None = None, headers: dict | None = None
    ) -> dict:
        raise NotImplementedError("DELETE method must be implemented by subclass.")
