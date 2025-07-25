import asyncio
from uuid import uuid4
from src.classes.Product import Product
from src.py_dk_custom_facade import MyApiSDK

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


async def main():
    # MyApiSDK init for API - https://python.exercise.applifting.cz/docs#/default/auth_api_v1_auth_post
    sdk = MyApiSDK(
        bearer="YOUR_BEARER_TOKEN"
        # get your own from https://python.exercise.applifting.cz/assignment/sdk/
        # optional - set custom api_url - str
        # optional - set custom product_path  - str
        # optional - set custom offer_path  - str
        # optional - set custom auth_path - str
        # optional - set custom token_ttl - int
        # optional - add your HTTP client by support of interface HTTPClientInterface - http_client=CustomHTTPClient(),
        # optional - add your TOKEN CACHE client by support AccessTokenCacheInterface - token_cache_client=MemoryCacheAdapter(),
    )

    # Test product data
    product = Product(
        id=uuid4(),
        name="Example Product",
        description="Example Description"
    )

    # Product registration
    response_register = await sdk.register_product(product)
    print("Register response: ")
    print(response_register.id)
    print(response_register.name)
    print(response_register.description)

    # Offer obtaining
    response_offers = await sdk.get_offers(product)
    print("Offer response: ")
    print(response_offers)

    # Get filled product Offers
    print("Product Offers: ")
    print(product.offers)

    # Product final
    print("Product final: ")
    print(product)

    # End client and release resources
    await sdk.aclose()


if __name__ == "__main__":
    asyncio.run(main())
