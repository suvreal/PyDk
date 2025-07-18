from src.classes.Product import Product
from src.client.http_client_interface import HTTPClientInterface
from src.token_manager.auth_client import AuthClient


class OfferService:
    def __init__(
        self, url_template: str, auth_client: AuthClient, http_client: HTTPClientInterface
    ):
        self._url_template = url_template
        self._auth_client = auth_client
        self._http_client = http_client

    async def get_offer(self, product: Product) -> dict:
        token = await self._auth_client.provide_token()
        return await self._http_client.get(
            url=self._url_template.format(product.id), headers={"Bearer": token}
        )
