import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from shared.logger import Logger

logger = Logger(__name__)
Base = declarative_base()

load_dotenv()


class SQLDatabase:
    def __init__(self):
        self.config = {
            "user": os.environ["DB_USER"],
            "password": os.environ["DB_PASSWORD"],
            "host": os.environ["DB_HOST"],
            "port": os.environ["DB_PORT"],
            "database": os.environ["DB_NAME"],
            "pool_size": int(os.environ["DB_POOL_SIZE"]),
            "max_overflow": int(os.environ["DB_MAX_OVERFLOW"]),
            "pool_timeout": int(os.environ["DB_POOL_TIMEOUT"]),
        }

        debug_params = {}
        if os.environ.get("LOG_LEVEL") == "DEBUG":
            debug_params["echo"] = True

        # Create engine
        self.engine = create_engine(
            f"mysql+pymysql://{self.config['user']}:{self.config['password']}@"
            f"{self.config['host']}:{self.config['port']}/{self.config['database']}",
            pool_size=self.config["pool_size"],
            max_overflow=self.config["max_overflow"],
            pool_timeout=self.config["pool_timeout"],
            **debug_params
        )

        self.Session = sessionmaker(bind=self.engine)
        self._session = None

    def get_session(self):
        """Return the single DB session (creates if not already created)."""
        if self._session is None:
            self._session = self.Session()
        return self._session
