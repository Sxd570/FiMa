from typing import Any, Dict, Optional
from uuid import UUID

from constants import APIConstants, TransactionConstants
from models.transaction_models import (
    TransactionType,
    GetTransactionsResponse,
    CreateTransactionResponse,
    TransactionFilters,
)
from utils.api_request import APIRequest
from utils.logger import Logger


logger = Logger(__name__)


class TransactionDomain:
    """
    Domain layer for transaction-related MCP tools.
    """

    def get_transactions(
        self,
        user_id: UUID,
        filters: Optional[TransactionFilters],
        limit: int,
        offset: int,
    ) -> GetTransactionsResponse:
        try:
            payload: Dict[str, Any] = {
                TransactionConstants.KEY_LIMIT.value: limit,
                TransactionConstants.KEY_OFFSET.value: offset,
            }
            if filters is not None:
                payload[TransactionConstants.KEY_FILTERS.value] = filters.dict()

            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=f"/transactions/{user_id}",
                payload=payload,
            )
            response = api_request.execute()
            return GetTransactionsResponse(**response)
        except Exception as e:
            logger.error(f"Error in TransactionDomain.get_transactions: {str(e)}")
            raise

    def create_transaction(
        self,
        user_id: UUID,
        budget_id: UUID,
        transaction_type: TransactionType,
        transaction_info: str,
        transaction_amount: float,
        transaction_date: str,
    ) -> CreateTransactionResponse:
        try:
            payload = {
                TransactionConstants.KEY_BUDGET_ID.value: str(budget_id),
                TransactionConstants.KEY_TRANSACTION_TYPE.value: transaction_type.value,
                TransactionConstants.KEY_TRANSACTION_INFO.value: transaction_info,
                TransactionConstants.KEY_TRANSACTION_AMOUNT.value: transaction_amount,
                TransactionConstants.KEY_TRANSACTION_DATE.value: transaction_date,
            }

            api_request = APIRequest(
                http_method=APIConstants.KEY_POST_METHOD.value,
                endpoint=f"/transactions/{user_id}",
                payload=payload,
            )
            response = api_request.execute()
            return CreateTransactionResponse(**response)
        except Exception as e:
            logger.error(f"Error in TransactionDomain.create_transaction: {str(e)}")
            raise


