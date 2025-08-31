from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any

class GetBudgetOverviewRequest(BaseModel):
    month: str = Field(..., description="The month for which the budget overview is requested, formatted as 'YYYY-MM'.")


class GetBudgetDetailsRequest(BaseModel):
    month: str = Field(..., description="The month for which the budget details are requested, formatted as 'YYYY-MM'.")


class GetBudgetOverviewPayload(BaseModel):
    user_id: str = Field(..., description="User ID of the person requesting the budget overview")
    date: str = Field(..., description="The month for which the budget overview is requested, formatted as 'YYYY-MM'")


class GetBudgetOverviewRequest(BaseModel):
    month: str = Field(..., description="The month for which the budget overview is requested, formatted as 'YYYY-MM'.")


class GetBudgetDetailsRequest(BaseModel):
    month: str = Field(..., description="The month for which the budget details are requested, formatted as 'YYYY-MM'.")


class GetBudgetOverviewPayload(BaseModel):
    user_id: str = Field(..., description="User ID of the person requesting the budget overview")
    date: str = Field(..., description="The month for which the budget overview is requested, formatted as 'YYYY-MM'")


class GetBudgetOverviewResponse(BaseModel):
    budget_total_budget: float = Field(..., description="Total budget amount")
    budget_total_spent: float = Field(..., description="Total amount spent")
    budget_near_limit_count: int = Field(..., description="Count of budgets near their limit")
    budget_over_limit_count: int = Field(..., description="Count of budgets that are over their limit")
    budget_remaining_amount: Optional[float] = Field(None, description="Total remaining budget amount for the month")
    budget_percentage_spent: Optional[float] = Field(None, description="Percentage of the budget that has been spent, calculated as (budget_total_spent / budget_total_budget) * 100 if budget_total_budget is not None and not zero")
    budget_date: str = Field(..., description="The month for which the budget overview is provided, formatted as 'YYYY-MM'")

class BudgetDetail(BaseModel):
    budget_id: str = Field(..., description="Unique identifier for the budget")
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


class GetBudgetDetailsPayload(BaseModel):
    user_id: str = Field(..., description="User ID of the person requesting the budget details")
    date: str = Field(..., description="The month for which the budget details are requested, formatted as 'YYYY-MM'")


class GetBudgetDetailsDBRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person requesting the budget details")
    date: str = Field(..., description="The month for which the budget details are requested, formatted as 'YYYY-MM'")
    limit: Optional[int] = Field(None, description="Optional limit on the number of budget details to return")
    offset: Optional[int] = Field(None, description="Optional offset for pagination of budget details")


class GetBudgetOverviewDBRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person requesting the budget overview")
    date: str = Field(..., description="The month for which the budget overview is requested, formatted as 'YYYY-MM'")


class EditBudgetDetailRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person editing the budget")
    new_budget_limit: float = Field(..., description="New budget limit to be set for the budget")


class EditBudgetDetailPayload(BaseModel):
    budget_id: str = Field(..., description="Unique identifier for the budget to be edited")
    new_budget_limit: float = Field(..., description="New budget limit to be set for the budget")
    user_id: str = Field(..., description="User ID of the person editing the budget")

class EditBudgetDetailDBRequest(BaseModel):
    budget_id: str = Field(..., description="Unique identifier for the budget to be edited")
    new_budget_limit: float = Field(..., description="New budget limit to be set for the budget")
    user_id: str = Field(..., description="User ID of the person editing the budget")


class DeleteBudgetDetailRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person deleting the budget")

class DeleteBudgetDetailDBRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person deleting the budget")
    budget_id: str = Field(..., description="Unique identifier for the budget to be deleted")

class DeleteBudgetDetailPayload(BaseModel):
    user_id: str = Field(..., description="User ID of the person deleting the budget")
    budget_id: str = Field(..., description="Unique identifier for the budget to be deleted")

class DeleteBudgetDetailDBRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person deleting the budget")
    budget_id: str = Field(..., description="Unique identifier for the budget to be deleted")


class CreateBudgetRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person creating the budget")
    month: str = Field(..., description="The month for which the budget is being created, formatted as 'YYYY-MM'")
    budget_limit: float = Field(..., description="The budget limit to be set for the specified month")
    name: str = Field(..., description="Name of the budget category")
    transaction_type: str = Field(..., description="Transaction type for the budget, if applicable. This can be used to specify a predefined type or a custom one.")
    description: Optional[str] = Field(None, description="Optional description for the budget")

class CreateBudgetPayload(BaseModel):
    user_id: str = Field(..., description="User ID of the person creating the budget")
    month: str = Field(..., description="The month for which the budget is being created, formatted as 'YYYY-MM'")
    budget_limit_amount: float = Field(..., description="The budget limit to be set for the specified month")
    name: str = Field(..., description="Name of the budget category")
    transaction_type: str = Field(..., description="Transaction type for the budget, if applicable. This can be used to specify a predefined type or a custom one.")
    description: Optional[str] = Field(None, description="Optional description for the budget")


class CreateBudgetDBRequest(BaseModel):
    user_id: str = Field(..., description="User ID of the person creating the budget")
    category_id: str = Field(..., description="Category ID for the budget")
    category_name: str = Field(..., description="Name of the budget category")
    category_description: Optional[str] = Field(None, description="Optional description for the budget category")
    budget_id: str = Field(..., description="Unique identifier for the budget")
    budget_allocated_amount: float = Field(..., description="The budget limit to be set for the specified month")
    budget_allocated_month: str = Field(..., description="The month for which the budget is being created, formatted as 'YYYY-MM'")
    transaction_type: str = Field(..., description="Transaction type for the budget, if applicable. This can be used to specify a predefined type or a custom one.")