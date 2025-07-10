from fastapi import APIRouter
from shared.logger import Logger
from core.use_cases.transaction import TransactionUseCase
from core.models.io_models.transaction_io_models import (
    GetTransactionRequest,
    GetTransactionPayload
)

router = APIRouter()
logger = Logger(__name__)


@router.get("/transactions/{user_id}")
def get_transactions(user_id: str, request: GetTransactionRequest):
    try:
        if request.filters:
            filters = request.filters
        if request.limit:
            limit = request.limit
        if request.offset:
            offset = request.offset

        payload = GetTransactionPayload(
            user_id=user_id,
            filters=filters,
            limit=limit,
            offset=offset
        )

        transaction = TransactionUseCase()

        transactions_data = transaction.get_transactions(
            payload=payload
        )
        return transactions_data
    except Exception as e:
        logger.error(f"Error fetching transactions for user {user_id}: {e}")
        raise e
    

@router.post("/transactions/{user_id}")
def create_transaction(user_id: str):
    try:
        ...
    except Exception as e:
        logger.error(f"Error creating transaction for user {user_id}: {e}")
        raise e
    

@router.put("/transactions/{user_id}")
def update_transaction(user_id: str):
    try:
        ...
    except Exception as e:
        logger.error(f"Error updating transaction for user {user_id}: {e}")
        raise e


@router.delete("/transactions/{user_id}")
def delete_transaction(user_id: str):
    try:
        ...
    except Exception as e:
        logger.error(f"Error deleting transaction for user {user_id}: {e}")
        raise e