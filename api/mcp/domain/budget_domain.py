from typing import Any, Dict

from constants import APIConstants, BudgetConstants
from models.budget_models import (
    GetBudgetOverviewResponse,
    GetBudgetDetailsResponse,
    EditBudgetLimitResponse,
    DeleteBudgetResponse,
    CreateBudgetResponse,
)
from utils.api_request import APIRequest
from utils.logger import Logger


logger = Logger(__name__)


class BudgetDomain:
    """
    Domain layer for budget-related MCP tools.

    Each method calls the downstream API directly via APIRequest and maps
    the response into the appropriate Pydantic model.
    """

    def get_budget_overview(
        self,
        user_id: str,
        budget_month: str,
    ) -> GetBudgetOverviewResponse:
        try:
            endpoint = f"/budget/{user_id}/overview"
            payload = {
                BudgetConstants.KEY_BUDGET_MONTH.value: budget_month
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=endpoint,
                payload=payload,
            )
            response_data = api_request.execute() or {}
            return GetBudgetOverviewResponse(**response_data)
        except Exception as e:
            logger.error(f"Error in BudgetDomain.get_budget_overview: {str(e)}")
            raise

    def get_budget_details(
        self,
        user_id: str,
        budget_month: str,
    ) -> GetBudgetDetailsResponse:
        try:
            endpoint = f"/budget/{user_id}/details"
            payload = {
                BudgetConstants.KEY_BUDGET_MONTH.value: budget_month
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=endpoint,
                payload=payload,
            )
            response_data = api_request.execute() or {}
            return GetBudgetDetailsResponse(**response_data)
        except Exception as e:
            logger.error(f"Error in BudgetDomain.get_budget_details: {str(e)}")
            raise

    def edit_budget_limit(
        self,
        user_id: str,
        budget_id: str,
        new_budget_limit: float,
    ) -> EditBudgetLimitResponse:
        try:
            endpoint = f"/budget/{user_id}/edit_limit/{budget_id}"
            payload = {
                BudgetConstants.KEY_NEW_BUDGET_LIMIT.value: new_budget_limit,
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_PATCH_METHOD.value,
                endpoint=endpoint,
                payload=payload,
            )
            response_data = api_request.execute() or {}
            return EditBudgetLimitResponse(**response_data)
        except Exception as e:
            logger.error(f"Error in BudgetDomain.edit_budget_limit: {str(e)}")
            raise

    def delete_budget(
        self,
        user_id: str,
        budget_id: str,
    ) -> DeleteBudgetResponse:
        try:
            endpoint = f"/budget/{user_id}/delete/{budget_id}"
            api_request = APIRequest(
                http_method=APIConstants.KEY_DELETE_METHOD.value,
                endpoint=endpoint,
            )
            response_data = api_request.execute() or {}
            return DeleteBudgetResponse(**response_data)
        except Exception as e:
            logger.error(f"Error in BudgetDomain.delete_budget: {str(e)}")
            raise

    def create_budget(
        self,
        user_id: str,
        budget_limit: float,
        budget_name: str,
        budget_month: str,
        description: str,
    ) -> CreateBudgetResponse:
        try:
            endpoint = f"/budget/{user_id}/create"
            payload = {
                BudgetConstants.KEY_BUDGET_LIMIT.value: budget_limit,
                BudgetConstants.KEY_BUDGET_NAME.value: budget_name,
                BudgetConstants.KEY_BUDGET_MONTH.value: budget_month,
                BudgetConstants.KEY_DESCRIPTION.value: description,
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_POST_METHOD.value,
                endpoint=endpoint,
                payload=payload,
            )
            response_data = api_request.execute() or {}
            return CreateBudgetResponse(**response_data)
        except Exception as e:
            logger.error(f"Error in BudgetDomain.create_budget: {str(e)}")
            raise

