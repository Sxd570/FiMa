from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any

class BudgetOverviewRequest(BaseModel):
    month: str = Field(..., description="The month for which the budget overview is requested, formatted as 'YYYY-MM'.")


class BudgetDetailsRequest(BaseModel):
    month: str = Field(..., description="The month for which the budget details are requested, formatted as 'YYYY-MM'.")


class GetBudgetOverviewResponse(BaseModel):
    budget_total_budget: float = Field(..., description="Total budget amount")
    budget_total_spent: float = Field(..., description="Total amount spent")
    budget_near_limit_count: int = Field(..., description="Count of budgets near their limit")
    budget_over_limit_count: int = Field(..., description="Count of budgets that are over their limit")
    budget_remaining_amount: Optional[float] = Field(None, description="Total remaining budget amount for the month")
    budget_percentage_spent: Optional[float] = Field(None, description="Percentage of the budget that has been spent, calculated as (budget_total_spent / budget_total_budget) * 100 if budget_total_budget is not None and not zero")


class BudgetDetail(BaseModel):
    budget_id: int = Field(..., description="Unique identifier for the budget")
    category_name: str = Field(..., description="Name of the budget category")
    budget_allocated_amount: float = Field(..., description="Allocated amount for the budget")
    budget_spent_amount: float = Field(..., description="Amount spent from the budget")
    budget_allocated_month: str = Field(..., description="Month for which the budget is allocated, formatted as 'YYYY-MM'")
    budget_remaining_amount: Optional[float] = Field(None, description="Remaining amount in the budget")
    is_limit_reached: bool = Field(..., description="Indicates if the budget limit has been reached")
    is_over_limit: bool = Field(..., description="Indicates if the budget is over its limit")
    budget_percentage_spent: Optional[float] = Field(None, description="Percentage of the budget that has been spent, calculated as (budget_spent_amount / budget_allocated_amount) * 100 if budget_allocated_amount is not None and not zero")


class BudgetDetailsDBResponse(BaseModel):
    budget_details: List[BudgetDetail] = Field(..., description="List of budget details for the specified month")


class GetBudgetDetailsResponse(BaseModel):
    budget_details: List[BudgetDetail] = Field(..., description="List of budget details for the specified month")