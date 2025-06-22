"""db_table_creation

Revision ID: e0b4df3ec714
Revises: 
Create Date: 2025-06-22 19:06:17.464495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0b4df3ec714'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_user_table():
    op.create_table(
        'users',
        sa.Column('user_id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('user_name', sa.String(255), nullable=False),
        sa.Column('user_email', sa.String(255), nullable=False, unique=True),
    )


def delete_user_table():
    op.drop_table('users')


def upgrade() -> None:
    """Upgrade schema."""
    create_user_table()


def downgrade() -> None:
    """Downgrade schema."""
    delete_user_table()
