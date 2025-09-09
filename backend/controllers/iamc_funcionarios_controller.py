from flask import jsonify, request
from extensions import db
from models.iamc_funcionarios import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FuncionarioController:
    
    @staticmethod
    def listar_todos():
        """Listar todos os funcionários com paginação"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            
            funcionarios = Funcionario.query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'success': True,
                'funcionarios': [f.to_dict() for f in funcionarios.items],
                'total': funcionarios.total,
                'pages': funcionarios.pages,
                'current_page': page
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar funcionários: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
    
    @staticmethod
    def obter_por_id(funcionario_id):
        """Obter funcionário por ID"""
        try:
            funcionario = Funcionario.query.get_or_404(funcionario_id)
            return jsonify({
                'success': True,
                'funcionario': funcionario.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Funcionário não encontrado'}), 404
    
    @staticmethod
    def criar():
        """Criar novo funcionário"""
        try:
            dados = request.get_json()
            
            # Validar campos obrigatórios
            if not dados.get('Nome') or not dados.get('Apelido') or not dados.get('BI'):
                return jsonify({
                    'success': False, 
                    'error': 'Nome, apelido e BI são obrigatórios'
                }), 400
            
            # Verificar se BI já existe
            if Funcionario.query.filter_by(BI=dados.get('BI')).first():
                return jsonify({
                    'success': False,
                    'error': 'Já existe um funcionário com este BI'
                }), 400
            
            funcionario = Funcionario(
                Nome=dados.get('Nome'),
                Apelido=dados.get('Apelido'),
                BI=dados.get('BI'),
                DataNascimento=datetime.strptime(dados.get('DataNascimento'), '%Y-%m-%d').date() if dados.get('DataNascimento') else None,
                Sexo=dados.get('Sexo'),
                EstadoCivil=dados.get('EstadoCivil'),
                Email=dados.get('Email'),
                Telefone=dados.get('Telefone'),
                Endereco=dados.get('Endereco'),
                DataAdmissao=datetime.strptime(dados.get('DataAdmissao'), '%Y-%m-%d').date() if dados.get('DataAdmissao') else datetime.now().date(),
                EstadoFuncionario=dados.get('EstadoFuncionario', 'Activo')
            )
            
            db.session.add(funcionario)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'funcionario': funcionario.to_dict(),
                'message': 'Funcionário criado com sucesso'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao criar funcionário'}), 500
    
    @staticmethod
    def atualizar(funcionario_id):
        """Atualizar funcionário"""
        try:
            funcionario = Funcionario.query.get_or_404(funcionario_id)
            dados = request.get_json()
            
            # Atualizar campos se fornecidos
            if 'Nome' in dados:
                funcionario.Nome = dados['Nome']
            if 'Apelido' in dados:
                funcionario.Apelido = dados['Apelido']
            if 'BI' in dados:
                # Verificar se o novo BI não está em uso por outro funcionário
                existing = Funcionario.query.filter_by(BI=dados['BI']).first()
                if existing and existing.FuncionarioID != funcionario_id:
                    return jsonify({
                        'success': False,
                        'error': 'Já existe um funcionário com este BI'
                    }), 400
                funcionario.BI = dados['BI']
            if 'DataNascimento' in dados:
                funcionario.DataNascimento = datetime.strptime(dados['DataNascimento'], '%Y-%m-%d').date() if dados['DataNascimento'] else None
            if 'Sexo' in dados:
                funcionario.Sexo = dados['Sexo']
            if 'EstadoCivil' in dados:
                funcionario.EstadoCivil = dados['EstadoCivil']
            if 'Email' in dados:
                funcionario.Email = dados['Email']
            if 'Telefone' in dados:
                funcionario.Telefone = dados['Telefone']
            if 'Endereco' in dados:
                funcionario.Endereco = dados['Endereco']
            if 'EstadoFuncionario' in dados:
                funcionario.EstadoFuncionario = dados['EstadoFuncionario']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'funcionario': funcionario.to_dict(),
                'message': 'Funcionário atualizado com sucesso'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao atualizar funcionário'}), 500
    
    @staticmethod
    def eliminar(funcionario_id):
        """Eliminar funcionário"""
        try:
            funcionario = Funcionario.query.get_or_404(funcionario_id)
            
            db.session.delete(funcionario)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Funcionário eliminado com sucesso'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao eliminar funcionário: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao eliminar funcionário'}), 500

class DepartamentoController:
    
    @staticmethod
    def listar_todos():
        """Listar todos os departamentos"""
        try:
            departamentos = Departamento.query.all()
            return jsonify({
                'success': True,
                'departamentos': [d.to_dict() for d in departamentos]
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar departamentos: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
    
    @staticmethod
    def obter_por_id(departamento_id):
        """Obter departamento por ID"""
        try:
            departamento = Departamento.query.get_or_404(departamento_id)
            return jsonify({
                'success': True,
                'departamento': departamento.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Departamento não encontrado'}), 404
    
    @staticmethod
    def criar():
        """Criar novo departamento"""
        try:
            dados = request.get_json()
            
            if not dados.get('Nome'):
                return jsonify({
                    'success': False, 
                    'error': 'Nome é obrigatório'
                }), 400
            
            departamento = Departamento(
                Nome=dados.get('Nome'),
                Descricao=dados.get('Descricao')
            )
            
            db.session.add(departamento)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'departamento': departamento.to_dict(),
                'message': 'Departamento criado com sucesso'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao criar departamento'}), 500
    
    @staticmethod
    def atualizar(departamento_id):
        """Atualizar departamento"""
        try:
            departamento = Departamento.query.get_or_404(departamento_id)
            dados = request.get_json()
            
            if 'Nome' in dados:
                departamento.Nome = dados['Nome']
            if 'Descricao' in dados:
                departamento.Descricao = dados['Descricao']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'departamento': departamento.to_dict(),
                'message': 'Departamento atualizado com sucesso'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao atualizar departamento'}), 500
    
    @staticmethod
    def eliminar(departamento_id):
        """Eliminar departamento"""
        try:
            departamento = Departamento.query.get_or_404(departamento_id)
            
            db.session.delete(departamento)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Departamento eliminado com sucesso'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao eliminar departamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao eliminar departamento'}), 500
