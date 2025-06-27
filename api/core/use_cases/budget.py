from shared.logger import Logger
from core.database.budget import BudgetDatabase
from core.models.io_models.budget_io_models import GetBudgetOverviewResponse
logger = Logger(__name__)

class BudgetUseCase:
    def __init__(self):
        self.budget_database = None
        
        self.user_id = None
        self.budget_total_budget = 0
        self.budget_total_spent = 0
        self.budget_near_limit_count = 0
        self.budget_over_limit_count = 0

    def get_budget_overview(self, user_id):
        try:
            self.budget_database = BudgetDatabase()

            self.user_id = user_id
            
            self.budget_total_budget = self.budget_database.get_total_budget(self.user_id)
            self.budget_total_spent = self.budget_database.get_total_spent(self.user_id)
            self.budget_near_limit_count = 111
            self.budget_over_limit_count = 123
            
            return GetBudgetOverviewResponse(
                budget_total_budget = float(self.budget_total_budget),
                budget_total_spent = float(self.budget_total_spent),
                budget_near_limit_count = int(self.budget_near_limit_count),
                budget_over_limit_count = int(self.budget_over_limit_count),
            )

        except Exception as e:
            logger.error(f"Error in get_budget_overview use case: {e}")
            raise e