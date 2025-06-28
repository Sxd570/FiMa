"""drop_description_in_transactions_table

Revision ID: f5fd47d4bc69
Revises: e0b4df3ec714
Create Date: 2025-06-28 12:45:20.657162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5fd47d4bc69'
down_revision: Union[str, Sequence[str], None] = 'e0b4df3ec714'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def drop_description_from_transactions_table() -> None:
    """Drop description column from transactions table."""
    op.drop_column("transactions", "description")


def add_description_to_transactions_table() -> None:
    """Add description column to transactions table."""
    op.add_column(
        "transactions",
        sa.Column("description", sa.String(), nullable=True)
    )


def upgrade() -> None:
    """Upgrade schema."""
    drop_description_from_transactions_table()


def downgrade() -> None:
    """Downgrade schema."""
    add_description_to_transactions_table()
