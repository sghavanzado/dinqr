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