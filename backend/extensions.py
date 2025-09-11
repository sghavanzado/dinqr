from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base de dados principal (SQL Server IAMC)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

# Base de datos IAMC (SQL Server) - conexión separada
iamc_engine = None
_IAMCSession = None

def init_iamc_db(app):
    """Inicializar conexão separada para IAMC"""
    global iamc_engine, _IAMCSession
    
    try:
        from config import Config
        iamc_engine = create_engine(
            Config.IAMC_SQLALCHEMY_DATABASE_URI,
            echo=app.config.get('SQLALCHEMY_ECHO', False),
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        _IAMCSession = sessionmaker(bind=iamc_engine)
        
        app.logger.info("IAMC SQL Server connection initialized successfully")
        return True
        
    except Exception as e:
        app.logger.error(f"ERROR: Failed to initialize IAMC connection: {str(e)}")
        return False

def IAMCSession():
    """Retorna uma nova sessão IAMC"""
    global iamc_engine, _IAMCSession
    
    if _IAMCSession:
        return _IAMCSession()
    else:
        # Fallback - inicializar se não foi inicializado
        from config import Config
        if not iamc_engine:
            iamc_engine = create_engine(
                Config.IAMC_SQLALCHEMY_DATABASE_URI,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            _IAMCSession = sessionmaker(bind=iamc_engine)
        return _IAMCSession()

def get_iamc_session():
    """Retorna uma nova sessão IAMC"""
    return IAMCSession()

# Flask-Login user_loader
@login_manager.user_loader
def load_user(user_id):
    try:
        from models.user import User
        return User.query.get(int(user_id))
    except Exception:
        return None