from fastmcp import FastMCP
from mcp.tools.budgets_tool import (
    get_budget_overview,
    get_budget_details,
    edit_budget_limit,
    delete_budget,
    create_budget
)
from mcp.tools.goals_tool import (
    get_goals_overview,
    get_goal_details,
    create_goal,
    edit_goal,
    delete_goal,
    add_amount_to_goal,
    get_goals_dashboard
)
from mcp.tools.transactions_tool import (
    get_transactions,
    create_transaction,
    update_transaction,
    delete_transaction
)

def register_all_tools(mcp: FastMCP):
    """
    Registers all domain tools to the FastMCP server.
    """
    # Budgets
    mcp.register_tool(get_budget_overview)
    mcp.register_tool(get_budget_details)
    mcp.register_tool(edit_budget_limit)
    mcp.register_tool(delete_budget)
    mcp.register_tool(create_budget)

    # Goals
    mcp.register_tool(get_goals_overview)
    mcp.register_tool(get_goal_details)
    mcp.register_tool(create_goal)
    mcp.register_tool(edit_goal)
    mcp.register_tool(delete_goal)
    mcp.register_tool(add_amount_to_goal)
    mcp.register_tool(get_goals_dashboard)

    # Transactions
    mcp.register_tool(get_transactions)
    mcp.register_tool(create_transaction)
    mcp.register_tool(update_transaction)
    mcp.register_tool(delete_transaction)
