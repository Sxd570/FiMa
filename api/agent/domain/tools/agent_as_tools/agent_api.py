import json
import os
from strands import tool

from domain.agent.base import AgentFactory
from domain.prompts import AGENT_API_SYSTEM_INSTRUCTIONS
from domain.use_cases.mcp_client import get_mcp_client
from domain.tools.get_current_date import get_current_date_tool
from domain.tools.execute_code import execute_code_tool

from shared.logger import Logger
logger = Logger(__name__)


def _is_get_tool(tool_name: str) -> bool:
    """Check if an MCP tool is a GET/read-only operation based on naming convention."""
    return tool_name.startswith("get_")


def _create_list_tools_tool(mcp_tools: list):
    """Create a tool that returns the schema of available MCP tools."""
    
    # Build schema information for each tool
    tool_schemas = []
    for t in mcp_tools:
        schema = {
            "name": t.tool_name,
            "description": t.mcp_tool.description,
            "parameters": t.mcp_tool.inputSchema if hasattr(t.mcp_tool, 'inputSchema') else {},
        }
        tool_schemas.append(schema)
    
    @tool
    def list_available_tools() -> str:
        """
        List all available MCP tools with their schemas.
        
        Use this to understand what tools are available and their parameters
        before writing code to call them via execute_code.
        
        Returns:
        - str: JSON array of tool schemas with name, description, and parameters.
        """
        return json.dumps(tool_schemas, indent=2)
    
    return list_available_tools


def agent_api_agent_as_tool(callback_handler=None, user_id: str = None):
    @tool
    def agent_api_bot(query: str) -> str:
        """
        TODO: Write tool description.
        """

        try:
            # Keep the MCP connection open for the entire duration of the agent call
            with get_mcp_client() as mcp_client:
                mcp_tools = mcp_client.list_tools_sync()

                # Separate GET (read) tools from non-GET (write) tools
                # GET operations go through execute_code, non-GET are direct tools
                non_get_tools = [t for t in mcp_tools if not _is_get_tool(t.tool_name)]
                
                # Create the execute_code tool with MCP client and user_id
                exec_code_tool = execute_code_tool(
                    mcp_client=mcp_client,
                    user_id=user_id or "",
                )
                
                # Create list_available_tools so agent knows what tools exist
                list_tools_tool = _create_list_tools_tool(mcp_tools)
                
                # Build tool list:
                # - execute_code: for GET operations via code
                # - list_available_tools: to see available MCP tool schemas
                # - non-GET MCP tools: for create/update/delete operations
                # - get_current_date: utility tool
                tools_list = [
                    exec_code_tool,
                    list_tools_tool,
                    get_current_date_tool(),
                ] + non_get_tools

                agent_factory = AgentFactory(
                    system_prompt=AGENT_API_SYSTEM_INSTRUCTIONS,
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