import time
from src.client.http_client_interface import HTTPClientInterface
from src.endpoint_implementation.authenticate import AuthService
from src.token_manager.cache_interface import AccessTokenCacheInterface


class AuthClient:
    def __init__(
        self,
        api_url: str,
        http_client: HTTPClientInterface,
        token_cache: AccessTokenCacheInterface,
        bearer: str,
        token_ttl: int,
    ):
        self._api_url = api_url
        self._http_client = http_client
        self._token_cache = token_cache
        self._bearer = bearer
        self._token_ttl = token_ttl

    async def provide_token(self) -> str:
        token, expires_at = await self._token_cache.get_token()
        if expires_at > int(time.time()):
            return token
        auth_service = AuthService(self._api_url, self._bearer, self._http_client)
        access_token = await auth_service.fetch_access_token()
        await self._token_cache.save_token(access_token, int(time.time()) + self._token_ttl)
        return access_token
