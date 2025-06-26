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


def create_goals_table():
    op.create_table(
        'goals',
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('goal_id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('goal_name', sa.String(255), nullable=False),
        sa.Column('goal_description', sa.String(255)),
        sa.Column('goal_target_amount', sa.Integer, nullable=False),
        sa.Column('goal_current_amount', sa.Integer, nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'])
    )


def delete_goals_table():
    op.drop_table('goals')


def create_category_table():
    op.create_table(
        'category',
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('category_id', sa.String(36), primary_key=True),
        sa.Column('type_id', sa.String(36), nullable=False),
        sa.Column('category_name', sa.String(255), nullable=False),
        sa.Column('category_description', sa.String(255)),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id']),
        sa.ForeignKeyConstraint(['type_id'], ['transaction_types.type_id'])
    )


def delete_category_table():
    op.drop_table('category')


def create_transaction_types_table():
    op.create_table(
        'transaction_types',
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('type_id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('type_name', sa.String(255), nullable=False),
        sa.Column('type_description', sa.String(255)),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'])
    )


def delete_transaction_types_table():
    op.drop_table('transaction_types')


def create_budget_table():
    op.create_table(
        'budget',
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('budget_id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('budget_name', sa.String(255), nullable=False),
        sa.Column('budget_description', sa.String(255)),
        sa.Column('budget_target_amount', sa.Integer, nullable=False),
        sa.Column('budget_current_amount', sa.Integer, server_default='0'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'])
    )


def delete_budget_table():  
    op.drop_table('budget')


def create_transactions_table():
    op.create_table(
        'transactions',
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('transaction_id', sa.String(36), primary_key=True, nullable=False),
        sa.Column('category_id', sa.String(36), nullable=False),
        sa.Column('type_id', sa.String(36), nullable=False),
        sa.Column('transaction_name', sa.String(255), nullable=False),
        sa.Column('transaction_description', sa.String(255)),
        sa.Column('transaction_amount', sa.Integer, nullable=False),
        sa.Column('transaction_date', sa.String(50), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id']),
        sa.ForeignKeyConstraint(['category_id'], ['category.category_id']),
        sa.ForeignKeyConstraint(['type_id'], ['transaction_types.type_id'])
    )


def delete_transactions_table():
    op.drop_table('transactions')


def upgrade() -> None:
    """Upgrade schema."""
    create_user_table()
    create_goals_table()
    create_transaction_types_table()
    create_category_table()
    create_budget_table()
    create_transactions_table()


def downgrade() -> None:
    """Downgrade schema."""
    delete_transactions_table()
    delete_budget_table()
    delete_transaction_types_table()
    delete_category_table()
    delete_goals_table()
    delete_user_table()
