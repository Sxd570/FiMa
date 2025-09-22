import os

from .db_config import get_db_config
from shared.logger import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = Logger(__name__)
Base = declarative_base()


Session = None
_Session = None

engine = None

debug_params = {}
log_level = os.environ.get("LOG_LEVEL")
if log_level == "DEBUG":
    debug_params["echo"] = True



config = get_db_config()

user = config["user"]
password = config["password"]
host = config["host"]
database = config["database"]
port = config.get("port", None)


if port:
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
        **debug_params
        )
else:
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}",
        **debug_params
        )


def get_db_session():
    global Session
    global _Session

    if not Session:
        Session = sessionmaker(bind=engine)

    if not _Session:
        _Session = Session()

    return _Session