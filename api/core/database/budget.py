from typing import Optional
from sqlalchemy import *
from shared.logger import Logger
from core.interfaces.budget_interface import BudgetInterface
from core.models.tables.budget import Budget
from shared.Utility.db_base import get_db_session
logger = Logger(__name__)

class BudgetDatabase(BudgetInterface):
    def __init__(self):
        self.db_session = None
        self.user_id = None
        self.total_budget = 0
        self.total_fund_allocated = 0
        
    def get_total_budget(self, user_id, date):
        try:
            self.db_session = get_db_session()
            
            self.user_id = user_id
            self.date = date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.allocated_month == self.date
            ]

            self.total_budget = self.db_session.query(
                func.sum(Budget.allocated_amount)
                ).filter(
                    *filter_group
                ).scalar()
                
            if self.total_budget is None:
                self.total_budget = 0

            return self.total_budget

        except Exception as e:
            logger.error(f"Error in get_total_budget: {e}")
            raise e


    def get_total_spent(self, user_id, date):
        try:
            self.db_session = get_db_session()

            self.user_id = user_id
            self.date = date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.allocated_month == self.date
            ]
  
            self.total_fund_allocated = self.db_session.query(
                func.sum(Budget.spent_amount)
                ).filter(
                    *filter_group
                ).scalar()
            
            if self.total_fund_allocated is None:
                self.total_fund_allocated = 0

            return self.total_fund_allocated
        except Exception as e:
            logger.error(f"Error in get_total_spent: {e}")
            raise e
        
        
    def get_near_limit_count(self, user_id, date):
        try:
            self.db_session = get_db_session()

            self.user_id = user_id
            self.date = date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.allocated_month == self.date,
                Budget.is_limit_reached == True,
                Budget.is_over_limit == False
            ]

            near_limit_count = self.db_session.query(
                func.count(Budget.budget_id)
                ).filter(
                    *filter_group
                ).scalar()

            return near_limit_count if near_limit_count is not None else 0

        except Exception as e:
            logger.error(f"Error in get_near_limit_count: {e}")
            raise e
        

    def get_over_limit_count(self, user_id, date):
        try:
            self.db_session = get_db_session()

            self.user_id = user_id
            self.date = date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.allocated_month == self.date,
                Budget.is_over_limit == True
            ]

            over_limit_count = self.db_session.query(
                func.count(Budget.budget_id)
                ).filter(
                    *filter_group
                ).scalar()

            return over_limit_count if over_limit_count is not None else 0

        except Exception as e:
            logger.error(f"Error in get_over_limit_count: {e}")
            raise e
        

    def get_budget_details(
        self, 
        user_id: str, 
        date: str,
        limit: Optional[int] = None,
        offset: Optional[int] = 0
    ):
        try:
            self.db_session = get_db_session()

            self.user_id = user_id
            self.date = date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.allocated_month == self.date
            ]

            # TODO - implement this logic
            

        except Exception as e:
            logger.error(f"Error in get_budget_details: {e}")
            raise e