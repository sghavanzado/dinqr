"""
SIGA - Sistema Integral de Gestión de Accesos
Decoradores RBAC (Role-Based Access Control)

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Decoradores para control de acceso basado en roles y permisos.
"""

from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.user import User

def require_permission(*permissions):
    """
    Decorador para requerir uno o más permisos específicos.
    
    Uso:
        @app.route('/admin/users')
        @require_permission('admin_access', 'create_user')
        def create_user():
            ...
    
    Args:
        *permissions: Nombres de los permisos requeridos (OR)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar JWT
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({'error': 'Token inválido o expirado', 'details': str(e)}), 401
            
            # Obtener usuario actual
            current_user_id = get_jwt_identity()
            try:
                user = User.query.get(int(current_user_id))
            except ValueError:
                return jsonify({'error': 'ID de usuario inválido'}), 400
            
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            if not user.is_active:
                return jsonify({'error': 'Usuario inactivo'}), 403
            
            # Verificar permisos (al menos uno debe coincidir)
            user_permissions = user.get_permissions()
            has_permission = any(perm in user_permissions for perm in permissions)
            
            if not has_permission:
                return jsonify({
                    'error': 'Permiso denegado',
                    'required_permissions': list(permissions),
                    'user_permissions': user_permissions
                }), 403
            
            # Almacenar usuario en contexto de request para uso posterior
            g.current_user = user
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_all_permissions(*permissions):
    """
    Decorador para requerir TODOS los permisos listados (AND).
    
    Uso:
        @app.route('/admin/critical')
        @require_all_permissions('admin_access', 'delete_user')
        def critical_action():
            ...
    
    Args:
        *permissions: Nombres de los permisos requeridos (todos)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar JWT
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({'error': 'Token inválido o expirado', 'details': str(e)}), 401
            
            # Obtener usuario actual
            current_user_id = get_jwt_identity()
            try:
                user = User.query.get(int(current_user_id))
            except ValueError:
                return jsonify({'error': 'ID de usuario inválido'}), 400
            
            if not user or not user.is_active:
                return jsonify({'error': 'Usuario no autorizado'}), 403
            
            # Verificar que tenga TODOS los permisos
            user_permissions = user.get_permissions()
            missing_permissions = [p for p in permissions if p not in user_permissions]
            
            if missing_permissions:
                return jsonify({
                    'error': 'Permisos insuficientes',
                    'missing_permissions': missing_permissions,
                    'required_permissions': list(permissions)
                }), 403
            
            # Almacenar usuario en contexto
            g.current_user = user
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_role(*roles):
    """
    Decorador para requerir uno o más roles específicos.
    
    Uso:
        @app.route('/admin/panel')
        @require_role('admin', 'superadmin')
        def admin_panel():
            ...
    
    Args:
        *roles: Nombres de los roles aceptados
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar JWT
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({'error': 'Token inválido o expirado', 'details': str(e)}), 401
            
            # Obtener usuario actual
            current_user_id = get_jwt_identity()
            try:
                user = User.query.get(int(current_user_id))
            except ValueError:
                return jsonify({'error': 'ID de usuario inválido'}), 400
            
            if not user or not user.is_active:
                return jsonify({'error': 'Usuario no autorizado'}), 403
            
            # Verificar rol
            if user.role.name not in roles:
                return jsonify({
                    'error': 'Rol insuficiente',
                    'user_role': user.role.name,
                    'required_roles': list(roles)
                }), 403
            
            # Almacenar usuario en contexto
            g.current_user = user
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorador simple para requerir rol de administrador.
    
    Uso:
        @app.route('/admin/secret')
        @admin_required
        def secret_function():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar JWT
        try:
            verify_jwt_extended()
        except Exception as e:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        # Obtener usuario actual
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))
        
        if not user or not user.is_active:
            return jsonify({'error': 'Usuario no autorizado'}), 403
        
        if not user.is_admin():
            return jsonify({'error': 'Se requiere acceso de administrador'}), 403
        
        # Almacenar usuario en contexto
        g.current_user = user
        
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """
    Función helper para obtener el usuario actual desde el contexto.
    
    Returns:
        User: Usuario actual o None
    """
    return g.get('current_user', None)
