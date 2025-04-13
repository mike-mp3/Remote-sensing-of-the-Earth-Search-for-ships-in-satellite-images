import httpx
from pydantic import HttpUrl


class BaseHttpClient:
    def __init__(self, base_url: HttpUrl, timeout: float = 10.0):
        self.base_url = str(base_url).rstrip("/")
        self.timeout = timeout

    async def __do_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
