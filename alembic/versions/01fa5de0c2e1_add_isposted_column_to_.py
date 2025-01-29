"""add isposted column to userextrainformation

Revision ID: 01fa5de0c2e1
Revises: 214edd0600c6
Create Date: 2025-01-28 16:15:34.774746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01fa5de0c2e1'
down_revision: Union[str, None] = '214edd0600c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
