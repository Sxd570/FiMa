from fastapi import APIRouter

from shared.logger import Logger
from core.use_cases.budget import BudgetUseCase
from core.models.io_models.budget_io_models import (
    GetBudgetOverviewRequest,
    GetBudgetDetailsRequest,
    EditBudgetDetailRequest,
    EditBudgetDetailPayload,
    DeleteBudgetDetailPayload,
    DeleteBudgetDetailRequest
)

logger = Logger(__name__)
router = APIRouter()


@router.get("/budget/overview/{user_id}")
async def get_budget_overview(user_id: str, request: GetBudgetOverviewRequest):
    try:
        date = request.month

        budget = BudgetUseCase()

        budget_overview = budget.get_budget_overview(user_id, date)

        return budget_overview
    except Exception as e:
        logger.error(f"Error in get_budget_overview: {e}")
        raise e
    

@router.get("/budget/details/{user_id}")
async def get_budget_details(user_id: str, request: GetBudgetDetailsRequest):
    try:
        date = request.month

        budget = BudgetUseCase()

        budget_details = budget.get_budget_details(user_id, date)

        return budget_details
    except Exception as e:
        logger.error(f"Error in get_budget_details: {e}")
        raise e
    

@router.patch("budget/edit_limit/{budget_id}")
async def edit_budget_limit(budget_id: str, request: EditBudgetDetailRequest):
    try:
        user_id = request.user_id
        new_budget_limit = request.new_budget_limit

        budget = BudgetUseCase()

        payload = EditBudgetDetailPayload(
            budget_id=budget_id,
            new_budget_limit=new_budget_limit,
            user_id=user_id
        )

        updated_budget_status = budget.edit_budget_limit(
            payload=payload
        )

        return updated_budget_status
    except Exception as e:
        logger.error(f"Error in edit_budget_limit: {e}")
        raise e


@router.delete("budget/delete/{budget_id}")
async def delete_budget(budget_id: str, request: DeleteBudgetDetailRequest):
    try:
        user_id = request.user_id

        budget = BudgetUseCase()

        payload = DeleteBudgetDetailPayload(
            budget_id=budget_id,
            user_id=user_id
        )

        deletion_status = budget.delete_budget(payload=payload)

        return deletion_status
    except Exception as e:
        logger.error(f"Error in delete_budget: {e}")
        raise e