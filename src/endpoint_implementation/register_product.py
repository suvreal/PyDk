from src.classes.Product import Product
from src.client.httpx.http_client_interface import HTTPClientInterface
from src.token_manager.auth_client import AuthClient


class ProductService:
    def __init__(self, url: str, auth_client: AuthClient, http_client: HTTPClientInterface):
        self._url = url
        self._auth_client = auth_client
        self._http_client = http_client

    async def register_product(self, product: Product) -> Product:
        token = await self._auth_client.provide_token()
        product_data = product.normalize()
        response = await self._http_client.post(
            url=self._url,
            data=product_data,
            headers={"Bearer": token},
        )

        return Product.from_response(response, product)
