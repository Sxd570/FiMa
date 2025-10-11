from fastapi import APIRouter

from shared.logger import Logger
from domain.use_cases.chat import ChatUseCases
from domain.models.io_models.conversations_io_model import (
    ListConversationsPayload,
    ListConversationResponse,
    GetConversationPayload,
    GetConversationResponse
)

logger = Logger(__name__)
router = APIRouter()


@router.get("/conversations/{user_id}")
def list_conversations(user_id: str) -> ListConversationResponse:
    try:
        payload = ListConversationsPayload(
            user_id=user_id
        )

        chat_use_cases = ChatUseCases()

        conversations = chat_use_cases.list_conversations(
            payload=payload
        )

        return conversations
    except Exception as e:
        logger.error(f"Failed to list conversations for user {user_id}: {str(e)}")
        raise e


@router.get("/{user_id}/conversation/{conversation_id}")
def get_conversation(user_id: str, conversation_id: str) -> GetConversationResponse:
    try:
        payload = GetConversationPayload(
            user_id=user_id,
            conversation_id=conversation_id
        )

        chat_use_cases = ChatUseCases()

        conversation = chat_use_cases.get_conversation(
            payload=payload
        )

        return conversation
    except Exception as e:
        logger.error(f"Failed to get conversation {conversation_id} for user {user_id}: {str(e)}")
        raise e
    

@router.websocket("/ws/{user_id}/chat")
async def chat(websocket, user_id: str):
    try:
        ...
    except Exception as e:
        logger.error(f"WebSocket connection error for user {user_id}: {str(e)}")
        raise e