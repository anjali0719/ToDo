"""Add created_at and updated_at to ToDo

Revision ID: 872248c97fe6
Revises: 
Create Date: 2024-12-21 21:49:24.265014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '872248c97fe6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('todo', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.add_column('todo', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True, onupdate=sa.func.now()))


def downgrade() -> None:
    op.drop_column('todo', 'created_at')
    op.drop_column('todo', 'updated_at')
