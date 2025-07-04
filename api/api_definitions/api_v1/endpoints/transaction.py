from fastapi import APIRouter
from shared.logger import Logger

router = APIRouter()
logger = Logger(__name__)


@router.get("/transactions/categories/{user_id}")
async def get_transaction_categories(user_id: str):
    try:
        pass
    except Exception as e:
        logger.error(f"Error in get_transaction_categories: {e}")
        raise e
    

@router.post("/transactions/categories/{user_id}")
async def create_transaction_category(user_id: str, request: AddTransactionCategoryPayload):
    try:
        pass
    except Exception as e:
        logger.error(f"Error in create_transaction_category: {e}")
        raise e
    

@router.get("/transactions/transactiontypes/{user_id}")
async def get_transaction_types(user_id: str):
    try:
        pass
    except Exception as e:
        logger.error(f"Error in get_transaction_types: {e}")
        raise e
    

@router.post("/transactions/transactiontypes/{user_id}")
async def create_transaction_type(user_id: str, request: AddTransactionTypePayload):
    try:
        pass
    except Exception as e:
        logger.error(f"Error in create_transaction_type: {e}")
        raise e
    

