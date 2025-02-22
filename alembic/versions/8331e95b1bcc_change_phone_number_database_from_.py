"""Change phone number database from interger to string

Revision ID: 8331e95b1bcc
Revises: 10274f1af1a9
Create Date: 2025-01-10 11:36:43.401460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8331e95b1bcc'
down_revision: Union[str, None] = '10274f1af1a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'Phone_number',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=10),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'Phone_number',
               existing_type=sa.String(length=10),
               type_=mysql.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
