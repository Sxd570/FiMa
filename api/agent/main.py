from mangum import Mangum
from shared.logger import Logger
from api_definitions.api_server import app
import uvicorn
import os

logger = Logger(__name__)


if __name__ == "__main__":
    try:
        # handler = Mangum(app)
        handler = app

        uvicorn.run(handler, host="0.0.0.0", port=8001)

    except Exception as e:
        logger.error(f"Error in API handler: {e}")
