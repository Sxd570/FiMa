import boto3
from shared.logger import Logger

logger = Logger(__name__)

class Boto3:
    def __init__(self):
        self.session = None

    def client(self, service_name: str):
        try:
            self.session = boto3.client(
                service_name
            )
            return self.session
        except Exception as e:
            logger.error(f"Error creating boto3 client for {service_name}: {e}")
            raise e
