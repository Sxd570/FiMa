import os
from services.aws.secret_manager import SecretManager


class RDS:
    def __init__(self):
        self.env = os.environ.get("ENVIRONMENT", "dev")
        self.secret_path = f"rds-config-{self.env}"

        self.secret_manager = SecretManager(self.secret_path)
        self.config = self.secret_manager.get_secret()

        if not self.config:
            raise ValueError("Database configuration could not be retrieved.")

        self.host = self.config.get("host")
        self.user = self.config.get("username")
        self.password = self.config.get("password")
        self.database = self.config.get("database")

        if not self.user or not self.password or not self.host or not self.database:
            raise ValueError("Database configuration is incomplete. Please check the RDS secret manager settings.")


def get_db_config():
    """
    Returns database configuration from AWS Secrets Manager without exposing the RDS class.
    """
    rds = RDS()
    return {
        "user": rds.user,
        "password": rds.password,
        "host": rds.host,
        "database": rds.database
    }
