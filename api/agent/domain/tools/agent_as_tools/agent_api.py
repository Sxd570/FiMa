from strands import tool
from pydantic import Field
from constants import (
    AgentEnum
)
from domain.agent.base import AgentFactory
from domain.prompts import AGENT_API_SYSTEM_INSTRUCTIONS

from domain.tools.api_tools import agent_api_tools

from shared.logger import Logger
logger = Logger(__name__)


def agent_api_agent_as_tool(callback_handler=None):
    @tool
    def agent_api_bot(
        query: str = Field(..., description="The query to interact with the API agent")
    ) -> str:
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