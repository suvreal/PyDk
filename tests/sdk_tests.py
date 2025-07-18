import time
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from httpx import HTTPStatusError, Response, Request
from pydantic import ValidationError

from src.py_dk_custom_facade import MyApiSDK
from src.classes.Product import Product
from src.classes.Offer import Offer


@pytest.fixture
def fake_http_client():
    mock_client = MagicMock()
    mock_client.aclose = AsyncMock()
    mock_client.post = AsyncMock(return_value={"status_code": 201, "data": {"access_token": "fake_token"}})
    mock_client.get = AsyncMock(return_value={"status_code": 200, "data": {"offers": []}})
    return mock_client


@pytest.fixture
def fake_cache_client():
    mock_cache = MagicMock()
    mock_cache.get_token = AsyncMock(return_value=("cached_token", 9999999999))
    mock_cache.save_token = AsyncMock()
    mock_cache.aclose = AsyncMock()
    return mock_cache


@pytest.mark.asyncio
async def test_product_registration_and_offer(fake_http_client, fake_cache_client):
    sdk = MyApiSDK(
        bearer="dummy-bearer",
        http_client=fake_http_client,
        token_cache_client=fake_cache_client
    )

    product = Product(
        id=uuid4(),
        name="Test Product",
        description="Test Description"
    )

    register_response = await sdk.product.register_product(product)
    assert register_response["status_code"] == 201
    fake_http_client.post.assert_called()

    offer_response = await sdk.offer.get_offer(product)
    assert offer_response["status_code"] == 200
    fake_http_client.get.assert_called()

    await sdk.aclose()
    fake_http_client.aclose.assert_called()
    fake_cache_client.aclose.assert_called()


@pytest.mark.asyncio
async def test_offer_service_returns_offer_for_product():
    from src.endpoint_implementation.get_offer import OfferService
    from src.token_manager.auth_client import AuthClient

    product = Product(
        id=uuid4(),
        name="Offer Product",
        description="To check GET offer"
    )

    mock_http_client = MagicMock()
    mock_http_client.get = AsyncMock(return_value={"status_code": 200, "data": {"offers": []}})
    mock_http_client.aclose = AsyncMock()

    fake_auth_client = MagicMock(spec=AuthClient)
    fake_auth_client.provide_token = AsyncMock(return_value="dummy-token")

    service = OfferService(
        url_template="https://example.com/api/v1/products/{}/offers",
        auth_client=fake_auth_client,
        http_client=mock_http_client
    )

    response = await service.get_offer(product)

    assert response["status_code"] == 200
    mock_http_client.get.assert_called_once()
    assert "offers" in response["data"]


@pytest.mark.asyncio
async def test_auth_client_token_fetch_without_cache(fake_http_client):
    from src.token_manager.auth_client import AuthClient
    from src.token_manager.memory_cache_adapter import MemoryCacheAdapter

    empty_cache = MemoryCacheAdapter()
    empty_cache.get_token = AsyncMock(return_value=(None, 0))
    empty_cache.save_token = AsyncMock()

    auth_client = AuthClient(
        api_url="https://example.com/api/v1/auth",
        http_client=fake_http_client,
        token_cache=empty_cache,
        bearer="dummy-bearer",
        token_ttl=295
    )

    token = await auth_client.provide_token()
    assert token == "fake_token"
    fake_http_client.post.assert_called()
    empty_cache.save_token.assert_called()


@pytest.mark.asyncio
async def test_sdk_init_with_defaults():
    sdk = MyApiSDK(bearer="dummy-bearer")
    assert sdk._http_client is not None
    assert sdk._token_cache_client is not None
    await sdk.aclose()


@pytest.mark.asyncio
async def test_product_registration_http_409_handling():
    from src.endpoint_implementation.register_product import ProductService
    from src.token_manager.auth_client import AuthClient

    product = Product(
        id=uuid4(),
        name="Conflict Product",
        description="Test Description"
    )

    mock_http_client = MagicMock()
    request = Request(method="POST", url="https://example.com")
    response = Response(status_code=409, request=request)
    error = HTTPStatusError("409 Conflict", request=request, response=response)

    mock_http_client.post = AsyncMock(side_effect=error)
    mock_http_client.aclose = AsyncMock()

    fake_auth_client = MagicMock(spec=AuthClient)
    fake_auth_client.provide_token = AsyncMock(return_value="dummy-token")

    service = ProductService("https://example.com", fake_auth_client, mock_http_client)

    with pytest.raises(HTTPStatusError) as exc_info:
        await service.register_product(product)

    assert exc_info.value.response.status_code == 409
    mock_http_client.post.assert_called()


@pytest.mark.asyncio
async def test_invalid_product_data_raises_validation_error():
    with pytest.raises(ValidationError):
        Product(
            id="invalid-uuid",
            name="Invalid Product",
            description="No UUID format"
        )


@pytest.mark.asyncio
async def test_custom_http_client_usage():
    custom_http_client = MagicMock()
    custom_http_client.aclose = AsyncMock()
    sdk = MyApiSDK(bearer="dummy-bearer", http_client=custom_http_client)
    assert sdk._http_client == custom_http_client
    await sdk.aclose()
    custom_http_client.aclose.assert_called()


@pytest.mark.asyncio
async def test_cache_fallback_on_api_error():
    from src.token_manager.auth_client import AuthClient
    from src.token_manager.memory_cache_adapter import MemoryCacheAdapter

    memory_cache = MemoryCacheAdapter()
    memory_cache.get_token = AsyncMock(return_value=("cached_token", int(time.time()) - 10))
    memory_cache.save_token = AsyncMock()

    mock_http_client = MagicMock()
    request = Request(method="POST", url="https://example.com")
    response = Response(status_code=500, request=request)
    error = HTTPStatusError("500 Server Error", request=request, response=response)

    mock_http_client.post = AsyncMock(side_effect=error)

    auth_client = AuthClient(
        api_url="https://example.com/api/v1/auth",
        http_client=mock_http_client,
        token_cache=memory_cache,
        bearer="dummy-bearer",
        token_ttl=295
    )

    with pytest.raises(HTTPStatusError):
        await auth_client.provide_token()

    mock_http_client.post.assert_called()
