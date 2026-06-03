import os
from strands import tool

from constants import AgentID
from domain.agent.base import AgentFactory
from domain.prompts.analyst import ANALYST_SYSTEM_INSTRUCTIONS
from domain.use_cases.callback_handler import AgentCallbackHandler
from domain.use_cases.mcp_client import get_mcp_client
from domain.tools.get_current_date import get_current_date_tool

from shared.logger import Logger
logger = Logger(__name__)


def analyst_agent_as_tool(shared_callback: AgentCallbackHandler, user_id: str):
    @tool
    def analyst_bot(query: str) -> str:
        """
        Analyse the user's FiMa financial data and return a complete, user-ready insight.

        Use this tool for ANY question about the user's transactions, budgets, or savings goals —
        including spending patterns, budget headroom or breaches, goal progress, category breakdowns,
        and trend analysis.

        The analyst fetches all relevant data from FiMa, reasons over it, and returns a
        self-contained response ready to relay directly to the user. Do NOT re-analyse,
        recompute, or add numbers to the analyst's response — relay it as-is.

        Args:
            query: A natural language description of what to analyse (e.g. "How much did the
                   user spend on food this month and how does it compare to their budget?").

        Returns:
            A complete, conversational financial insight grounded in real data.
        """
        try:
            with get_mcp_client() as mcp_client:
                mcp_tools = mcp_client.list_tools_sync()
                tools_list = mcp_tools + [get_current_date_tool()]

                system_prompt = ANALYST_SYSTEM_INSTRUCTIONS + f"\n\nuser ID: {user_id}"

                agent_factory = AgentFactory(
                    system_prompt=system_prompt,
                    model_name=os.getenv("ANALYST_MODEL_NAME"),
                    agent_id=AgentID.ANALYST.value,
                    shared_callback=shared_callback,
                    silent=False,
                    tool_list=tools_list,
                )

                agent = agent_factory.create_agent()
                response = agent(query)

                return str(response.message)
        except Exception as e:
            logger.error("Exception in analyst_bot", str(e))
            raise e

    return analyst_bot
