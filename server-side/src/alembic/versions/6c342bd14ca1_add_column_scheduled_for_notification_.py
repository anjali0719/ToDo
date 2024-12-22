"""add column scheduled_for, notification_sent_at and auto_aupdated in todo table

Revision ID: 6c342bd14ca1
Revises: 872248c97fe6
Create Date: 2024-12-22 17:03:40.572685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6c342bd14ca1'
down_revision: Union[str, None] = '872248c97fe6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('todo', sa.Column('scheduled_for', sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP + interval '1 week')") ,nullable=False))
    op.add_column('todo', sa.Column('notification_sent_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('todo', sa.Column('auto_updated', sa.Boolean(), server_default=sa.text('false'), nullable=False))


def downgrade() -> None:
    op.drop_column('todo', 'scheduled_for')
    op.drop_column('todo', 'notification_sent_at')
    op.drop_column('todo', 'auto_updated')
