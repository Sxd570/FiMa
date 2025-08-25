from fastapi import APIRouter

from shared.logger import Logger
from core.use_cases.budget import BudgetUseCase
from core.models.io_models.budget_io_models import (
    GetBudgetOverviewRequest,
    GetBudgetOverviewPayload,
    GetBudgetDetailsRequest,
    GetBudgetDetailsPayload,
    EditBudgetDetailRequest,
    EditBudgetDetailPayload,
    DeleteBudgetDetailPayload,
    DeleteBudgetDetailRequest,
    CreateBudgetRequest,
    CreateBudgetPayload
)

logger = Logger(__name__)
router = APIRouter()


@router.get("/budget/overview/{user_id}")
async def get_budget_overview(user_id: str, request: GetBudgetOverviewRequest):
    try:
        date = request.month

        payload = GetBudgetOverviewPayload(
            user_id=user_id,
            date=date
        )

        budget = BudgetUseCase()

        budget_overview = budget.get_budget_overview(payload=payload)

        return budget_overview
    except Exception as e:
        logger.error(f"Error in get_budget_overview: {e}")
        raise e
    

@router.get("/budget/details/{user_id}")
async def get_budget_details(user_id: str, request: GetBudgetDetailsRequest):
    try:
        date = request.month

        budget = BudgetUseCase()

        payload = GetBudgetDetailsPayload(
            user_id=user_id,
            date=date
        )

        budget_details = budget.get_budget_details(
            payload=payload
        )

        return budget_details
    except Exception as e:
        logger.error(f"Error in get_budget_details: {e}")
        raise e
    

@router.patch("/budget/edit_limit/{budget_id}")
async def edit_budget_limit(budget_id: str, request: EditBudgetDetailRequest):
    try:
        user_id = request.user_id
        new_budget_limit = request.new_budget_limit

        payload = EditBudgetDetailPayload(
            budget_id=budget_id,
            new_budget_limit=new_budget_limit,
            user_id=user_id
        )

        budget = BudgetUseCase()

        updated_budget_status = budget.edit_budget_limit(
            payload=payload
        )

        return updated_budget_status
    except Exception as e:
        logger.error(f"Error in edit_budget_limit: {e}")
        raise e


@router.delete("/budget/delete/{budget_id}")
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
    

@router.post("/budget/create")
async def create_budget(request: CreateBudgetRequest):
    try:
        user_id = request.user_id
        budget_limit_amount = request.budget_limit
        name = request.name
        month = request.month
        transaction_type = request.transaction_type
        description = request.description
        

        payload = CreateBudgetPayload(
            user_id=user_id,
            month=month,
            budget_limit_amount=budget_limit_amount,
            name=name,
            transaction_type=transaction_type,
            description=description
        )

        budget = BudgetUseCase()
        creation_status = budget.create_budget(
            payload=payload
        )

        return creation_status
    except Exception as e:
        logger.error(f"Error in create_budget: {e}")
        raise e