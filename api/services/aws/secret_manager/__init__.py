import boto3
import json
from shared.logger import Logger

logger = Logger(__name__)

class SecretManager:
    def __init__(self, secret_name):
        self.client = boto3.client("secretsmanager")
        self.secret_name = secret_name

    def get_secret(self):
        try:
            response = self.client.get_secret_value(SecretId=self.secret_name)

            if "SecretString" in response:
                return json.loads(response["SecretString"])
            else:
                raise ValueError("SecretString not found in AWS response.")

        except Exception as e:
            logger.error(f"Error fetching secret [{self.secret_name}]: {e}")
            return None
