"""
SIGA - Sistema Integral de Gestión de Accesos
Backend Principal - Flask Application

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Aplicación Flask principal que gestiona la API REST y autenticación.
"""

from flask import Flask, jsonify, request, g, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
import logging, os, uuid, sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from extensions import db, migrate, login_manager
from config import Config
from cli import register_commands
from models.user import initialize_permissions
from models.cv_code import CVCode  # Importar modelo para Flask-Migrate
from routes import auth_routes, user_routes, qr_routes
from routes.settings_routes import settings_bp
from routes.health_check import health_bp

def create_app(config_class=None):
    """Application factory pattern for creating Flask app"""
    app = Flask(__name__, static_folder='static')
    # Importar y registrar blueprint de contacto/qrdata
    from routes.route_qrdata import qrdata_bp
    app.register_blueprint(qrdata_bp)
    
    # Use provided config or default
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object(Config)
    
    # Ensure required directories exist
    ensure_directories(app)
    
    # Configure Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    Swagger(app, config=swagger_config)

    # Configure Rate Limiting (Memory only - No Redis)
    limiter = Limiter(
        get_remote_address,
        storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://'),
        app=app,
        default_limits=[app.config.get('RATELIMIT_DEFAULT', '500 per hour')]
    )

    # Configure CORS
    cors_origins = app.config.get('CORS_ORIGINS', [])
    if not cors_origins:
        cors_origins = ['*']  # Permitir todos los orígenes si la lista está vacía (solo desarrollo)
        app.logger.warning('CORS_ORIGINS está vacío, permitiendo todos los orígenes (solo desarrollo)')
    else:
        app.logger.info(f'Orígenes CORS permitidos: {cors_origins}')
    CORS(app,
         resources={r"/*": {"origins": cors_origins}},
         supports_credentials=app.config.get('CORS_SUPPORTS_CREDENTIALS', True),
         expose_headers=app.config.get('CORS_EXPOSE_HEADERS', []))

    # Configure Security Headers (disable HTTPS enforcement for IIS proxy)
    talisman = Talisman(
        app,
        force_https=False,  # IIS will handle HTTPS termination
        strict_transport_security=False,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline'",
            'style-src': "'self' 'unsafe-inline'",
            'img-src': "'self' data:",
        }
    )
    # Setup logging
    setup_logging(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt = JWTManager(app)

    # Register CLI commands
    register_commands(app)

    # Initialize permissions
    with app.app_context():
        try:
            initialize_permissions(app)
            app.logger.info("Permissions initialized successfully")
        except Exception as e:
            app.logger.error(f"Error initializing permissions: {str(e)}")
            # Don't raise in production to allow service to start

    # Configure JWT error handlers
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expired'}), 401

    # Request middleware
    @app.before_request
    def before_all():
        g.request_id = str(uuid.uuid4())
        # Log de todas las peticiones entrantes
        try:
            app.logger.info(f"Petición: {request.method} {request.path} desde {request.remote_addr} - args: {dict(request.args)} - json: {request.get_json(silent=True)}")
        except Exception as e:
            app.logger.warning(f"No se pudo registrar el cuerpo JSON de la petición: {e}")

        # Handle CORS preflight requests
        if request.method == "OPTIONS":
            origin = request.headers.get("Origin")
            if origin and origin in app.config.get('CORS_ORIGINS', []):
                resp = make_response()
                resp.headers["Access-Control-Allow-Origin"] = origin
                resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
                resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                resp.headers["Access-Control-Allow-Credentials"] = "true"
                return resp
            return jsonify({"error": "Origin not allowed"}), 403

    @app.after_request
    def after_all(response):
        origin = request.headers.get("Origin")
        if origin and origin in app.config.get('CORS_ORIGINS', []):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        
        # Security headers for Windows Server
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

    # Register blueprints
    app.register_blueprint(auth_routes.auth_bp, url_prefix='/auth')
    app.register_blueprint(user_routes.user_bp, url_prefix='/users')
    app.register_blueprint(qr_routes.qr_bp, url_prefix='/qr')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    from routes.cv_routes import cv_bp
    app.register_blueprint(cv_bp, url_prefix='/cv')

    app.register_blueprint(health_bp)

    # Global error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'error': 'Resource not found', 
            'request_id': g.get('request_id', ''),
            'path': request.path
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        app.logger.error(f"Internal server error: {str(e)}")
        return jsonify({
            'error': 'Internal server error', 
            'request_id': g.get('request_id', '')
        }), 500

    @app.errorhandler(Exception)
    def unhandled(e):
        app.logger.error(f"Unhandled exception: {str(e)}")
        db.session.rollback()
        return jsonify({
            'error': 'An unexpected error occurred',
            'request_id': g.get('request_id', '')
        }), 500

    return app

def ensure_directories(app):
    """Ensure required directories exist"""
    directories = [
        Path('logs'),
        Path('static'),
        Path('uploads'),
        Path(app.config.get('LOG_FILE', 'logs/app.log')).parent
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def setup_logging(app):
    """Setup comprehensive logging for production"""
    if not app.debug and not app.testing:
        # Ensure logs directory exists
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        # Main application log
        log_file = app.config.get('LOG_FILE', 'logs/app.log')
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=app.config.get('LOG_MAX_BYTES', 10240000),
            backupCount=app.config.get('LOG_BACKUP_COUNT', 10),
            encoding='utf-8'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper()))
        
        # Console handler for Windows Service debugging
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        
        # Add handlers to app logger
        app.logger.addHandler(file_handler)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper()))
        
        # Log startup information
        app.logger.info('=' * 50)
        app.logger.info('DINQR Backend Application Starting')
        app.logger.info('=' * 50)
        app.logger.info(f'Environment: {app.config.get("FLASK_ENV", "unknown")}')
        app.logger.info(f'Debug mode: {app.debug}')
        app.logger.info(f'Database URI: {app.config.get("SQLALCHEMY_DATABASE_URI", "").split("@")[-1] if "@" in app.config.get("SQLALCHEMY_DATABASE_URI", "") else "Not configured"}')

# Application instance for WSGI servers
application = create_app()

# Lista todas las rutas registradas para depuración
print("=== RUTAS REGISTRADAS ===")
for rule in application.url_map.iter_rules():
    print(f"[ROUTE] {rule}")
print("=========================")

if __name__ == '__main__':
    # This section is only for development/testing
    # Production deployment should use waitress_server.py or windows_service.py
    
    app = create_app()
    
    # Development server warning
    app.logger.warning("=" * 60)
    app.logger.warning("WARNING: Running development server")
    app.logger.warning("For production use:")
    app.logger.warning("  python waitress_server.py")
    app.logger.warning("  python windows_service.py install")
    app.logger.warning("=" * 60)
    
    # Run development server
    app.run(
        host=app.config.get('HOST', '127.0.0.1'), 
        port=app.config.get('PORT', 5000), 
        debug=app.config.get('DEBUG', False)
    )