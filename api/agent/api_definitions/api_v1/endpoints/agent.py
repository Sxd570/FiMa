from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

from domain.use_cases.agent import AgentUseCase

from shared.logger import Logger

logger = Logger(__name__)
router = APIRouter()


@router.websocket("/ws/{user_id}/chat")
async def chat(websocket: WebSocket, user_id: str):
    try:
        ...
    except WebSocketDisconnect:
        logger.warning("Websocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket connection error for user {user_id}: {str(e)}")
        raise e