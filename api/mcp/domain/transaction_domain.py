from typing import Any, Dict, Optional
from uuid import UUID

from constants import APIConstants, TransactionConstants
from models.transaction_models import (
    TransactionType,
    GetTransactionsResponse,
    CreateTransactionResponse,
    TransactionItem,
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
        limit: Optional[int],
        offset: Optional[int],
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        budget_id: Optional[UUID] = None,
    ) -> GetTransactionsResponse:
        try:
            params: Dict[str, Any] = {}
            if limit is not None:
                params[TransactionConstants.KEY_LIMIT.value] = limit
            if offset is not None:
                params[TransactionConstants.KEY_OFFSET.value] = offset
            if from_date is not None:
                params[TransactionConstants.KEY_FROM_DATE.value] = from_date
            if to_date is not None:
                params[TransactionConstants.KEY_TO_DATE.value] = to_date
            if budget_id is not None:
                params[TransactionConstants.KEY_BUDGET_ID.value] = str(budget_id)

            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=f"/transactions/{user_id}",
                params=params,
            )
            response = api_request.execute()
            raw_transactions = response.get(TransactionConstants.KEY_TRANSACTIONS.value) or []
            if not raw_transactions:
                return GetTransactionsResponse(
                    transactions=[],
                    has_more=response.get(TransactionConstants.KEY_HAS_MORE.value),
                )
            transactions = [
                TransactionItem(
                    transaction_id=item.get(TransactionConstants.KEY_TRANSACTION_ID.value),
                    budget_name=item.get(TransactionConstants.KEY_BUDGET_NAME.value),
                    transaction_type=item.get(TransactionConstants.KEY_TRANSACTION_TYPE.value),
                    transaction_info=item.get(TransactionConstants.KEY_TRANSACTION_INFO.value),
                    transaction_amount=item.get(TransactionConstants.KEY_TRANSACTION_AMOUNT.value),
                    transaction_date=item.get(TransactionConstants.KEY_TRANSACTION_DATE.value),
                )
                for item in raw_transactions
            ]
            return GetTransactionsResponse(
                transactions=transactions,
                has_more=response.get(TransactionConstants.KEY_HAS_MORE.value),
            )
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
            return CreateTransactionResponse(
                transaction_id=response.get(TransactionConstants.KEY_TRANSACTION_ID.value),
                message=response.get(TransactionConstants.KEY_MESSAGE.value),
            )
        except Exception as e:
            logger.error(f"Error in TransactionDomain.create_transaction: {str(e)}")
            raise


