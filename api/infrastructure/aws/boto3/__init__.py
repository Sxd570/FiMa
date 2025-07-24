import boto3
from shared.logger import Logger

logger = Logger(__name__)

class Boto3:
    def __init__(self):
        self.endpoint_url = "http://localhost:4566"

    def client(self, service_name: str):
        try:
            return boto3.client(
                service_name,
                endpoint_url=self.endpoint_url
            )
        except Exception as e:
            logger.error(f"Error creating boto3 client for {service_name}: {e}")
            raise
