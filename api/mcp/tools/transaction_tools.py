from fastmcp import FastMCP
from pydantic import Field
from typing import Optional
from uuid import UUID

from domain.transaction_domain import TransactionDomain
from models.transaction_models import (
    TransactionType,
    GetTransactionsResponse,
    CreateTransactionResponse,
)
from utils.logger import Logger


logger = Logger(__name__)
_transaction_domain = TransactionDomain()


def get_transactions(
    user_id: UUID = Field(
        ...,
        description=(
            "The unique ID of the user whose transactions are to be fetched."
        ),
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
    from_date: Optional[str] = Field(
        None,
        description="Filter transactions from this date (format: YYYY-MM-DD).",
    ),
    to_date: Optional[str] = Field(
        None,
        description="Filter transactions up to this date (format: YYYY-MM-DD).",
    ),
    budget_id: Optional[UUID] = Field(
        None,
        description="Filter transactions belonging to a specific budget ID.",
    ),
) -> GetTransactionsResponse:
    """Fetch a paginated list of transactions for a user with optional filters.

    What it does:
        Returns the user's transactions, optionally filtered by date
        range and/or a specific budget. Supports pagination via limit
        and offset.

    Inputs:
        user_id (UUID): The unique ID of the user.
        limit (int, optional): Max transactions to return (default 15, max 100).
        offset (int, optional): Number of transactions to skip (default 0).
        from_date (str, optional): Lower bound date in 'YYYY-MM-DD' format.
        to_date (str, optional): Upper bound date in 'YYYY-MM-DD' format.
        budget_id (UUID, optional): Filter to a specific budget.

    Returns (GetTransactionsResponse):
        transactions (list[TransactionItem]): Each item contains:
            - transaction_id (UUID)
            - budget_name (str)
            - transaction_type (str: 'expense' or 'income')
            - transaction_info (str)
            - transaction_amount (float)
            - transaction_date (str, 'YYYY-MM-DD')
        has_more (bool): True if more transactions exist beyond this page.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "limit": 2,
                "offset": 0,
                "from_date": "2026-05-01",
                "to_date": "2026-05-31"
            }
        Response:
            {
                "transactions": [
                    {
                        "transaction_id": "c3d4e5f6-7777-8888-9999-aaaabbbbcccc",
                        "budget_name": "Groceries",
                        "transaction_type": "expense",
                        "transaction_info": "Weekly shopping",
                        "transaction_amount": 82.45,
                        "transaction_date": "2026-05-12"
                    }
                ],
                "has_more": true
            }
    """
    try:
        return _transaction_domain.get_transactions(
            user_id=user_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
            budget_id=budget_id,
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
        gt=1,
        description="Amount of the transaction (must be greater than 1).",
    ),
    transaction_date: str = Field(
        ...,
        description="Date of the transaction in 'YYYY-MM-DD' format.",
    ),
) -> CreateTransactionResponse:
    """Create a new transaction (expense or income) tied to a user's budget.

    What it does:
        Records a new transaction for the user against the specified
        budget, with type, amount, descriptive info, and date.

    Inputs:
        user_id (UUID): The unique ID of the user.
        budget_id (UUID): The unique ID of the associated budget.
        transaction_type (TransactionType): 'expense' or 'income'.
        transaction_info (str): Description (1-255 chars).
        transaction_amount (float): Amount (must be greater than 1).
        transaction_date (str): Date in 'YYYY-MM-DD' format.

    Returns (CreateTransactionResponse):
        transaction_id (UUID): ID of the newly created transaction.
        message (str): Success or failure message.

    Example:
        Input:
            {
                "user_id": "4f1c2a8e-1234-4abc-9def-0123456789ab",
                "budget_id": "a1b2c3d4-1111-2222-3333-444455556666",
                "transaction_type": "expense",
                "transaction_info": "Weekly grocery shopping",
                "transaction_amount": 82.45,
                "transaction_date": "2026-05-12"
            }
        Response:
            {
                "transaction_id": "c3d4e5f6-7777-8888-9999-aaaabbbbcccc",
                "message": "Transaction created successfully."
            }
    """
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

