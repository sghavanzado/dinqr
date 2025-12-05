"""Merge migrations

Revision ID: 6befd028b37e
Revises: 17a0055a5687, create_business_cards_table
Create Date: 2025-12-01 22:51:38.673389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6befd028b37e'
down_revision = ('17a0055a5687', 'create_business_cards_table')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
