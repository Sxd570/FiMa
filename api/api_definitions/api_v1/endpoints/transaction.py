from fastapi import APIRouter
from shared.logger import Logger
from domain.use_cases.transaction import TransactionUseCase
from domain.models.io_models.transaction_io_models import (
    GetTransactionRequest,
    GetTransactionPayload,
    CreateTransactionRequest,
    CreateTransactionPayload
)

router = APIRouter()
logger = Logger(__name__)


@router.get("/transactions/{user_id}")
def get_transactions(user_id: str, request: GetTransactionRequest):
    try:
        filters = request.filters if hasattr(request, 'filters') and request.filters is not None else None
        limit = request.limit if hasattr(request, 'limit') and request.limit is not None else None
        offset = request.offset if hasattr(request, 'offset') and request.offset is not None else None

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
def create_transaction(user_id: str, request: CreateTransactionRequest):
    try:
        budget_id = request.budget_id
        transaction_type = request.transaction_type
        transaction_info = request.transaction_info
        transaction_amount = request.transaction_amount
        transaction_date = request.transaction_date

        payload = CreateTransactionPayload(
            user_id=user_id,
            budget_id=budget_id,
            transaction_type=transaction_type,
            transaction_info=transaction_info,
            transaction_amount=transaction_amount,
            transaction_date=transaction_date
        )

        transaction = TransactionUseCase()

        response = transaction.create_transaction(
            payload=payload
        )

        return response

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