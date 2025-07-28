from mangum import Mangum
from shared.logger import Logger

logger = Logger(__name__)

try:
    ...
except Exception as e:
    logger.error(f"Error in MCP handler: {e}")