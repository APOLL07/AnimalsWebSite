"""add media_type to product_images

Revision ID: a1b2c3d4e5f6
Revises: 65423ff8c929
Create Date: 2026-03-18 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '65423ff8c929'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('product_images', sa.Column('media_type', sa.String(length=10), nullable=False, server_default='image'))


def downgrade() -> None:
    op.drop_column('product_images', 'media_type')
