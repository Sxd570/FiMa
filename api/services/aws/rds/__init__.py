import os
from services.aws.secret_manager import SecretManager


class RDS:
    def __init__(self):
        self.env = os.environ.get("ENVIRONMENT", "dev")
        self.secret_path = f"fima-{self.env}-rds-secret"

        self.host = None
        self.user = None
        self.password = None
        self.database = None
        self.port = None

    def get_connection_config(self):
        self.secret_manager = SecretManager(self.secret_path)
        self.config = self.secret_manager.get_secret()

        if not self.config:
            raise ValueError("Database configuration could not be retrieved.")

        self.host = self.config.get("host")
        if not self.host:
            raise ValueError("Database host is not set in the configuration.")
        
        self.user = self.config.get("username")
        if not self.user:
            raise ValueError("Database username is not set in the configuration.")
        
        self.password = self.config.get("password")
        if not self.password:
            raise ValueError("Database password is not set in the configuration.")
        
        self.database = self.config.get("database")
        if not self.database:
            raise ValueError("Database name is not set in the configuration.")
        
        self.port = self.config.get("port", None)

        return {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "port": self.port
        }