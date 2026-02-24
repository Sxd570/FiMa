from fastmcp import FastMCP
from pydantic import Field

from domain.budget_domain import BudgetDomain
from middleware import LoggingMiddleware
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
_logging_middleware = LoggingMiddleware(__name__)


def get_budget_overview(
    user_id: str = Field(..., description="The ID of the user (UUID string)."),
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
    user_id: str = Field(..., description="The ID of the user (UUID string)."),
    budget_month: str = Field(
        ..., description="The month for which to get the budget details in 'YYYY-MM' format."
    ),
) -> GetBudgetDetailsResponse:
    """Get details of all budgets created by a user for a specific month."""
    try:
        return _budget_domain.get_budget_details(
            user_id=user_id,
            budget_month=budget_month,
        )
    except Exception as e:
        logger.error(f"Error in tool get_budget_details: {str(e)}")
        raise


def edit_budget_limit(
    user_id: str = Field(..., description="The ID of the user (UUID string)."),
    budget_id: str = Field(
        ..., description="The ID of the budget to be edited (UUID string)."
    ),
    new_budget_limit: float = Field(
        ..., description="The new limit to be set for the budget."
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
    user_id: str = Field(..., description="The ID of the user (UUID string)."),
    budget_id: str = Field(
        ..., description="The ID of the budget to be deleted (UUID string)."
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
    user_id: str = Field(..., description="The ID of the user (UUID string)."),
    budget_limit: float = Field(..., description="The limit for the new budget."),
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
