from shared.Utility.api_request import APIRequest
from strands import tool
from shared.logger import Logger
from constants import APIConstants, BudgetConstants

logger = Logger(__name__)


class BudgetTools:
    def __init__(self):
        ...
    
    @tool
    def get_budget_overview(self, user_id: str, budget_month: str):
        """
        This tool is used to get the budget overview for a user for a specific month.

        Args:
            user_id (str): The ID of the user.
            budget_month (str): The month for which to get the budget overview in 'YYYY-MM' format.

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
        def _get_budget_overview(user_id: str, budget_month: str):
            try:
                api_request = APIRequest(
                    http_method = APIConstants.KEY_GET_METHOD.value,
                    endpoint = f"/budget/{user_id}/overview",
                    payload = {
                        BudgetConstants.KEY_BUDGET_MONTH.value: budget_month
                    }
                )
                response = api_request.execute()

                return response
            except Exception as e:
                logger.error(f"Error in get budget overview tool, {str(e)}")
                raise e
        
        return _get_budget_overview(user_id, budget_month)
        
    @tool
    def get_budget_details(self, user_id: str, budget_month: str):
        """
        This tool is used to get details of all budgets created by a user for a specific month.

        Args:
            user_id (str): The ID of the user.
            budget_month (str): The month for which to get the budget details in 'YYYY-MM' format.

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
        def _get_budget_details(user_id: str, budget_month: str):
            try:
                api_request = APIRequest(
                    http_method = APIConstants.KEY_GET_METHOD.value,
                    endpoint = f"/budget/{user_id}/details",
                    payload = {
                        BudgetConstants.KEY_BUDGET_MONTH.value: budget_month
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in get budget detail tool, {str(e)}")
                raise e

        return _get_budget_details(user_id, budget_month)

    @tool
    def edit_budget_limit(self, user_id: str, budget_id: str, new_budget_limit: float):
        """
        This tool is used to edit the limit of an existing budget for a user for a specific budget ID.

        Args:
            user_id (str): The ID of the user.
            budget_id (str): The ID of the budget to be edited.
            new_budget_limit (float): The new limit to be set for the budget.

        Returns:
            dict: Response is a dictionary with the following fields:
                - message: Confirmation message indicating the budget limit has been updated.

        Raises:
            Exception: If there is an error during the API request.

        Example response:
        {
            "message": "Budget limit updated successfully"
        }
        """
        def _edit_budget_limit(user_id: str, budget_id: str, new_budget_limit: float):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_PATCH_METHOD.value,
                    endpoint=f"/budget/{user_id}/edit_limit/{budget_id}",
                    payload={
                        BudgetConstants.KEY_NEW_BUDGET_LIMIT.value: new_budget_limit
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in edit budget limit tool, {str(e)}")
                raise e
            
        return _edit_budget_limit(user_id, budget_id, new_budget_limit)
        
    @tool
    def delete_budget(self, user_id: str, budget_id: str):
        """
        This tool is used to delete an existing budget for a user for a specific budget ID.
        Args:
            user_id (str): The ID of the user.
            budget_id (str): The ID of the budget to be deleted.
        
        Returns:
            dict: Response is a dictionary with the following fields:
                - message: Confirmation message indicating the budget has been deleted.
            
        Raises:
            Exception: If there is an error during the API request.

        Example response:
        {
            "message": "Budget deleted successfully"
        }
        """
        def _delete_budget(user_id: str, budget_id: str):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_DELETE_METHOD.value,
                    endpoint=f"/budget/{user_id}/delete/{budget_id}"
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in delete budget tool, {str(e)}")
                raise e

        return _delete_budget(user_id, budget_id)

    @tool
    def create_budget(self, user_id: str, budget_limit: str, budget_name: str, budget_month: str, transaction_type: str, description: str):
        """
        This tool is used to create a new budget for a user.
        Args:
            user_id (str): The ID of the user.
            budget_limit (str): The limit for the new budget.
            budget_name (str): The name of the new budget.
            budget_month (str): The month for which the budget is being created in 'YYYY-MM' format.
            transaction_type (str): The type of transactions the budget applies to (e.g., "expense", "income").
            description (str): A brief description of the budget.
        
        Returns:
            dict: Response is a dictionary with the following fields:
                - message: Confirmation message indicating the budget has been created.
                - budget_id: The ID of the newly created budget.

        Raises:
            Exception: If there is an error during the API request.

        Example response:
        {
            "message": "Budget created successfully",
            "budget_id": "abcd-01234"
        }

        """
        def _create_budget(user_id: str, budget_limit: str, budget_name: str, budget_month: str, transaction_type: str, description: str):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_POST_METHOD.value,
                    endpoint=f"/budget/{user_id}/create",
                    payload={
                        BudgetConstants.KEY_BUDGET_LIMIT.value: budget_limit,
                        BudgetConstants.KEY_BUDGET_NAME.value: budget_name,
                        BudgetConstants.KEY_BUDGET_MONTH.value: budget_month,
                        BudgetConstants.KEY_TRANSACTION_TYPE.value: transaction_type,
                        BudgetConstants.KEY_DESCRIPTION.value: description
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in create budget tool, {str(e)}")
                raise e

        return _create_budget(user_id, budget_limit, budget_name, budget_month, transaction_type, description)