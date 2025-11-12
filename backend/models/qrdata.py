"""
SIGA - Sistema Integral de Gestión de Accesos
Modelo de Datos QR

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Modelo para almacenar información de códigos QR generados.
"""

from extensions import db

class QRCode(db.Model):
    __tablename__ = 'qr_codes'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    firma = db.Column(db.String(64), nullable=False)  # HMAC-SHA256
    archivo_qr = db.Column(db.String(255), nullable=False)
