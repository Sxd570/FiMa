from shared.Utility.api_request import APIRequest
from strands import tool
from shared.logger import Logger

logger = Logger(__name__)


class BudgetTools:
    def __init__(self):
        ...
    
    @tool
    def get_budget_overview(self, user_id: str, month: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in get budget overview tool, {str(e)}")
            raise e
        
    @tool
    def get_budget_details(self, user_id: str, month: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in get budget detail tool, {str(e)}")
            raise e
        
    @tool
    def edit_budget_limit(self, user_id: str, budget_id: str, new_budget_limit: float):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in edit budget limit tool, {str(e)}")
            raise e
        
    @tool
    def delete_budget(self, user_id: str, budget_id: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in delete budget tool, {str(e)}")
            raise e
        
    
    @tool
    def create_budget(self, user_id: str, budget_limit: str, budget_name: str, month: str, transaction_type: str, description: str):
        """
        function description
        """
        try:
            ...
        except Exception as e:
            logger.error(f"Error in create budget tool, {str(e)}")
            raise e