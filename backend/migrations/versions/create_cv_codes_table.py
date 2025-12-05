"""create cv_codes table

Revision ID: create_cv_codes_table
Revises: 
Create Date: 2025-12-02

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_cv_codes_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'cv_codes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('contact_id', sa.String(length=50), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('firma', sa.String(length=64), nullable=False),
        sa.Column('archivo_qr', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('contact_id')
    )

def downgrade():
    op.drop_table('cv_codes')
