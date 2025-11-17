from enum import Enum

KEY_YEAR = "year"
KEY_MONTH = "month"
KEY_WEEK = "week"

class TransactionConstants(Enum):
    KEY_USER_ID = "user_id"
    KEY_TRANSACTION_ID = "transaction_id"
    KEY_CATEGORY_ID = "category_id"
    KEY_TRANSACTION_NAME = "transaction_name"
    KEY_TRANSACTION_DESCRIPTION = "transaction_description"
    KEY_TRANSACTION_AMOUNT = "transaction_amount"
    KEY_TRANSACTION_DATE = "transaction_date"


class TransactionTypesConstants(Enum):
    KEY_USER_ID = "user_id"
    KEY_TYPE_ID = "type_id"
    KEY_TYPE_NAME = "type_name"
    KEY_TYPE_DESCRIPTION = "type_description"