"""
MCP Client for communicating with the FiMa MCP Server.

Uses strands-agents' built-in MCPClient with streamable HTTP transport
to connect to the FastMCP server (stateless_http=True).
"""

from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp import MCPClient

from shared.logger import Logger


logger = Logger(__name__)

MCP_SERVER_URL = "http://localhost:8002"


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
    logger.debug(f"Creating MCP client for {MCP_SERVER_URL}")
    return MCPClient(lambda: streamablehttp_client(f"{MCP_SERVER_URL}/mcp/"))