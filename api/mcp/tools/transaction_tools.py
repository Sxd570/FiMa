from fastmcp import FastMCP
from pydantic import Field
from typing import Optional
from uuid import UUID

from domain.transaction_domain import TransactionDomain
from middleware import LoggingMiddleware
from models.transaction_models import (
    TransactionType,
    GetTransactionsResponse,
    CreateTransactionResponse,
    TransactionFilters,
)
from utils.logger import Logger


logger = Logger(__name__)
_transaction_domain = TransactionDomain()
_logging_middleware = LoggingMiddleware(__name__)


def get_transactions(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose transactions are to be fetched."
        ),
    ),
    filters: Optional[TransactionFilters] = Field(
        None,
        description="Optional filters for transactions.",
    ),
    limit: int = Field(
        15,
        gt=0,
        le=100,
        description=(
            "Maximum number of transactions to return "
            "(default: 15, max: 100)."
        ),
    ),
    offset: int = Field(
        0,
        ge=0,
        description=(
            "Number of transactions to skip before starting to collect "
            "the result set."
        ),
    ),
) -> GetTransactionsResponse:
    """
    Fetch transactions for a given user with optional filters, limit,
    and offset.
    """
    try:
        return _transaction_domain.get_transactions(
            user_id=user_id,
            filters=filters,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error(f"Error in tool get_transactions: {str(e)}")
        raise


def create_transaction(
    user_id: UUID = Field(
        ...,
        description="The unique ID of the user creating the transaction.",
    ),
    budget_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the budget associated with the transaction."
        ),
    ),
    transaction_type: TransactionType = Field(
        ...,
        description="Type of the transaction. Must be 'expense' or 'income'.",
    ),
    transaction_info: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Additional information about the transaction.",
    ),
    transaction_amount: float = Field(
        ...,
        gt=0,
        description="Amount of the transaction (must be greater than 0).",
    ),
    transaction_date: str = Field(
        ...,
        description="Date of the transaction in 'YYYY-MM-DD' format.",
    ),
) -> CreateTransactionResponse:
    """Create a new transaction for a user."""
    try:
        return _transaction_domain.create_transaction(
            user_id=user_id,
            budget_id=budget_id,
            transaction_type=transaction_type,
            transaction_info=transaction_info,
            transaction_amount=transaction_amount,
            transaction_date=transaction_date,
        )
    except Exception as e:
        logger.error(f"Error in tool create_transaction: {str(e)}")
        raise


def register_transaction_tools(mcp: FastMCP) -> None:
    """
    Register transaction tools on a FastMCP instance.
    """
    mcp.tool(get_transactions)
    mcp.tool(create_transaction)

