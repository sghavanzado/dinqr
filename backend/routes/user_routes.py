from flask import Blueprint, jsonify, request, g
from extensions import db
from models.user import User, Role, Permission
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import require_permission  # Importar el decorador global

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obtiene el perfil del usuario actual."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    g.current_user = user  # Set g.current_user
    return jsonify(user.to_dict()), 200

@user_bp.route('/', methods=['GET'])
@jwt_required()
@require_permission('view_users')
def get_users():
    """Obtiene una lista paginada de usuarios."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    users = User.query.paginate(page=page, per_page=per_page)
    return jsonify({
        'users': [user.to_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    }), 200

@user_bp.route('/', methods=['POST'])
@jwt_required()
@require_permission('create_user')
def create_user():
    """Crea un nuevo usuario."""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400

    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    if not email or not password or not role_id:
        return jsonify({'message': 'Email, password y role_id son requeridos'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email ya registrado'}), 400

    role = Role.query.get(role_id)
    if not role:
        return jsonify({'message': 'Rol no encontrado'}), 400

    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado'}), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_permission('update_user')
def update_user(user_id):
    """Actualiza un usuario existente."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400

    email = data.get('email')
    role_id = data.get('role_id')

    if email:
        if User.query.filter(User.email == email, User.id != user_id).first():
            return jsonify({'message': 'Email ya registrado'}), 400
        user.email = email

    if role_id:
        role = Role.query.get(role_id)
        if not role:
            return jsonify({'message': 'Rol no encontrado'}), 400
        user.role = role

    db.session.commit()
    return jsonify({'message': 'Usuario actualizado'}), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_permission('delete_user')
def delete_user(user_id):
    """Elimina un usuario."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado'}), 200

@user_bp.route('/permissions', methods=['GET'])
@jwt_required()
def get_permissions():
    """Obtiene los permisos del usuario actual."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    permissions = [permission.name for permission in user.role.permissions]
    return jsonify({'permissions': permissions}), 200

@user_bp.route('/<int:user_id>/activate', methods=['PUT'])
@jwt_required()
@require_permission('manage_users')
def activate_user(user_id):
    """Activa o desactiva un usuario."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado'}), 200

@user_bp.route('/admin', methods=['GET'])
@jwt_required()
@require_permission('admin_access')
def admin_panel():
    """Ruta de panel de administración."""
    return jsonify({'message': 'Panel de administración'}), 200