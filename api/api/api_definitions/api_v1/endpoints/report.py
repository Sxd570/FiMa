from fastapi import APIRouter
from shared.logger import Logger

from domain.use_cases.report import ReportUseCase
from domain.models.io_models.report_io_models import (
    GetReportChartPayload,
    GetReportChartRequest,
    GetReportCategoryRequest,
    GetReportCategoryPayload
)

logger = Logger(__name__)
router = APIRouter()


@router.post("/report/{user_id}/transaction/chart")
async def get_report_transaction_chart(user_id: str, request: GetReportChartRequest):
    try:
        time_period = request.time_period
        transaction_type = request.transaction_type

        payload = GetReportChartPayload(
            user_id=user_id,
            time_period=time_period,
            transaction_type=transaction_type
        )
        report_use_case = ReportUseCase()

        response = report_use_case.get_report_chart(
            payload=payload
        )
        return response
    except Exception as e:
        logger.error(f"Error in get_report_chart: {e}")
        raise e
    

@router.post("/report/{user_id}/category/chart")
async def get_report_category_chart(user_id: str, request: GetReportCategoryRequest):
    try:
        time_period = request.time_period

        payload = GetReportCategoryPayload(
            user_id=user_id,
            time_period=time_period
        )

        report_use_case = ReportUseCase()
        response = report_use_case.get_report_category(
            payload=payload
        )
        return response
    except Exception as e:
        logger.error(f"Error in get_report_category_chart: {e}")
        raise e