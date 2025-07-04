from fastapi import APIRouter
from shared.logger import Logger
from core.use_cases.goals import GoalsUseCase
from core.models.io_models.goals_io_models import (
    CreateGoalDetailRequest,
    CreateGoalDetailPayload,
    UpdateGoalDetailRequest,
    UpdateGoalDetailPayload,
    DeleteGoalDetailRequest,
    DeleteGoalDetailPayload,
    AddAmountToGoalDetailPayload,
    AddAmountToGoalDetailRequest,
    GetGoalsDashboardRequest,
    GetGoalsDashboardPayload
)

logger = Logger(__name__)
router = APIRouter()

@router.get("/goals/overview/{user_id}")
async def get_goals_overview(user_id: str):
    try:      
        goals = GoalsUseCase()
        goals_overview = goals.get_goals_overview(user_id)
        return goals_overview
    except Exception as e:
        logger.error(f"Error in get_goals_overview: {e}")
        raise e
    

@router.get("/goals/{user_id}")
async def get_goal_details(user_id: str):
    try:
        goals = GoalsUseCase()
        goal_details = goals.get_goal_details(user_id)
        return goal_details
    except Exception as e:
        logger.error(f"Error in get_goal_details: {e}")
        raise e
    

@router.post("/goals/{user_id}")
async def create_goal(user_id: str, request: CreateGoalDetailRequest):
    try:
        payload = CreateGoalDetailPayload(
            user_id=user_id,
            goal_name=request.goal_name,
            goal_description=request.goal_description,
            goal_target_amount=request.goal_target_amount
        )

        goals = GoalsUseCase()

        status = goals.create_goal(
            payload=payload
        )
        return status
    except Exception as e:
        logger.error(f"Error in create_goal: {e}")
        raise e
    

@router.put("/goals/{user_id}")
async def edit_goal(user_id: str, request: UpdateGoalDetailRequest):
    try:
        payload = UpdateGoalDetailPayload(
            user_id=user_id,
            goal_id=request.goal_id,
            goal_name=request.goal_name,
            goal_description=request.goal_description,
            goal_target_amount=request.goal_target_amount,
            goal_current_amount=request.goal_current_amount
        )
        goals = GoalsUseCase()

        status = goals.edit_goal(
            payload=payload
        )
        return status
    except Exception as e:
        logger.error(f"Error in edit_goal: {e}")
        raise e
    

@router.delete("/goals/{user_id}")
async def delete_goal(user_id: str, request: DeleteGoalDetailRequest):
    try:
        payload = DeleteGoalDetailPayload(
            goal_id=request.goal_id,
            user_id=user_id
        )

        goals = GoalsUseCase()

        status = goals.delete_goal(
            payload=payload
        )

        return status
    except Exception as e:
        logger.error(f"Error in delete_goal: {e}")
        raise e
    

@router.patch("/goals/{user_id}")
async def add_amount_to_goal(user_id: str, request: AddAmountToGoalDetailRequest):
    try:
        payload = AddAmountToGoalDetailPayload(
            user_id=user_id,
            goal_id=request.goal_id,
            amount_to_add=request.amount_to_add
        )

        goals = GoalsUseCase()

        status = goals.add_amount_to_goal(
            payload=payload
        )

        return status
    except Exception as e:
        logger.error(f"Error in add_amount_to_goal: {e}")
        raise e
    

@router.get("/goals/dashboard/{user_id}")
async def get_goals_dashboard(user_id: str, request: GetGoalsDashboardRequest):
    try:
        payload = GetGoalsDashboardPayload(
            user_id=user_id,
            limit=request.limit,
            offset=request.offset
        )

        goals = GoalsUseCase()

        dashboard_data = goals.get_goals_dashboard(
            payload=payload
        )

        return dashboard_data
    except Exception as e:
        logger.error(f"Error in get_goals_dashboard: {e}")
        raise e