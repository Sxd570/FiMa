import asyncio
import os
from fastapi import WebSocket, WebSocketDisconnect
from concurrent.futures import ThreadPoolExecutor

from constants import AgentID
from domain.agent.base import AgentFactory
from domain.prompts import ORCHESTRATOR_SYSTEM_INSTRUCTIONS
from domain.tools.agent_as_tools.analyst import analyst_agent_as_tool
from domain.tools.get_current_date import get_current_date_tool
from domain.use_cases.callback_handler import AgentCallbackHandler

from shared.logger import Logger
logger = Logger(__name__)

executor = ThreadPoolExecutor(max_workers=4)


class AgentUseCase:
    def __init__(self, user_id: str, websocket: WebSocket):
        self.user_id = user_id
        self.websocket = websocket

    async def execute(self, query: str):
        try:
            loop = asyncio.get_running_loop()
            shared_callback = AgentCallbackHandler(self.websocket, loop)

            orchestrator_model_name = os.getenv("ORCHESTRATOR_MODEL_NAME")

            orchestrator_tool_list = [
                analyst_agent_as_tool(
                    shared_callback=shared_callback,
                    user_id=self.user_id
                )
            ]

            orchestrator = AgentFactory(
                system_prompt=ORCHESTRATOR_SYSTEM_INSTRUCTIONS,
                model_name=orchestrator_model_name,
                agent_id=AgentID.ORCHESTRATOR.value,
                shared_callback=shared_callback,
                silent=False,
                tool_list=orchestrator_tool_list,
            ).create_agent()

            await self.websocket.send_json({"type": "response_start", "data": ""})

            agent_error = None

            def run_agent():
                nonlocal agent_error
                try:
                    orchestrator(query)
                except Exception as e:
                    agent_error = e
                    logger.error(f"Agent error: {e}")

            await loop.run_in_executor(executor, run_agent)

            if agent_error:
                await self.websocket.send_json({
                    "type": "response_error",
                    "data": str(agent_error),
                })

            await self.websocket.send_json({"type": "response_end", "data": ""})

        except WebSocketDisconnect:
            logger.warning(f"Websocket client disconnected: {self.user_id}")
        except Exception as e:
            logger.error(f"Error handling message for user {self.user_id}: {str(e)}")
            raise e