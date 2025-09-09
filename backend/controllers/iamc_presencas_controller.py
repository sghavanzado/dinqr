from flask import jsonify, request
from extensions import db
from models.iamc_presencas import Presenca, Licenca, Formacao, AvaliacaoDesempenho, FolhaSalarial, Beneficio, FuncionarioBeneficio
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class PresencaController:
    
    @staticmethod
    def listar_todas():
        """Listar todas as presenças com paginação"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            funcionario_id = request.args.get('funcionario_id', type=int)
            
            query = Presenca.query
            if funcionario_id:
                query = query.filter_by(funcionario_id=funcionario_id)
            
            presencas = query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'success': True,
                'presencas': [p.to_dict() for p in presencas.items],
                'total': presencas.total,
                'pages': presencas.pages,
                'current_page': page
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar presenças: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
    
    @staticmethod
    def obter_por_id(presenca_id):
        """Obter presença por ID"""
        try:
            presenca = Presenca.query.get_or_404(presenca_id)
            return jsonify({
                'success': True,
                'presenca': presenca.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter presença: {str(e)}")
            return jsonify({'success': False, 'error': 'Presença não encontrada'}), 404
    
    @staticmethod
    def criar():
        """Criar nova presença"""
        try:
            dados = request.get_json()
            
            if not dados.get('FuncionarioID'):
                return jsonify({
                    'success': False, 
                    'error': 'ID do funcionário é obrigatório'
                }), 400
            
            presenca = Presenca(
                FuncionarioID=dados.get('FuncionarioID'),
                Data=datetime.strptime(dados.get('Data'), '%Y-%m-%d').date() if dados.get('Data') else date.today(),
                HoraEntrada=datetime.strptime(dados.get('HoraEntrada'), '%H:%M:%S').time() if dados.get('HoraEntrada') else None,
                HoraSaida=datetime.strptime(dados.get('HoraSaida'), '%H:%M:%S').time() if dados.get('HoraSaida') else None,
                Observacao=dados.get('Observacao')
            )
            
            db.session.add(presenca)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'presenca': presenca.to_dict(),
                'message': 'Presença registrada com sucesso'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar presença: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao registrar presença'}), 500

class LicencaController:
    
    @staticmethod
    def listar_todas():
        """Listar todas as licenças com paginação"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            funcionario_id = request.args.get('funcionario_id', type=int)
            
            query = Licenca.query
            if funcionario_id:
                query = query.filter_by(funcionario_id=funcionario_id)
            
            licencas = query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'success': True,
                'licencas': [l.to_dict() for l in licencas.items],
                'total': licencas.total,
                'pages': licencas.pages,
                'current_page': page
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar licenças: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
    
    @staticmethod
    def obter_por_id(licenca_id):
        """Obter licença por ID"""
        try:
            licenca = Licenca.query.get_or_404(licenca_id)
            return jsonify({
                'success': True,
                'licenca': licenca.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter licença: {str(e)}")
            return jsonify({'success': False, 'error': 'Licença não encontrada'}), 404
    
    @staticmethod
    def criar():
        """Criar nova licença"""
        try:
            dados = request.get_json()
            
            campos_obrigatorios = ['funcionario_id', 'tipo_licenca', 'data_inicio', 'data_fim']
            for campo in campos_obrigatorios:
                if not dados.get(campo):
                    return jsonify({
                        'success': False, 
                        'error': f'{campo} é obrigatório'
                    }), 400
            
            licenca = Licenca(
                funcionario_id=dados.get('funcionario_id'),
                tipo_licenca=dados.get('tipo_licenca'),
                data_inicio=datetime.strptime(dados.get('data_inicio'), '%Y-%m-%d').date(),
                data_fim=datetime.strptime(dados.get('data_fim'), '%Y-%m-%d').date(),
                estado=dados.get('estado', 'Pendente')
            )
            
            db.session.add(licenca)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'licenca': licenca.to_dict(),
                'message': 'Licença criada com sucesso'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar licença: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao criar licença'}), 500

class BeneficioController:
    
    @staticmethod
    def listar_todos():
        """Listar todos os benefícios"""
        try:
            beneficios = Beneficio.query.all()
            return jsonify({
                'success': True,
                'beneficios': [b.to_dict() for b in beneficios]
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar benefícios: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
    
    @staticmethod
    def obter_por_id(beneficio_id):
        """Obter benefício por ID"""
        try:
            beneficio = Beneficio.query.get_or_404(beneficio_id)
            return jsonify({
                'success': True,
                'beneficio': beneficio.to_dict()
            }), 200
        except Exception as e:
            logger.error(f"Erro ao obter benefício: {str(e)}")
            return jsonify({'success': False, 'error': 'Benefício não encontrado'}), 404
    
    @staticmethod
    def criar():
        """Criar novo benefício"""
        try:
            dados = request.get_json()
            
            campos_obrigatorios = ['nome', 'tipo']
            for campo in campos_obrigatorios:
                if not dados.get(campo):
                    return jsonify({
                        'success': False, 
                        'error': f'{campo} é obrigatório'
                    }), 400
            
            beneficio = Beneficio(
                nome=dados.get('nome'),
                descricao=dados.get('descricao'),
                tipo=dados.get('tipo')
            )
            
            db.session.add(beneficio)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'beneficio': beneficio.to_dict(),
                'message': 'Benefício criado com sucesso'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao criar benefício: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao criar benefício'}), 500
    
    @staticmethod
    def atualizar(beneficio_id):
        """Atualizar benefício"""
        try:
            beneficio = Beneficio.query.get_or_404(beneficio_id)
            dados = request.get_json()
            
            if 'nome' in dados:
                beneficio.nome = dados['nome']
            if 'descricao' in dados:
                beneficio.descricao = dados['descricao']
            if 'tipo' in dados:
                beneficio.tipo = dados['tipo']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'beneficio': beneficio.to_dict(),
                'message': 'Benefício atualizado com sucesso'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar benefício: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao atualizar benefício'}), 500
    
    @staticmethod
    def eliminar(beneficio_id):
        """Eliminar benefício"""
        try:
            beneficio = Beneficio.query.get_or_404(beneficio_id)
            
            db.session.delete(beneficio)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Benefício eliminado com sucesso'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao eliminar benefício: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao eliminar benefício'}), 500

class FolhaSalarialController:
    
    @staticmethod
    def listar_todas():
        """Listar todas as folhas salariais com paginação"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            funcionario_id = request.args.get('funcionario_id', type=int)
            
            query = FolhaSalarial.query
            if funcionario_id:
                query = query.filter_by(funcionario_id=funcionario_id)
            
            folhas = query.paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'success': True,
                'folhas_salariais': [f.to_dict() for f in folhas.items],
                'total': folhas.total,
                'pages': folhas.pages,
                'current_page': page
            }), 200
        except Exception as e:
            logger.error(f"Erro ao listar folhas salariais: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500
