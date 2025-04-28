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

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    Swagger(app)

    # Seguridad HTTP
    Talisman(
        app,
        content_security_policy=None,
        force_https=False,
        strict_transport_security=False,
        frame_options='DENY'
    )

    # Rate limit
    limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri=Config.RATELIMIT_STORAGE_URL,
    default_limits=[Config.RATELIMIT_DEFAULT]
)


    # CORS
    CORS(app,
         resources={r"/*": {"origins": Config.CORS_ORIGINS}},
         supports_credentials=Config.CORS_SUPPORTS_CREDENTIALS,
         expose_headers=Config.CORS_EXPOSE_HEADERS)

    # Logging
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

if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, ssl_context=None)
