"""
MCP Client for communicating with the FiMa MCP Server.

This client makes HTTP requests to the MCP server to invoke tools
instead of using local tool implementations.
"""

import httpx
import json
from typing import Any, Dict, List, Optional
from shared.logger import Logger
from strands import tool


logger = Logger(__name__)


class MCPClient:
    """Client for communicating with the FiMa MCP Server."""

    def __init__(self, base_url: str = "http://localhost:8002"):
        """
        Initialize MCP Client.

        Args:
            base_url: The base URL of the MCP server
        """
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)
        self.request_id = 0

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools on the MCP server.

        Returns:
            A list of available tools with their descriptions and parameters

        Raises:
            Exception: If the tools list call fails
        """
        try:
            self.request_id += 1
            
            # Prepare the JSON-RPC request
            payload = {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": "tools/list",
                "params": {}
            }

            logger.debug("Listing available MCP tools")

            # Make the HTTP request to the MCP server
            response = self.client.post(
                f"{self.base_url}/",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()

            # Parse the response
            result = response.json()

            # Check for JSON-RPC errors
            if "error" in result:
                error_msg = result["error"].get("message", "Unknown error")
                logger.error(f"MCP tools list error: {error_msg}")
                raise Exception(f"MCP tools list failed: {error_msg}")

            # Extract the result
            if "result" in result:
                tools = result["result"].get("tools", [])
                logger.debug(f"Retrieved {len(tools)} available tools")
                return tools
            else:
                logger.warning("No result in MCP tools list response")
                return []

        except httpx.HTTPError as e:
            logger.error(f"HTTP error listing MCP tools: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in MCP tools list response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error listing MCP tools: {str(e)}")
            raise

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool on the MCP server via HTTP.

        Args:
            tool_name: The name of the tool to call
            arguments: The arguments to pass to the tool

        Returns:
            The result from the tool

        Raises:
            Exception: If the tool call fails
        """
        try:
            self.request_id += 1
            
            # Prepare the JSON-RPC request
            payload = {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }

            logger.debug(
                f"Calling MCP tool '{tool_name}' with arguments: {arguments}"
            )

            # Make the HTTP request to the MCP server
            response = self.client.post(
                f"{self.base_url}/",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()

            # Parse the response
            result = response.json()

            # Check for JSON-RPC errors
            if "error" in result:
                error_msg = result["error"].get("message", "Unknown error")
                logger.error(f"MCP tool error: {error_msg}")
                raise Exception(f"MCP tool '{tool_name}' failed: {error_msg}")

            # Extract the result
            if "result" in result:
                return result["result"]
            else:
                logger.warning(f"No result in MCP response for tool '{tool_name}'")
                return None

        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling MCP tool '{tool_name}': {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in MCP response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error calling MCP tool '{tool_name}': {str(e)}")
            raise

    def close(self):
        """Close the HTTP client connection."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Global MCP client instance
_mcp_client: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    """
    Get or create the global MCP client instance.

    Returns:
        MCPClient: The global MCP client instance
    """
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client




def create_mcp_tools():
    """Fetch tools from MCP server and wrap them as strands tools."""
    client = get_mcp_client()
    mcp_tool_definitions = client.list_tools()
    
    tools = []
    for tool_def in mcp_tool_definitions:
        tool_name = tool_def["name"]
        tool_description = tool_def.get("description", "")
        
        # Create a closure to capture tool_name
        def make_tool(name):
            @tool(name=name, description=tool_description)
            def mcp_tool(**kwargs):
                result = client.call_tool(name, kwargs)
                return result
            return mcp_tool
        
        tools.append(make_tool(tool_name))
    
    return tools