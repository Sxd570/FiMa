from fastapi import APIRouter

from shared.logger import Logger

logger = Logger(__name__)
router = APIRouter()


@router.websocket("/ws/{user_id}/chat")
async def chat(websocket, user_id: str):
    try:
        ...
    except Exception as e:
        logger.error(f"WebSocket connection error for user {user_id}: {str(e)}")
        raise e