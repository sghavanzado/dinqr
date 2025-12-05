"""
SIGA - Sistema Integral de Gestión de Accesos
Migración: Crear tabla para Cartones de Visita

Desarrollado por: Ing. Maikel Cuao
Fecha: 2025
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers
revision = 'create_business_cards_table'
down_revision = None  # Actualizar con la última migración
branch_labels = None
depends_on = None


def upgrade():
    """Crear tabla business_cards para cartones de visita"""
    op.create_table(
        'business_cards',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('contact_id', sa.String(20), nullable=False, unique=True, index=True),
        sa.Column('firma', sa.String(256), nullable=False),
        sa.Column('qr_code_path', sa.String(512), nullable=False),
        sa.Column('qr_code_data', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
    )
    
    # Índices adicionales
    op.create_index('idx_business_cards_contact_id', 'business_cards', ['contact_id'])
    op.create_index('idx_business_cards_active', 'business_cards', ['is_active'])


def downgrade():
    """Eliminar tabla business_cards"""
    op.drop_index('idx_business_cards_active', table_name='business_cards')
    op.drop_index('idx_business_cards_contact_id', table_name='business_cards')
    op.drop_table('business_cards')
