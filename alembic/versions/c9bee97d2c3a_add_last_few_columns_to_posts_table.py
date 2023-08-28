"""add last few columns to posts table

Revision ID: c9bee97d2c3a
Revises: 906a234c5dcd
Create Date: 2023-08-26 21:32:43.482457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9bee97d2c3a'
down_revision: Union[str, None] = '906a234c5dcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'),)
    )
    
    pass


def downgrade() -> None:
    op.drop_column(
        'posts', 'published'
    )
    op.drop_column(
        'posts', 'created_at'
    )
    pass
