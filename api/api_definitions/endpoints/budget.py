from fastapi import APIRouter

from shared.logger import Logger
from core.use_cases.budget import BudgetUseCase
# from core.models.io_models.budget_io_models import (
#     CreateBudgetRequest, 
#     GetBudgetRequest,
#     EditBudgetRequest,
#     DeleteBudgetRequest,
#     GetBudgetOverviewRequest
# )


logger = Logger(__name__)
router = APIRouter()


# @router.get("/budget/overview/{user_id}")
def get_budget_overview(user_id: str):
    try:
        budget = BudgetUseCase()

        budget_overview = budget.get_budget_overview(user_id)

        return budget_overview
    except Exception as e:
        logger.error(f"Error in get_budget_overview: {e}")
        raise e
    

if __name__ == "__main__":
    user_id = "1234"
    get_budget_overview(user_id)

@router.post("/budget/add")
async def create_budget():
    try:
        return {
            "message": "Budget created successfully"
        }
    except Exception as e:
        logger.error(f"Error in create_budget: {e}")
        raise e
    

@router.put("/budget/edit")
async def edit_budget():
    try:
        return {
            "message": "Budget edited successfully"
        }
    except Exception as e:
        logger.error(f"Error in edit_budget: {e}")
        raise e
    

@router.delete("/budget/delete")
async def delete_budget():
    try:
        return {
            "message": "Budget deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error in delete_budget: {e}")
        raise e