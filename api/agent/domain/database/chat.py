from shared.logger import Logger
from domain.models.tables.conversation import Conversations
from domain.models.io_models.conversations_io_model import (
    ConversationDBResponse,
    Conversation
)
from shared.Utility.db_base import MySQLDatabase
from shared.Utility.mongo_db_base import MongoDatabase
from copy import deepcopy

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
                Conversations.user_id == self.user_id
            ]

            query = self.mysql_db_session.query(
                Conversations.conversation_id,
                Conversations.title,
                Conversations.created_at,
                Conversations.updated_at,
                Conversations.last_message_at,
                Conversations.total_token_used,
                Conversations.status
            ).filter(
                *filter_group
            ).order_by(
                Conversations.updated_at.desc()
            )

            db_response = query.all()
            if not db_response:
                return ConversationDBResponse(
                    conversations=[]
                )
            response = deepcopy(db_response)
            
            conversation_details = ConversationDBResponse(
                conversations = [
                    Conversation(
                        conversation_id=conversation_id,
                        title=title,
                        created_at=created_at,
                        updated_at=updated_at,
                        last_message_at=last_message_at,
                        total_token_used=total_token_used,
                        status=status
                    ) for (
                        conversation_id,
                        title,
                        created_at,
                        updated_at,
                        last_message_at,
                        total_token_used,
                        status
                    ) in response
                ]
            )
            return conversation_details
        except Exception as e:
            logger.error(f"Exception in list conversation db {user_id}: {str(e)}")
            raise e