from sqlalchemy import *
from shared.logger import Logger
from core.interfaces.budget_interface import BudgetInterface
from core.models.tables.budget import Budget
from core.database.base import get_db_session
logger = Logger(__name__)

class BudgetDatabase(BudgetInterface):
    def __init__(self):
        self.db_session = None
        self.user_id = None
        self.total_budget = 0
        self.total_fund_allocated = 0
        
    def get_total_budget(self, user_id):
        try:
            return 0

        except Exception as e:
            logger.error(f"Error in get_total_budget: {e}")
            raise e
        
    def get_total_spent(self, user_id):
        try:
            return 0

        except Exception as e:
            logger.error(f"Error in get_total_spent: {e}")
            raise e