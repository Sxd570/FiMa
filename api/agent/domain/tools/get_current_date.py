from strands import tool
from datetime import datetime

from shared.logger import Logger
logger = Logger(__name__)


def get_current_date_tool():
    @tool
    def get_current_date() -> str:
        """
        Get the current date and time.
        
        Returns:
        - str: Current date and time in ISO 8601 format (YYYY-MM-DD HH:MM:SS).
        
        This tool provides the current date and time, useful for context-aware
        financial queries and decision-making.
        """
        try:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"Current date retrieved: {current_date}")
            return current_date
        except Exception as e:
            logger.error(f"Error retrieving current date: {str(e)}")
            raise e
    
    return get_current_date
