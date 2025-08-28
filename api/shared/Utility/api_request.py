import json
import requests
from shared.logger import Logger
import os
from dotenv import load_dotenv

load_dotenv()

logger = Logger(__name__)


class APIRequest:
    def __init__(self, http_method, endpoint, payload):
        self.http_method = http_method
        self.endpoint = endpoint
        self.payload = payload
        self.url = self.generate_url(endpoint)
        self.headers = {"Content-Type": "application/json"}

    def generate_url(self, endpoint):
        api = "api"
        
        base_url = os.getenv("API_BASE_URL")
        if not base_url:
            logger.error("API_BASE_URL is not set in environment variables.")
            raise ValueError("API_BASE_URL is not set in environment variables.")
        
        port = os.getenv("API_PORT")
        if not port:
            logger.error("API_PORT is not set in environment variables.")
            raise ValueError("API_PORT is not set in environment variables.")
        
        version = os.getenv("API_VERSION")
        if not version:
            logger.error("API_VERSION is not set in environment variables.")
            raise ValueError("API_VERSION is not set in environment variables.")

        return f"{base_url}:{port}/{api}/{version}/{endpoint}"

    def execute(self):
        try:
            ...
        except Exception as e:
            logger.error(f"Error occurred while making API request: {e}")
            return {"error": str(e)}


# def get

# def api_request(http_method, endpoint, query_params):
#     """
#     Prepares and sends an API request.
#     """
#     url = f"{API_BASE_URL}:{API_PORT}/{endpoint}"
#     headers = {"Content-Type": "application/json"}
#     try:
#         if http_method == "GET":
#             response = requests.get(url, headers=headers, params=query_params)
#         elif http_method == "POST":
#             response = requests.post(url, headers=headers, json=query_params)
#         else:
#             logger.error(f"Unsupported HTTP method: {http_method}")
#             return {"error": "Unsupported HTTP method"}, 405

#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         logger.error(f"Error occurred while making API request: {e}")
#         return {"error": str(e)}, 500