"""fix publishedrides mapping

Revision ID: f546c4599b78
Revises: 1769e29b9e93
Create Date: 2025-01-15 14:53:39.687065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f546c4599b78'
down_revision: Union[str, None] = '1769e29b9e93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('RequestRide',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('UserID', sa.Integer(), nullable=True),
    sa.Column('RideID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['RideID'], ['publishedrides.id'], ),
    sa.ForeignKeyConstraint(['UserID'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('requestride')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requestride',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('UserID', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('RideID', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['RideID'], ['publishedrides.id'], name='requestride_ibfk_2'),
    sa.ForeignKeyConstraint(['UserID'], ['users.id'], name='requestride_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('RequestRide')
    # ### end Alembic commands ###
