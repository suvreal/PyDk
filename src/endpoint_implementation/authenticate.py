from src.client.http_client_interface import HTTPClientInterface
from src.endpoint_implementation.correct_response import CorrectResponse


class AuthService:
    def __init__(self, url: str, bearer_token: str, http_client: HTTPClientInterface):
        self._url = url
        self._bearer_token = bearer_token
        self._http_client = http_client

    async def fetch_access_token(self) -> str:
        auth_response = await self._http_client.post(
            url=self._url, headers={"Bearer": self._bearer_token}
        )
        if CorrectResponse.is_correct(auth_response["status_code"]):
            return auth_response["data"]["access_token"]
        raise ValueError(f"Auth failed: {auth_response}")
