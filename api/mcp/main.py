import uvicorn
from fastmcp import FastMCP

from tools.register_tools import register_all_tools
from utils.logger import Logger


logger = Logger(__name__)


def create_mcp() -> FastMCP:
    mcp = FastMCP(name="fima-mcp")
    register_all_tools(mcp)
    return mcp


if __name__ == "__main__":
    logger.debug("Creating FiMa MCP server...")
    mcp = create_mcp()

    http_app = mcp.http_app(stateless_http=True)

    logger.debug("Starting FiMa MCP server with uvicorn on 0.0.0.0:8000")
    uvicorn.run(http_app, host="0.0.0.0", port=8000)

