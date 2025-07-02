from fastapi import APIRouter

from shared.logger import Logger
from core.use_cases.budget import BudgetUseCase
from core.models.io_models.budget_io_models import (
    BudgetOverviewRequest,
    BudgetDetailsRequest
)

logger = Logger(__name__)
router = APIRouter()


@router.get("/budget/overview/{user_id}")
async def get_budget_overview(user_id: str, request: BudgetOverviewRequest):
    try:
        date = request.month

        budget = BudgetUseCase()

        budget_overview = budget.get_budget_overview(user_id, date)

        return budget_overview
    except Exception as e:
        logger.error(f"Error in get_budget_overview: {e}")
        raise e
    

@router.get("/budget/details/{user_id}")
async def get_budget_details(user_id: str, request: BudgetDetailsRequest):
    try:
        date = request.month

        budget = BudgetUseCase()

        budget_details = budget.get_budget_details(user_id, date)

        return budget_details
    except Exception as e:
        logger.error(f"Error in get_budget_details: {e}")
        raise e