from flask import Blueprint, request, jsonify
from extensions import db
from models.user import Role

role_bp = Blueprint('role', __name__)

@role_bp.route('', methods=['GET'])
def get_roles():
    """Obtiene una lista de todos los roles."""
    roles = Role.query.all()
    return jsonify([{
        'id': role.id,
        'name': role.name
    } for role in roles])

@role_bp.route('', methods=['POST'])
def create_role():
    """Crea un nuevo rol."""
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'error': 'El nombre del rol es obligatorio'}), 400
    role = Role.query.filter_by(name=data['name']).first()
    if role:
        return jsonify({'error': 'El rol ya existe'}), 400
    new_role = Role(name=data['name'])
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'message': 'Rol creado correctamente'}), 201

@role_bp.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """Elimina un rol."""
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Rol eliminado correctamente'}), 200