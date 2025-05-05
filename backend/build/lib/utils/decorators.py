from functools import wraps
from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User

def require_permission(permission):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            g.current_user = User.query.get(current_user_id)  # Ensure g.current_user is set
            if not g.current_user or not g.current_user.has_permission(permission):
                return jsonify({'message': 'No tienes permiso para realizar esta acción'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator