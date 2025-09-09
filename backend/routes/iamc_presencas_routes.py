from flask import Blueprint
from controllers.iamc_presencas_controller_new import (
    PresencaController, LicencaController, BeneficioController, FolhaSalarialController
)

presencas_bp = Blueprint('presencas', __name__)

# === ROTAS PARA PRESENÇAS ===
@presencas_bp.route('/presencas', methods=['GET'])
def listar_presencas():
    """GET /api/presencas - Listar todas as presenças"""
    return PresencaController.listar_todas()

@presencas_bp.route('/presencas/<int:presenca_id>', methods=['GET'])
def obter_presenca(presenca_id):
    """GET /api/presencas/{id} - Obter presença por ID"""
    return PresencaController.obter_por_id(presenca_id)

@presencas_bp.route('/presencas', methods=['POST'])
def criar_presenca():
    """POST /api/presencas - Criar nova presença"""
    return PresencaController.criar()

@presencas_bp.route('/presencas/<int:presenca_id>', methods=['PUT'])
def atualizar_presenca(presenca_id):
    """PUT /api/presencas/{id} - Atualizar presença"""
    return PresencaController.atualizar(presenca_id)

@presencas_bp.route('/presencas/<int:presenca_id>', methods=['DELETE'])
def eliminar_presenca(presenca_id):
    """DELETE /api/presencas/{id} - Eliminar presença"""
    return PresencaController.eliminar(presenca_id)

# === ROTAS PARA LICENÇAS ===
@presencas_bp.route('/licencas', methods=['GET'])
def listar_licencas():
    """GET /api/licencas - Listar todas as licenças"""
    return LicencaController.listar_todas()

@presencas_bp.route('/licencas/<int:licenca_id>', methods=['GET'])
def obter_licenca(licenca_id):
    """GET /api/licencas/{id} - Obter licença por ID"""
    return LicencaController.obter_por_id(licenca_id)

@presencas_bp.route('/licencas', methods=['POST'])
def criar_licenca():
    """POST /api/licencas - Criar nova licença"""
    return LicencaController.criar()

@presencas_bp.route('/licencas/<int:licenca_id>', methods=['PUT'])
def atualizar_licenca(licenca_id):
    """PUT /api/licencas/{id} - Atualizar licença"""
    return LicencaController.atualizar(licenca_id)

@presencas_bp.route('/licencas/<int:licenca_id>', methods=['DELETE'])
def eliminar_licenca(licenca_id):
    """DELETE /api/licencas/{id} - Eliminar licença"""
    return LicencaController.eliminar(licenca_id)

# === ROTAS PARA BENEFÍCIOS ===
@presencas_bp.route('/beneficios', methods=['GET'])
def listar_beneficios():
    """GET /api/beneficios - Listar todos os benefícios"""
    return BeneficioController.listar_todos()

@presencas_bp.route('/beneficios/<int:beneficio_id>', methods=['GET'])
def obter_beneficio(beneficio_id):
    """GET /api/beneficios/{id} - Obter benefício por ID"""
    return BeneficioController.obter_por_id(beneficio_id)

@presencas_bp.route('/beneficios', methods=['POST'])
def criar_beneficio():
    """POST /api/beneficios - Criar novo benefício"""
    return BeneficioController.criar()

@presencas_bp.route('/beneficios/<int:beneficio_id>', methods=['PUT'])
def atualizar_beneficio(beneficio_id):
    """PUT /api/beneficios/{id} - Atualizar benefício"""
    return BeneficioController.atualizar(beneficio_id)

@presencas_bp.route('/beneficios/<int:beneficio_id>', methods=['DELETE'])
def eliminar_beneficio(beneficio_id):
    """DELETE /api/beneficios/{id} - Eliminar benefício"""
    return BeneficioController.eliminar(beneficio_id)

# === ROTAS PARA FOLHA SALARIAL ===
@presencas_bp.route('/folha-salarial', methods=['GET'])
def listar_folhas_salariais():
    """GET /api/folha-salarial - Listar todas as folhas salariais"""
    return FolhaSalarialController.listar_todas()

@presencas_bp.route('/folha-salarial/<int:folha_id>', methods=['GET'])
def obter_folha_salarial(folha_id):
    """GET /api/folha-salarial/{id} - Obter folha salarial por ID"""
    return FolhaSalarialController.obter_por_id(folha_id)

@presencas_bp.route('/folha-salarial', methods=['POST'])
def criar_folha_salarial():
    """POST /api/folha-salarial - Criar nova folha salarial"""
    return FolhaSalarialController.criar()

@presencas_bp.route('/folha-salarial/<int:folha_id>', methods=['PUT'])
def atualizar_folha_salarial(folha_id):
    """PUT /api/folha-salarial/{id} - Atualizar folha salarial"""
    return FolhaSalarialController.atualizar(folha_id)

@presencas_bp.route('/folha-salarial/<int:folha_id>', methods=['DELETE'])
def eliminar_folha_salarial(folha_id):
    """DELETE /api/folha-salarial/{id} - Eliminar folha salarial"""
    return FolhaSalarialController.eliminar(folha_id)
