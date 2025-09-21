from flask import jsonify
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo
from extensions import IAMCSession
import logging

logger = logging.getLogger(__name__)

class DashboardController:
    
    @staticmethod
    def listar_funcionarios_com_qr():
        """Listar funcionários que têm códigos QR gerados, com nomes de Cargo e Departamento"""
        try:
            # Return test data for demo purposes
            result = [
                {
                    'id': 1001,
                    'funcionarioId': 1001,
                    'nome': 'João',
                    'apelido': 'Silva',
                    'email': 'joao.silva@sonangol.co.ao',
                    'telefone': '+244 912 345 678',
                    'cargo': 'Engenheiro de Petróleo',
                    'cargoId': 101,
                    'departamento': 'Exploração e Produção',
                    'departamentoId': 201,
                    'qrGenerated': True
                },
                {
                    'id': 1002,
                    'funcionarioId': 1002,
                    'nome': 'Maria',
                    'apelido': 'Santos',
                    'email': 'maria.santos@sonangol.co.ao',
                    'telefone': '+244 923 456 789',
                    'cargo': 'Analista Financeiro',
                    'cargoId': 102,
                    'departamento': 'Finanças',
                    'departamentoId': 202,
                    'qrGenerated': True
                },
                {
                    'id': 1003,
                    'funcionarioId': 1003,
                    'nome': 'Carlos',
                    'apelido': 'Fernandes',
                    'email': 'carlos.fernandes@sonangol.co.ao',
                    'telefone': '+244 934 567 890',
                    'cargo': 'Especialista em RH',
                    'cargoId': 103,
                    'departamento': 'Recursos Humanos',
                    'departamentoId': 203,
                    'qrGenerated': True
                },
                {
                    'id': 1004,
                    'funcionarioId': 1004,
                    'nome': 'Ana',
                    'apelido': 'Costa',
                    'email': 'ana.costa@sonangol.co.ao',
                    'telefone': '+244 945 678 901',
                    'cargo': 'Gerente de Projetos',
                    'cargoId': 104,
                    'departamento': 'Tecnologia da Informação',
                    'departamentoId': 204,
                    'qrGenerated': True
                },
                {
                    'id': 1005,
                    'funcionarioId': 1005,
                    'nome': 'Pedro',
                    'apelido': 'Oliveira',
                    'email': 'pedro.oliveira@sonangol.co.ao',
                    'telefone': '+244 956 789 012',
                    'cargo': 'Supervisor de Segurança',
                    'cargoId': 105,
                    'departamento': 'Segurança e Meio Ambiente',
                    'departamentoId': 205,
                    'qrGenerated': True
                }
            ]
            
            logger.info(f"Retornando {len(result)} funcionários de teste com QR")
            
            return jsonify(result), 200
            
        except Exception as e:
            logger.error(f"Erro ao listar funcionários com QR: {str(e)}")
            logger.error(f"Tipo do erro: {type(e)}")
            import traceback
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            return jsonify({'error': 'Erro interno do servidor'}), 500
    
    @staticmethod
    def obter_total_funcionarios():
        """Obter total de funcionários na base de dados IAMC"""
        session = IAMCSession()
        try:
            # For now, return test data
            return jsonify({'total': 150}), 200
        except Exception as e:
            logger.error(f"Erro ao obter total de funcionários: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor'}), 500
        finally:
            session.close()
    
    @staticmethod
    def obter_total_funcionarios_com_qr():
        """Obter total de funcionários com QR codes"""
        try:
            # For now, return test data (same as the sample data count)
            return jsonify({'total': 5}), 200
        except Exception as e:
            logger.error(f"Erro ao obter total de funcionários com QR: {str(e)}")
            return jsonify({'error': 'Erro interno do servidor'}), 500
