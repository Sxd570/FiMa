from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any

class GetTransactionRequest(BaseModel):
    limit: Optional[int] = Field(None, ge=1, description="Limit the number of transactions returned")
    offset: Optional[int] = Field(None, ge=0, description="Offset for pagination")
    from_date: Optional[str] = Field(None, description="Filter transactions from this date (YYYY-MM-DD)")
    to_date: Optional[str] = Field(None, description="Filter transactions up to this date (YYYY-MM-DD)")
    budget_id: Optional[str] = Field(None, description="Filter transactions by budget ID")

class GetTransactionPayload(BaseModel):
    user_id: str
    limit: Optional[int] = Field(None, ge=1, description="Limit the number of transactions returned")
    offset: Optional[int] = Field(None, ge=0, description="Offset for pagination")
    from_date: Optional[str] = Field(None, description="Filter transactions from this date (YYYY-MM-DD)")
    to_date: Optional[str] = Field(None, description="Filter transactions up to this date (YYYY-MM-DD)")
    budget_id: Optional[str] = Field(None, description="Filter transactions by budget ID")

class GetTransactionDBRequest(BaseModel):
    user_id: str
    limit: Optional[int] = Field(None, ge=1, description="Limit the number of transactions returned")
    offset: Optional[int] = Field(None, ge=0, description="Offset for pagination")
    from_date: Optional[str] = Field(None, description="Filter transactions from this date (YYYY-MM-DD)")
    to_date: Optional[str] = Field(None, description="Filter transactions up to this date (YYYY-MM-DD)")
    budget_id: Optional[str] = Field(None, description="Filter transactions by budget ID")


class TransactionDetail(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    budget_name: str = Field(..., description="Name of the category")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")


class GetTransactionDBResponse(BaseModel):
    transactions: List[TransactionDetail] = Field([], description="List of transactions")


class GetTransactionResponse(BaseModel):
    transactions: List[TransactionDetail] = Field([], description="List of transactions")


class CreateTransactionRequest(BaseModel):
    budget_id: Optional[str] = Field(None, description="ID of the budget for the transaction")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")
    

class CreateTransactionPayload(BaseModel):
    user_id: str = Field(..., description="ID of the user creating the transaction")
    budget_id: Optional[str] = Field(None, description="ID of the budget for the transaction")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")


class CreateTransactionDBRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user creating the transaction")
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    budget_id: Optional[str] = Field(None, description="ID of the budget for the transaction")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")


class CreateTransactionResponse(BaseModel):
    message: str = Field(..., description="Status of the creation operation")
    transaction_id: str = Field(..., description="Unique identifier of the created transaction")