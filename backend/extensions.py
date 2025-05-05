from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Importar Flask-Migrate

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Ruta para redirigir si el usuario no está autenticado
migrate = Migrate()  # Inicializar Flask-Migrate