"""fix_notification_enabled_default

Revision ID: 9ecadd71099d
Revises: 0a19600cfd38
Create Date: 2026-03-05 12:08:41.997388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ecadd71099d'
down_revision: Union[str, Sequence[str], None] = '0a19600cfd38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Set default value for notification_enabled."""
    # Update any NULL values to TRUE
    op.execute("UPDATE todos SET notification_enabled = 1 WHERE notification_enabled IS NULL")

    # Alter column to set default and NOT NULL
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('notification_enabled',
                              existing_type=sa.Boolean(),
                              nullable=False,
                              server_default='1')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('notification_enabled',
                              existing_type=sa.Boolean(),
                              nullable=True,
                              server_default=None)
