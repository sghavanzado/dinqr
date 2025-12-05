"""
SIGA - Sistema Integral de Gestión de Accesos
Modelo de Cartón de Visita

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Modelo de datos para cartones de visita digitales.
"""

from extensions import db
from datetime import datetime


class BusinessCard(db.Model):
    """Modelo para almacenar cartones de visita generados"""
    __tablename__ = 'business_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    firma = db.Column(db.String(256), nullable=False)
    qr_code_path = db.Column(db.String(512), nullable=False)
    qr_code_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'contact_id': self.contact_id,
            'firma': self.firma,
            'qr_code_path': self.qr_code_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<BusinessCard {self.contact_id}>'
