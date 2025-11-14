from typing import Optional
from uuid import UUID
from pydantic import Field
from strands import tool

from constants import APIConstants, GoalConstants

from domain.models.io_models.api_tool_models.goals_model import (
    GetGoalsOverviewResponse,
    GetGoalDetailsResponse,
    CreateGoalResponse,
    DeleteGoalResponse,
    EditGoalResponse,
    AddAmountToGoalResponse
)

from shared.Utility.api_request import APIRequest
from shared.logger import Logger

logger = Logger(__name__)


@tool
def get_goals_overview(
    user_id: UUID = Field(..., description="The unique ID of the user whose goals overview is to be fetched.")
) -> GetGoalsOverviewResponse:
    """
    Fetches the overview of goals for a user.
    """
    try:
        endpoint = f"/goals/overview/{user_id}"
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_GET_METHOD.value,
            endpoint=endpoint,
        )
        
        response = api_request.execute()
        
        return GetGoalsOverviewResponse(**response)
    except Exception as e:
        logger.error(f"Error in get goals overview tool, {str(e)}")
        raise e


@tool
def get_goal_details(
    user_id: UUID = Field(..., description="The unique ID of the user whose goal details are to be fetched.")
) -> GetGoalDetailsResponse:
    """
    Fetches detailed goal information for a specific user.
    """
    try:
        endpoint = f"/goals/details/{user_id}"
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_GET_METHOD.value,
            endpoint=endpoint,
        )
        
        response = api_request.execute()
        
        return GetGoalDetailsResponse(**response)
    except Exception as e:
        logger.error(f"Error in get goal details tool, {str(e)}")
        raise e


@tool
def create_goal(
    user_id: UUID = Field(..., description="The unique ID of the user creating the goal."),
    goal_name: str = Field(..., min_length=1, max_length=100, description="Name of the goal."),
    goal_description: str = Field(..., min_length=1, max_length=255, description="Description of the goal."),
    goal_target_amount: float = Field(..., gt=0, description="Target amount for the goal (must be greater than 0).")
) -> CreateGoalResponse:
    """
    Creates a new goal for a user.
    """
    try:
        endpoint = f"/goals/{user_id}"
        
        payload = {
            GoalConstants.KEY_GOAL_NAME.value: goal_name,
            GoalConstants.KEY_GOAL_DESCRIPTION.value: goal_description,
            GoalConstants.KEY_GOAL_TARGET_AMOUNT.value: goal_target_amount
        }
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_POST_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        
        response = api_request.execute()
        
        return CreateGoalResponse(**response)
    except Exception as e:
        logger.error(f"Error in create goal tool, {str(e)}")
        raise e


@tool
def delete_goal(
    user_id: UUID = Field(..., description="The unique ID of the user whose goal is to be deleted."),
    goal_id: UUID = Field(..., description="The unique ID of the goal to delete.")
) -> DeleteGoalResponse:
    """
    Deletes a specific goal for a user.
    """
    try:
        endpoint = f"/goals/{user_id}"
        
        payload = {
            GoalConstants.KEY_GOAL_ID.value: str(goal_id)
        }
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_DELETE_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        
        response = api_request.execute()
        
        return DeleteGoalResponse(**response)
    except Exception as e:
        logger.error(f"Error in delete goal tool, {str(e)}")
        raise e


@tool
def edit_goal(
    user_id: UUID = Field(..., description="The unique ID of the user whose goal is to be edited."),
    goal_id: UUID = Field(..., description="The unique ID of the goal to edit."),
    goal_name: Optional[str] = Field(None, min_length=1, max_length=100, description="The new name of the goal."),
    goal_description: Optional[str] = Field(None, min_length=1, max_length=255, description="The new description of the goal."),
    goal_target_amount: Optional[float] = Field(None, gt=0, description="The new target amount for the goal."),
    goal_current_amount: Optional[float] = Field(None, ge=0, description="The updated current amount saved towards the goal.")
) -> EditGoalResponse:
    """
    Edits the details of a specific goal for a user.
    """
    try:
        endpoint = f"/goals/{user_id}"
        
        payload = {
            GoalConstants.KEY_GOAL_ID.value: str(goal_id)
        }

        if goal_name is not None:
            payload[GoalConstants.KEY_GOAL_NAME.value] = goal_name
        if goal_description is not None:
            payload[GoalConstants.KEY_GOAL_DESCRIPTION.value] = goal_description
        if goal_target_amount is not None:
            payload[GoalConstants.KEY_GOAL_TARGET_AMOUNT.value] = goal_target_amount
        if goal_current_amount is not None:
            payload[GoalConstants.KEY_GOAL_CURRENT_AMOUNT.value] = goal_current_amount

        api_request = APIRequest(
            http_method=APIConstants.KEY_PUT_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        response = api_request.execute()
        return EditGoalResponse(**response)
    except Exception as e:
        logger.error(f"Error in edit goal tool, {str(e)}")
        raise e


@tool
def add_amount_to_goal(
    user_id: UUID = Field(..., description="The unique ID of the user whose goal is to be updated."),
    goal_id: UUID = Field(..., description="The unique ID of the goal to which the amount will be added."),
    amount_to_add: float = Field(..., gt=0, description="The amount to add to the goal's current amount.")
) -> AddAmountToGoalResponse:
    """
    Adds a specified amount to a user's goal.
    """
    try:
        endpoint = f"/goals/{user_id}"
        
        payload = {
            GoalConstants.KEY_GOAL_ID.value: str(goal_id),
            GoalConstants.KEY_GOAL_CURRENT_AMOUNT.value: amount_to_add
        }
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_PATCH_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        
        response = api_request.execute()
        
        return AddAmountToGoalResponse(**response)
    except Exception as e:
        logger.error(f"Error in add amount to goal tool, {str(e)}")
        raise e
