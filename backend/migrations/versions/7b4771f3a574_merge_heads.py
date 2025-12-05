"""merge heads

Revision ID: 7b4771f3a574
Revises: 6befd028b37e, create_cv_codes_table
Create Date: 2025-12-02 11:01:51.128790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b4771f3a574'
down_revision = ('6befd028b37e', 'create_cv_codes_table')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
