from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Verificar si el servidor está operativo."""
    return jsonify({"status": "ok", "message": "El servidor está funcionando correctamente."}), 200
