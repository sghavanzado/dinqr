"""
Controller para gestão de presenças, licenças, benefícios e folhas salariais do IAMC
Utiliza conexão direta ao SQL Server através de SQLAlchemy sessions
"""

from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from models.iamc_presencas_new import Presenca, Licenca, Beneficio, FolhaSalarial
from extensions import IAMCSession
import logging

logger = logging.getLogger(__name__)

class PresencaController:
    """Controller para gestão de presenças"""
    
    @staticmethod
    def listar_todas():
        """Lista todas as presenças"""
        session = IAMCSession()
        try:
            presencas = session.query(Presenca).all()
            return jsonify({
                'success': True,
                'data': [p.to_dict() for p in presencas]
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar presenças: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def obter_por_id(presenca_id):
        """Obtém presença por ID"""
        session = IAMCSession()
        try:
            presenca = session.query(Presenca).filter(Presenca.PresencaID == presenca_id).first()
            if not presenca:
                return jsonify({
                    'success': False,
                    'message': 'Presença não encontrada'
                }), 404
            
            return jsonify({
                'success': True,
                'data': presenca.to_dict()
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao obter presença {presenca_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def criar():
        """Cria nova presença"""
        session = IAMCSession()
        try:
            data = request.get_json()
            
            # Validação básica
            if not data.get('FuncionarioID'):
                return jsonify({
                    'success': False,
                    'message': 'FuncionarioID é obrigatório'
                }), 400
            
            # Converter strings de data para objetos date
            if 'DataPresenca' in data and isinstance(data['DataPresenca'], str):
                data['DataPresenca'] = datetime.strptime(data['DataPresenca'], '%Y-%m-%d').date()
            
            if 'HoraEntrada' in data and isinstance(data['HoraEntrada'], str):
                data['HoraEntrada'] = datetime.strptime(data['HoraEntrada'], '%H:%M:%S').time()
            
            if 'HoraSaida' in data and isinstance(data['HoraSaida'], str):
                data['HoraSaida'] = datetime.strptime(data['HoraSaida'], '%H:%M:%S').time()
            
            nova_presenca = Presenca(**data)
            session.add(nova_presenca)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Presença criada com sucesso',
                'data': nova_presenca.to_dict()
            }), 201
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao criar presença: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data/hora inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def atualizar(presenca_id):
        """Atualiza presença"""
        session = IAMCSession()
        try:
            presenca = session.query(Presenca).filter(Presenca.PresencaID == presenca_id).first()
            if not presenca:
                return jsonify({
                    'success': False,
                    'message': 'Presença não encontrada'
                }), 404
            
            data = request.get_json()
            
            # Converter strings de data para objetos date/time se necessário
            if 'DataPresenca' in data and isinstance(data['DataPresenca'], str):
                data['DataPresenca'] = datetime.strptime(data['DataPresenca'], '%Y-%m-%d').date()
            
            if 'HoraEntrada' in data and isinstance(data['HoraEntrada'], str):
                data['HoraEntrada'] = datetime.strptime(data['HoraEntrada'], '%H:%M:%S').time()
            
            if 'HoraSaida' in data and isinstance(data['HoraSaida'], str):
                data['HoraSaida'] = datetime.strptime(data['HoraSaida'], '%H:%M:%S').time()
            
            # Atualizar campos
            for key, value in data.items():
                if hasattr(presenca, key):
                    setattr(presenca, key, value)
            
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Presença atualizada com sucesso',
                'data': presenca.to_dict()
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao atualizar presença {presenca_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data/hora inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def eliminar(presenca_id):
        """Elimina presença"""
        session = IAMCSession()
        try:
            presenca = session.query(Presenca).filter(Presenca.PresencaID == presenca_id).first()
            if not presenca:
                return jsonify({
                    'success': False,
                    'message': 'Presença não encontrada'
                }), 404
            
            session.delete(presenca)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Presença eliminada com sucesso'
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao eliminar presença {presenca_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()


class LicencaController:
    """Controller para gestão de licenças"""
    
    @staticmethod
    def listar_todas():
        """Lista todas as licenças"""
        session = IAMCSession()
        try:
            licencas = session.query(Licenca).all()
            return jsonify({
                'success': True,
                'data': [l.to_dict() for l in licencas]
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar licenças: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def obter_por_id(licenca_id):
        """Obtém licença por ID"""
        session = IAMCSession()
        try:
            licenca = session.query(Licenca).filter(Licenca.LicencaID == licenca_id).first()
            if not licenca:
                return jsonify({
                    'success': False,
                    'message': 'Licença não encontrada'
                }), 404
            
            return jsonify({
                'success': True,
                'data': licenca.to_dict()
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao obter licença {licenca_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def criar():
        """Cria nova licença"""
        session = IAMCSession()
        try:
            data = request.get_json()
            
            # Validação básica
            if not data.get('FuncionarioID'):
                return jsonify({
                    'success': False,
                    'message': 'FuncionarioID é obrigatório'
                }), 400
            
            # Converter strings de data para objetos date
            if 'DataInicio' in data and isinstance(data['DataInicio'], str):
                data['DataInicio'] = datetime.strptime(data['DataInicio'], '%Y-%m-%d').date()
            
            if 'DataFim' in data and isinstance(data['DataFim'], str):
                data['DataFim'] = datetime.strptime(data['DataFim'], '%Y-%m-%d').date()
            
            nova_licenca = Licenca(**data)
            session.add(nova_licenca)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Licença criada com sucesso',
                'data': nova_licenca.to_dict()
            }), 201
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao criar licença: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def atualizar(licenca_id):
        """Atualiza licença"""
        session = IAMCSession()
        try:
            licenca = session.query(Licenca).filter(Licenca.LicencaID == licenca_id).first()
            if not licenca:
                return jsonify({
                    'success': False,
                    'message': 'Licença não encontrada'
                }), 404
            
            data = request.get_json()
            
            # Converter strings de data para objetos date se necessário
            if 'DataInicio' in data and isinstance(data['DataInicio'], str):
                data['DataInicio'] = datetime.strptime(data['DataInicio'], '%Y-%m-%d').date()
            
            if 'DataFim' in data and isinstance(data['DataFim'], str):
                data['DataFim'] = datetime.strptime(data['DataFim'], '%Y-%m-%d').date()
            
            # Atualizar campos
            for key, value in data.items():
                if hasattr(licenca, key):
                    setattr(licenca, key, value)
            
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Licença atualizada com sucesso',
                'data': licenca.to_dict()
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao atualizar licença {licenca_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def eliminar(licenca_id):
        """Elimina licença"""
        session = IAMCSession()
        try:
            licenca = session.query(Licenca).filter(Licenca.LicencaID == licenca_id).first()
            if not licenca:
                return jsonify({
                    'success': False,
                    'message': 'Licença não encontrada'
                }), 404
            
            session.delete(licenca)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Licença eliminada com sucesso'
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao eliminar licença {licenca_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()


class BeneficioController:
    """Controller para gestão de benefícios"""
    
    @staticmethod
    def listar_todos():
        """Lista todos os benefícios"""
        session = IAMCSession()
        try:
            beneficios = session.query(Beneficio).all()
            return jsonify({
                'success': True,
                'data': [b.to_dict() for b in beneficios]
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar benefícios: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def obter_por_id(beneficio_id):
        """Obtém benefício por ID"""
        session = IAMCSession()
        try:
            beneficio = session.query(Beneficio).filter(Beneficio.BeneficioID == beneficio_id).first()
            if not beneficio:
                return jsonify({
                    'success': False,
                    'message': 'Benefício não encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'data': beneficio.to_dict()
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao obter benefício {beneficio_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def criar():
        """Cria novo benefício"""
        session = IAMCSession()
        try:
            data = request.get_json()
            
            # Validação básica
            if not data.get('FuncionarioID'):
                return jsonify({
                    'success': False,
                    'message': 'FuncionarioID é obrigatório'
                }), 400
            
            # Converter strings de data para objetos date
            if 'DataInicio' in data and isinstance(data['DataInicio'], str):
                data['DataInicio'] = datetime.strptime(data['DataInicio'], '%Y-%m-%d').date()
            
            if 'DataFim' in data and isinstance(data['DataFim'], str):
                data['DataFim'] = datetime.strptime(data['DataFim'], '%Y-%m-%d').date()
            
            novo_beneficio = Beneficio(**data)
            session.add(novo_beneficio)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Benefício criado com sucesso',
                'data': novo_beneficio.to_dict()
            }), 201
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao criar benefício: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def atualizar(beneficio_id):
        """Atualiza benefício"""
        session = IAMCSession()
        try:
            beneficio = session.query(Beneficio).filter(Beneficio.BeneficioID == beneficio_id).first()
            if not beneficio:
                return jsonify({
                    'success': False,
                    'message': 'Benefício não encontrado'
                }), 404
            
            data = request.get_json()
            
            # Converter strings de data para objetos date se necessário
            if 'DataInicio' in data and isinstance(data['DataInicio'], str):
                data['DataInicio'] = datetime.strptime(data['DataInicio'], '%Y-%m-%d').date()
            
            if 'DataFim' in data and isinstance(data['DataFim'], str):
                data['DataFim'] = datetime.strptime(data['DataFim'], '%Y-%m-%d').date()
            
            # Atualizar campos
            for key, value in data.items():
                if hasattr(beneficio, key):
                    setattr(beneficio, key, value)
            
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Benefício atualizado com sucesso',
                'data': beneficio.to_dict()
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao atualizar benefício {beneficio_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def eliminar(beneficio_id):
        """Elimina benefício"""
        session = IAMCSession()
        try:
            beneficio = session.query(Beneficio).filter(Beneficio.BeneficioID == beneficio_id).first()
            if not beneficio:
                return jsonify({
                    'success': False,
                    'message': 'Benefício não encontrado'
                }), 404
            
            session.delete(beneficio)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Benefício eliminado com sucesso'
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao eliminar benefício {beneficio_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()


class FolhaSalarialController:
    """Controller para gestão de folhas salariais"""
    
    @staticmethod
    def listar_todas():
        """Lista todas as folhas salariais"""
        session = IAMCSession()
        try:
            folhas = session.query(FolhaSalarial).all()
            return jsonify({
                'success': True,
                'data': [f.to_dict() for f in folhas]
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar folhas salariais: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def obter_por_id(folha_id):
        """Obtém folha salarial por ID"""
        session = IAMCSession()
        try:
            folha = session.query(FolhaSalarial).filter(FolhaSalarial.FolhaID == folha_id).first()
            if not folha:
                return jsonify({
                    'success': False,
                    'message': 'Folha salarial não encontrada'
                }), 404
            
            return jsonify({
                'success': True,
                'data': folha.to_dict()
            }), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao obter folha salarial {folha_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
    
    @staticmethod
    def criar():
        """Cria nova folha salarial"""
        session = IAMCSession()
        try:
            data = request.get_json()
            
            # Validação básica
            if not data.get('FuncionarioID'):
                return jsonify({
                    'success': False,
                    'message': 'FuncionarioID é obrigatório'
                }), 400
            
            # Converter strings de data para objetos date
            if 'DataFolha' in data and isinstance(data['DataFolha'], str):
                data['DataFolha'] = datetime.strptime(data['DataFolha'], '%Y-%m-%d').date()
            
            nova_folha = FolhaSalarial(**data)
            session.add(nova_folha)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Folha salarial criada com sucesso',
                'data': nova_folha.to_dict()
            }), 201
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao criar folha salarial: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def atualizar(folha_id):
        """Atualiza folha salarial"""
        session = IAMCSession()
        try:
            folha = session.query(FolhaSalarial).filter(FolhaSalarial.FolhaID == folha_id).first()
            if not folha:
                return jsonify({
                    'success': False,
                    'message': 'Folha salarial não encontrada'
                }), 404
            
            data = request.get_json()
            
            # Converter strings de data para objetos date se necessário
            if 'DataFolha' in data and isinstance(data['DataFolha'], str):
                data['DataFolha'] = datetime.strptime(data['DataFolha'], '%Y-%m-%d').date()
            
            # Atualizar campos
            for key, value in data.items():
                if hasattr(folha, key):
                    setattr(folha, key, value)
            
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Folha salarial atualizada com sucesso',
                'data': folha.to_dict()
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao atualizar folha salarial {folha_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        except ValueError as e:
            logger.error(f"Erro de formato de data: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Formato de data inválido'
            }), 400
        finally:
            session.close()

    @staticmethod
    def eliminar(folha_id):
        """Elimina folha salarial"""
        session = IAMCSession()
        try:
            folha = session.query(FolhaSalarial).filter(FolhaSalarial.FolhaID == folha_id).first()
            if not folha:
                return jsonify({
                    'success': False,
                    'message': 'Folha salarial não encontrada'
                }), 404
            
            session.delete(folha)
            session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Folha salarial eliminada com sucesso'
            }), 200
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao eliminar folha salarial {folha_id}: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Erro interno do servidor'
            }), 500
        finally:
            session.close()
