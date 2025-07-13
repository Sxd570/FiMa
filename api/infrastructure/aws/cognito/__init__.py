import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from shared.logger import Logger

logger = Logger(__name__)
load_dotenv()  # Load environment variables from .env


class Cognito:
    def __init__(self):
        self.user_pool_id = os.getenv("USER_POOL_ID")
        self.client_id = os.getenv("CLIENT_ID")
        self.region_name = os.getenv("REGION_NAME", "us-east-1")

        if not all([self.user_pool_id, self.client_id, self.region_name]):
            raise ValueError("Missing required environment variables for Cognito")

        self.client = boto3.client("cognito-idp", region_name=self.region_name)
        

    def signup(self, username: str, password: str, email: str) -> dict:
        try:
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                ]
            )
            return response
        except ClientError as e:
            logger.error(f"Signup failed for {username}: {e}")
            raise e


    def login(self, username: str, password: str) -> dict:
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password
                }
            )
            return response["AuthenticationResult"]
        except ClientError as e:
            logger.error(f"Login failed for {username}: {e}")
            raise e
        

    def refresh_tokens(self, refresh_token: str) -> dict:
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token
                }
            )
            auth_result = response["AuthenticationResult"]
            return auth_result
        except ClientError as e:
            logger.error(f"Failed to refresh token: {e}")
            raise e
