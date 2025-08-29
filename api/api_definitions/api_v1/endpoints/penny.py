from fastapi import APIRouter

from shared.logger import Logger
# from core.use_cases.agent import AgentUseCase
# from core.models.io_models.agent_io_models import (
# )

logger = Logger(__name__)
router = APIRouter()

@router.get("/health")
def health_check():
    ...

@router.get("/conversations/{user_id}")
def list_conversations(user_id: str):
    ...


@router.post("{user_id}/conversations/{conversation_id}")
def get_conversation(user_id: str, conversation_id: str):
    ...