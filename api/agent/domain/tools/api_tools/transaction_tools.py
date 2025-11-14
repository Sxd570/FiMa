from typing import Optional
from uuid import UUID
from pydantic import Field
from strands import tool

from constants import APIConstants, TransactionConstants

from domain.models.io_models.api_tool_models.transaction_model import (
    TransactionType,
    GetTransactionsResponse,
    CreateTransactionResponse,
    TransactionFilters
)

from shared.Utility.api_request import APIRequest
from shared.logger import Logger

logger = Logger(__name__)


@tool
def get_transactions(
    user_id: UUID = Field(..., description="The unique ID of the user whose transactions are to be fetched."),
    filters: Optional[TransactionFilters] = Field(None, description="Optional filters for transactions."),
    limit: int = Field(15, gt=0, le=100, description="Maximum number of transactions to return (default: 15, max: 100)."),
    offset: int = Field(0, ge=0, description="Number of transactions to skip before starting to collect the result set.")
) -> GetTransactionsResponse:
    """
    Fetches transactions for a given user with optional filters, limit, and offset.
    """
    try:
        api_request = APIRequest(
            http_method=APIConstants.KEY_GET_METHOD.value,
            endpoint=f"/transactions/{user_id}",
            params={
                TransactionConstants.KEY_FILTERS.value: filters.dict() if filters else {},
                TransactionConstants.KEY_LIMIT.value: limit,
                TransactionConstants.KEY_OFFSET.value: offset
            }
        )
        response = api_request.execute()
        return GetTransactionsResponse(**response)
    except Exception as e:
        logger.error(f"Error in get transactions tool, {str(e)}")
        raise e


@tool
def create_transaction(
    user_id: UUID = Field(..., description="The unique ID of the user creating the transaction."),
    budget_id: UUID = Field(..., description="The unique ID of the budget associated with the transaction."),
    transaction_type: TransactionType = Field(..., description="Type of the transaction. Must be 'expense' or 'income'."),
    transaction_info: str = Field(..., min_length=1, max_length=255, description="Additional information about the transaction."),
    transaction_amount: float = Field(..., gt=0, description="Amount of the transaction (must be greater than 0)."),
    transaction_date: str = Field(..., description="Date of the transaction in 'YYYY-MM-DD' format.")
) -> CreateTransactionResponse:
    """
    Creates a new transaction for a user.
    """
    try:
        api_request = APIRequest(
            http_method=APIConstants.KEY_POST_METHOD.value,
            endpoint=f"/transactions/{user_id}",
            body={
                TransactionConstants.KEY_BUDGET_ID.value: str(budget_id),
                TransactionConstants.KEY_TRANSACTION_TYPE.value: transaction_type.value,
                TransactionConstants.KEY_TRANSACTION_INFO.value: transaction_info,
                TransactionConstants.KEY_TRANSACTION_AMOUNT.value: transaction_amount,
                TransactionConstants.KEY_TRANSACTION_DATE.value: transaction_date
            }
        )
        response = api_request.execute()
        return CreateTransactionResponse(**response)
    except Exception as e:
        logger.error(f"Error in create transaction tool, {str(e)}")
        raise e
