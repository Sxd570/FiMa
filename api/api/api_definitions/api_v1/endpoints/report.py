from fastapi import APIRouter
from shared.logger import Logger

from domain.use_cases.report import ReportUseCase
from domain.models.io_models.report_io_models import (
    GetReportChartPayload,
    GetReportChartRequest
)

logger = Logger(__name__)
router = APIRouter()


@router.post("/report/{user_id}/chart")
async def get_report_chart(user_id: str, request: GetReportChartRequest):
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