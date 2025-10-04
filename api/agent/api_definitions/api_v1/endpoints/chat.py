from fastapi import APIRouter

from shared.logger import Logger
from domain.use_cases.chat import ChatUseCases

logger = Logger(__name__)
router = APIRouter()


@router.get("/conversations/{user_id}")
def list_conversations(user_id: str):
    try:
        chat_use_cases = ChatUseCases()

        conversations = chat_use_cases.list_conversations(user_id)

        return conversations
    except Exception as e:
        logger.error(f"Failed to list conversations for user {user_id}: {str(e)}")
        raise e


@router.post("{user_id}/conversation/{conversation_id}")
def get_conversation(user_id: str, conversation_id: str):
    try:
        chat_use_cases = ChatUseCases()

        conversation = chat_use_cases.get_conversation(
            user_id=user_id, 
            conversation_id=conversation_id
        )

        return conversation
    except Exception as e:
        logger.error(f"Failed to get conversation {conversation_id} for user {user_id}: {str(e)}")
        raise e