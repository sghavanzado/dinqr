from flask import Flask, jsonify, request, g, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
import logging, os, uuid
from logging.handlers import RotatingFileHandler
import sys 
from extensions import db, migrate, login_manager
from config import Config
from cli import register_commands
from models.user import initialize_permissions
from routes import auth_routes, user_routes, qr_routes
from routes.settings_routes import settings_bp
from routes.health_check import health_bp
from server_manager import iniciar_servidor, detener_servidor, logger
import redis  # Import Redis
import signal  # Import signal to handle termination signals

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    Swagger(app)

 
    # Conexión a Redis
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()  # Verificar conexión a Redis
        app.logger.info("Conexión a Redis establecida correctamente.")
    except redis.ConnectionError as e:
        app.logger.error(f"Error al conectar con Redis: {str(e)}")
        r = None  # Establecer Redis como None si no está disponible

    # Rate limit
    limiter = Limiter(
        get_remote_address,
        storage_uri="redis://localhost:6379" if r else "memory://",  # Usar memoria si Redis no está disponible
        app=app,
    )


    # CORS
    CORS(app,
         resources={r"/*": {"origins": Config.CORS_ORIGINS}},  # Permitir peticiones desde las IPs especificadas en Config.CORS_ORIGINS
         supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS,
         expose_headers=Config.CORS_EXPOSE_HEADERS)

    # Loggin
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # Añade un StreamHandler para enviar logs a stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App iniciada')

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt = JWTManager(app)

    register_commands(app)

    # Permisos iniciales
    with app.app_context():
        try:
            initialize_permissions(app)
            app.logger.info("Permisos inicializados correctamente")
        except Exception as e:
            app.logger.error(f"Error inicializando permisos: {str(e)}")
            raise

    # Error tokens
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Token inválido'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expirado'}), 401

    # Middleware general
    @app.before_request
    def before_all():
        g.request_id = str(uuid.uuid4())
        if request.method == "OPTIONS":
            origin = request.headers.get("Origin")
            if origin in Config.CORS_ORIGINS:
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
        if origin is not None and origin in Config.CORS_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

    # Blueprints
    app.register_blueprint(auth_routes.auth_bp, url_prefix='/auth')
    app.register_blueprint(user_routes.user_bp, url_prefix='/users')
    app.register_blueprint(qr_routes.qr_bp, url_prefix='/qr')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(health_bp)

    # Errores globales
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'No encontrado', 'request_id': g.get('request_id', '')}), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return jsonify({'error': 'Error interno', 'request_id': g.get('request_id', '')}), 500

    @app.errorhandler(Exception)
    def unhandled(e):
        app.logger.error(f"Excepción no controlada: {str(e)}")
        return jsonify({'error': 'Error desconocido'}), 500

    return app

def handle_exit_signal(signum, frame):
    """Handle termination signals to stop the server gracefully."""
    logger.info("Signal received, stopping the server...")
    detener_servidor()
    logger.info("Application terminated.")
    exit(0)

if __name__ == '__main__':
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_exit_signal)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit_signal)  # Handle termination signals

    app = create_app()
    logger.info("Use Gunicorn to run this application in production.")
    logger.info("Example: gunicorn -w 4 -b 0.0.0.0:5000 server:app")

    # Start the server in server_manager
    try:
        logger.info("Starting the server using server_manager...")
        iniciar_servidor()
    except Exception as e:
        logger.error(f"Failed to start the server: {str(e)}")
        exit(1)

    # Run the Flask application
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG, ssl_context=None)  # Escuchar en todas las IPs