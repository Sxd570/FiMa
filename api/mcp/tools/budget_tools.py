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
    """Get an aggregated budget overview for a user for a given month.

    What it does:
        Returns a high-level summary of all budgets a user has for the
        specified month, including totals, remaining amount, percentage
        spent, and counts of budgets near or over their limit.

    Inputs:
        user_id (UUID): The unique ID of the user.
        budget_month (str): The target month in 'YYYY-MM' format.

    Returns (GetBudgetOverviewResponse):
        budget_total_budget (float): Total budget allocated for the month.
        budget_total_spent (float): Total amount spent during the month.
        budget_near_limit_count (int): Number of budgets near their limit.
        budget_over_limit_count (int): Number of budgets exceeding their limit.
        budget_remaining_amount (float): Remaining budget for the month.
        budget_percentage_spent (float): Percentage of budget spent.
        budget_date (str): The month covered by this overview ('YYYY-MM').

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "budget_month": "2026-05"
            }
        Response:
            {
                "budget_total_budget": 2000.0,
                "budget_total_spent": 1450.75,
                "budget_near_limit_count": 1,
                "budget_over_limit_count": 0,
                "budget_remaining_amount": 549.25,
                "budget_percentage_spent": 72.5,
                "budget_date": "2026-05"
            }
    """
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
    """Get a paginated list of all budgets a user created for a given month.

    What it does:
        Returns detailed information for each budget the user created in
        the specified month, including allocated and spent amounts,
        remaining balance, percentage used, and limit status flags.

    Inputs:
        user_id (UUID): The unique ID of the user.
        budget_month (str): The target month in 'YYYY-MM' format.
        limit (int, optional): Max budgets to return (default 15, max 100).
        offset (int, optional): Number of budgets to skip (default 0).

    Returns (GetBudgetDetailsResponse):
        budget_details (list[BudgetDetail]): Each item contains:
            - budget_id (UUID)
            - budget_name (str)
            - budget_allocated_amount (float)
            - budget_spent_amount (float)
            - budget_allocated_month (str, 'YYYY-MM')
            - budget_remaining_amount (float)
            - is_limit_reached (bool)
            - is_over_limit (bool)
            - budget_percentage_spent (float)
        has_more (bool): True if more budgets exist beyond this page.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "budget_month": "2026-05",
                "limit": 2,
                "offset": 0
            }
        Response:
            {
                "budget_details": [
                    {
                        "budget_id": "a1b2c3d4-1111-2222-3333-444455556666",
                        "budget_name": "Groceries",
                        "budget_allocated_amount": 500.0,
                        "budget_spent_amount": 425.30,
                        "budget_allocated_month": "2026-05",
                        "budget_remaining_amount": 74.70,
                        "is_limit_reached": false,
                        "is_over_limit": false,
                        "budget_percentage_spent": 85.06
                    }
                ],
                "has_more": true
            }
    """
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
    """Update the spending limit of an existing budget.

    What it does:
        Changes the allocated limit of the specified budget owned by the
        user to the supplied value.

    Inputs:
        user_id (UUID): The unique ID of the user owning the budget.
        budget_id (UUID): The unique ID of the budget to update.
        new_budget_limit (float): The new limit (must be greater than 1).

    Returns (EditBudgetLimitResponse):
        message (str): Confirmation message that the limit was updated.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "budget_id": "a1b2c3d4-1111-2222-3333-444455556666",
                "new_budget_limit": 750.0
            }
        Response:
            {
                "message": "Budget limit updated successfully."
            }
    """
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
    """Delete an existing budget belonging to the user.

    What it does:
        Permanently removes the budget identified by budget_id for the
        given user.

    Inputs:
        user_id (UUID): The unique ID of the user owning the budget.
        budget_id (UUID): The unique ID of the budget to delete.

    Returns (DeleteBudgetResponse):
        message (str): Confirmation message that the budget was deleted.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "budget_id": "a1b2c3d4-1111-2222-3333-444455556666"
            }
        Response:
            {
                "message": "Budget deleted successfully."
            }
    """
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
    """Create a new monthly budget for a user.

    What it does:
        Creates a new budget for the specified user and month with the
        given name, limit, and description.

    Inputs:
        user_id (UUID): The unique ID of the user.
        budget_limit (float): The spending limit (must be greater than 1).
        budget_name (str): Name of the budget (e.g. 'Groceries').
        budget_month (str): The target month in 'YYYY-MM' format.
        description (str): A short description of the budget.

    Returns (CreateBudgetResponse):
        message (str): Confirmation message that the budget was created.
        budget_id (UUID): ID of the newly created budget.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "budget_limit": 500.0,
                "budget_name": "Groceries",
                "budget_month": "2026-05",
                "description": "Monthly grocery spending"
            }
        Response:
            {
                "message": "Budget created successfully.",
                "budget_id": "a1b2c3d4-1111-2222-3333-444455556666"
            }
    """
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
