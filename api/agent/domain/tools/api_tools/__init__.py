from budget_tools import BudgetTools
from goal_tools import GoalTools
from transaction_tools import TransactionTools
from shared.logger import Logger

logger = Logger(__name__)


def extract_tools(obj):
        tools = []
        for attr_name in dir(obj):
            attr = getattr(obj, attr_name)
            if hasattr(attr, "_tool_spec"):
                tools.append(attr)
        return tools


def insight_bot_tools():
    try:
        tools = None

        tools = (
            extract_tools(BudgetTools) +
            extract_tools(GoalTools) +
            extract_tools(TransactionTools)
        )

        return tools
    except Exception as e:
        logger.error("Error while getting insight tools", str(e))
        raise e