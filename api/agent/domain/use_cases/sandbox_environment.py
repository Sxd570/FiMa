"""
Sandbox Environment for executing LLM-generated Python code safely.

This module provides a restricted execution environment where the agent
can run Python code to fetch data via MCP tools, with security measures
to prevent malicious code execution.
"""

import json
import re
import threading
from datetime import datetime, timedelta
from typing import Any, Tuple

from shared.logger import Logger


logger = Logger(__name__)

# Timeout for code execution (seconds)
EXECUTION_TIMEOUT = 30

# Whitelist of allowed imports/modules
ALLOWED_IMPORTS = frozenset({
    "json",
    "datetime",
    "re",
})

# Dangerous patterns that should be blocked
DANGEROUS_PATTERNS = [
    # Import-based attacks
    r"\bimport\s+os\b",
    r"\bimport\s+sys\b",
    r"\bimport\s+subprocess\b",
    r"\bimport\s+shutil\b",
    r"\bimport\s+socket\b",
    r"\bimport\s+requests\b",
    r"\bimport\s+urllib\b",
    r"\bimport\s+http\b",
    r"\bimport\s+ftplib\b",
    r"\bimport\s+smtplib\b",
    r"\bimport\s+pickle\b",
    r"\bimport\s+marshal\b",
    r"\bimport\s+ctypes\b",
    r"\bfrom\s+os\b",
    r"\bfrom\s+sys\b",
    r"\bfrom\s+subprocess\b",
    r"\bfrom\s+shutil\b",
    r"\bfrom\s+socket\b",
    r"\bfrom\s+pickle\b",
    r"\bfrom\s+ctypes\b",
    
    # Dangerous built-in functions
    r"\b__import__\s*\(",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bcompile\s*\(",
    r"\bopen\s*\(",
    r"\bfile\s*\(",
    r"\binput\s*\(",
    r"\bbreakpoint\s*\(",
    
    # Attribute access attacks
    r"\b__builtins__\b",
    r"\b__globals__\b",
    r"\b__locals__\b",
    r"\b__code__\b",
    r"\b__class__\b",
    r"\b__bases__\b",
    r"\b__subclasses__\b",
    r"\b__mro__\b",
    r"\b__dict__\b",
    r"\b__getattribute__\b",
    r"\bgetattr\s*\(",
    r"\bsetattr\s*\(",
    r"\bdelattr\s*\(",
    r"\bvars\s*\(",
    r"\bdir\s*\(",
    r"\bglobals\s*\(",
    r"\blocals\s*\(",
    
    # System commands
    r"\bos\s*\.\s*system\b",
    r"\bos\s*\.\s*popen\b",
    r"\bos\s*\.\s*spawn\b",
    r"\bos\s*\.\s*exec\b",
    r"\bsubprocess\s*\.",
    
    # File operations
    r"\bos\s*\.\s*remove\b",
    r"\bos\s*\.\s*unlink\b",
    r"\bos\s*\.\s*rmdir\b",
    r"\bos\s*\.\s*mkdir\b",
    r"\bos\s*\.\s*rename\b",
    r"\bshutil\s*\.",
    
    # Network operations
    r"\bsocket\s*\.",
    r"\burllib\s*\.",
    r"\brequests\s*\.",
]

# Compile patterns for efficiency
COMPILED_DANGEROUS_PATTERNS = [re.compile(p, re.IGNORECASE) for p in DANGEROUS_PATTERNS]


def validate_code(code: str) -> Tuple[bool, str]:
    """
    Validate that the code is safe to execute.
    
    Checks for:
    - Dangerous imports
    - Dangerous function calls
    - Attribute access attacks
    - File/network operations
    
    Args:
        code: The Python code string to validate
        
    Returns:
        Tuple of (is_safe, error_message).
        If is_safe is True, error_message will be empty.
    """
    if not code or not code.strip():
        return False, "Code cannot be empty"
    
    for pattern in COMPILED_DANGEROUS_PATTERNS:
        match = pattern.search(code)
        if match:
            return False, f"Dangerous pattern detected: '{match.group()}'"
    
    return True, ""


def execute_code(
    code: str,
    mcp_client: Any,
    user_id: str,
) -> dict:
    """
    Execute Python code in a sandboxed environment.
    
    The code has access to:
    - call_tool(name, **args): Function to invoke MCP tools
    - user_id: The current user's ID
    - json: JSON module for parsing/serializing
    - datetime, timedelta: For date operations
    
    The code must store its final output in a variable named 'result'.
    
    Args:
        code: The Python code to execute
        mcp_client: The MCP client instance for tool calls
        user_id: The current user's ID
        
    Returns:
        dict with keys:
        - success (bool): Whether execution succeeded
        - result (Any): The value of 'result' variable if successful
        - error (str): Error message if failed
    """
    # Validate code first
    is_safe, error_msg = validate_code(code)
    if not is_safe:
        logger.warning(f"Code validation failed: {error_msg}")
        return {
            "success": False,
            "result": None,
            "error": f"Code validation failed: {error_msg}",
        }
    
    # Log the code being executed
    logger.info(f"Executing sandboxed code:\n{code}")
    
    # Create the call_tool wrapper
    def call_tool(tool_name: str, **kwargs) -> Any:
        """
        Call an MCP tool by name with the provided arguments.
        
        Args:
            tool_name: Name of the MCP tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            The tool's response data
        """
        logger.debug(f"call_tool invoked: {tool_name} with args {kwargs}")
        response = mcp_client.call_tool_sync(tool_name, kwargs)
        # Extract content from MCP response
        if hasattr(response, 'content') and response.content:
            # MCP returns content as a list of content blocks
            for block in response.content:
                if hasattr(block, 'text'):
                    try:
                        return json.loads(block.text)
                    except json.JSONDecodeError:
                        return block.text
            return response.content
        return response
    
    # Build restricted namespace
    sandbox_namespace = {
        # Pre-injected context
        "call_tool": call_tool,
        "user_id": user_id,
        
        # Allowed modules
        "json": json,
        "datetime": datetime,
        "timedelta": timedelta,
        
        # Safe built-ins only
        "True": True,
        "False": False,
        "None": None,
        "len": len,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
        "range": range,
        "enumerate": enumerate,
        "zip": zip,
        "map": map,
        "filter": filter,
        "sorted": sorted,
        "reversed": reversed,
        "sum": sum,
        "min": min,
        "max": max,
        "abs": abs,
        "round": round,
        "isinstance": isinstance,
        "print": lambda *args, **kwargs: logger.debug(f"[sandbox print] {' '.join(str(a) for a in args)}"),
    }
    
    # Execute with timeout
    execution_result = {"success": False, "result": None, "error": None}
    
    def run_code():
        try:
            exec(code, {"__builtins__": {}}, sandbox_namespace)
            
            if "result" not in sandbox_namespace:
                execution_result["success"] = False
                execution_result["error"] = (
                    "Code must store final output in a variable named 'result'. "
                    "Example: result = call_tool('get_transactions', user_id=user_id, limit=100)"
                )
            else:
                execution_result["success"] = True
                execution_result["result"] = sandbox_namespace["result"]
                
        except Exception as e:
            logger.error(f"Sandbox execution error: {str(e)}")
            execution_result["success"] = False
            execution_result["error"] = f"Execution error: {str(e)}"
    
    # Run in thread with timeout
    thread = threading.Thread(target=run_code)
    thread.start()
    thread.join(timeout=EXECUTION_TIMEOUT)
    
    if thread.is_alive():
        logger.error(f"Code execution timed out after {EXECUTION_TIMEOUT} seconds")
        return {
            "success": False,
            "result": None,
            "error": f"Execution timed out after {EXECUTION_TIMEOUT} seconds. "
                     "Consider optimizing your code or reducing the data scope.",
        }
    
    return execution_result
