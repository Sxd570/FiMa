import os
from strands import tool

from domain.agent.base import AgentFactory
from domain.prompts import AGENT_API_SYSTEM_INSTRUCTIONS
from domain.use_cases.mcp_client import get_mcp_client
from domain.tools.get_current_date import get_current_date_tool

from shared.logger import Logger
logger = Logger(__name__)


def agent_api_agent_as_tool(callback_handler=None, user_id: str = None):
    @tool
    def agent_api_bot(query: str) -> str:
        """
        Fetch and narrate financial data from FiMa for a given user query.

        Use this tool whenever the user asks about their transactions, budgets, or savings goals.
        The agent retrieves the relevant data from FiMa and returns it as a plain-language
        description of the numbers — amounts, dates, totals, and breakdowns by category.

        This tool does NOT interpret, evaluate, or advise. It only returns factual data
        in a readable format. Use the result to form your own insights and recommendations.

        Args:
            query: A natural language description of what data to fetch (e.g. "get all
                   food transactions this month" or "show budget allocations and spending for the user.").

        Returns:
            A plain-language narrative of the fetched data, ready for the Orchestrator to
            reason about.
        """

        try:
            with get_mcp_client() as mcp_client:
                mcp_tools = mcp_client.list_tools_sync()

                tools_list = mcp_tools + [get_current_date_tool()]

                system_prompt = AGENT_API_SYSTEM_INSTRUCTIONS + f"\n\nCurrent user ID: {user_id}"

                agent_factory = AgentFactory(
                    system_prompt=system_prompt,
                    model_name=os.getenv("AGENT_API_MODEL_NAME"),
                    callback_handler=callback_handler,
                    tool_list=tools_list
                )

                agent = agent_factory.create_agent()
                response = agent(query)

                return str(response.message)
        except Exception as e:
            logger.error("Exception in agent_api_bot", str(e))
            raise e

    return agent_api_bot
