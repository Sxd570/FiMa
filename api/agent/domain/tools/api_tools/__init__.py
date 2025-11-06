from .budget_tools import * 
from .goal_tools import *
from .transaction_tools import *
from shared.logger import Logger

logger = Logger(__name__)


def agent_api_tools():
    try:
        tools = None

        tools = [
            get_budget_overview,
            get_budget_details,
            get_goal_details,
            get_goal_details,
            get_transactions
        ]

        return tools
    except Exception as e:
        logger.error("Error while getting insight tools", str(e))
        raise e