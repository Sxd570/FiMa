from typing import Optional
from uuid import UUID

from constants import APIConstants, GoalConstants
from models.goal_models import (
    GetGoalsOverviewResponse,
    GetGoalDetailsResponse,
    CreateGoalResponse,
    DeleteGoalResponse,
    EditGoalResponse,
    AddAmountToGoalResponse,
    GoalDetail,
)
from utils.api_request import APIRequest
from utils.logger import Logger


logger = Logger(__name__)


class GoalDomain:
    """
    Domain layer for goal-related MCP tools.
    """

    def get_goals_overview(self, user_id: UUID) -> GetGoalsOverviewResponse:
        try:
            endpoint = f"/goals/overview/{user_id}"
            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=endpoint,
            )
            response = api_request.execute()
            return GetGoalsOverviewResponse(
                total_goals_count=response.get(GoalConstants.KEY_TOTAL_GOALS_COUNT.value),
                total_goals_completed=response.get(GoalConstants.KEY_TOTAL_GOALS_COMPLETED.value),
                total_amount_saved=response.get(GoalConstants.KEY_TOTAL_AMOUNT_SAVED.value),
                total_goal_amount=response.get(GoalConstants.KEY_TOTAL_GOAL_AMOUNT.value),
            )
        except Exception as e:
            logger.error(f"Error in GoalDomain.get_goals_overview: {str(e)}")
            raise

    def get_goal_details(
        self,
        user_id: UUID,
        limit: int = 15,
        offset: int = 0,
    ) -> GetGoalDetailsResponse:
        try:
            endpoint = f"/goals/{user_id}"
            params = {
                GoalConstants.KEY_LIMIT.value: limit,
                GoalConstants.KEY_OFFSET.value: offset,
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=endpoint,
                params=params,
            )
            response = api_request.execute()
            raw_goal_details = response.get(GoalConstants.KEY_GOAL_DETAILS.value) or []
            if not raw_goal_details:
                return GetGoalDetailsResponse(
                    goal_details=[],
                    has_more=response.get(GoalConstants.KEY_HAS_MORE.value),
                )
            goal_details = [
                GoalDetail(
                    goal_id=item.get(GoalConstants.KEY_GOAL_ID.value),
                    goal_name=item.get(GoalConstants.KEY_GOAL_NAME.value),
                    goal_description=item.get(GoalConstants.KEY_GOAL_DESCRIPTION.value),
                    goal_target_amount=item.get(GoalConstants.KEY_GOAL_TARGET_AMOUNT.value),
                    goal_current_amount=item.get(GoalConstants.KEY_GOAL_CURRENT_AMOUNT.value),
                    goal_remaining_amount=item.get(GoalConstants.KEY_GOAL_REMAINING_AMOUNT.value),
                    goal_percentage=item.get(GoalConstants.KEY_GOAL_PERCENTAGE.value),
                    is_goal_reached=item.get(GoalConstants.KEY_IS_GOAL_REACHED.value),
                )
                for item in raw_goal_details
            ]
            return GetGoalDetailsResponse(
                goal_details=goal_details,
                has_more=response.get(GoalConstants.KEY_HAS_MORE.value),
            )
        except Exception as e:
            logger.error(f"Error in GoalDomain.get_goal_details: {str(e)}")
            raise

    def create_goal(
        self,
        user_id: UUID,
        goal_name: str,
        goal_description: str,
        goal_target_amount: float,
    ) -> CreateGoalResponse:
        try:
            endpoint = f"/goals/{user_id}"
            payload = {
                GoalConstants.KEY_GOAL_NAME.value: goal_name,
                GoalConstants.KEY_GOAL_DESCRIPTION.value: goal_description,
                GoalConstants.KEY_GOAL_TARGET_AMOUNT.value: goal_target_amount,
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_POST_METHOD.value,
                endpoint=endpoint,
                payload=payload,
            )
            response = api_request.execute()
            return CreateGoalResponse(
                status=response.get(GoalConstants.KEY_STATUS.value),
            )
        except Exception as e:
            logger.error(f"Error in GoalDomain.create_goal: {str(e)}")
            raise

    def delete_goal(
        self,
        user_id: UUID,
        goal_id: UUID,
    ) -> DeleteGoalResponse:
        try:
            endpoint = f"/goals/{user_id}"
            payload = {
                GoalConstants.KEY_GOAL_ID.value: str(goal_id),
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_DELETE_METHOD.value,
                endpoint=endpoint,
                payload=payload,
            )
            response = api_request.execute()
            return DeleteGoalResponse(
                status=response.get(GoalConstants.KEY_STATUS.value),
                goal_id=response.get(GoalConstants.KEY_GOAL_ID.value),
            )
        except Exception as e:
            logger.error(f"Error in GoalDomain.delete_goal: {str(e)}")
            raise

    def edit_goal(
        self,
        user_id: UUID,
        goal_id: UUID,
        goal_name: Optional[str],
        goal_description: Optional[str],
        goal_target_amount: Optional[float],
        goal_current_amount: Optional[float],
    ) -> EditGoalResponse:
        try:
            endpoint = f"/goals/{user_id}"

            payload = {
                GoalConstants.KEY_GOAL_ID.value: str(goal_id),
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
                payload=payload,
            )
            response = api_request.execute()
            return EditGoalResponse(
                status=response.get(GoalConstants.KEY_STATUS.value),
            )
        except Exception as e:
            logger.error(f"Error in GoalDomain.edit_goal: {str(e)}")
            raise

    def add_amount_to_goal(
        self,
        user_id: UUID,
        goal_id: UUID,
        amount_to_add: float,
    ) -> AddAmountToGoalResponse:
        try:
            endpoint = f"/goals/{user_id}"
            payload = {
                GoalConstants.KEY_GOAL_ID.value: str(goal_id),
                GoalConstants.KEY_AMOUNT_TO_ADD.value: amount_to_add,
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_PATCH_METHOD.value,
                endpoint=endpoint,
                payload=payload,
            )
            response = api_request.execute()
            return AddAmountToGoalResponse(
                status=response.get(GoalConstants.KEY_STATUS.value),
            )
        except Exception as e:
            logger.error(f"Error in GoalDomain.add_amount_to_goal: {str(e)}")
            raise


