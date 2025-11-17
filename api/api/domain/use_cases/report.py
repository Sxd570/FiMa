from domain.database.transaction import TransactionDatabase
from constants.transaction_constants import ( 
    KEY_YEAR, 
    KEY_MONTH,
    KEY_WEEK
)
from domain.database.budget import BudgetDatabase
from shared.logger import Logger
from domain.models.io_models.report_io_models import (
    GetReportChartPayload,
    GetReportChartDBRequest,
    GetReportChartResponse
)

logger = Logger(__name__)

class ReportUseCase:
    def __init__(self):
        self.transaction_database = None
        self.budget_database = None

    def get_report_chart(self, payload: GetReportChartPayload):
        try:
            self.transaction_database = TransactionDatabase()
            self.budget_database = BudgetDatabase()

            user_id = payload.user_id
            time_period = payload.time_period
            transaction_type = payload.transaction_type

            get_report_chart_data_db_request = GetReportChartDBRequest(
                user_id=user_id,
                time_period=time_period,
                transaction_type=transaction_type
            )

            if time_period == KEY_YEAR:
                report_chart_data = self.transaction_database.get_yearly_data(
                    db_request=get_report_chart_data_db_request
                )
            elif time_period == KEY_MONTH:
                report_chart_data = self.transaction_database.get_monthly_data(
                    db_request=get_report_chart_data_db_request
                )
            elif time_period == KEY_WEEK:
                report_chart_data = self.transaction_database.get_weekly_data(
                    db_request=get_report_chart_data_db_request
                )
            else:
                raise ValueError("Invalid time period specified.")

            response = GetReportChartResponse(
                time_period=time_period,
                transaction_type=transaction_type,
                data=report_chart_data.data
            )

            return response
        except Exception as e:
            logger.error(f"Error in get_report_chart use case: {str(e)}")
            raise e