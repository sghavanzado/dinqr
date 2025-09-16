# config.py

import os
from datetime import timedelta
from dotenv import load_dotenv
import pyodbc

load_dotenv()  # Cargar variables de entorno desde .env

class Config:
    # Configuración básica del servidor
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    
    # Configuración de SQLAlchemy - IAMC como BD principal (forzar MSSQL)
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://sa:Global2020@localhost/IAMC"
        f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Base de datos IAMC (SQL Server) - Configuración principal
    IAMC_DB_CONFIG = {
        'server': os.environ.get('IAMC_DB_SERVER', 'localhost'),
        'database': os.environ.get('IAMC_DB_NAME', 'IAMC'),
        'username': os.environ.get('IAMC_DB_USERNAME', 'sa'),
        'password': os.environ.get('IAMC_DB_PASSWORD', 'Global2020'),
        'driver': 'ODBC Driver 17 for SQL Server'
    }
    
    # SQLAlchemy URI para IAMC (MSSQL) - URI principal
    IAMC_SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{IAMC_DB_CONFIG['username']}:{IAMC_DB_CONFIG['password']}"
        f"@{IAMC_DB_CONFIG['server']}/{IAMC_DB_CONFIG['database']}"
        f"?driver={IAMC_DB_CONFIG['driver'].replace(' ', '+')}&TrustServerCertificate=yes"
    )
    
    # Configuración CORS - permitir tanto HTTP quanto HTTPS para desenvolvimento
    _CORS_ORIGINS_RAW = os.environ.get('CORS_ORIGINS', 'http://localhost,http://localhost:3000,http://localhost:5173,http://127.0.0.1,http://127.0.0.1:3000,http://127.0.0.1:5173,https://localhost,https://localhost:443,https://127.0.0.1,https://localhost:9000,https://127.0.0.1:9000')
    CORS_ORIGINS = [o.strip() for o in _CORS_ORIGINS_RAW.split(',') if o.strip()]
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = ['Content-Type', 'X-Total-Count', 'X-Requested-With', 'Authorization'] 
    
    # Configuración del servidor
    HOST = os.environ.get('HOST', '127.0.0.1')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    
    # Configuración de Seguridad de Sesiones
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Configuración de Token JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-key-only'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configuración del directorio de archivos estáticos y subidos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    @staticmethod
    def init_app(app):
        """Inicializar configuraciones específicas de la aplicación"""
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def obtener_conexion_iamc():
    """Establece una conexión con la base de datos IAMC (SQL Server)"""
    try:
        config = Config.IAMC_DB_CONFIG
        return pyodbc.connect(
            f"DRIVER={{{config['driver']}}};"
            f"SERVER={config['server']};"
            f"DATABASE={config['database']};"
            f"UID={config['username']};"
            f"PWD={config['password']};"
            f"TrustServerCertificate=yes",
            timeout=10
        )
    except Exception as e:
        import logging
        logging.error(f"Error connecting to IAMC database: {str(e)}")
        raise

def obtener_conexion_principal():
    """Alias para obtener_conexion_iamc - Conexión principal del sistema"""
    return obtener_conexion_iamc()

def get_database_connection():
    """Conexión genérica para compatibilidad con código legacy"""
    return obtener_conexion_iamc()
