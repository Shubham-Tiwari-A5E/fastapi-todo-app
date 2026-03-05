"""add notification_sent field

Revision ID: b42470e0ac23
Revises: 9ecadd71099d
Create Date: 2026-03-05 14:33:48.763709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b42470e0ac23'
down_revision: Union[str, Sequence[str], None] = '9ecadd71099d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add notification_sent column with default False
    # Use sa.false() for compatibility with both MySQL and PostgreSQL
    op.add_column('todos', sa.Column('notification_sent', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove notification_sent column
    op.drop_column('todos', 'notification_sent')
