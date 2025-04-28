from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User, Role
from flask_jwt_extended import create_access_token, create_refresh_token  # Import JWT functions
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Inicia sesión de usuario."""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email y password son requeridos'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    if not user.is_active:
        return jsonify({'message': 'Usuario inactivo'}), 401

    access_token = create_access_token(identity=str(user.id))  # Ensure user ID is a string
    refresh_token = create_refresh_token(identity=str(user.id))  # Ensure user ID is a string

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario."""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos no proporcionados'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email y password son requeridos'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email ya registrado'}), 400

    role = Role.query.filter_by(name='user').first()
    if not role:
        return jsonify({'message': 'Rol "user" no encontrado'}), 500

    user = User(email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado'}), 201
