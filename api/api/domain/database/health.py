from shared.logger import Logger
from sqlalchemy import text
from shared.Utility.db_base import get_db_session

logger = Logger(__name__)


class Database:
    def __init__(self):
        self.db_session = None

    def ping(self) -> dict:
        try:
            self.db_session = get_db_session()
            self.db_session.execute(text("SELECT 1"))
            return {"database": "connected"}
        except Exception as e:
            logger.error(f"Error in ping: {e}")
            raise e
