from mangum import Mangum
from shared.logger import Logger
from api_definitions.api_server import app

logger = Logger(__name__)

try:
    handler = Mangum(app)
except Exception as e:
    logger.error(f"Error in API handler: {e}")