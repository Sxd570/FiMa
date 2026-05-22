from uuid import UUID

from constants import APIConstants, BudgetConstants
from models.budget_models import (
    GetBudgetOverviewResponse,
    GetBudgetDetailsResponse,
    EditBudgetLimitResponse,
    DeleteBudgetResponse,
    CreateBudgetResponse,
    BudgetDetail,
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
        user_id: UUID,
        budget_month: str,
    ) -> GetBudgetOverviewResponse:
        try:
            endpoint = f"/budget/{user_id}/overview"
            params = {
                BudgetConstants.KEY_BUDGET_MONTH_QUERY.value: budget_month
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=endpoint,
                params=params,
            )
            response_data = api_request.execute()
            return GetBudgetOverviewResponse(
                budget_total_budget=response_data.get(BudgetConstants.KEY_BUDGET_TOTAL_BUDGET.value),
                budget_total_spent=response_data.get(BudgetConstants.KEY_BUDGET_TOTAL_SPENT.value),
                budget_near_limit_count=response_data.get(BudgetConstants.KEY_BUDGET_NEAR_LIMIT_COUNT.value),
                budget_over_limit_count=response_data.get(BudgetConstants.KEY_BUDGET_OVER_LIMIT_COUNT.value),
                budget_remaining_amount=response_data.get(BudgetConstants.KEY_BUDGET_REMAINING_AMOUNT.value),
                budget_percentage_spent=response_data.get(BudgetConstants.KEY_BUDGET_PERCENTAGE_SPENT.value),
                budget_date=response_data.get(BudgetConstants.KEY_BUDGET_DATE.value),
            )
        except Exception as e:
            logger.error(f"Error in BudgetDomain.get_budget_overview: {str(e)}")
            raise

    def get_budget_details(
        self,
        user_id: UUID,
        budget_month: str,
        limit: int = 15,
        offset: int = 0,
    ) -> GetBudgetDetailsResponse:
        try:
            endpoint = f"/budget/{user_id}/details"
            params = {
                BudgetConstants.KEY_BUDGET_MONTH_QUERY.value: budget_month,
                BudgetConstants.KEY_LIMIT.value: limit,
                BudgetConstants.KEY_OFFSET.value: offset,
            }
            api_request = APIRequest(
                http_method=APIConstants.KEY_GET_METHOD.value,
                endpoint=endpoint,
                params=params,
            )
            response_data = api_request.execute()
            raw_budget_details = response_data.get(BudgetConstants.KEY_BUDGET_DETAILS.value) or []
            if not raw_budget_details:
                return GetBudgetDetailsResponse(
                    budget_details=[],
                    has_more=response_data.get(BudgetConstants.KEY_HAS_MORE.value),
                )
            budget_details = [
                BudgetDetail(
                    budget_id=item.get(BudgetConstants.KEY_BUDGET_ID.value),
                    budget_name=item.get(BudgetConstants.KEY_BUDGET_NAME.value),
                    budget_allocated_amount=item.get(BudgetConstants.KEY_BUDGET_ALLOCATED_AMOUNT.value),
                    budget_spent_amount=item.get(BudgetConstants.KEY_BUDGET_SPENT_AMOUNT.value),
                    budget_allocated_month=item.get(BudgetConstants.KEY_BUDGET_ALLOCATED_MONTH.value),
                    budget_remaining_amount=item.get(BudgetConstants.KEY_BUDGET_REMAINING_AMOUNT.value),
                    is_limit_reached=item.get(BudgetConstants.KEY_IS_LIMIT_REACHED.value),
                    is_over_limit=item.get(BudgetConstants.KEY_IS_OVER_LIMIT.value),
                    budget_percentage_spent=item.get(BudgetConstants.KEY_BUDGET_PERCENTAGE_SPENT.value),
                )
                for item in raw_budget_details
            ]
            return GetBudgetDetailsResponse(
                budget_details=budget_details,
                has_more=response_data.get(BudgetConstants.KEY_HAS_MORE.value),
            )
        except Exception as e:
            logger.error(f"Error in BudgetDomain.get_budget_details: {str(e)}")
            raise

    def edit_budget_limit(
        self,
        user_id: UUID,
        budget_id: UUID,
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
            response_data = api_request.execute()
            return EditBudgetLimitResponse(
                message=response_data.get(BudgetConstants.KEY_MESSAGE.value),
            )
        except Exception as e:
            logger.error(f"Error in BudgetDomain.edit_budget_limit: {str(e)}")
            raise

    def delete_budget(
        self,
        user_id: UUID,
        budget_id: UUID,
    ) -> DeleteBudgetResponse:
        try:
            endpoint = f"/budget/{user_id}/delete/{budget_id}"
            api_request = APIRequest(
                http_method=APIConstants.KEY_DELETE_METHOD.value,
                endpoint=endpoint,
            )
            response_data = api_request.execute()
            return DeleteBudgetResponse(
                message=response_data.get(BudgetConstants.KEY_MESSAGE.value),
            )
        except Exception as e:
            logger.error(f"Error in BudgetDomain.delete_budget: {str(e)}")
            raise

    def create_budget(
        self,
        user_id: UUID,
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
            response_data = api_request.execute()
            return CreateBudgetResponse(
                message=response_data.get(BudgetConstants.KEY_MESSAGE.value),
                budget_id=response_data.get(BudgetConstants.KEY_BUDGET_ID.value),
            )
        except Exception as e:
            logger.error(f"Error in BudgetDomain.create_budget: {str(e)}")
            raise

