from fastapi import APIRouter
from shared.logger import Logger
from core.use_cases.goals import GoalsUseCase

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