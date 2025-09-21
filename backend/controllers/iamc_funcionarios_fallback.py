from flask import jsonify, request
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FuncionarioControllerFallback:
    """
    Fallback controller for when IAMC database is not accessible.
    Provides mock data to keep the frontend functional.
    """
    
    @staticmethod
    def verificar_status():
        """Status check with fallback data"""
        return jsonify({
            'success': False,
            'status': 'Database IAMC não acessível - Modo Fallback',
            'error': 'IAMC connection timeout',
            'dados': {
                'totalFuncionarios': 0,
                'totalDepartamentos': 0,
                'totalCargos': 0,
                'funcionariosPorEstado': {}
            },
            'timestamp': datetime.now().isoformat()
        }), 200
    
    @staticmethod
    def listar_todos():
        """List funcionarios with fallback empty data"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível',
            'data': [],
            'total': 0,
            'page': page,
            'per_page': per_page,
            'pages': 0
        }), 200
    
    @staticmethod
    def obter_por_id(funcionario_id):
        """Get funcionario by ID with fallback"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível'
        }), 404
    
    @staticmethod
    def criar():
        """Create funcionario fallback"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível - Não é possível criar funcionários'
        }), 503
    
    @staticmethod
    def atualizar(funcionario_id):
        """Update funcionario fallback"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível - Não é possível atualizar funcionários'
        }), 503
    
    @staticmethod
    def eliminar(funcionario_id):
        """Delete funcionario fallback"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível - Não é possível eliminar funcionários'
        }), 503

class DepartamentoControllerFallback:
    """Fallback controller for departamentos"""
    
    @staticmethod
    def listar_todos():
        """List departamentos with fallback data"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível',
            'data': []
        }), 200
    
    @staticmethod
    def listar_cargos():
        """List cargos with fallback data"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível',
            'data': [],
            'total': 0
        }), 200
    
    @staticmethod
    def obter_por_id(departamento_id):
        """Get departamento by ID fallback"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível'
        }), 404
    
    @staticmethod
    def obter_cargo_por_id(cargo_id):
        """Get cargo by ID fallback"""
        return jsonify({
            'success': False,
            'error': 'Database IAMC não acessível'
        }), 404
