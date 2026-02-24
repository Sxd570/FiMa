from fastmcp import FastMCP
from pydantic import Field
from typing import Optional
from uuid import UUID

from domain.goal_domain import GoalDomain
from middleware import LoggingMiddleware
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
_logging_middleware = LoggingMiddleware(__name__)


def get_goals_overview(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose goals overview is to be fetched."
        ),
    ),
) -> GetGoalsOverviewResponse:
    """Fetch the overview of goals for a user."""
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
) -> GetGoalDetailsResponse:
    """Fetch detailed goal information for a specific user."""
    try:
        return _goal_domain.get_goal_details(user_id=user_id)
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
        gt=0,
        description="Target amount for the goal (must be greater than 0).",
    ),
) -> CreateGoalResponse:
    """Create a new goal for a user."""
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
    """Delete a specific goal for a user."""
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
        gt=0,
        description="The new target amount for the goal.",
    ),
    goal_current_amount: Optional[float] = Field(
        None,
        ge=0,
        description=(
            "The updated current amount saved towards the goal."
        ),
    ),
) -> EditGoalResponse:
    """Edit the details of a specific goal for a user."""
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
        gt=0,
        description=(
            "The amount to add to the goal's current amount."
        ),
    ),
) -> AddAmountToGoalResponse:
    """Add a specified amount to a user's goal."""
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
    mcp.tool()(_logging_middleware.wrap_tool(get_goals_overview))
    mcp.tool()(_logging_middleware.wrap_tool(get_goal_details))
    mcp.tool()(_logging_middleware.wrap_tool(create_goal))
    mcp.tool()(_logging_middleware.wrap_tool(delete_goal))
    mcp.tool()(_logging_middleware.wrap_tool(edit_goal))
    mcp.tool()(_logging_middleware.wrap_tool(add_amount_to_goal))

    # i want to do this format
    mcp.tool(add_amount_to_goal)
