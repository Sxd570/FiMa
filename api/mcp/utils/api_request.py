import httpx
from .logger import Logger
import os
from dotenv import load_dotenv

load_dotenv()
logger = Logger(__name__)


class APIRequest:
    def __init__(self, http_method, endpoint, payload=None):
        self.http_method = http_method
        self.endpoint = endpoint
        self.payload = payload
        self.url = self.generate_url(endpoint)
        self.headers = {
            "Content-Type": "application/json"
        }

    def generate_url(self, endpoint):
        api = "api"

        base_url = os.getenv("API_BASE_URL")
        port = os.getenv("API_PORT")
        version = os.getenv("API_VERSION")

        if not base_url or not port or not version:
            missing = [k for k, v in {
                "API_BASE_URL": base_url,
                "API_PORT": port,
                "API_VERSION": version
            }.items() if not v]
            logger.error(f"Missing environment variables: {', '.join(missing)}")
            raise ValueError(f"Missing env vars: {', '.join(missing)}")

        return f"{base_url}:{port}/{api}/{version}{endpoint}"

    def execute(self):
        try:
            response = httpx.request(
                method=self.http_method,
                url=self.url,
                headers=self.headers,
                json=self.payload
            )
            if response.status_code in (200, 202):
                return response.json()
            else:
                logger.warning(
                    f"API returned non-success status {response.status_code} "
                    f"for {self.http_method} {self.url}: {response.text}"
                )
                return {}
        except Exception as e:
            logger.error(f"Error occurred while making API request: {e}")
            return {}
        


# if __name__ == "__main__":
#     method = "GET"
#     endpoint = "/goals/dashboard/be2323eb-38ac-5a90-85a3-26b6f4fdfb25"
#     payload = {
#         "limit": 5,
#         "offset": 0
#     }
#     api_request = APIRequest("GET", endpoint, payload)
#     response = api_request.execute()
#     print(response)