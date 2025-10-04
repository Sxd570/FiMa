from shared.logger import Logger
from domain.models.tables.chat import Chat
from shared.Utility.db_base import MySQLDatabase
from shared.Utility.mongo_db_base import MongoDatabase

logger = Logger(__name__)


class ChatDatabase:
    def __init__(self):
        self.mysql_db = MySQLDatabase()
        self.mongo_db = MongoDatabase()

        self.mysql_db_session = None
        self.mongo_db_session = None

    def list_conversations(self, user_id: str):
        try:
            self.mysql_db_session = self.mysql_db.get_session()

            self.user_id = user_id

            filter_group = [
                Chat.user_id == self.user_id
            ]

            query = self.mysql_db_session.query(
                Chat
            ).filter(
                *filter_group
            ).order_by(
                Chat.updated_at.desc()
            )
            db_response = query.all()
            if not db_response:
                return []
            return db_response
        except Exception as e:
            logger.error(f"Exception in list conversation db {user_id}: {str(e)}")
            raise e