from strands import tool

from domain.agent.base import AgentFactory
from domain.prompts import AGENT_API_SYSTEM_INSTRUCTIONS
from domain.use_cases.mcp_client import create_mcp_tools

from shared.logger import Logger
logger = Logger(__name__)


def agent_api_agent_as_tool(callback_handler=None):
    @tool
    def agent_api_bot(query: str) -> str:
        """
        This tool invokes the API Agent, which is responsible for retrieving
        accurate and user-specific financial data from the  Fima platform.

        Parameters:
        - query (str): A natural language description of the data to fetch.
        
        Returns:
        - str: JSON or structured text response containing the requested financial data.

        Error Handling:
        - If the query lacks required context, the API Agent may request clarification.
        - If data is unavailable or retrieval fails, it will return a clear, factual message
          rather than fabricated or estimated data.

        Raises:
        - Exception: If any internal error occurs during data retrieval.
        """

        try:
            mcp_tools = create_mcp_tools() 

            agent_api_bot_factory = AgentFactory(
                system_prompt=AGENT_API_SYSTEM_INSTRUCTIONS,
                callback_handler=callback_handler,
                tool_list=mcp_tools
            )

            agent = agent_api_bot_factory.create_agent()

            response = agent(query)

            return str(response.message)
        except Exception as e:
            logger.error("Exception in get_agent_api_as_tools", str(e))
            raise e

    return agent_api_bot