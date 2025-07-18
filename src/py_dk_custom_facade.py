from src.client.http_client_interface import HTTPClientInterface
from src.client.http_x_client_adapter import HTTPXClientAdapter
from src.token_manager.auth_client import AuthClient
from src.endpoint_implementation.register_product import ProductService
from src.endpoint_implementation.get_offer import OfferService
from src.token_manager.cache_interface import AccessTokenCacheInterface
from src.token_manager.sqlite_cache_adapter import SQLiteCacheAdapter

import asyncio

AUTH_PATH = "/api/v1/auth"
OFFER_PATH = "/api/v1/products/{}/offers"
PRODUCT_PATH = "/api/v1/products/register"
DEFAULT_API_URL = "https://python.exercise.applifting.cz"
TTL_SECONDS = 295


class MyApiSDK:
    def __init__(
        self,
        bearer: str,
        api_url: str = DEFAULT_API_URL,
        product_path: str = PRODUCT_PATH,
        offer_path: str = OFFER_PATH,
        auth_path: str = AUTH_PATH,
        token_ttl: int = TTL_SECONDS,
        http_client: HTTPClientInterface | None = None,
        token_cache_client: AccessTokenCacheInterface | None = None,
    ):
        self._bearer = bearer
        self._http_client = http_client or HTTPXClientAdapter()
        self._token_cache_client = token_cache_client or SQLiteCacheAdapter()

        self._auth_client = AuthClient(
            api_url + auth_path,
            self._http_client,
            self._token_cache_client,
            self._bearer,
            token_ttl,
        )

        self.product = ProductService(api_url + product_path, self._auth_client, self._http_client)

        self.offer = OfferService(api_url + offer_path, self._auth_client, self._http_client)

    async def aclose(self):
        await self._http_client.aclose()

        close_method = getattr(self._token_cache_client, "aclose", None)
        if close_method and asyncio.iscoroutinefunction(close_method):
            await close_method()
