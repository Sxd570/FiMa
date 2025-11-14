from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class TransactionItem(BaseModel):
    transaction_id: UUID = Field(..., description="Unique identifier of the transaction.")
    budget_name: str = Field(..., min_length=1, max_length=100, description="Name of the budget associated with the transaction.")
    transaction_type: TransactionType = Field(..., description="Type of the transaction (e.g., 'expense', 'income').")
    transaction_info: Optional[str] = Field(None, max_length=255, description="Additional information about the transaction.")
    transaction_amount: float = Field(..., gt=0, description="Amount of the transaction.")
    transaction_date: str = Field(..., description="Date of the transaction in 'YYYY-MM-DD' format.")


class GetTransactionsResponse(BaseModel):
    transactions: List[TransactionItem] = Field(..., description="List of transaction objects.")


class CreateTransactionResponse(BaseModel):
    transaction_id: UUID = Field(..., description="Unique identifier of the created transaction.")
    message: str = Field(..., description="Message indicating success or failure of the transaction creation.")


class TransactionFilters(BaseModel):
    from_date: Optional[str] = Field(None, description="Start date for filtering transactions in 'YYYY-MM-DD' format.")
    to_date: Optional[str] = Field(None, description="End date for filtering transactions in 'YYYY-MM-DD' format.")
    budget_id: Optional[UUID] = Field(None, description="The budget ID to filter transactions by.")
