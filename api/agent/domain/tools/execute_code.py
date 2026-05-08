"""
Execute Code Tool for the Agent API.

This tool allows the agent to execute Python code in a sandboxed environment
to fetch data from MCP tools programmatically, enabling efficient handling
of paginated data and complex data retrieval patterns.
"""

import json
from typing import Any, Callable

from strands import tool

from shared.logger import Logger


logger = Logger(__name__)


def execute_code_tool(mcp_client: Any, user_id: str) -> Callable:
    """
    Create an execute_code tool with the MCP client and user_id pre-configured.

    Args:
        mcp_client: The MCP client instance for tool calls
        user_id: The current user's ID

    Returns:
        A @tool decorated function ready to be used by the agent
    """
    # Import here to avoid circular imports
    from domain.use_cases.sandbox_environment import SandboxEnvironment

    # Create sandbox instance
    sandbox = SandboxEnvironment(
        mcp_client=mcp_client,
        user_id=user_id,
    )

    @tool
    def execute_code(code: str) -> str:
        """
        Execute Python code for read-only Fima data retrieval.

        Use this only for GET/read operations, especially when pagination,
        batching, filtering, or aggregation is needed.

        This tool runs Python code in a sandboxed environment with access to
        MCP read tools via the call_tool() function.

        Use this tool for requests like:
            - Fetching transactions
            - Fetching budget overviews or budget details
            - Fetching goal details or progress
            - Handling pagination across read endpoints
            - Combining multiple read calls into one factual result

        Do NOT use this tool for write operations, including:
            - Creating budgets, goals, transactions, or other records
            - Updating budgets, limits, goals, transactions, or user data
            - Deleting any data
            - Calling any MCP tool whose name or schema indicates create,
              update, edit, patch, delete, remove, archive, or any other
              mutating behavior

        For write operations, use the dedicated direct MCP write tools instead.

        **Available in the sandbox:**
            - call_tool(tool_name, **kwargs): Call MCP read tools by name
            - user_id: The current user's ID as a string
            - json: For JSON operations
            - datetime, timedelta: For date handling
            - Basic Python: len, str, int, list, dict, range, etc.

        **Important Rules:**
            1. Store your final output in a variable named `result`
            2. Only use call_tool() for GET/read operations
            3. For pagination, use the `has_more` field in responses
            4. Respect tool schemas and required parameters
            5. The code has a 30 second timeout
            6. Return only data relevant to the user's request

        **Pagination with has_more:**
        All paginated endpoints return a `has_more` boolean field indicating
        if more records exist. Use this instead of checking if list is empty:
            - get_transactions: returns {transactions: [...], has_more: bool}
            - get_budget_details: returns {budget_details: [...], has_more: bool}
            - get_goal_details: returns {goal_details: [...], has_more: bool}

        **Example - Fetch all transactions with pagination:**
        ```python
        all_transactions = []
        offset = 0
        limit = 100

        while True:
            response = call_tool(
                "get_transactions",
                user_id=user_id,
                limit=limit,
                offset=offset
            )

            transactions = response.get("transactions", [])
            all_transactions.extend(transactions)

            # Use has_more to check if more records exist
            if not response.get("has_more", False):
                break

            offset += limit

        result = {
            "transactions": all_transactions,
            "total": len(all_transactions)
        }
        ```

        Parameters:
            code (str): Python code to execute. Must set a `result` variable.

        Returns:
            str: JSON string of the result, or an error message if failed.
        """
        logger.info("execute_code tool invoked")

        execution_result = sandbox.execute(code)

        if execution_result["success"]:
            try:
                return json.dumps(execution_result["result"], default=str)
            except (TypeError, ValueError) as e:
                logger.error(f"Failed to serialize result: {e}")
                return json.dumps({
                    "error": f"Failed to serialize result: {str(e)}",
                    "raw_result": str(execution_result["result"])
                })
        else:
            error_response = {
                "error": execution_result["error"],
                "hint": "Check your code syntax and ensure 'result' variable is set. "
                        "You can retry with corrected code."
            }
            return json.dumps(error_response)

    return execute_code
