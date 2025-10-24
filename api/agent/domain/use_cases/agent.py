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
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.response = ""
        self._loop = asyncio.get_event_loop()

    def __call__(self, **kwargs):
        if "data" in kwargs:
            chunk = kwargs["data"]
            self.response += chunk
            asyncio.run_coroutine_threadsafe(self._send_chunk_async(chunk), self._loop)

    async def _send_chunk_async(self, chunk: str):
        try:
            await self.websocket.send_json({"type": "chunk", "data": chunk})
        except Exception as e:
            logger.error(f"Error sending chunk: {e}")

    def clear(self):
        self.response = ""


class AgentUseCase:
    def __init__(self, user_id: str, websocket: WebSocket):
        self.user_id = user_id
        self.websocket = websocket
        self.callback_handler = WebSocketCallback(websocket)
        self.orchestrator_agent = self.get_orchestrator_agent()


    def get_orchestrator_agent(self) -> Agent:
        try:
            orchestrator_bot_factory = AgentFactory(
                agent_name=AgentEnum.ORCHESTRATOR.value,
                system_prompt=ORCHESTRATOR_SYSTEM_INSTRUCTIONS,
                callback_handler=self.callback_handler,
                tool_list=[
                    agent_api_agent_as_tool(
                        callback_handler=self.callback_handler
                    ),
                    ui_smith_agent_as_tool(
                        callback_handler=self.callback_handler
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

            await self.websocket.send_json(
                {
                    "type": "response_start", 
                    "data": ""
                }
            )

            self.callback_handler.clear()

            loop = asyncio.get_event_loop()

            def run_agent():
                try:
                    self.orchestrator_agent(self.query)
                except Exception as e:
                    logger.error(f"Agent error: {e}")

            await loop.run_in_executor(executor, run_agent)

            await self.websocket.send_json(
                {
                    "type": "response_end", 
                    "data": ""
                }
            )
            
        except WebSocketDisconnect:
            logger.warning(f"Websocket client disconnected: {self.user_id}")
        except Exception as e:
            logger.error(f"Error handling message for user {self.user_id}: {str(e)}")
            raise e