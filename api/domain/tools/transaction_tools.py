from shared.Utility.api_request import APIRequest
from strands import tool
from shared.logger import Logger

logger = Logger(__name__)


class TransactionTools:

    @tool
    def get_transactions(self, user_id: str, filters: dict, limit: int, offset: int):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in get transaction overview tool, {str(e)}")
            raise e
        
    
    @tool
    def create_transaction(self, user_id: str, category_id: str, transaction_type: str, transaction_info: str, transaction_amount: float, transaction_date: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in create transaction tool, {str(e)}")
            raise e