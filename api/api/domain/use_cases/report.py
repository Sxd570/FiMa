from domain.database.transaction import TransactionDatabase
from domain.database.budget import BudgetDatabase
from shared.logger import Logger
from domain.models.io_models.report_io_models import (
    GetReportSummaryPayload,
    GetReportChartDataDBRequest,
    GetReportChartDataResponse
)

logger = Logger(__name__)

class ReportUseCase:
    def __init__(self):
        self.transaction_database = None
        self.budget_database = None

    def get_report_summary(self, payload: GetReportSummaryPayload):
        try:
            self.transaction_database = TransactionDatabase()
            self.budget_database = BudgetDatabase()

            user_id = payload.user_id
            time_period = payload.time_period
            transaction_type = payload.transaction_type

            get_report_chart_data_db_request = GetReportChartDataDBRequest(
                user_id=user_id,
                time_period=time_period,
                transaction_type=transaction_type
            )

            report_chart_data = self.transaction_database.get_report_chart_data(
                db_request=get_report_chart_data_db_request
            )

            response = GetReportChartDataResponse(
                time_period=time_period,
                transaction_type=transaction_type,
                data=report_chart_data.data
            )

            return response
        except Exception as e:
            logger.error(f"Error in get_report_summary use case: {str(e)}")
            raise e