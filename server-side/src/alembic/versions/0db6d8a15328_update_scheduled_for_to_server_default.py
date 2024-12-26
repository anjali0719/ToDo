"""update scheduled_for to server_default

Revision ID: 0db6d8a15328
Revises: 6c342bd14ca1
Create Date: 2024-12-24 00:06:12.113031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0db6d8a15328'
down_revision: Union[str, None] = '6c342bd14ca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'todo',
        'scheduled_for',
        server_default=sa.text("(CURRENT_TIMESTAMP + interval '1 week')"),
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )


def downgrade() -> None:
    pass
