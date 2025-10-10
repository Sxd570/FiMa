"""chat_table_creation

Revision ID: dafb06a9c48e
Revises: a249f5e81f4b
Create Date: 2025-10-10 22:26:50.348418

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'dafb06a9c48e'
down_revision: Union[str, Sequence[str], None] = 'a249f5e81f4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_conversation_table():
    op.execute('''
    CREATE TABLE `conversation` (
        `conversation_id` VARCHAR(36) NOT NULL PRIMARY KEY,
        `user_id` VARCHAR(36) NOT NULL,
        `title` VARCHAR(255) DEFAULT NULL,
        `status` VARCHAR(50) DEFAULT 'active',
        `total_token_used` INT DEFAULT 0,
        `last_message_at` DATETIME DEFAULT NULL,
        `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE,
        INDEX `idx_user_id` (`user_id`),
        INDEX `idx_last_message_at` (`last_message_at`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ''')


def drop_conversation_table():
    op.execute('''
    DROP TABLE IF EXISTS `conversation`;
    ''')


def upgrade() -> None:
    """Upgrade schema."""
    create_conversation_table()


def downgrade() -> None:
    """Downgrade schema."""
    drop_conversation_table()
