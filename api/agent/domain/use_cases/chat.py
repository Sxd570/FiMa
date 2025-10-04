from shared.logger import Logger
from domain.database.chat import ChatDatabase

logger = Logger(__name__)


class ChatUseCases:
    def __init__(self):
        ...

    def list_conversations(self, user_id: str):
        try:
            ...
        except Exception as e:
            logger.error(f"Failed to list conversations for user {user_id}: {str(e)}")
            raise e

    def get_conversation(self, user_id: str, conversation_id: str):
        try:
            ...
        except Exception as e:
            logger.error(f"Failed to get conversation {conversation_id} for user {user_id}: {str(e)}")
            raise e