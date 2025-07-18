from src.token_manager.cache_interface import AccessTokenCacheInterface


class MemoryCacheAdapter(AccessTokenCacheInterface):
    def __init__(self):
        self._token = None
        self._expires_at = 0

    async def get_token(self) -> tuple[str, int]:
        if self._token is None or self._expires_at is None:
            raise ValueError("Token cache returned None unexpectedly.")

        return self._token, self._expires_at

    async def save_token(self, token: str, expires_at: int) -> None:
        self._token = token
        self._expires_at = expires_at
