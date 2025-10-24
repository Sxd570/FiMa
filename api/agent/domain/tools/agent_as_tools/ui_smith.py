from strands import tool, Agents
from pydantic import Field
from constants import (
    AgentUISmithFormatEnum,
    AgentEnum
)
from domain.agent.base import AgentFactory
from domain.prompts import UI_SMITH_SYSTEM_INSTRUCTIONS

from shared.logger import Logger
logger = Logger(__name__)


def ui_smith_agent_as_tool(callback_handler=None):
    @tool
    def agent_ui_smith_bot(
        query: str = Field(..., description="The query to generate the UI artifact"), 
        format: AgentUISmithFormatEnum = Field(..., description="The format of the UI artifact")
    ) -> str:
        """
        #TODO: Update the description
        """
        prompt = (
            f"Generate the required {format} artifact as per the query below\n"
            f"Generation query:\n{query}"
        )

        try:
            agent_ui_smith_factory = AgentFactory(
                agent_name=AgentEnum.UI_SMITH.value,
                system_prompt=UI_SMITH_SYSTEM_INSTRUCTIONS,
                callback_handler=callback_handler
            )

            agent = agent_ui_smith_factory.create_agent()

            response = agent(prompt)

            return str(response)
        except Exception as e:
            logger.error("Exception in get_agent_ui_smith_as_tools", str(e))
            raise e
    
    return agent_ui_smith_bot