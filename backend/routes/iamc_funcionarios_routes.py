from flask import Blueprint, send_from_directory
from controllers.iamc_funcionarios_controller_new import FuncionarioController, DepartamentoController
import os

funcionarios_bp = Blueprint('funcionarios', __name__)

# === ROTAS PARA FUNCIONÁRIOS ===
@funcionarios_bp.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    """GET /api/funcionarios - Listar todos os funcionários"""
    return FuncionarioController.listar_todos()

@funcionarios_bp.route('/funcionarios/<int:funcionario_id>', methods=['GET'])
def obter_funcionario(funcionario_id):
    """GET /api/funcionarios/{id} - Obter funcionário por ID"""
    return FuncionarioController.obter_por_id(funcionario_id)

@funcionarios_bp.route('/funcionarios', methods=['POST'])
def criar_funcionario():
    """POST /api/funcionarios - Criar novo funcionário"""
    return FuncionarioController.criar()

@funcionarios_bp.route('/funcionarios/<int:funcionario_id>', methods=['PUT'])
def atualizar_funcionario(funcionario_id):
    """PUT /api/funcionarios/{id} - Atualizar funcionário"""
    return FuncionarioController.atualizar(funcionario_id)

@funcionarios_bp.route('/funcionarios/<int:funcionario_id>', methods=['DELETE'])
def eliminar_funcionario(funcionario_id):
    """DELETE /api/funcionarios/{id} - Eliminar funcionário"""
    return FuncionarioController.eliminar(funcionario_id)

@funcionarios_bp.route('/funcionarios/<int:funcionario_id>/foto', methods=['POST'])
def upload_foto_funcionario(funcionario_id):
    """POST /api/funcionarios/{id}/foto - Upload da foto do funcionário"""
    return FuncionarioController.upload_foto(funcionario_id)

@funcionarios_bp.route('/funcionarios/<int:funcionario_id>/foto', methods=['GET'])
def obter_foto_funcionario(funcionario_id):
    """GET /api/funcionarios/{id}/foto - Obter foto do funcionário"""
    return FuncionarioController.obter_foto(funcionario_id)

@funcionarios_bp.route('/funcionarios/<int:funcionario_id>/foto', methods=['DELETE'])
def remover_foto_funcionario(funcionario_id):
    """DELETE /api/funcionarios/{id}/foto - Remover foto do funcionário"""
    return FuncionarioController.remover_foto(funcionario_id)

# Rota para servir arquivos de foto
@funcionarios_bp.route('/uploads/fotos_funcionarios/<filename>')
def servir_foto_funcionario(filename):
    """GET /api/uploads/fotos_funcionarios/{filename} - Servir arquivo de foto"""
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'fotos_funcionarios')
    return send_from_directory(upload_dir, filename)

# === ROTAS PARA DEPARTAMENTOS ===
@funcionarios_bp.route('/departamentos', methods=['GET'])
def listar_departamentos():
    """GET /api/departamentos - Listar todos os departamentos"""
    return DepartamentoController.listar_todos()

@funcionarios_bp.route('/departamentos/<int:departamento_id>', methods=['GET'])
def obter_departamento(departamento_id):
    """GET /api/departamentos/{id} - Obter departamento por ID"""
    return DepartamentoController.obter_por_id(departamento_id)

@funcionarios_bp.route('/departamentos', methods=['POST'])
def criar_departamento():
    """POST /api/departamentos - Criar novo departamento"""
    return DepartamentoController.criar()

@funcionarios_bp.route('/departamentos/<int:departamento_id>', methods=['PUT'])
def atualizar_departamento(departamento_id):
    """PUT /api/departamentos/{id} - Atualizar departamento"""
    return DepartamentoController.atualizar(departamento_id)

@funcionarios_bp.route('/departamentos/<int:departamento_id>', methods=['DELETE'])
def eliminar_departamento(departamento_id):
    """DELETE /api/departamentos/{id} - Eliminar departamento"""
    return DepartamentoController.eliminar(departamento_id)
