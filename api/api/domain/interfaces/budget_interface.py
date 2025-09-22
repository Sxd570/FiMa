from abc import ABC, abstractmethod


from domain.models.io_models.budget_io_models import (
    GetBudgetOverviewDBRequest,
    GetBudgetDetailsDBRequest,
    BudgetDetailsDBResponse,
    EditBudgetDetailDBRequest,
    DeleteBudgetDetailDBRequest
)

class BudgetInterface(ABC):
    @abstractmethod
    def get_total_budget(self, db_request: GetBudgetOverviewDBRequest) -> float:
        """
        Get the total budget for a user for a given month.
        """
        pass

    @abstractmethod
    def get_total_spent(self, db_request: GetBudgetOverviewDBRequest) -> float:
        """
        Get the total amount spent by a user for a given month.
        """
        pass

    @abstractmethod
    def get_near_limit_count(self, db_request: GetBudgetOverviewDBRequest) -> int:
        """
        Get the count of budgets near their limit for a user for a given month.
        """
        pass

    @abstractmethod
    def get_over_limit_count(self, db_request: GetBudgetOverviewDBRequest) -> int:
        """
        Get the count of budgets over their limit for a user for a given month.
        """
        pass

    @abstractmethod
    def get_budget_details(self, db_request: GetBudgetDetailsDBRequest) -> BudgetDetailsDBResponse:
        """
        Get the details of all budgets for a user for a given month.
        """
        pass

    @abstractmethod
    def edit_budget_limit(self, db_request: EditBudgetDetailDBRequest) -> dict:
        """
        Edit the budget limit for a specific budget.
        """
        pass

    @abstractmethod
    def delete_budget(self, db_request: DeleteBudgetDetailDBRequest) -> dict:
        """
        Delete a specific budget for a user.
        """
        pass