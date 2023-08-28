"""add content column to posts table

Revision ID: acfe93a328eb
Revises: 77d24725a502
Create Date: 2023-08-26 20:29:47.095276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acfe93a328eb'
down_revision: Union[str, None] = '77d24725a502'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column(
        'posts',
        'content'
    )
    pass
