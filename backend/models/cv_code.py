"""
SIGA - Sistema Integral de Gestión de Accesos
Modelo de Datos Cartón de Visita

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Modelo para almacenar información de cartones de visita generados.
             Estructura idéntica a qr_codes.
"""

from extensions import db

class CVCode(db.Model):
    __tablename__ = 'cv_codes'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    firma = db.Column(db.String(64), nullable=False)  # HMAC-SHA256
    archivo_qr = db.Column(db.String(255), nullable=False)
