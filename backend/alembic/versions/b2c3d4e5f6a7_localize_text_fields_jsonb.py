"""localize text fields to JSONB

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-03-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Products: name, description
    op.execute(
        "ALTER TABLE products ALTER COLUMN name TYPE jsonb "
        "USING jsonb_build_object('uk', name, 'ru', name)"
    )
    op.execute(
        "ALTER TABLE products ALTER COLUMN description TYPE jsonb "
        "USING jsonb_build_object('uk', description, 'ru', description)"
    )

    # Product attributes: key, value
    op.drop_index('ix_product_attributes_key_value', table_name='product_attributes')
    op.execute(
        "ALTER TABLE product_attributes ALTER COLUMN key TYPE jsonb "
        "USING jsonb_build_object('uk', key, 'ru', key)"
    )
    op.execute(
        "ALTER TABLE product_attributes ALTER COLUMN value TYPE jsonb "
        "USING jsonb_build_object('uk', value, 'ru', value)"
    )

    # Animals: name
    op.execute(
        "ALTER TABLE animals ALTER COLUMN name TYPE jsonb "
        "USING jsonb_build_object('uk', name, 'ru', name)"
    )

    # Categories: name
    op.execute(
        "ALTER TABLE categories ALTER COLUMN name TYPE jsonb "
        "USING jsonb_build_object('uk', name, 'ru', name)"
    )


def downgrade() -> None:
    # Revert to string columns, extracting 'ru' key
    op.execute(
        "ALTER TABLE products ALTER COLUMN name TYPE varchar(255) "
        "USING name->>'ru'"
    )
    op.execute(
        "ALTER TABLE products ALTER COLUMN description TYPE text "
        "USING description->>'ru'"
    )

    op.execute(
        "ALTER TABLE product_attributes ALTER COLUMN key TYPE varchar(100) "
        "USING key->>'ru'"
    )
    op.execute(
        "ALTER TABLE product_attributes ALTER COLUMN value TYPE varchar(255) "
        "USING value->>'ru'"
    )
    op.create_index(
        'ix_product_attributes_key_value',
        'product_attributes',
        ['key', 'value'],
    )

    op.execute(
        "ALTER TABLE animals ALTER COLUMN name TYPE varchar(100) "
        "USING name->>'ru'"
    )

    op.execute(
        "ALTER TABLE categories ALTER COLUMN name TYPE varchar(100) "
        "USING name->>'ru'"
    )
