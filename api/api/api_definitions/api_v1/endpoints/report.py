from fastapi import APIRouter
from shared.logger import Logger

from domain.use_cases.report import ReportUseCase
from domain.models.io_models.report_io_models import (
    GetReportSummaryPayload,
    GetReportSummaryRequest
)

logger = Logger(__name__)
router = APIRouter()


@router.post("/report/{user_id}/summary")
async def get_report_summary(user_id: str, request: GetReportSummaryRequest):
    try:
        time_period = request.time_period
        transaction_type = request.transaction_type

        payload = GetReportSummaryPayload(
            user_id=user_id,
            time_period=time_period,
            transaction_type=transaction_type
        )
        report_use_case = ReportUseCase()

        response = report_use_case.get_report_summary(payload=payload)
        return response
    except Exception as e:
        logger.error(f"Error in get_report_summary: {e}")
        raise e