import json
import requests
from shared.logger import Logger

logger = Logger(__name__)


def api_request(http_method, path, query_params):
    """
    Prepares and sends an API request.
    """
    url = 
    headers = {"Content-Type": "application/json"}
    try:
        if http_method == "GET":
            response = requests.get(url, headers=headers, params=query_params)
        elif http_method == "POST":
            response = requests.post(url, headers=headers, json=query_params)
        else:
            logger.error(f"Unsupported HTTP method: {http_method}")
            return {"error": "Unsupported HTTP method"}, 405

        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error occurred while making API request: {e}")
        return {"error": str(e)}, 500