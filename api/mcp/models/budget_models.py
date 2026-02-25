from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

class GetBudgetOverviewResponse(BaseModel):
    budget_total_budget: Optional[float] = Field(None, description="Total budget allocated for the month")
    budget_total_spent: Optional[float] = Field(None, description="Total amount spent in the month")
    budget_near_limit_count: Optional[int] = Field(None, description="Number of budgets near their limit")
    budget_over_limit_count: Optional[int] = Field(None, description="Number of budgets that have exceeded their limit")
    budget_remaining_amount: Optional[float] = Field(None, description="Remaining budget for the month")
    budget_percentage_spent: Optional[float] = Field(None, description="Percentage of budget spent")
    budget_date: Optional[str] = Field(None, description="The month for the budget overview")


class BudgetDetail(BaseModel):
    budget_id: Optional[str] = Field(None, description="Unique identifier for the budget.")
    budget_name: Optional[str] = Field(None, description="Name of the budget category.")
    budget_allocated_amount: Optional[float] = Field(None, description="Amount allocated for the budget.")
    budget_spent_amount: Optional[float] = Field(None, description="Amount spent from the budget.")
    budget_allocated_month: Optional[str] = Field(None, description="The month for which the budget is allocated (format 'YYYY-MM').")
    budget_remaining_amount: Optional[float] = Field(None, description="Remaining amount in the budget.")
    is_limit_reached: Optional[bool] = Field(None, description="Whether the budget limit has been reached.")
    is_over_limit: Optional[bool] = Field(None, description="Whether the budget has been exceeded.")
    budget_percentage_spent: Optional[float] = Field(None, description="Percentage of the budget that has been spent.")


class GetBudgetDetailsResponse(BaseModel):
    budget_details: Optional[List[BudgetDetail]] = Field(None, description="List of detailed budget information for the given user and month.")


class EditBudgetLimitResponse(BaseModel):
    message: Optional[str] = Field(None, description="Confirmation message indicating the budget limit has been updated.")


class DeleteBudgetResponse(BaseModel):
    message: Optional[str] = Field(None, description="Confirmation message indicating the budget has been deleted.")


class CreateBudgetResponse(BaseModel):
    message: Optional[str] = Field(None, description="Confirmation message indicating the budget has been created.")
    budget_id: Optional[str] = Field(None, description="The ID of the newly created budget.")
