from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any

class GetBudgetOverviewResponse(BaseModel):
    budget_total_budget: float = Field(..., description="Total budget amount")
    budget_total_spent: float = Field(..., description="Total amount spent")
    budget_near_limit_count: int = Field(..., description="Count of budgets near their limit")
    budget_over_limit_count: int = Field(..., description="Count of budgets that are over their limit")