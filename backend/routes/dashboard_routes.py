from flask import Blueprint
from controllers.dashboard_controller import DashboardController

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/funcionarios-com-qr', methods=['GET'])
def listar_funcionarios_com_qr():
    """GET /api/dashboard/funcionarios-com-qr - Listar funcionários com QR codes e joins das tabelas relacionadas"""
    return DashboardController.listar_funcionarios_com_qr()

@dashboard_bp.route('/funcionarios/total', methods=['GET'])
def obter_total_funcionarios():
    """GET /api/dashboard/funcionarios/total - Obter total de funcionários"""
    return DashboardController.obter_total_funcionarios()

@dashboard_bp.route('/funcionarios/total-com-qr', methods=['GET'])
def obter_total_funcionarios_com_qr():
    """GET /api/dashboard/funcionarios/total-com-qr - Obter total de funcionários com QR"""
    return DashboardController.obter_total_funcionarios_com_qr()
