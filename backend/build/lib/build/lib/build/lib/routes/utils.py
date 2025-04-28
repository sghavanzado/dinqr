from functools import wraps
from flask import request, abort, current_app, jsonify
from flask_jwt_extended import create_access_token, decode_token
from flask_login import current_user

def require_permission(permission_name):
    """Decorador para verificar si el usuario tiene un permiso específico."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(permission_name):
                return jsonify({'error': 'No tienes permiso para realizar esta acción'}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

def generate_auth_token(user_id):
    """Genera un token de autenticación JWT."""
    return create_access_token(identity=user_id)

def decode_auth_token(token):
    """Decodifica un token JWT."""
    try:
        payload = decode_token(token)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        abort(401, description="Token expirado")
    except jwt.InvalidTokenError:
        abort(401, description="Token inválido")