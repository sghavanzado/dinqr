"""
SIGA - Sistema Integral de Gestión de Accesos
Extensiones de Flask

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Inicialización de extensiones compartidas de Flask.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Importar Flask-Migrate

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Ruta para redirigir si el usuario no está autenticado
migrate = Migrate()  # Inicializar Flask-Migrate

# Flask-Login user_loader
from models.user import User

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None