import boto3
import json
from shared.logger import Logger

logger = Logger(__name__)

class SecretManager:
    def __init__(self):
        self.client = boto3.client("secretsmanager")
        self.secret_name = None

    def get_secret(self, secret_name):
        self.secret_name = secret_name
        try:
            response = self.client.get_secret_value(SecretId=self.secret_name)

            if "SecretString" in response:
                return json.loads(response["SecretString"])
            else:
                raise ValueError("SecretString not found in AWS response.")

        except Exception as e:
            logger.error(f"Error fetching secret [{self.secret_name}]: {e}")
            return None
