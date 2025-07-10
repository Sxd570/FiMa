"""create_tables

Revision ID: a249f5e81f4b
Revises: 
Create Date: 2025-07-03 13:29:04.090760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a249f5e81f4b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_user_table():
    op.execute('''
    CREATE TABLE `user` (
        `user_id` VARCHAR(36) PRIMARY KEY NOT NULL,
        `user_name` VARCHAR(255) NOT NULL,
        `user_email` VARCHAR(255) NOT NULL UNIQUE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')


def drop_user_table():
    op.execute('DROP TABLE IF EXISTS `user`;')


def create_category_table():
    op.execute('''
    CREATE TABLE `category` (
        `user_id` VARCHAR(36) NOT NULL,
        `transaction_type` VARCHAR(36) NOT NULL,
        `category_id` VARCHAR(36) PRIMARY KEY,
        `category_name` VARCHAR(255) NOT NULL,
        `category_description` VARCHAR(255),
        FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')


def drop_category_table():
    op.execute('DROP TABLE IF EXISTS `category`;')


def create_budget_table():
    op.execute('''
    CREATE TABLE `budget` (
        `user_id` VARCHAR(36) NOT NULL,
        `category_id` VARCHAR(36) NOT NULL,
        `budget_id` VARCHAR(36) PRIMARY KEY NOT NULL,
        `budget_allocated_amount` INT NOT NULL,
        `budget_spent_amount` INT NOT NULL,
        `budget_allocated_month` VARCHAR(7) NOT NULL,
        `is_budget_limit_reached` TINYINT(1) NOT NULL DEFAULT 0,
        `is_budget_over_limit` TINYINT(1) NOT NULL DEFAULT 0,
        FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
        FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')


def drop_budget_table():
    op.execute('DROP TABLE IF EXISTS `budget`;')


def create_goals_table():
    op.execute('''
    CREATE TABLE `goals` (
        `user_id` VARCHAR(36) NOT NULL,
        `goal_id` VARCHAR(36) PRIMARY KEY NOT NULL,
        `goal_name` VARCHAR(255) NOT NULL,
        `goal_description` VARCHAR(255),
        `goal_target_amount` INT NOT NULL,
        `goal_current_amount` INT NOT NULL DEFAULT 0,
        `is_goal_reached` TINYINT(1) NOT NULL DEFAULT 0,
        FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')


def drop_goals_table():
    op.execute('DROP TABLE IF EXISTS `goals`;')


def create_transaction_table():
    op.execute('''
    CREATE TABLE `transaction` (
        `transaction_id` VARCHAR(36) PRIMARY NOT NULL,
        `user_id` VARCHAR(36) NOT NULL,
        `category_id` VARCHAR(36) NOT NULL,
        `transaction_type` VARCHAR(36) NOT NULL,
        `transaction_info` VARCHAR(255) NOT NULL,
        `transaction_amount` INT NOT NULL,
        `transaction_date` VARCHAR(50) NOT NULL,
        FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
        FOREIGN KEY (`category_id`) REFERENCES `category`(`category_id`),
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')


def drop_transaction_table():
    op.execute('DROP TABLE IF EXISTS `transaction`;')


def upgrade() -> None:
    """Upgrade schema."""
    create_user_table()
    create_category_table()
    create_budget_table()
    create_goals_table()
    create_transaction_table()


def downgrade() -> None:
    """Downgrade schema."""
    drop_transaction_table()
    drop_goals_table()
    drop_budget_table()
    drop_category_table()
    drop_user_table()
