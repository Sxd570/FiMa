from fastmcp import FastMCP
from pydantic import Field
from typing import Optional
from uuid import UUID

from domain.goal_domain import GoalDomain
from models.goal_models import (
    GetGoalsOverviewResponse,
    GetGoalDetailsResponse,
    CreateGoalResponse,
    DeleteGoalResponse,
    EditGoalResponse,
    AddAmountToGoalResponse,
)
from utils.logger import Logger


logger = Logger(__name__)
_goal_domain = GoalDomain()


def get_goals_overview(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose goals overview is to be fetched."
        ),
    ),
) -> GetGoalsOverviewResponse:
    """Fetch a high-level overview of all goals for a user.

    What it does:
        Returns aggregated statistics across every goal owned by the
        user, including totals, completion count, and saved amount.

    Inputs:
        user_id (UUID): The unique ID of the user.

    Returns (GetGoalsOverviewResponse):
        total_goals_count (int): Total number of goals created.
        total_goals_completed (int): Number of completed goals.
        total_amount_saved (float): Total amount saved across all goals.
        total_goal_amount (float): Sum of all goal target amounts.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab"
            }
        Response:
            {
                "total_goals_count": 4,
                "total_goals_completed": 1,
                "total_amount_saved": 3200.0,
                "total_goal_amount": 10000.0
            }
    """
    try:
        return _goal_domain.get_goals_overview(user_id=user_id)
    except Exception as e:
        logger.error(f"Error in tool get_goals_overview: {str(e)}")
        raise


def get_goal_details(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose goal details are to be fetched."
        ),
    ),
    limit: int = Field(
        15,
        gt=0,
        le=100,
        description="Maximum number of goals to return (default: 15, max: 100).",
    ),
    offset: int = Field(
        0,
        ge=0,
        description="Number of goals to skip before starting to collect the result set.",
    ),
) -> GetGoalDetailsResponse:
    """Fetch a paginated list of detailed goals for a user.

    What it does:
        Returns detailed information for each goal owned by the user,
        including progress, remaining amount, and completion flag.

    Inputs:
        user_id (UUID): The unique ID of the user.
        limit (int, optional): Max goals to return (default 15, max 100).
        offset (int, optional): Number of goals to skip (default 0).

    Returns (GetGoalDetailsResponse):
        goal_details (list[GoalDetail]): Each item contains:
            - goal_id (UUID)
            - goal_name (str)
            - goal_description (str)
            - goal_target_amount (float)
            - goal_current_amount (float)
            - goal_remaining_amount (float)
            - goal_percentage (float)
            - is_goal_reached (bool)
        has_more (bool): True if more goals exist beyond this page.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "limit": 1,
                "offset": 0
            }
        Response:
            {
                "goal_details": [
                    {
                        "goal_id": "b2c3d4e5-1111-2222-3333-444455556666",
                        "goal_name": "Emergency Fund",
                        "goal_description": "Six months of expenses",
                        "goal_target_amount": 6000.0,
                        "goal_current_amount": 1500.0,
                        "goal_remaining_amount": 4500.0,
                        "goal_percentage": 25.0,
                        "is_goal_reached": false
                    }
                ],
                "has_more": true
            }
    """
    try:
        return _goal_domain.get_goal_details(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error(f"Error in tool get_goal_details: {str(e)}")
        raise


def create_goal(
    user_id: UUID = Field(
        ...,
        description="The unique ID of the user creating the goal.",
    ),
    goal_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the goal.",
    ),
    goal_description: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Description of the goal.",
    ),
    goal_target_amount: float = Field(
        ...,
        gt=1,
        description="Target amount for the goal (must be greater than 1).",
    ),
) -> CreateGoalResponse:
    """Create a new savings goal for a user.

    What it does:
        Creates a new goal with the supplied name, description, and
        target amount for the specified user.

    Inputs:
        user_id (UUID): The unique ID of the user.
        goal_name (str): Name of the goal (1-100 chars).
        goal_description (str): Description of the goal (1-255 chars).
        goal_target_amount (float): Target amount (must be greater than 1).

    Returns (CreateGoalResponse):
        status (str): Indicates whether the goal was created successfully.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "goal_name": "Vacation",
                "goal_description": "Trip to Japan in 2027",
                "goal_target_amount": 4000.0
            }
        Response:
            {
                "status": "Goal created successfully."
            }
    """
    try:
        return _goal_domain.create_goal(
            user_id=user_id,
            goal_name=goal_name,
            goal_description=goal_description,
            goal_target_amount=goal_target_amount,
        )
    except Exception as e:
        logger.error(f"Error in tool create_goal: {str(e)}")
        raise


