from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"


class TransactionItem(BaseModel):
    transaction_id: Optional[UUID] = Field(None, description="Unique identifier of the transaction.")
    budget_name: Optional[str] = Field(None, description="Name of the budget associated with the transaction.")
    transaction_type: Optional[TransactionType] = Field(None, description="Type of the transaction (e.g., 'expense', 'income').")
    transaction_info: Optional[str] = Field(None, max_length=255, description="Additional information about the transaction.")
    transaction_amount: Optional[float] = Field(None, description="Amount of the transaction.")
    transaction_date: Optional[str] = Field(None, description="Date of the transaction in 'YYYY-MM-DD' format.")


class GetTransactionsResponse(BaseModel):
    transactions: Optional[List[TransactionItem]] = Field(None, description="List of transaction objects.")


class CreateTransactionResponse(BaseModel):
    transaction_id: Optional[UUID] = Field(None, description="Unique identifier of the created transaction.")
    message: Optional[str] = Field(None, description="Message indicating success or failure of the transaction creation.")


class TransactionFilters(BaseModel):
    from_date: Optional[str] = Field(None, description="Start date for filtering transactions in 'YYYY-MM-DD' format.")
    to_date: Optional[str] = Field(None, description="End date for filtering transactions in 'YYYY-MM-DD' format.")
    budget_id: Optional[UUID] = Field(None, description="The budget ID to filter transactions by.")
