import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from strands import tool, Agent
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor
import json
from pydantic import Field

from constants import AgentEnum
from domain.agent.base import AgentFactory
from domain.prompts import ORCHESTRATOR_SYSTEM_INSTRUCTIONS
from domain.tools.agent_as_tools.agent_api import agent_api_agent_as_tool
from domain.tools.agent_as_tools.ui_smith import ui_smith_agent_as_tool

from shared.logger import Logger
logger = Logger(__name__)

agents: Dict[WebSocket, Agent] = {}
executor = ThreadPoolExecutor()


class WebSocketCallback:
    def __init__(self, websocket: WebSocket, agent_name: str):
        self.websocket = websocket
        self.agent_name = agent_name
        self.response = ""
        self._loop = asyncio.get_event_loop()

    def __call__(self, **kwargs):
        if "data" in kwargs:
            chunk = kwargs["data"]
            self.response += chunk
            asyncio.run_coroutine_threadsafe(
                self._send_chunk_async(chunk),
                self._loop
            )

    async def _send_chunk_async(self, chunk: str):
        try:
            await self.websocket.send_json({
                "type": "chunk",
                "agent": self.agent_name,
                "data": chunk
            })
        except Exception as e:
            logger.error(f"Error sending chunk from {self.agent_name}: {e}")

    def clear(self):
        self.response = ""


class AgentUseCase:
    def __init__(self, user_id: str, websocket: WebSocket):
        self.user_id = user_id
        self.websocket = websocket
        self.orchestrator_agent = None


    def get_orchestrator_agent(self) -> Agent:
        try:
            orchestrator_bot_factory = AgentFactory(
                agent_name=AgentEnum.ORCHESTRATOR.value,
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
            orchestrator_agent = orchestrator_bot_factory.create_agent()
            return orchestrator_agent
        except Exception as e:
            logger.error("Error while creating orchestrator agent", str(e))
            raise e
        

    async def execute(self, query: str):
        try:
            self.query = query
            self.orchestrator_agent = self.get_orchestrator_agent()

            await self.websocket.send_json({
                "type": "response_start", 
                "data": ""
            })

            loop = asyncio.get_event_loop()

            def run_agent():
                try:
                    self.orchestrator_agent(self.query)
                except Exception as e:
                    logger.error(f"Agent error: {e}")

            await loop.run_in_executor(executor, run_agent)

            await self.websocket.send_json({
                "type": "response_end", 
                "data": ""
            })
            
        except WebSocketDisconnect:
            logger.warning(f"Websocket client disconnected: {self.user_id}")
        except Exception as e:
            logger.error(f"Error handling message for user {self.user_id}: {str(e)}")
            raise e