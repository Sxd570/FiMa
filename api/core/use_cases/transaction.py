from shared.logger import Logger
from shared.Utility.generate_id import generate_transaction_id
from core.database.transaction import TransactionDatabase
from core.models.io_models.transaction_io_models import (
    GetTransactionPayload,
    GetTransactionDBRequest,
    GetTransactionResponse,
    TransactionDetail
)

logger = Logger(__name__)

class TransactionUseCase:
    def __init__(self):
        self.goal_database = TransactionDatabase()

        self.user_id = None
        self.transaction_id = None

    def get_transactions(self, payload: GetTransactionPayload):
        try:
            self.user_id = payload.user_id

            filters = payload.filters if payload.filters else {}
            limit = payload.limit if payload.limit else 15
            offset = payload.offset if payload.offset else 0

            db_request = GetTransactionDBRequest(
                user_id=self.user_id,
                filters=filters,
                limit=limit,
                offset=offset
            )

            transactions_data = self.goal_database.get_transactions(
                db_request=db_request
            )

            transaction_details = GetTransactionResponse(
                transactions=[
                    TransactionDetail(
                        transaction_id=transaction.transaction_id,
                        transaction_type_id=transaction.transaction_type_id,
                        transaction_info=transaction.transaction_info,
                        transaction_amount=float(transaction.transaction_amount),
                        transaction_date=transaction.transaction_date,
                        category_name=transaction.category_name
                    ) for transaction in transactions_data.transactions
                ]
            )

            return transaction_details
        except Exception as e:
            logger.error(f"Error in get_transactions use case: {e}")
            raise e