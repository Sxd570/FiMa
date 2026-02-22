from fastapi import APIRouter

from shared.logger import Logger
from domain.use_cases.chat import ChatUseCases
from domain.models.io_models.conversations_io_model import (
    ListConversationsPayload,
    ListConversationResponse,
    GetConversationPayload,
    GetConversationResponse
)
from domain.exceptions import ConversationNotFoundException

logger = Logger(__name__)
router = APIRouter()


@router.get("/conversations/{user_id}", response_model=ListConversationResponse)
def list_conversations(user_id: str):
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


@router.get("/{user_id}/conversation/{conversation_id}", response_model=GetConversationResponse)
def get_conversation(user_id: str, conversation_id: str):
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

    except ConversationNotFoundException as e:
        raise e
    except Exception as e:
        logger.error(f"Failed to get conversation {conversation_id} for user {user_id}: {str(e)}")
        raise e