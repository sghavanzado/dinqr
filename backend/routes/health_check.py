from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Verificar se o servidor está operacional."""
    return jsonify({"status": "ok", "message": "O servidor está a funcionar corretamente."}), 200
