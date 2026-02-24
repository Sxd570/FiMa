import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from strands import Agent
from concurrent.futures import ThreadPoolExecutor

from domain.agent.base import AgentFactory
from domain.prompts import ORCHESTRATOR_SYSTEM_INSTRUCTIONS
from domain.tools.agent_as_tools.agent_api import agent_api_agent_as_tool
from domain.tools.agent_as_tools.ui_smith import ui_smith_agent_as_tool
from domain.use_cases.callback_handler import WebSocketCallback

from shared.logger import Logger
logger = Logger(__name__)

executor = ThreadPoolExecutor(max_workers=4)


class AgentUseCase:
    def __init__(self, user_id: str, websocket: WebSocket):
        self.user_id = user_id
        self.websocket = websocket
        self.orchestrator_agent = self._create_orchestrator_agent()


    def _create_orchestrator_agent(self) -> Agent:
        try:
            orchestrator_bot_factory = AgentFactory(
                system_prompt=ORCHESTRATOR_SYSTEM_INSTRUCTIONS,
                callback_handler=WebSocketCallback(self.websocket, "orchestrator"),
                tool_list=[
                    agent_api_agent_as_tool(
                        callback_handler=WebSocketCallback(self.websocket, "agent_api")
                    ),
                    ui_smith_agent_as_tool(
                        callback_handler=WebSocketCallback(self.websocket, "ui_smith")
                    )
                ]
            )
            return orchestrator_bot_factory.create_agent()
        except Exception as e:
            logger.error("Error while creating orchestrator agent", str(e))
            raise e
        

    async def execute(self, query: str):
        try:
            await self.websocket.send_json({
                "type": "response_start", 
                "data": ""
            })

            loop = asyncio.get_running_loop()
            agent_error = None

            def run_agent():
                nonlocal agent_error
                try:
                    self.orchestrator_agent(query)
                except Exception as e:
                    agent_error = e
                    logger.error(f"Agent error: {e}")

            await loop.run_in_executor(executor, run_agent)

            if agent_error:
                await self.websocket.send_json({
                    "type": "response_error",
                    "data": str(agent_error)
                })
            
            await self.websocket.send_json({
                "type": "response_end", 
                "data": ""
            })
            
        except WebSocketDisconnect:
            logger.warning(f"Websocket client disconnected: {self.user_id}")
        except Exception as e:
            logger.error(f"Error handling message for user {self.user_id}: {str(e)}")
            raise e