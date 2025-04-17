# app.py 
from flask import Flask, jsonify, request, g, make_response
from flask_cors import CORS
from extensions import db, migrate, login_manager
from flask_jwt_extended import JWTManager  
from config import Config
from models.user import User, Role, initialize_permissions
from cli import register_commands
from routes import auth_routes, user_routes, qr_routes
from routes.settings_routes import settings_bp  # Import the settings_routes blueprint
from routes.health_check import health_bp  # Importar la nueva ruta de salud
import logging
from logging.handlers import RotatingFileHandler
import os
import uuid
from flask_talisman import Talisman
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    # Inicializar Swagger para documentación
    Swagger(app)

    # Configurar Talisman para cabeceras de seguridad
    Talisman(
        app,
        content_security_policy=None,
        force_https=False,  # Deshabilitar HTTPS
        strict_transport_security=False,  # No habilitar HSTS
        frame_options='DENY'
    )

    # Configurar rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=Config.RATELIMIT_STORAGE_URL,
        default_limits=[Config.RATELIMIT_DEFAULT]
    )

    # Configurar extensiones
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}})


    # Configurar logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Inicio de la aplicación')

     # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt = JWTManager(app)  # Initialize JWTManager

    # Registrar comandos CLI
    register_commands(app)

    # Configuración inicial de permisos
    with app.app_context():
        try:
            initialize_permissions(app)
            app.logger.info("Permisos y roles inicializados correctamente")
        except Exception as e:
            app.logger.error(f"Error inicializando permisos: {str(e)}")
            raise

    # Configurar manejadores de errores JWT
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.warning(f'Intento de acceso con token inválido: {error}')
        return jsonify({
            'error': 'Token inválido',
            'message': 'La autenticación falló'
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.warning(f'Token expirado para el usuario: {jwt_payload["sub"]}')
        return jsonify({
            'error': 'Token expirado',
            'message': 'Renueve su token de acceso'
        }), 401

    # Middleware de seguridad global
    @app.after_request
    def security_middleware(response):
        """Middleware para agregar headers de seguridad a TODAS las respuestas"""
        # Headers de seguridad
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'self'"

        # Headers CORS (solo desarrollo)
        if app.config.get('ENV') == 'development':
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response.headers['Access-Control-Allow-Credentials'] = 'true'

        return response

    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            return response

    # Middleware para inicializar request_id
    @app.before_request
    def initialize_request_id():
        g.request_id = str(uuid.uuid4())

    # Registrar blueprints
    register_blueprints(app)

    # Manejador de errores global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Recurso no encontrado',
            'request_id': g.get('request_id', '')
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'error': 'Error interno del servidor',
            'request_id': g.get('request_id', '')
        }), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.error(f"Error inesperado: {str(error)}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
    return app


def register_blueprints(app):
    app.register_blueprint(auth_routes.auth_bp, url_prefix='/auth')
    app.register_blueprint(user_routes.user_bp, url_prefix='/users')
    app.register_blueprint(qr_routes.qr_bp, url_prefix='/qr')
    app.register_blueprint(settings_bp, url_prefix='/settings')  # Register settings_routes
    app.register_blueprint(health_bp)  # Registrar el blueprint de salud


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        ssl_context=None  # No usar SSL
    )