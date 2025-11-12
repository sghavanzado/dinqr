"""
SIGA - Sistema Integral de Gestión de Accesos
Configuración del Sistema

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Archivo de configuración central para el backend Flask.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv
import pyodbc
import psycopg2

load_dotenv()  # Cargar variables de entorno desde .env

class Config:
    # Configuración básica del servidor
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    
    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgr3s@192.168.253.133:5432/localdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Base de datos remota (SQL Server)
    DB_CONFIG = {
        'server': os.environ.get('DB_SERVER', 'localhost'),
        'database': os.environ.get('DB_NAME', 'empresadb'),
        'username': os.environ.get('DB_USERNAME', 'sa'),
        'password': os.environ.get('DB_PASSWORD', 'Global2020')
    }
    
    # Base de datos local (PostgreSQL)
    LOCAL_DB_CONFIG = {
        'host': os.environ.get('LOCAL_DB_HOST', '192.168.253.133'),
        'port': os.environ.get('LOCAL_DB_PORT', '5432'),
        'database': os.environ.get('LOCAL_DB_NAME', 'localdb'),
        'user': os.environ.get('LOCAL_DB_USER', 'postgres'),
        'password': os.environ.get('LOCAL_DB_PASSWORD', 'postgr3s')
    }
    
    # Configuración CORS
    _CORS_ORIGINS_RAW = os.environ.get('CORS_ORIGINS', 'https://localhost,https://localhost:443,https://127.0.0.1,https://localhost:9000,https://127.0.0.1:9000,https://localhost:5137')
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
    
    # Configuración HTTPS
    ENABLE_HTTPS = os.environ.get('ENABLE_HTTPS', 'false').lower() == 'true'
    
    # Configuración de Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = 1024 * 1024 * 10  # 10 MB
    LOG_BACKUP_COUNT = 10
    
    # Configuración de Ratelimit (Sin Redis - Solo memoria)
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '500 per hour'
    
    # Configuración de Auditoría
    AUDIT_LOG_ENABLED = True
    AUDIT_LOG_FILE = 'logs/audit.log'
    
    # Configuración JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or os.urandom(32).hex()
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=45)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE', 'false').lower() == 'true'
    JWT_COOKIE_CSRF_PROTECT = False  # Disable for API usage
    JWT_COOKIE_SAMESITE = 'Lax'

    # Configuración específica para Windows Server
    WINDOWS_SERVICE_NAME = 'DINQRBackend'
    WINDOWS_SERVICE_DISPLAY_NAME = 'DINQR Backend Service'
    WINDOWS_SERVICE_DESCRIPTION = 'DINQR Flask Backend Service with Waitress'
    
    # Configuración de Waitress
    WAITRESS_HOST = os.environ.get('WAITRESS_HOST', '127.0.0.1')
    WAITRESS_PORT = int(os.environ.get('WAITRESS_PORT', 5000))
    WAITRESS_THREADS = int(os.environ.get('WAITRESS_THREADS', 4))
    WAITRESS_CONNECTION_LIMIT = int(os.environ.get('WAITRESS_CONNECTION_LIMIT', 100))
    WAITRESS_CLEANUP_INTERVAL = int(os.environ.get('WAITRESS_CLEANUP_INTERVAL', 30))
    WAITRESS_CHANNEL_TIMEOUT = int(os.environ.get('WAITRESS_CHANNEL_TIMEOUT', 120))

    @staticmethod
    def obtener_conexion_remota():
        """Establece una conexión con la base de datos SQL Server"""
        try:
            return pyodbc.connect(
                f"DRIVER={{SQL Server}};"
                f"SERVER={Config.DB_CONFIG['server']};"
                f"DATABASE={Config.DB_CONFIG['database']};"
                f"UID={Config.DB_CONFIG['username']};"
                f"PWD={Config.DB_CONFIG['password']};"
                f"TrustServerCertificate=yes;"
                f"Encrypt=yes"
            )
        except Exception as e:
            import logging
            logging.error(f"Error connecting to SQL Server: {str(e)}")
            raise

    @staticmethod
    def obtener_conexion_local():
        """Establece una conexión con la base de datos PostgreSQL local"""
        try:
            return psycopg2.connect(
                dbname=Config.LOCAL_DB_CONFIG['database'],
                user=Config.LOCAL_DB_CONFIG['user'],
                password=Config.LOCAL_DB_CONFIG['password'],
                host=Config.LOCAL_DB_CONFIG['host'],
                port=Config.LOCAL_DB_CONFIG['port']
            )
        except Exception as e:
            import logging
            logging.error(f"Error connecting to PostgreSQL: {str(e)}")
            raise

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    JWT_COOKIE_SECURE = True
    ENABLE_HTTPS = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 30,
        'echo': False
    }
    # Configuración optimizada para Windows Server
    WAITRESS_THREADS = 8
    WAITRESS_CONNECTION_LIMIT = 200

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    JWT_COOKIE_SECURE = False
    ENABLE_HTTPS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'max_overflow': 10,
        'echo': True
    }
    # Configuración para desarrollo
    WAITRESS_THREADS = 2
    WAITRESS_CONNECTION_LIMIT = 50

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    JWT_COOKIE_SECURE = False