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
            self.db_session = get_db_session()
            
            self.user_id = user_id

            filter_group = [
                Budget.user_id == self.user_id
            ]

            self.total_budget = self.db_session.query(
                func.sum(Budget.budget_target_amount)
                ).filter(
                    *filter_group
                ).scalar()
                
            if self.total_budget is None:
                self.total_budget = 0

            return self.total_budget

        except Exception as e:
            logger.error(f"Error in get_total_budget: {e}")
            raise e
        
        
    def get_total_spent(self, user_id):
        try:
            self.db_session = get_db_session()

            self.user_id = user_id

            filter_group = [
                Budget.user_id == self.user_id
            ]
  
            self.total_fund_allocated = self.db_session.query(
                func.sum(Budget.budget_current_amount)
                ).filter(
                    *filter_group
                ).scalar()
            
            if self.total_fund_allocated is None:
                self.total_fund_allocated = 0

            return self.total_fund_allocated
        except Exception as e:
            logger.error(f"Error in get_total_spent: {e}")
            raise e