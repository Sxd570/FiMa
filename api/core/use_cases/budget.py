from shared.logger import Logger
from core.database.budget import BudgetDatabase
from core.models.io_models.budget_io_models import (
    GetBudgetOverviewResponse,
    GetBudgetDetailsResponse,
    BudgetDetail,
)

logger = Logger(__name__)


class BudgetUseCase:
    def __init__(self):
        self.budget_database = None
        self.user_id = None
        self.date = None
        self.budget_total_budget = 0
        self.budget_total_spent = 0
        self.budget_near_limit_count = 0
        self.budget_over_limit_count = 0

    def get_budget_overview(self, user_id, date):
        try:
            self.budget_database = BudgetDatabase()
            self.user_id = user_id
            self.date = date

            self.budget_total_budget = self.budget_database.get_total_budget(
                self.user_id, self.date
            )
            self.budget_total_spent = self.budget_database.get_total_spent(
                self.user_id, self.date
            )
            self.budget_near_limit_count = self.budget_database.get_near_limit_count(
                self.user_id, self.date
            )
            self.budget_over_limit_count = self.budget_database.get_over_limit_count(
                self.user_id, self.date
            )

            return GetBudgetOverviewResponse(
                budget_total_budget=float(self.budget_total_budget),
                budget_total_spent=float(self.budget_total_spent),
                budget_near_limit_count=int(self.budget_near_limit_count),
                budget_over_limit_count=int(self.budget_over_limit_count),
                budget_remaining_amount=(
                    float(self.budget_total_budget) - float(self.budget_total_spent)
                    if self.budget_total_budget
                    else None
                ),
                budget_percentage_spent=(
                    (float(self.budget_total_spent) / float(self.budget_total_budget) * 100)
                    if self.budget_total_budget and self.budget_total_budget != 0
                    else None
                ),
            )

        except Exception as e:
            logger.error(f"Error in get_budget_overview use case: {e}")
            raise e

    def get_budget_details(self, user_id, date):
        try:
            self.budget_database = BudgetDatabase()
            self.user_id = user_id
            self.date = date

            budget_details = self.budget_database.get_budget_details(self.user_id, self.date)

            return GetBudgetDetailsResponse(
                budget_details=[
                    BudgetDetail(
                        budget_id=detail.budget_id,
                        category_name=detail.category_name,
                        budget_allocated_amount=float(detail.budget_allocated_amount),
                        budget_spent_amount=float(detail.budget_spent_amount),
                        budget_allocated_month=detail.budget_allocated_month,
                        budget_remaining_amount=(
                            float(detail.budget_allocated_amount) - float(detail.budget_spent_amount)
                        ),
                        is_limit_reached=detail.is_limit_reached,
                        is_over_limit=detail.is_over_limit,
                        budget_percentage_spent=(
                            (float(detail.budget_spent_amount) / float(detail.budget_allocated_amount) * 100)
                            if float(detail.budget_allocated_amount) != 0
                            else None
                        ),
                    )
                    for detail in budget_details.budget_details
                ]
            )

        except Exception as e:
            logger.error(f"Error in get_budget_details use case: {e}")
            raise e