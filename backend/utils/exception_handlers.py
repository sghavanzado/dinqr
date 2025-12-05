"""
SIGA - Sistema Integral de Gestión de Accesos
Exception Handlers - Manejo Centralizado de Excepciones

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Excepciones personalizadas y manejo centralizado de errores.
"""

from flask import jsonify, g
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError
import logging

logger = logging.getLogger(__name__)


# ========== EXCEPCIONES PERSONALIZADAS ==========

class APIException(Exception):
    """Excepción base para la API"""
    status_code = 400
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        rv['request_id'] = g.get('request_id', '')
        return rv


class ResourceNotFoundError(APIException):
    """Recurso no encontrado"""
    status_code = 404
    
    def __init__(self, resource_type, resource_id):
        message = f"{resource_type} con ID {resource_id} no encontrado"
        super().__init__(message, status_code=404)


class AuthenticationError(APIException):
    """Error de autenticación"""
    status_code = 401
    
    def __init__(self, message="Autenticación requerida"):
        super().__init__(message, status_code=401)


class AuthorizationError(APIException):
    """Error de autorización / permisos"""
    status_code = 403
    
    def __init__(self, message="No tiene permisos para realizar esta acción"):
        super().__init__(message, status_code=403)


class ValidationError(APIException):
    """Error de validación de datos"""
    status_code = 400
    
    def __init__(self, message="Datos inválidos", errors=None):
        super().__init__(message, status_code=400, payload={'validation_errors': errors})


class DatabaseError(APIException):
    """Error de base de datos"""
    status_code = 500
    
    def __init__(self, message="Error de base de datos"):
        super().__init__(message, status_code=500)


class DuplicateResourceError(APIException):
    """Recurso duplicado"""
    status_code = 409
    
    def __init__(self, resource_type, field):
        message = f"{resource_type} con {field} ya existe"
        super().__init__(message, status_code=409)


class RateLimitExceededError(APIException):
    """Límite de tasa excedido"""
    status_code = 429
    
    def __init__(self, message="Demasiadas peticiones. Intente más tarde."):
        super().__init__(message, status_code=429)


class BusinessLogicError(APIException):
    """Error de lógica de negocio"""
    status_code = 422
    
    def __init__(self, message):
        super().__init__(message, status_code=422)


# ========== HANDLERS DE EXCEPCIONES ==========

def register_error_handlers(app):
    """
    Registra todos losmanejadores de errores en la aplicación Flask.
    
    Args:
        app: Instancia de Flask
    """
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        """Manejar excepciones personalizadas de la API"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logger.error(f"APIException: {error.message} | Status: {error.status_code} | Request ID: {g.get('request_id', 'N/A')}")
        return response
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Manejar 404 Not Found"""
        return jsonify({
            'error': 'Recurso no encontrado',
            'path': g.get('request_path', ''),
            'request_id': g.get('request_id', '')
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Manejar 405 Method Not Allowed"""
        return jsonify({
            'error': 'Método HTTP no permitido para este endpoint',
            'allowed_methods': error.valid_methods if hasattr(error, 'valid_methods') else [],
            'request_id': g.get('request_id', '')
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_server_error(error):
        """Manejar 500 Internal Server Error"""
        from extensions import db
        db.session.rollback()
        logger.error(f"Internal Server Error: {str(error)}", exc_info=True)
        return jsonify({
            'error': 'Error interno del servidor',
            'request_id': g.get('request_id', ''),
            'message': str(error) if app.debug else 'Ha ocurrido un error inesperado'
        }), 500
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        """Manejar errores de SQLAlchemy"""
        from extensions import db
        db.session.rollback()
        logger.error(f"SQLAlchemy Error: {str(error)}", exc_info=True)
        
        # No exponer detalles de BD en producción
        if app.debug:
            message = str(error)
        else:
            message = "Error de base de datos"
        
        return jsonify({
            'error': message,
            'request_id': g.get('request_id', '')
        }), 500
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        """Manejar errores de integridad de BD (duplicados, FK, etc)"""
        from extensions import db
        db.session.rollback()
        logger.warning(f"Integrity Error: {str(error)}")
        
        # Detectar tipo de error de integridad
        error_str = str(error).lower()
        if 'unique' in error_str or 'duplicate' in error_str:
            message = "El recurso ya existe (violación de unicidad)"
        elif 'foreign key' in error_str:
            message = "Violación de clave foránea"
        elif 'not null' in error_str:
            message = "Campo requerido faltante"
        else:
            message = "Error de integridad de datos"
        
        return jsonify({
            'error': message,
            'details': str(error) if app.debug else None,
            'request_id': g.get('request_id', '')
        }), 400
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Manejar errores de validación de Marshmallow"""
        logger.warning(f"Validation Error: {error.messages}")
        return jsonify({
            'error': 'Error de validación',
            'validation_errors': error.messages,
            'request_id': g.get('request_id', '')
        }), 400
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Manejar excepciones HTTP de Werkzeug"""
        response = jsonify({
            'error': error.description,
            'code': error.code,
            'request_id': g.get('request_id', '')
        })
        response.status_code = error.code
        return response
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Manejar errores inesperados"""
        from extensions import db
        db.session.rollback()
        logger.error(f"Unexpected Error: {str(error)}", exc_info=True)
        
        return jsonify({
            'error': 'Ha ocurrido un error inesperado',
            'details': str(error) if app.debug else None,
            'request_id': g.get('request_id', ''),
            'type': type(error).__name__
        }), 500
    
    logger.info("Error handlers registrados correctamente")


# ========== DECORADOR PARA LOGGING DE ERRORES ==========

from functools import wraps

def log_errors(f):
    """
    Decorador para logging automático de errores en endpoints.
    
    Uso:
        @app.route('/endpoint')
        @log_errors
        def my_endpoint():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error en {f.__name__}: {str(e)}",
                exc_info=True,
                extra={
                    'function': f.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'request_id': g.get('request_id', '')
                }
            )
            raise
    return decorated_function
