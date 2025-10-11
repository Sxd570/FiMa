from shared.logger import Logger
from domain.database.chat import ChatDatabase
from domain.models.io_models.conversations_io_model import (
    ListConversationsPayload,
    ListConversationsDBRequest,
    ListConversationResponse,
    Conversation,
    GetConversationPayload,
    GetConversationDBRequest,
    GetConversationResponse
)

logger = Logger(__name__)


class ChatUseCases:
    def __init__(self):
        self.chat_db = ChatDatabase()

    def list_conversations(self, payload: ListConversationsPayload) -> ListConversationResponse:
        try:
            user_id = payload.user_id

            db_request = ListConversationsDBRequest(
                user_id=user_id
            )

            db_response = self.chat_db.list_conversations(
                db_request=db_request
            )

            conversations_list = ListConversationResponse(
                conversations=[
                    Conversation(
                        conversation_id=conv.conversation_id,
                        title=conv.title,
                        created_at=conv.created_at,
                        updated_at=conv.updated_at,
                        last_message_at=conv.last_message_at,
                        total_token_used=conv.total_token_used,
                        status=conv.status
                    )
                    for conv in db_response.conversations
                ]
            )

            return conversations_list
        except Exception as e:
            logger.error(f"Failed to list conversations for user {user_id}: {str(e)}")
            raise e

    def get_conversation(self, payload: GetConversationPayload) -> GetConversationResponse:
        try:
            user_id = payload.user_id
            conversation_id = payload.conversation_id

            db_request = GetConversationDBRequest(
                user_id=user_id,
                conversation_id=conversation_id
            )

            db_response = self.chat_db.get_conversation(
                db_request=db_request
            )

            return GetConversationResponse(
                message_details=db_response.message_details
            )
        except Exception as e:
            logger.error(f"Failed to get conversation {conversation_id} for user {user_id}: {str(e)}")
            raise e
        
    def chat():
        try:
            ...
        except Exception as e:
            logger.error(f"WebSocket connection error for user {user_id}: {str(e)}")
            raise e