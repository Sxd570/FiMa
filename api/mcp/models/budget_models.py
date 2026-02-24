from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class GetBudgetOverviewResponse(BaseModel):
    budget_total_budget: float = Field(..., description="Total budget allocated for the month")
    budget_total_spent: float = Field(..., description="Total amount spent in the month")
    budget_near_limit_count: int = Field(..., description="Number of budgets near their limit")
    budget_over_limit_count: int = Field(..., description="Number of budgets that have exceeded their limit")
    budget_remaining_amount: float = Field(..., description="Remaining budget for the month")
    budget_percentage_spent: float = Field(..., description="Percentage of budget spent")
    budget_date: str = Field(..., description="The month for the budget overview")


class BudgetDetail(BaseModel):
    budget_id: str = Field(..., description="Unique identifier for the budget.")
    category_name: str = Field(..., description="Name of the budget category.")
    budget_allocated_amount: float = Field(..., description="Amount allocated for the budget.")
    budget_spent_amount: float = Field(..., description="Amount spent from the budget.")
    budget_allocated_month: str = Field(..., description="The month for which the budget is allocated (format 'YYYY-MM').")
    budget_remaining_amount: float = Field(..., description="Remaining amount in the budget.")
    is_limit_reached: bool = Field(..., description="Whether the budget limit has been reached.")
    is_over_limit: bool = Field(..., description="Whether the budget has been exceeded.")
    budget_percentage_spent: float = Field(..., description="Percentage of the budget that has been spent.")


class GetBudgetDetailsResponse(BaseModel):
    budget_details: Optional[List[BudgetDetail]] = Field(..., description="List of detailed budget information for the given user and month.")


class EditBudgetLimitResponse(BaseModel):
    message: str = Field(..., description="Confirmation message indicating the budget limit has been updated.")


class DeleteBudgetResponse(BaseModel):
    message: str = Field(..., description="Confirmation message indicating the budget has been deleted.")


class CreateBudgetResponse(BaseModel):
    message: str = Field(..., description="Confirmation message indicating the budget has been created.")
    budget_id: str = Field(..., description="The ID of the newly created budget.")
