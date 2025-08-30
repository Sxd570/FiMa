from typing import Optional
from copy import deepcopy
from typing import Optional
from copy import deepcopy
from sqlalchemy import *
from shared.logger import Logger
from core.interfaces.budget_interface import BudgetInterface
from core.models.io_models.budget_io_models import (
    GetBudgetOverviewDBRequest,
    GetBudgetDetailsDBRequest,
    BudgetDetailsDBResponse,
    BudgetDetail,
    EditBudgetDetailDBRequest,
    DeleteBudgetDetailDBRequest,
    CreateBudgetDBRequest
)
from core.models.tables.budget import Budget
from core.models.tables.category import Category
from shared.Utility.db_base import get_db_session
from core.models.tables.category import Category
from shared.Utility.db_base import get_db_session
logger = Logger(__name__)

class BudgetDatabase(BudgetInterface):
    def __init__(self):
        self.db_session = None
        self.user_id = None
        
    def get_total_budget(self, db_request: GetBudgetOverviewDBRequest):
        try:
            self.db_session = get_db_session()
            self.user_id = db_request.user_id
            self.date = db_request.date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.budget_allocated_month == self.date
            ]

            self.total_budget = self.db_session.query(
                func.sum(
                    Budget.budget_allocated_amount
                )
            ).filter(
                *filter_group
            ).scalar()
            
            if self.total_budget is None:
                self.total_budget = 0

            return self.total_budget

        except Exception as e:
            logger.error(f"Error in get_total_budget: {e}")
            raise e


    def get_total_spent(self, db_request: GetBudgetOverviewDBRequest):
        try:
            self.db_session = get_db_session()
            self.user_id = db_request.user_id
            self.date = db_request.date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.budget_allocated_month == self.date
            ]

            self.total_fund_allocated = self.db_session.query(
                func.sum(
                    Budget.budget_spent_amount
                )
            ).filter(
                *filter_group
            ).scalar()
            
            if self.total_fund_allocated is None:
                self.total_fund_allocated = 0

            return self.total_fund_allocated
        except Exception as e:
            logger.error(f"Error in get_total_spent: {e}")
            raise e
        
        
    def get_near_limit_count(self, db_request: GetBudgetOverviewDBRequest):
        try:
            self.db_session = get_db_session()

            self.user_id = db_request.user_id
            self.date = db_request.date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.budget_allocated_month == self.date,
                Budget.is_budget_limit_reached == True,
                Budget.is_budget_over_limit == False
            ]

            near_limit_count = self.db_session.query(
                func.count(Budget.budget_id)
                ).filter(
                    *filter_group
                ).scalar()
            
            if not near_limit_count:
                near_limit_count = 0

            return near_limit_count

        except Exception as e:
            logger.error(f"Error in get_near_limit_count: {e}")
            raise e
        

    def get_over_limit_count(self, db_request: GetBudgetOverviewDBRequest):
        try:
            self.db_session = get_db_session()

            self.user_id = db_request.user_id
            self.date = db_request.date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.budget_allocated_month == self.date,
                Budget.is_budget_over_limit == True
            ]

            over_limit_count = self.db_session.query(
                func.count(Budget.budget_id)
                ).filter(
                    *filter_group
                ).scalar()
            
            if over_limit_count is None:
                over_limit_count = 0

            return over_limit_count

        except Exception as e:
            logger.error(f"Error in get_over_limit_count: {e}")
            raise e
        

    def get_budget_details(self, db_request: GetBudgetDetailsDBRequest):
        try:
            self.db_session = get_db_session()

            self.user_id = db_request.user_id
            self.date = db_request.date

            filter_group = [
                Budget.user_id == self.user_id,
                Budget.budget_allocated_month == self.date
            ]

            query = self.db_session.query(
                Budget.budget_id,
                Budget.budget_allocated_amount,
                Budget.budget_spent_amount,
                Budget.budget_allocated_month,
                Budget.is_budget_limit_reached,
                Budget.is_budget_over_limit,
                Category.category_name
            ).join(
                Category, Budget.category_id == Category.category_id
            ).filter(
                *filter_group
            )

            db_response = query.all()

            if not db_response:
                return BudgetDetailsDBResponse(
                    budget_details=[]
                )

            budget_details = BudgetDetailsDBResponse(
                budget_details=[
                    BudgetDetail(
                        budget_id=budget_id,
                        category_name=category_name,
                        budget_allocated_amount=budget_allocated_amount,
                        budget_spent_amount=budget_spent_amount,
                        budget_allocated_month=budget_allocated_month,
                        is_limit_reached=is_budget_limit_reached,
                        is_over_limit=is_budget_over_limit
                    ) for (
                        budget_id,
                        budget_allocated_amount,
                        budget_spent_amount,
                        budget_allocated_month,
                        is_budget_limit_reached,
                        is_budget_over_limit,
                        category_name
                    ) in db_response
                ]
            )

            return budget_details
        except Exception as e:
            logger.error(f"Error in get_budget_details: {e}")
            raise e
        
    
    def edit_budget_limit(self, db_request: EditBudgetDetailDBRequest):
        try:
            self.db_session = get_db_session()

            self.user_id = db_request.user_id
            self.budget_id = db_request.budget_id
            self.new_budget_limit = db_request.new_budget_limit

            filter_group = [
                Budget.budget_id == self.budget_id,
                Budget.user_id == self.user_id
            ]

            budget_detail = self.db_session.query(
                Budget
                ).filter(
                    *filter_group
                ).first()

            if not budget_detail:
                raise ValueError("Budget not found to edit.")

            budget_detail.budget_allocated_amount = self.new_budget_limit

            self.db_session.commit()

            return {
                "message": "Budget limit updated successfully.",
            }
        except Exception as e:
            logger.error(f"Error in edit_budget_limit: {e}")
            raise e
        
    
    def delete_budget(self, db_request: DeleteBudgetDetailDBRequest):
        try:
            self.db_session = get_db_session()

            self.user_id = db_request.user_id
            self.budget_id = db_request.budget_id

            filter_group = [
                Budget.budget_id == self.budget_id,
                Budget.user_id == self.user_id
            ]

            budget_detail = self.db_session.query(
                Budget
                ).filter(
                    *filter_group
                ).first()

            if not budget_detail:
                raise ValueError("Budget not found to delete.")

            self.db_session.delete(budget_detail)
            self.db_session.commit()

            return {
                "message": "Budget deleted successfully.",
            }
        except Exception as e:
            logger.error(f"Error in delete_budget: {e}")
            raise e
        
    def create_budget(self, db_request: CreateBudgetDBRequest):
        try:
            self.db_session = get_db_session()

            user_id = db_request.user_id
            category_id = db_request.category_id
            category_name = db_request.category_name
            budget_id = db_request.budget_id
            budget_allocated_amount = db_request.budget_allocated_amount
            budget_allocated_month = db_request.budget_allocated_month
            transaction_type = db_request.transaction_type
            category_description = db_request.category_description

            new_category = Category(
                user_id=user_id,
                category_id=category_id,
                category_name=category_name,
                category_description=category_description,
                transaction_type=transaction_type
            )
            self.db_session.add(new_category)
            self.db_session.commit()

            new_budget = Budget(
                user_id=user_id,
                category_id=category_id,
                budget_id=budget_id,
                budget_allocated_amount=budget_allocated_amount,
                budget_allocated_month=budget_allocated_month,
                budget_spent_amount=0,
                is_budget_limit_reached=False,
                is_budget_over_limit=False
            )
            self.db_session.add(new_budget)
            self.db_session.commit()

            return {
                "message": "Budget created successfully.",
                "budget_id": budget_id
            }
        except Exception as e:
            logger.error(f"Error in create_budget: {e}")
            raise e