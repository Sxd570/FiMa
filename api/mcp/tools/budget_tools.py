from fastmcp import FastMCP
from pydantic import Field
from uuid import UUID

from domain.budget_domain import BudgetDomain
from models.budget_models import (
    GetBudgetOverviewResponse,
    GetBudgetDetailsResponse,
    EditBudgetLimitResponse,
    DeleteBudgetResponse,
    CreateBudgetResponse,
)
from utils.logger import Logger


logger = Logger(__name__)
_budget_domain = BudgetDomain()


def get_budget_overview(
    user_id: UUID = Field(..., description="The unique ID of the user."),
    budget_month: str = Field(
        ..., description="The month for which to get the budget overview in 'YYYY-MM' format."
    ),
) -> GetBudgetOverviewResponse:
    """Get the budget overview for a user for a specific month."""
    try:
        return _budget_domain.get_budget_overview(
            user_id=user_id,
            budget_month=budget_month,
        )
    except Exception as e:
        logger.error(f"Error in tool get_budget_overview: {str(e)}")
        raise


def get_budget_details(
    user_id: UUID = Field(..., description="The unique ID of the user."),
    budget_month: str = Field(
        ..., description="The month for which to get the budget details in 'YYYY-MM' format."
    ),
    limit: int = Field(
        15,
        gt=0,
        le=100,
        description="Maximum number of budget details to return (default: 15, max: 100).",
    ),
    offset: int = Field(
        0,
        ge=0,
        description="Number of budget details to skip before starting to collect the result set.",
    ),
) -> GetBudgetDetailsResponse:
    """Get details of all budgets created by a user for a specific month."""
    try:
        return _budget_domain.get_budget_details(
            user_id=user_id,
            budget_month=budget_month,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error(f"Error in tool get_budget_details: {str(e)}")
        raise


def edit_budget_limit(
    user_id: UUID = Field(..., description="The unique ID of the user."),
    budget_id: UUID = Field(
        ..., description="The unique ID of the budget to be edited."
    ),
    new_budget_limit: float = Field(
        ..., gt=1, description="The new limit to be set for the budget (must be greater than 1)."
    ),
) -> EditBudgetLimitResponse:
    """Edit the limit of an existing budget."""
    try:
        return _budget_domain.edit_budget_limit(
            user_id=user_id,
            budget_id=budget_id,
            new_budget_limit=new_budget_limit,
        )
    except Exception as e:
        logger.error(f"Error in tool edit_budget_limit: {str(e)}")
        raise


def delete_budget(
    user_id: UUID = Field(..., description="The unique ID of the user."),
    budget_id: UUID = Field(
        ..., description="The unique ID of the budget to be deleted."
    ),
) -> DeleteBudgetResponse:
    """Delete an existing budget."""
    try:
        return _budget_domain.delete_budget(
            user_id=user_id,
            budget_id=budget_id,
        )
    except Exception as e:
        logger.error(f"Error in tool delete_budget: {str(e)}")
        raise


def create_budget(
    user_id: UUID = Field(..., description="The unique ID of the user."),
    budget_limit: float = Field(..., gt=1, description="The limit for the new budget (must be greater than 1)."),
    budget_name: str = Field(..., description="The name of the new budget."),
    budget_month: str = Field(
        ..., description="The month for which the budget is being created in 'YYYY-MM' format."
    ),
    description: str = Field(..., description="A brief description of the budget."),
) -> CreateBudgetResponse:
    """Create a new budget for a user."""
    try:
        return _budget_domain.create_budget(
            user_id=user_id,
            budget_limit=budget_limit,
            budget_name=budget_name,
            budget_month=budget_month,
            description=description,
        )
    except Exception as e:
        logger.error(f"Error in tool create_budget: {str(e)}")
        raise


def register_budget_tools(mcp: FastMCP) -> None:
    """
    Register budget tools on a FastMCP instance.
    """
    mcp.tool(get_budget_overview)
    mcp.tool(get_budget_details)
    mcp.tool(edit_budget_limit)
    mcp.tool(delete_budget)
    mcp.tool(create_budget)
