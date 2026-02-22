from sqlalchemy import *
from shared.logger import Logger
from domain.interfaces.budget_interface import BudgetInterface
from domain.models.io_models.budget_io_models import (
    GetBudgetOverviewDBRequest,
    GetBudgetDetailsDBRequest,
    BudgetDetailsDBResponse,
    BudgetDetail,
    EditBudgetDetailDBRequest,
    DeleteBudgetDetailDBRequest,
    CreateBudgetDBRequest,
    UpdateAmountInBudgetDBRequest,
    EditBudgetResponse,
    DeleteBudgetResponse,
    CreateBudgetResponse
)
from domain.models.io_models.report_io_models import (
    GetReportCategoryDBRequest
)
from domain.models.tables.budget import Budget
from domain.exceptions import BudgetNotFoundException
from shared.Utility.db_base import get_db_session
logger = Logger(__name__)


class BudgetDatabase(BudgetInterface):
    def __init__(self):
        self.db_session = None
        self.user_id = None
        

    def get_total_budget(self, db_request: GetBudgetOverviewDBRequest) -> int:
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


    def get_total_spent(self, db_request: GetBudgetOverviewDBRequest) -> int:
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
        
        
    def get_near_limit_count(self, db_request: GetBudgetOverviewDBRequest) -> int:
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
        

    def get_over_limit_count(self, db_request: GetBudgetOverviewDBRequest) -> int:
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
        

    def get_budget_details(self, db_request: GetBudgetDetailsDBRequest) -> BudgetDetailsDBResponse:
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
                Budget.budget_name
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
                        budget_name=budget_name,
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
                        budget_name
                    ) in db_response
                ]
            )

            return budget_details
        except Exception as e:
            logger.error(f"Error in get_budget_details: {e}")
            raise e
        
    
    def edit_budget_limit(self, db_request: EditBudgetDetailDBRequest) -> EditBudgetResponse:
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
                raise BudgetNotFoundException(detail="Budget not found to edit.")

            budget_detail.budget_allocated_amount = self.new_budget_limit

            # Update is_budget_limit_reached (90%) and is_budget_over_limit (spent >= limit)
            spent = budget_detail.budget_spent_amount
            limit = self.new_budget_limit

            budget_detail.is_budget_limit_reached = spent >= (0.9 * limit)
            budget_detail.is_budget_over_limit = spent >= limit

            self.db_session.commit()

            return EditBudgetResponse(
                message="Budget limit updated successfully.",
            )
        except Exception as e:
            logger.error(f"Error in edit_budget_limit: {e}")
            raise e


    def delete_budget(self, db_request: DeleteBudgetDetailDBRequest) -> DeleteBudgetResponse:
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
                raise BudgetNotFoundException(detail="Budget not found to delete.")

            self.db_session.delete(budget_detail)
            self.db_session.commit()

            return DeleteBudgetResponse(
                message="Budget deleted successfully.",
            )
        except Exception as e:
            logger.error(f"Error in delete_budget: {e}")
            raise e


    def create_budget(self, db_request: CreateBudgetDBRequest) -> CreateBudgetResponse:
        try:
            self.db_session = get_db_session()

            user_id = db_request.user_id
            budget_id = db_request.budget_id
            budget_name = db_request.budget_name
            budget_allocated_amount = db_request.budget_allocated_amount
            budget_allocated_month = db_request.budget_allocated_month
            budget_description = db_request.budget_description


            new_budget = Budget(
                user_id=user_id,
                budget_id=budget_id,
                budget_name=budget_name,
                budget_description=budget_description,
                budget_allocated_amount=budget_allocated_amount,
                budget_allocated_month=budget_allocated_month,
                budget_spent_amount=0,
                is_budget_limit_reached=False,
                is_budget_over_limit=False
            )
            self.db_session.add(new_budget)
            self.db_session.commit()

            return CreateBudgetResponse(
                message="Budget created successfully.",
                budget_id=budget_id
            )
        except Exception as e:
            logger.error(f"Error in create_budget: {e}")
            raise e
        

    def update_amount_in_budget(self, db_request: UpdateAmountInBudgetDBRequest) -> dict:
        try:
            self.db_session = get_db_session()

            user_id = db_request.user_id
            budget_id = db_request.budget_id
            amount_to_add = db_request.amount_to_add

            filter_group = [
                Budget.budget_id == budget_id,
                Budget.user_id == user_id
            ]

            budget_detail = self.db_session.query(
                Budget
            ).filter(
                *filter_group
            ).first()

            if not budget_detail:
                raise BudgetNotFoundException(detail="Budget not found to update.")

            # Add the new amount to spent amount
            budget_detail.budget_spent_amount += amount_to_add

            # Check if budget limit is reached (>= 90%) or over limit
            if budget_detail.budget_allocated_amount > 0 and budget_detail.budget_spent_amount >= 0.9 * budget_detail.budget_allocated_amount:
                budget_detail.is_budget_limit_reached = True
            else:
                budget_detail.is_budget_limit_reached = False

            if budget_detail.budget_spent_amount > budget_detail.budget_allocated_amount:
                budget_detail.is_budget_over_limit = True
            else:
                budget_detail.is_budget_over_limit = False

            # Commit changes
            self.db_session.commit()

            return {
                "message": "Budget amount updated successfully.",
            }

        except Exception as e:
            logger.error(f"Error in update amount in budget function: {e}")
            raise e


    def get_weekly_data(self, db_request: GetReportCategoryDBRequest):
        pass


    def get_monthly_data(self, db_request: GetReportCategoryDBRequest):
        pass


    def get_yearly_data(self, db_request: GetReportCategoryDBRequest):
        pass