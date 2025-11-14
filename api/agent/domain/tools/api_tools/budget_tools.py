from pydantic import BaseModel, Field
from strands import tool
from typing import List, Optional
from uuid import UUID

from constants import APIConstants, BudgetConstants

from domain.models.io_models.api_tool_models.budget_model import (
    GetBudgetOverviewResponse,
    GetBudgetDetailsResponse,
    EditBudgetLimitResponse,
    DeleteBudgetResponse,
    CreateBudgetResponse
)

from shared.logger import Logger
from shared.Utility.api_request import APIRequest

logger = Logger(__name__)


@tool
def get_budget_overview(
    user_id: UUID = Field(..., description="The ID of the user."),
    budget_month: str = Field(..., description="The month for which to get the budget overview in 'YYYY-MM' format.")
) -> GetBudgetOverviewResponse:
    """
    This tool is used to get the budget overview for a user for a specific month.
    """
    try:
        endpoint=f"/budget/{user_id}/overview",
        
        payload = {
            BudgetConstants.KEY_BUDGET_MONTH.value: budget_month
        }
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_GET_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        
        response_data = api_request.execute()
        
        return GetBudgetOverviewResponse(**response_data)
    except Exception as e:
        logger.error(f"Error in get budget overview tool, {str(e)}")
        raise e


@tool
def get_budget_details(
    user_id: UUID = Field(..., description="The ID of the user."),
    budget_month: str = Field(..., description="The month for which to get the budget details in 'YYYY-MM' format.")
) -> GetBudgetDetailsResponse:
    """
    This tool is used to get details of all budgets created by a user for a specific month.
    """
    try:
        endpoint=f"/budget/{user_id}/details"
        
        payload = {
            BudgetConstants.KEY_BUDGET_MONTH.value: budget_month
        }
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_GET_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        
        response_data = api_request.execute()
        
        return GetBudgetDetailsResponse(**response_data)
    except Exception as e:
        logger.error(f"Error in get budget detail tool, {str(e)}")
        raise e


@tool
def edit_budget_limit(
    user_id: UUID = Field(..., description="The ID of the user."),
    budget_id: UUID = Field(..., description="The ID of the budget to be edited."),
    new_budget_limit: float = Field(..., description="The new limit to be set for the budget.")
) -> EditBudgetLimitResponse:
    """
    This tool is used to edit the limit of an existing budget.
    """
    try:
        endpoint=f"/budget/{user_id}/edit_limit/{budget_id}"
        
        payload = {
            BudgetConstants.KEY_NEW_BUDGET_LIMIT.value: new_budget_limit
        }
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_PATCH_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        
        response_data = api_request.execute()
        
        return EditBudgetLimitResponse(**response_data)
    except Exception as e:
        logger.error(f"Error in edit budget limit tool, {str(e)}")
        raise e


@tool
def delete_budget(
    user_id: UUID = Field(..., description="The ID of the user."),
    budget_id: UUID = Field(..., description="The ID of the budget to be deleted.")
) -> DeleteBudgetResponse:
    """
    This tool is used to delete an existing budget.
    """
    try:
        endpoint=f"/budget/{user_id}/delete/{budget_id}"
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_DELETE_METHOD.value,
            endpoint=endpoint
        )
        
        response_data = api_request.execute()
        
        return DeleteBudgetResponse(**response_data)
    except Exception as e:
        logger.error(f"Error in delete budget tool, {str(e)}")
        raise e


@tool
def create_budget(
    user_id: UUID = Field(..., description="The ID of the user."),
    budget_limit: float = Field(..., description="The limit for the new budget."),
    budget_name: str = Field(..., description="The name of the new budget."),
    budget_month: str = Field(..., description="The month for which the budget is being created in 'YYYY-MM' format."),
    description: str = Field(..., description="A brief description of the budget.")
) -> CreateBudgetResponse:
    """
    This tool is used to create a new budget for a user.
    """
    try:
        endpoint=f"/budget/{user_id}/create"
        
        payload = {
            BudgetConstants.KEY_BUDGET_LIMIT.value: budget_limit,
            BudgetConstants.KEY_BUDGET_NAME.value: budget_name,
            BudgetConstants.KEY_BUDGET_MONTH.value: budget_month,
            BudgetConstants.KEY_DESCRIPTION.value: description
        }
        
        api_request = APIRequest(
            http_method=APIConstants.KEY_POST_METHOD.value,
            endpoint=endpoint,
            payload=payload
        )
        
        response_data = api_request.execute()
        
        return CreateBudgetResponse(**response_data)
    except Exception as e:
        logger.error(f"Error in create budget tool, {str(e)}")
        raise e
