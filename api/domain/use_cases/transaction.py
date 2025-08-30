from shared.logger import Logger
from shared.Utility.generate_id import generate_transaction_id
from domain.database.transaction import TransactionDatabase
from domain.models.io_models.transaction_io_models import (
    GetTransactionPayload,
    GetTransactionDBRequest,
    GetTransactionResponse,
    TransactionDetail,
    CreateTransactionPayload,
    CreateTransactionDBRequest
)

logger = Logger(__name__)

class TransactionUseCase:
    def __init__(self):
        self.goal_database = TransactionDatabase()

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
                        transaction_type=transaction.transaction_type,
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
        

    def create_transaction(self, payload: CreateTransactionPayload):
        try:
            user_id = payload.user_id
            category_id = payload.category_id
            transaction_type = payload.transaction_type
            transaction_info = payload.transaction_info
            transaction_amount = payload.transaction_amount
            transaction_date = payload.transaction_date

            transaction_id = generate_transaction_id(
                user_id=user_id,
                category_id=category_id,
                transaction_type=transaction_type,
                transaction_date=transaction_date,
                amount=transaction_amount
            )

            db_request = CreateTransactionDBRequest(
                user_id=user_id,
                transaction_id=transaction_id,
                category_id=category_id,
                transaction_type=transaction_type,
                transaction_info=transaction_info,
                transaction_amount=transaction_amount,
                transaction_date=transaction_date
            
            )

            create_transaction_response = self.goal_database.create_transaction(
                db_request=db_request
            )

            return create_transaction_response

        except Exception as e:
            logger.error(f"Error in create_transaction use case: {e}")
            raise e