# config.py

import os
from datetime import timedelta
from dotenv import load_dotenv
import pyodbc
import psycopg2

load_dotenv()  # Cargar variables de entorno desde .env

class Config:

    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Configuración CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS')
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = ['Content-Type', 'X-Total-Count', 'X-Requested-With', 'Authorization'] 
    
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'
    
    # Configuración de Seguridad de Sesiones
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    
    # Configuración HTTPS
    ENABLE_HTTPS = False  # Deshabilitar HTTPS
    
    # Configuración de Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = 1024 * 1024 * 10  # 10 MB
    LOG_BACKUP_COUNT = 10
    
    # Configuración de Ratelimit
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '500 per hour'
    
    # Configuración de Auditoría
    AUDIT_LOG_ENABLED = True
    AUDIT_LOG_FILE = 'logs/audit.log'
    
    # Configuración JWT
    JWT_SECRET_KEY = os.urandom(32).hex()  # Generate a new random JWT_SECRET_KEY
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=45)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SAMESITE = 'Lax'  # Asegúrate de que sea compatible con tu flujo

    @staticmethod
    def obtener_conexion_remota():
        """Establece una conexión con la base de datos SQL Server"""
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={Config.DB_CONFIG['server']};"
            f"DATABASE={Config.DB_CONFIG['database']};"
            f"UID={Config.DB_CONFIG['username']};"
            f"PWD={Config.DB_CONFIG['password']};"
            f"TrustServerCertificate=yes"
        )

    @staticmethod
    def obtener_conexion_local():
        """Establece una conexión con la base de datos PostgreSQL local"""
        return psycopg2.connect(
            dbname=Config.LOCAL_DB_CONFIG['database'],
            user=Config.LOCAL_DB_CONFIG['user'],
            password=Config.LOCAL_DB_CONFIG['password'],
            host=Config.LOCAL_DB_CONFIG['host'],
            port=Config.LOCAL_DB_CONFIG['port']
        )

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 30
    }
    ENABLE_HTTPS = True

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'max_overflow': 10
    }

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False