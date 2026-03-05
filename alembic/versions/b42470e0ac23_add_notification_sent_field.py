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
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
