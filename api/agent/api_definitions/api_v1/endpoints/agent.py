from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Path
from typing import Dict, List
from pydantic import Field

from domain.use_cases.agent import AgentUseCase

from shared.logger import Logger
logger = Logger(__name__)


router = APIRouter()
active_connections: List[WebSocket] = []


@router.websocket("/ws/{user_id}/chat")
async def chat(
    websocket: WebSocket, 
    user_id: str = Path(..., description="The ID of the user")
):
    try:
        await websocket.accept()

        active_connections.append(websocket)

        agent_use_case = AgentUseCase(
            user_id=user_id, 
            websocket=websocket
        )
        while True:
            message = await websocket.receive_text()

            message = message.strip()

            if not message:
                continue

            await agent_use_case.execute(
                query=message
            )

    except WebSocketDisconnect:
        logger.warning("Websocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket connection error for user {user_id}: {str(e)}")
        raise e
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)