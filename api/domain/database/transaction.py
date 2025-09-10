from shared.logger import Logger
from copy import deepcopy
from domain.interfaces.transaction_interface import TransactionInterface
from domain.models.tables.transaction import Transaction
from domain.models.tables.budget import Budget
from shared.Utility.db_base import get_db_session
from domain.models.io_models.transaction_io_models import (
    TransactionDetail,
    GetTransactionDBRequest,
    GetTransactionDBResponse,
    CreateTransactionDBRequest,
)

logger = Logger(__name__)

class TransactionDatabase(TransactionInterface):
    def __init__(self):
        self.db_session = None
        self.user_id = None


    @staticmethod
    def format_filters(filters: dict):
        formatted_filters = []
        for key, value in filters.items():
            if key == "from_date":
                # Filter for date >= from_date
                formatted_filters.append(getattr(Transaction, "transaction_date") >= value)
            elif key == "to_date":
                # Filter for date <= to_date
                formatted_filters.append(getattr(Transaction, "transaction_date") <= value)
            elif isinstance(value, list):
                formatted_filters.append(getattr(Transaction, key).in_(value))
            else:
                formatted_filters.append(getattr(Transaction, key) == value)
        return formatted_filters


    def get_transactions(self, db_request: GetTransactionDBRequest):
        try:
            self.db_session = get_db_session()

            self.user_id = db_request.user_id

            filter_group = [
                Transaction.user_id == self.user_id,
            ]

            if db_request.filters:
                filters = self.format_filters(db_request.filters)
                filter_group.extend(filters)

            query = self.db_session.query(
                Transaction.transaction_id,
                Transaction.transaction_type,
                Transaction.transaction_info,
                Transaction.transaction_amount,
                Transaction.transaction_date,
                Budget.budget_name
            ).join(
                Budget, Transaction.budget_id == Budget.budget_id
            ).filter(
                *filter_group
            )

            if db_request.limit:
                query = query.limit(db_request.limit)

            if db_request.offset:
                query = query.offset(db_request.offset)

            results = query.all()

            if not results:
                return GetTransactionDBResponse(
                    transactions=[]
                )

            return GetTransactionDBResponse(
                transactions=[
                    TransactionDetail(
                        transaction_id=transaction_id,
                        budget_name=budget_name,
                        transaction_type=transaction_type,
                        transaction_info=transaction_info,
                        transaction_amount=transaction_amount,
                        transaction_date=transaction_date
                    )
                    for (
                        transaction_id,
                        transaction_type,
                        transaction_info,
                        transaction_amount,
                        transaction_date,
                        budget_name
                    ) in results
                ]
            )
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            raise e
        
    
    def create_transaction(self, db_request: CreateTransactionDBRequest):
        try:
            self.db_session = get_db_session()

            user_id = db_request.user_id
            transaction_id = db_request.transaction_id
            budget_id = db_request.budget_id
            transaction_type = db_request.transaction_type
            transaction_info = db_request.transaction_info
            transaction_amount = db_request.transaction_amount
            transaction_date = db_request.transaction_date

            new_transaction = Transaction(
                user_id=user_id,
                transaction_id=transaction_id,
                budget_id=budget_id,
                transaction_type=transaction_type,
                transaction_info=transaction_info,
                transaction_amount=transaction_amount,
                transaction_date=transaction_date
            )

            self.db_session.add(new_transaction)
            self.db_session.commit()

            return {
                "message": "Transaction created successfully",
                "transaction_id": transaction_id
            }
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            self.db_session.rollback()
            raise e