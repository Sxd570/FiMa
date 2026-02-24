from shared.logger import Logger
from sqlalchemy import extract, func, case, or_, and_
from copy import deepcopy
from datetime import datetime, timedelta
from domain.interfaces.transaction_interface import TransactionInterface
from domain.models.tables.transaction import Transaction
from domain.models.tables.budget import Budget
from shared.Utility.db_base import get_db_session
from domain.models.io_models.transaction_io_models import (
    TransactionDetail,
    GetTransactionDBRequest,
    GetTransactionDBResponse,
    CreateTransactionDBRequest,
    CreateTransactionResponse
)
from domain.exceptions import TransactionNotFoundException
from domain.models.io_models.report_io_models import (
    GetReportChartDBRequest,
    GetReportChartYearData,
    GetReportChartDataDBResponse,
    GetReportChartMonthData,
    GetReportChartWeekData
)

logger = Logger(__name__)

class TransactionDatabase(TransactionInterface):
    def __init__(self):
        self.db_session = None
        self.user_id = None


    @staticmethod
    def format_filters(filters: dict):
        formatted_filters = []
        for key, value in filters.items():
            if key == "from_date":
                # Filter for date >= from_date
                formatted_filters.append(getattr(Transaction, "transaction_date") >= value)
            elif key == "to_date":
                # Filter for date <= to_date
                formatted_filters.append(getattr(Transaction, "transaction_date") <= value)
            elif isinstance(value, list):
                formatted_filters.append(getattr(Transaction, key).in_(value))
            else:
                formatted_filters.append(getattr(Transaction, key) == value)
        return formatted_filters


    def get_transactions(self, db_request: GetTransactionDBRequest) -> GetTransactionDBResponse:
        try:
            self.db_session = get_db_session()

            self.user_id = db_request.user_id

            filter_group = [
                Transaction.user_id == self.user_id,
            ]

            if db_request.filters:
                filters = self.format_filters(db_request.filters)
                filter_group.extend(filters)

            query = self.db_session.query(
                Transaction.transaction_id,
                Transaction.transaction_type,
                Transaction.transaction_info,
                Transaction.transaction_amount,
                Transaction.transaction_date,
                Budget.budget_name
            ).join(
                Budget, Transaction.budget_id == Budget.budget_id
            ).filter(
                *filter_group
            ).order_by(
                Transaction.transaction_date.desc()
            )

            if db_request.limit:
                query = query.limit(db_request.limit)

            if db_request.offset:
                query = query.offset(db_request.offset)

            results = query.all()

            if not results:
                return GetTransactionDBResponse(
                    transactions=[]
                )

            return GetTransactionDBResponse(
                transactions=[
                    TransactionDetail(
                        transaction_id=transaction_id,
                        budget_name=budget_name,
                        transaction_type=transaction_type,
                        transaction_info=transaction_info,
                        transaction_amount=transaction_amount,
                        transaction_date=transaction_date
                    )
                    for (
                        transaction_id,
                        transaction_type,
                        transaction_info,
                        transaction_amount,
                        transaction_date,
                        budget_name
                    ) in results
                ]
            )
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            raise e


    def create_transaction(self, db_request: CreateTransactionDBRequest) -> CreateTransactionResponse:
        try:
            self.db_session = get_db_session()

            user_id = db_request.user_id
            transaction_id = db_request.transaction_id
            budget_id = db_request.budget_id
            transaction_type = db_request.transaction_type
            transaction_info = db_request.transaction_info
            transaction_amount = db_request.transaction_amount
            transaction_date = db_request.transaction_date

            new_transaction = Transaction(
                user_id=user_id,
                transaction_id=transaction_id,
                budget_id=budget_id,
                transaction_type=transaction_type,
                transaction_info=transaction_info,
                transaction_amount=transaction_amount,
                transaction_date=transaction_date
            )

            self.db_session.add(new_transaction)
            self.db_session.commit()

            return CreateTransactionResponse(
                message="Transaction created successfully",
                transaction_id=transaction_id
            )
        except TransactionNotFoundException as e:
            raise e
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            self.db_session.rollback()
            raise e
                

    def get_yearly_data(self, db_request: GetReportChartDBRequest):
        try:
            self.db_session = get_db_session()
            user_id = db_request.user_id
            transaction_type = db_request.transaction_type

            filters = [
                Transaction.user_id == str(user_id),
                Transaction.transaction_type == transaction_type,
            ]

            db_response = self.db_session.query(
                extract('year', Transaction.transaction_date).label("year"),
                func.sum(Transaction.transaction_amount).label("total_amount")
            ).filter(
                *filters
            ).group_by(
                extract('year', Transaction.transaction_date)
            ).order_by(
                extract('year', Transaction.transaction_date)
            ).all()

            data = [
                GetReportChartYearData(
                    year=int(record.year),
                    total_amount=float(record.total_amount)
                )
                for record in db_response
            ]

            response = GetReportChartDataDBResponse(
                data=data
            )
            return response

        except Exception as e:
            logger.error(f"Error in get_yearly_data: {e}")
            raise e
        
    
    def get_monthly_data(self, db_request: GetReportChartDBRequest):
        try:
            self.db_session = get_db_session()

            user_id = db_request.user_id
            transaction_type = db_request.transaction_type

            filters = [
                Transaction.user_id == str(user_id),
                Transaction.transaction_type == transaction_type,
            ]

            current_year = datetime.now().year
            previous_year = current_year - 1

            db_response = self.db_session.query(
                extract('year', Transaction.transaction_date).label("year"),
                extract('month', Transaction.transaction_date).label("month"),
                func.sum(Transaction.transaction_amount).label("total_amount")
            ).filter(
                *filters,
                extract('year', Transaction.transaction_date).in_([current_year, previous_year])
            ).group_by(
                extract('year', Transaction.transaction_date),
                extract('month', Transaction.transaction_date)
            ).order_by(
                extract('year', Transaction.transaction_date),
                extract('month', Transaction.transaction_date)
            ).all()

            data = [
                GetReportChartMonthData(
                    year=int(record.year),
                    month=int(record.month),
                    total_amount=float(record.total_amount)
                )
                for record in db_response
            ]

            response = GetReportChartDataDBResponse(
                data=data
            )
            return response

        except Exception as e:
            logger.error(f"Error in get_monthly_data: {e}")
            raise e 
        
    
    def get_weekly_data(self, db_request: GetReportChartDBRequest):
        try:
            self.db_session = get_db_session()

            user_id = db_request.user_id
            transaction_type = db_request.transaction_type

            filters = [
                Transaction.user_id == str(user_id),
                Transaction.transaction_type == transaction_type,
            ]

            today = datetime.now()

            start_of_this_week = today - timedelta(days=today.weekday())

            start_of_prev_week = start_of_this_week - timedelta(days=7)
            end_of_prev_week = start_of_this_week - timedelta(seconds=1)

            db_response = self.db_session.query(
                Transaction.transaction_date.label("date"),
                func.sum(Transaction.transaction_amount).label("total_amount"),
                case(
                    (
                        and_(
                            Transaction.transaction_date >= start_of_this_week,
                            Transaction.transaction_date <= today
                        ),
                        "current"
                    ),
                    (
                        and_(
                            Transaction.transaction_date >= start_of_prev_week,
                            Transaction.transaction_date <= end_of_prev_week
                        ),
                        "previous"
                    ),
                ).label("period")
            ).filter(
                *filters,
                or_(
                    and_(Transaction.transaction_date >= start_of_this_week,
                        Transaction.transaction_date <= today),
                    and_(Transaction.transaction_date >= start_of_prev_week,
                        Transaction.transaction_date <= end_of_prev_week)
                )
            ).group_by(
                Transaction.transaction_date
            ).order_by(
                Transaction.transaction_date
            ).all()

            data = [
                GetReportChartWeekData(
                    date=record.date,
                    total_amount=float(record.total_amount),
                    period=record.period
                )
                for record in db_response
            ]

            response = GetReportChartDataDBResponse(
                data=data
            )
            return response
        except Exception as e:
            logger.error(f"Error in get_weekly_data: {e}")
            raise e