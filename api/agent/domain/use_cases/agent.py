import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from strands import tool, Agent
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor
import json
from pydantic import Field
from constants import (
    AgentUISmithFormatEnum,
    AgentEnum
)


from domain.prompts import (
    AGENT_API_SYSTEM_INSTRUCTIONS,
    ORCHESTRATOR_SYSTEM_INSTRUCTIONS,
    UI_SMITH_SYSTEM_INSTRUCTIONS
)

from domain.tools.api_tools import agent_api_tools

from domain.use_cases.agent_base import AgentFactory

from shared.logger import Logger
logger = Logger(__name__)

agents: Dict[WebSocket, Agent] = {}
executor = ThreadPoolExecutor()



def get_agent_api_as_tool(callback_handler=None):
    @tool
    def agent_api_bot(query: str) -> str:
        """
        #TODO: Update the description
        """
        try:
            agent_api_bot_factory = AgentFactory(
                agent_name=AgentEnum.AGENT_API.value,
                system_prompt=AGENT_API_SYSTEM_INSTRUCTIONS,
                callback_handler=callback_handler,
                tool_list=agent_api_tools()
            )

            agent = agent_api_bot_factory.create_agent()

            response = agent(query)

            return str(response)
        except Exception as e:
            logger.error("Exception in get_agent_api_as_tools", str(e))
            raise e

    return agent_api_bot


def get_agent_ui_smith_as_tool():
    @tool
    def agent_ui_smith_bot(
        query: str = Field(..., description="The query to generate the UI artifact"), 
        format: AgentUISmithFormatEnum = Field(..., description="The format of the UI artifact")
    ) -> str:
        """
        #TODO: Update the description
        """
        try:
            prompt = (
                f"Generate the required {format} artifact as per the query below\n"
                f"Generation query:\n{query}"
            )
            agent_ui_smith_factory = AgentFactory(
                agent_name=AgentEnum.UI_SMITH.value,
                system_prompt=UI_SMITH_SYSTEM_INSTRUCTIONS,
                callback_handler=None
            )

            agent = agent_ui_smith_factory.create_agent()
            
            response = agent(prompt)

            return str(response)
        except Exception as e:
            logger.error("Exception in get_agent_ui_smith_as_tools", str(e))
            raise e
        
    return agent_ui_smith_bot


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
            orchestrator_agent = AgentFactory(
                agent_name=AgentEnum.ORCHESTRATOR.value,
                system_prompt=ORCHESTRATOR_SYSTEM_INSTRUCTIONS,
                callback_handler=self.callback_handler,
                tool_list=[
                    get_agent_api_as_tool(
                        callback_handler=self.callback_handler
                    ),
                    get_agent_ui_smith_as_tool(
                        callback_handler=self.callback_handler
                    )
                ]
            )

            agent = orchestrator_agent.create_agent()

            agents[self.websocket] = agent

            return agent
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