def delete_goal(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose goal is to be deleted."
        ),
    ),
    goal_id: UUID = Field(
        ...,
        description="The unique ID of the goal to delete.",
    ),
) -> DeleteGoalResponse:
    """Delete a specific goal owned by the user.

    What it does:
        Permanently removes the goal identified by goal_id for the
        specified user.

    Inputs:
        user_id (UUID): The unique ID of the user.
        goal_id (UUID): The unique ID of the goal to delete.

    Returns (DeleteGoalResponse):
        status (str): Whether the goal was deleted successfully.
        goal_id (UUID): The ID of the deleted goal.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "goal_id": "b2c3d4e5-1111-2222-3333-444455556666"
            }
        Response:
            {
                "status": "Goal deleted successfully.",
                "goal_id": "b2c3d4e5-1111-2222-3333-444455556666"
            }
    """
    try:
        return _goal_domain.delete_goal(user_id=user_id, goal_id=goal_id)
    except Exception as e:
        logger.error(f"Error in tool delete_goal: {str(e)}")
        raise


def edit_goal(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose goal is to be edited."
        ),
    ),
    goal_id: UUID = Field(
        ...,
        description="The unique ID of the goal to edit.",
    ),
    goal_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="The new name of the goal.",
    ),
    goal_description: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="The new description of the goal.",
    ),
    goal_target_amount: Optional[float] = Field(
        None,
        gt=1,
        description="The new target amount for the goal (must be greater than 1).",
    ),
    goal_current_amount: Optional[float] = Field(
        None,
        gt=1,
        description=(
            "The updated current amount saved towards the goal (must be greater than 1)."
        ),
    ),
) -> EditGoalResponse:
    """Edit one or more fields of an existing goal.

    What it does:
        Updates the supplied fields (name, description, target amount,
        or current amount) on the specified goal. Only fields with a
        non-null value are updated.

    Inputs:
        user_id (UUID): The unique ID of the user.
        goal_id (UUID): The unique ID of the goal to edit.
        goal_name (str, optional): New name (1-100 chars).
        goal_description (str, optional): New description (1-255 chars).
        goal_target_amount (float, optional): New target amount (> 1).
        goal_current_amount (float, optional): New current saved amount (> 1).

    Returns (EditGoalResponse):
        status (str): Whether the goal was edited successfully.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "goal_id": "b2c3d4e5-1111-2222-3333-444455556666",
                "goal_target_amount": 5000.0
            }
        Response:
            {
                "status": "Goal updated successfully."
            }
    """
    try:
        return _goal_domain.edit_goal(
            user_id=user_id,
            goal_id=goal_id,
            goal_name=goal_name,
            goal_description=goal_description,
            goal_target_amount=goal_target_amount,
            goal_current_amount=goal_current_amount,
        )
    except Exception as e:
        logger.error(f"Error in tool edit_goal: {str(e)}")
        raise


def add_amount_to_goal(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose goal is to be updated."
        ),
    ),
    goal_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the goal to which the amount will be added."
        ),
    ),
    amount_to_add: float = Field(
        ...,
        gt=1,
        description=(
            "The amount to add to the goal's current amount (must be greater than 1)."
        ),
    ),
) -> AddAmountToGoalResponse:
    """Add an amount to the current saved value of a user's goal.

    What it does:
        Increments the goal's current saved amount by the supplied
        value, moving the goal closer to its target.

    Inputs:
        user_id (UUID): The unique ID of the user.
        goal_id (UUID): The unique ID of the goal to update.
        amount_to_add (float): The amount to add (must be greater than 1).

    Returns (AddAmountToGoalResponse):
        status (str): Whether the amount was added successfully.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "goal_id": "b2c3d4e5-1111-2222-3333-444455556666",
                "amount_to_add": 250.0
            }
        Response:
            {
                "status": "Amount added to goal successfully."
            }
    """
    try:
        return _goal_domain.add_amount_to_goal(
            user_id=user_id,
            goal_id=goal_id,
            amount_to_add=amount_to_add,
        )
    except Exception as e:
        logger.error(f"Error in tool add_amount_to_goal: {str(e)}")
        raise


def register_goal_tools(mcp: FastMCP) -> None:
    """
    Register goal tools on a FastMCP instance.
    """
    mcp.tool(get_goals_overview)
    mcp.tool(get_goal_details)
    mcp.tool(create_goal)
    mcp.tool(delete_goal)
    mcp.tool(edit_goal)
    mcp.tool(add_amount_to_goal)
