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
        bearer="" # get your own from https://python.exercise.applifting.cz/assignment/sdk/
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
    response_register = await sdk.product.register_product(product)
    print("Register response:", response_register)

    # Offer obtaining
    response_offers = await sdk.offer.get_offer(product)
    print("Offer response:", response_offers)

    # End client and release resources
    await sdk.aclose()


if __name__ == "__main__":
    asyncio.run(main())
