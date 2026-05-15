"""
MCP Client for communicating with the FiMa MCP Server.

Uses strands-agents' built-in MCPClient with streamable HTTP transport
to connect to the FastMCP server (stateless_http=True).
"""

import os

from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp import MCPClient

from shared.logger import Logger


load_dotenv()
logger = Logger(__name__)


def _create_transport(mcp_server_url: str):
    return streamablehttp_client(f"{mcp_server_url}/mcp")


def get_mcp_client() -> MCPClient:
    """
    Create an MCP client connected to the FiMa MCP server.

    Must be used as a context manager so the HTTP transport stays
    open while the agent is running its tools.

    Example:
        with get_mcp_client() as client:
            tools = client.list_tools_sync()
            agent = Agent(tools=tools)
            agent(query)

    Returns:
        MCPClient: A strands MCPClient instance using streamable HTTP transport.
    """
    mcp_server_url = os.getenv("MCP_SERVER_URL")
    if not mcp_server_url:
        raise ValueError("MCP_SERVER_URL environment variable is not set")
    
    logger.debug(f"Creating MCP client for {mcp_server_url}")
    return MCPClient(lambda: _create_transport(mcp_server_url))