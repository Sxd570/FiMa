from enum import Enum

class TransactionConstants(Enum):
    KEY_BUDGET_ID = "budget_id"
    KEY_TRANSACTION_TYPE = "transaction_type"
    KEY_TRANSACTION_INFO = "transaction_info"
    KEY_TRANSACTION_AMOUNT = "transaction_amount"
    KEY_TRANSACTION_DATE = "transaction_date"
    KEY_FILTERS = "filters"
    KEY_LIMIT = "limit"
    KEY_OFFSET = "offset"
    KEY_TRANSACTIONS = "transactions"
    KEY_TRANSACTION_ID = "transaction_id"
    KEY_BUDGET_NAME = "budget_name"
    KEY_MESSAGE = "message"


class BudgetConstants(Enum):
    KEY_BUDGET_MONTH = "budget_month"
    KEY_USER_ID = "user_id"
    KEY_BUDGET_ID = "budget_id"
    KEY_NEW_BUDGET_LIMIT = "new_budget_limit"
    KEY_BUDGET_NAME = "budget_name"
    KEY_TRANSACTION_TYPE = "transaction_type"
    KEY_DESCRIPTION = "description"
    KEY_BUDGET_LIMIT = "budget_limit"


class APIConstants(Enum):    
    KEY_GET_METHOD = "GET"
    KEY_POST_METHOD = "POST"
    KEY_PUT_METHOD = "PUT"
    KEY_PATCH_METHOD = "PATCH"
    KEY_DELETE_METHOD = "DELETE"
    

class GoalConstants(Enum):
    KEY_GOAL_ID = "goal_id"
    KEY_USER_ID = "user_id"
    KEY_GOAL_NAME = "goal_name"
    KEY_GOAL_DESCRIPTION = "goal_description"
    KEY_GOAL_TARGET_AMOUNT = "goal_target_amount"
    KEY_GOAL_CURRENT_AMOUNT = "goal_current_amount"
    KEY_GOAL_COMPLETED = "is_goal_completed"