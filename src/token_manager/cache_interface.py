from abc import ABC, abstractmethod


class AccessTokenCacheInterface(ABC):
    @abstractmethod
    async def get_token(self) -> tuple[str, int]:
        pass

    @abstractmethod
    async def save_token(self, token: str, expires_at: int) -> None:
        pass
