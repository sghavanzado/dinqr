from flask import Blueprint
from .iamc_funcionarios_routes import funcionarios_bp
from .iamc_presencas_routes import presencas_bp

# Blueprint principal para IAMC
iamc_bp = Blueprint('iamc', __name__)

# Registrar sub-blueprints
iamc_bp.register_blueprint(funcionarios_bp)
iamc_bp.register_blueprint(presencas_bp)

# Rota de status/saúde para IAMC
@iamc_bp.route('/status', methods=['GET'])
def iamc_status():
    """GET /api/iamc/status - Verificar status do módulo IAMC"""
    return {
        'success': True,
        'module': 'IAMC - Gestão de Funcionários',
        'status': 'Operacional',
        'endpoints': {
            'funcionarios': '/api/iamc/funcionarios',
            'departamentos': '/api/iamc/departamentos',
            'presencas': '/api/iamc/presencas',
            'licencas': '/api/iamc/licencas',
            'beneficios': '/api/iamc/beneficios',
            'folha_salarial': '/api/iamc/folha-salarial'
        }
    }, 200
