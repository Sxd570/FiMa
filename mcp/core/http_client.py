import httpx
from shared.logger import Logger

logger = Logger(__name__)

class HttpClient:
    def __init__(self, timeout: int = 10):
        self.client = httpx.AsyncClient(timeout=timeout)

    async def get(self, url: str, headers: dict = None):
        logger.debug(f"GET request to {url}")
        response = await self.client.get(url, headers=headers)
        response.raise_for_status()
        return response

    async def post(self, url: str, json: dict = None, headers: dict = None):
        logger.debug(f"POST request to {url} with payload {json}")
        response = await self.client.post(url, json=json, headers=headers)
        response.raise_for_status()
        return response

    async def put(self, url: str, json: dict = None, headers: dict = None):
        logger.debug(f"PUT request to {url} with payload {json}")
        response = await self.client.put(url, json=json, headers=headers)
        response.raise_for_status()
        return response

    async def patch(self, url: str, json: dict = None, headers: dict = None):
        logger.debug(f"PATCH request to {url} with payload {json}")
        response = await self.client.patch(url, json=json, headers=headers)
        response.raise_for_status()
        return response

    async def delete(self, url: str, headers: dict = None):
        logger.debug(f"DELETE request to {url}")
        response = await self.client.delete(url, headers=headers)
        response.raise_for_status()
        return response

    async def close(self):
        await self.client.aclose()


# Singleton instance for reuse
http_client = HttpClient()
