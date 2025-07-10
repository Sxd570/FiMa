from shared.logger import Logger
from copy import deepcopy
from core.interfaces.transaction_interface import TransactionInterface
from core.models.tables.transaction import Transaction
from core.models.tables.category import Category
from shared.Utility.db_base import get_db_session
from core.models.io_models.transaction_io_models import (
    TransactionDetail,
    GetTransactionDBRequest,
    GetTransactionDBResponse
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
                Transaction.transaction_type_id,
                Transaction.transaction_info,
                Transaction.transaction_amount,
                Transaction.transaction_date,
                Category.category_name
            ).join(
                Category, Transaction.category_id == Category.category_id
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
                        category_name=category_name,
                        transaction_type_id=transaction_type_id,
                        transaction_info=transaction_info,
                        transaction_amount=transaction_amount,
                        transaction_date=transaction_date
                    )
                    for (
                        transaction_id, 
                        transaction_type_id, 
                        transaction_info, 
                        transaction_amount, 
                        transaction_date, 
                        category_name
                    ) in results
                ]
            )
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            raise e