from api.agent.shared.Utility.api_request import APIRequest
from strands import tool
from shared.logger import Logger
from constants import APIConstants

logger = Logger(__name__)


class TransactionTools:

    @tool
    def get_transactions(self, user_id: str, filters: dict, limit: int, offset: int):
        """
        Fetches transactions for a given user with optional filters, limit, and offset.

        Args:
            user_id (str): The ID of the user whose transactions are to be fetched.

            filters (dict, optional): Dictionary of filters to apply to the transaction query. Use only if applicable. Following fields are optional:
                - from_date (str): The start date for filtering transactions. Format: YYYY-MM-DD. Example: "2025-01-01"
                - to_date (str): The end date for filtering transactions. Format: YYYY-MM-DD. Example: "2025-01-01"
                - budget_id (str): The ID of the budget to filter transactions. Example: "d5c8bff9-6b25-5aa0-8d6b-28dc687011cc"

            limit (int): The maximum number of transactions to return. Example: 15
            offset (int): The number of transactions to skip before starting to collect the result set. Example: 0

        Returns:
            dict: A dictionary containing the key `transactions`, which is a list of transaction objects. Each object contains:
                - transaction_id (str): The unique identifier of the transaction.
                - budget_name (str): The name of the budget associated with the transaction.
                - transaction_type (str): The type of the transaction (e.g., "expense", "income").
                - transaction_info (str): Additional information about the transaction.
                - transaction_amount (float): The amount of the transaction.
                - transaction_date (str): The date of the transaction in 'YYYY-MM-DD' format.

        Raises:
            Exception: If there is an error during the API request.

        Example response:
        {
            "transactions": [
                {
                    "transaction_id": "23ac23b6-f222-59e0-943e-e8d1ba9e671b",
                    "budget_name": "Food",
                    "transaction_type": "expense",
                    "transaction_info": "food 1234",
                    "transaction_amount": 4500.0,
                    "transaction_date": "2025-01-01"
                },
                {
                    "transaction_id": "31fa589a-3adc-5fcb-b35a-1d92403933fd",
                    "budget_name": "Food",
                    "transaction_type": "expense",
                    "transaction_info": "food 1234",
                    "transaction_amount": 4500.0,
                    "transaction_date": "2025-01-01"
                }
            ]
        }
        """
        def _get_transactions(user_id: str, filters: dict, limit: int, offset: int):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_GET_METHOD.value,
                    endpoint=f"/transactions/{user_id}",
                    params={
                        "filters": filters,
                        "limit": limit,
                        "offset": offset
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in get transactions tool, {str(e)}")
                raise e

        return _get_transactions(user_id, filters, limit, offset)


    @tool
    def create_transaction(self, user_id: str, budget_id: str, transaction_type: str, transaction_info: str, transaction_amount: float, transaction_date: str):
        """
        Creates a new transaction for a user.

        Args:
            user_id (str): The ID of the user creating the transaction.
            budget_id (str): The ID of the budget associated with the transaction.
            transaction_type (str): The type of the transaction (e.g., "expense", "income").
            transaction_info (str): Additional information about the transaction.
            transaction_amount (float): The amount of the transaction.
            transaction_date (str): The date of the transaction. Format: YYYY-MM-DD.

        Returns:
            dict: A dictionary containing the created transaction.
                - transaction_id (str): The unique identifier of the transaction.
                - message (str): A message indicating the success of the operation.

        Raises:
            Exception: If there is an error during the API request.

        Example:
            {
                "transaction_id": "23ac23b6-f222-59e0-943e-e8d1ba9e671b",
                "message": "Transaction created successfully"
            }
        """
        def _create_transaction(user_id: str, budget_id: str, transaction_type: str, transaction_info: str, transaction_amount: float, transaction_date: str):
            try:
                api_request = APIRequest(
                    http_method=APIConstants.KEY_POST_METHOD.value,
                    endpoint=f"/transactions/{user_id}",
                    body={
                        "budget_id": budget_id,
                        "transaction_type": transaction_type,
                        "transaction_info": transaction_info,
                        "transaction_amount": transaction_amount,
                        "transaction_date": transaction_date
                    }
                )
                response = api_request.execute()
                return response
            except Exception as e:
                logger.error(f"Error in create transaction tool, {str(e)}")
                raise e
        
        return _create_transaction(user_id, budget_id, transaction_type, transaction_info, transaction_amount, transaction_date)