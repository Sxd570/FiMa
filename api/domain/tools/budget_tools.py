from shared.Utility.api_request import APIRequest
from strands import tool
from shared.logger import Logger
from constants import APIConstants, ToolConstants

logger = Logger(__name__)


class BudgetTools:
    def __init__(self):
        ...
    
    @tool
    def get_budget_overview(self, user_id: str, month: str):
        """
        This tool is used to get the budget overview for a user for a specific month.

        Args:
            user_id (str): The ID of the user.
            month (str): The month for which to get the budget overview in 'YYYY-MM' format.

        Returns:
            dict: Response is a dictionary with the following fields:
                - budget_total_budget: Total budget allocated for the month
                - budget_total_spent: Total amount spent in the month
                - budget_near_limit_count: Number of budgets near their limit
                - budget_over_limit_count: Number of budgets that have exceeded their limit
                - budget_remaining_amount: Remaining budget for the month
                - budget_percentage_spent: Percentage of budget spent
                - budget_date: The month for the budget overview
        Raises:
            Exception: If there is an error during the API request.

        Example response:
        {
            "budget_total_budget": 2000.0,
            "budget_total_spent": 1500.0,
            "budget_near_limit_count": 2,
            "budget_over_limit_count": 1,
            "budget_remaining_amount": 500.0,
            "budget_percentage_spent": 75.0,
            "budget_date": "2023-10"
        }
        """
        def _get_budget_overview(user_id: str, month: str):
            try:
                api_request = APIRequest(
                    http_method = APIConstants.KEY_GET_METHOD.value,
                    endpoint = f"/budget/overview/{user_id}",
                    payload = {
                        ToolConstants.KEY_MONTH.value: month
                    }
                )
                response = api_request.execute()

                return response
            except Exception as e:
                logger.error(f"Error in get budget overview tool, {str(e)}")
                raise e
        
        return _get_budget_overview(user_id, month)
        
    @tool
    def get_budget_details(self, user_id: str, month: str):
        """
        This tool is used to get details of all budgets created by a user for a specific month.

        Args:
            user_id (str): The ID of the user.
            month (str): The month for which to get the budget details in 'YYYY-MM' format.

        Returns:
            dict: Response is a dictionary containing a list of budget details with the following fields for each:
                - budget_id: Unique identifier for the budget
                - category_name: Name of the budget category
                - budget_allocated_amount: Amount allocated for the budget
                - budget_spent_amount: Amount spent from the budget
                - budget_allocated_month: The month for which the budget is allocated
                - budget_remaining_amount: Remaining amount in the budget
                - is_limit_reached: Whether the budget limit has been reached (boolean)
                - is_over_limit: Whether the budget has been exceeded (boolean)
                - budget_percentage_spent: Percentage of the budget that has been spent
        Raises:
            Exception: If there is an error during the API request.

        Example response:
        {
            "budget_details": [
                {
                    "budget_id": "1234-abcd",
                    "category_name": "test_budget",
                    "budget_allocated_amount": 15000.0,
                    "budget_spent_amount": 0.0,
                    "budget_allocated_month": "2025-01",
                    "budget_remaining_amount": 15000.0,
                    "is_limit_reached": false,
                    "is_over_limit": false,
                    "budget_percentage_spent": 0.0
                },
                {
                    "budget_id": "abcd-1234",
                    "category_name": "test_budget 3",
                    "budget_allocated_amount": 20000.0,
                    "budget_spent_amount": 0.0,
                    "budget_allocated_month": "2025-01",
                    "budget_remaining_amount": 20000.0,
                    "is_limit_reached": false,
                    "is_over_limit": false,
                    "budget_percentage_spent": 0.0
                }
            ]
        }
        """
        try:
            api_request = APIRequest(
                http_method = APIConstants.KEY_GET_METHOD.value,
                endpoint = f"/budget/details/{user_id}",
                payload = {
                    ToolConstants.KEY_MONTH.value: month
                }
            )
            response = api_request.execute()
            return response
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