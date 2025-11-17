from uuid import UUID
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Optional


class GetReportSummaryRequest(BaseModel):
    time_period: str = Field(..., description="Time period for the report summary: 'week', 'month', 'year'")
    transaction_type: str = Field(..., description="Type of transactions to include: 'income', 'expense'")

class GetReportSummaryPayload(BaseModel):
    user_id: UUID = Field(..., description="ID of the user for whom the report summary is generated")
    time_period: str = Field(..., description="Time period for the report summary: 'week', 'month', 'year'")
    transaction_type: str = Field(..., description="Type of transactions to include: 'income', 'expense'")


class GetReportChartDataDBRequest(BaseModel):
    user_id: UUID = Field(..., description="ID of the user for whom to fetch report chart data")
    time_period: str = Field(..., description="Time period for the report chart data: 'week', 'month', 'year'")
    transaction_type: str = Field(..., description="Type of transactions to include: 'income', 'expense'")


class ReportChartPeriodData(BaseModel):
    data: Dict[str, int] = Field(..., description="Grouped transaction data for the period")

class ReportChartResponse(BaseModel):
    time_period: str = Field(..., description="Time period for the report chart data")
    transaction_type: str = Field(..., description="Type of transactions included in the report")

    current: Optional[ReportChartPeriodData] = Field(..., description="Data for the current time period")
    previous: Optional[ReportChartPeriodData] = Field(..., description="Data for the previous time period")



class GetReportChartYearData(BaseModel):
    year: int = Field(..., description="Year of the transactions")
    total_amount: float = Field(..., description="Total amount of transactions for the year")

class GetReportChartMonthData(BaseModel):
    year: int = Field(..., description="Year of the transactions")
    month: int = Field(..., description="Month of the transactions")
    total_amount: float = Field(..., description="Total amount of transactions for the month")


class GetReportChartWeekData(BaseModel):
    date: str = Field(..., description="Date of the transactions in 'YYYY-MM-DD' format")
    total_amount: float = Field(..., description="Total amount of transactions for the date")
    period: str = Field(..., description="Period indicator: 'current' or 'previous'")


class GetReportChartDataDBResponse(BaseModel):
    data: Optional[list[GetReportChartYearData | GetReportChartMonthData | GetReportChartWeekData]] = Field(..., description="Chart data for the report")


class GetReportChartDataResponse(BaseModel):
    time_period: str = Field(..., description="Time period for the report chart data")
    transaction_type: str = Field(..., description="Type of transactions included in the report")
    data: Optional[list[GetReportChartYearData | GetReportChartMonthData | GetReportChartWeekData]] = Field(..., description="Chart data for the report")
