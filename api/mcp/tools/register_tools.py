"""
Tool registration module for FiMa MCP Server.

This module centralizes all tool registrations for the MCP server,
keeping main.py focused on server creation.
"""

from fastmcp import FastMCP

from tools.budget_tools import register_budget_tools
from tools.goal_tools import register_goal_tools
from tools.transaction_tools import register_transaction_tools
from utils.logger import Logger


logger = Logger(__name__)


def register_all_tools(mcp: FastMCP) -> None:
    """
    Register all FiMa tools on the FastMCP instance.

    Args:
        mcp: The FastMCP instance to register tools on.
    """
    logger.info("Registering budget tools...")
    register_budget_tools(mcp)

    logger.info("Registering goal tools...")
    register_goal_tools(mcp)

    logger.info("Registering transaction tools...")
    register_transaction_tools(mcp)

    logger.info("All tools registered successfully")
