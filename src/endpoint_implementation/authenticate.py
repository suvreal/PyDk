from src.client.httpx.http_client_interface import HTTPClientInterface
from src.utils.correct_response import CorrectResponse


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
            access_token = auth_response["data"]["access_token"]
            if not isinstance(access_token, str):
                raise ValueError(f"Auth failed - inobtainable access token: {auth_response}")
            return access_token
        raise ValueError(f"Auth failed: {auth_response}")
