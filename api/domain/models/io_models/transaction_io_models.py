from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Union, Any

class GetTransactionRequest(BaseModel):
    filters: Optional[dict] = Field(None, description="Filters to apply on the transactions")
    limit: Optional[int] = Field(None, ge=1, description="Limit the number of transactions returned")
    offset: Optional[int] = Field(None, ge=0, description="Offset for pagination")

class GetTransactionPayload(BaseModel):
    user_id: str
    filters: Optional[dict] = Field(None, description="Filters to apply on the transactions")
    limit: Optional[int] = Field(None, ge=1, description="Limit the number of transactions returned")
    offset: Optional[int] = Field(None, ge=0, description="Offset for pagination")

class GetTransactionDBRequest(BaseModel):
    user_id: str
    filters: Optional[dict] = Field(None, description="Filters to apply on the transactions")
    limit: Optional[int] = Field(None, ge=1, description="Limit the number of transactions returned")
    offset: Optional[int] = Field(None, ge=0, description="Offset for pagination")


class TransactionDetail(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    category_name: str = Field(..., description="Name of the category")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")


class GetTransactionDBResponse(BaseModel):
    transactions: List[TransactionDetail] = Field([], description="List of transactions")


class GetTransactionResponse(BaseModel):
    transactions: List[TransactionDetail] = Field([], description="List of transactions")


class CreateTransactionRequest(BaseModel):
    category_id: Optional[str] = Field(None, description="ID of the category for the transaction")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")
    

class CreateTransactionPayload(BaseModel):
    user_id: str = Field(..., description="ID of the user creating the transaction")
    category_id: Optional[str] = Field(None, description="ID of the category for the transaction")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")


class CreateTransactionDBRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user creating the transaction")
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    category_id: Optional[str] = Field(None, description="ID of the category for the transaction")
    transaction_type: str = Field(..., description="ID of the transaction type")
    transaction_info: str = Field(..., description="Information about the transaction")
    transaction_amount: float = Field(..., description="Amount of the transaction")
    transaction_date: str = Field(..., description="Date of the transaction")