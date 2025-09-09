"""
Script de inicialização para criar as tabelas IAMC no SQL Server
Execute este script para criar a estrutura da base de dados IAMC
"""

from extensions import db
from models.iamc_funcionarios import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from models.iamc_presencas import Presenca, Licenca, Formacao, AvaliacaoDesempenho, FolhaSalarial, Beneficio, FuncionarioBeneficio
from app import create_app
from config import Config

def criar_tabelas_iamc():
    """Criar todas as tabelas IAMC"""
    try:
        app = create_app(Config)
        
        with app.app_context():
            print("Criando tabelas IAMC...")
            
            # Criar todas as tabelas
            db.create_all()
            
            print("✅ Tabelas IAMC criadas com sucesso!")
            
            # Inserir dados de exemplo
            inserir_dados_exemplo()
            
    except Exception as e:
        print(f"❌ Erro ao criar tabelas IAMC: {str(e)}")

def inserir_dados_exemplo():
    """Inserir dados de exemplo nas tabelas"""
    try:
        # Criar departamentos de exemplo
        if not Departamento.query.first():
            departamentos = [
                Departamento(nome='Recursos Humanos', descricao='Gestão de pessoas e talentos'),
                Departamento(nome='Tecnologia da Informação', descricao='Desenvolvimento e infraestrutura'),
                Departamento(nome='Financeiro', descricao='Gestão financeira e contabilidade'),
                Departamento(nome='Operações', descricao='Operações diárias da empresa')
            ]
            
            for dept in departamentos:
                db.session.add(dept)
            
            print("✅ Departamentos de exemplo criados")
        
        # Criar cargos de exemplo
        if not Cargo.query.first():
            cargos = [
                Cargo(nome='Analista', descricao='Profissional de nível médio', nivel=3),
                Cargo(nome='Coordenador', descricao='Profissional de coordenação', nivel=5),
                Cargo(nome='Gerente', descricao='Profissional de gestão', nivel=7),
                Cargo(nome='Diretor', descricao='Profissional de direção', nivel=9)
            ]
            
            for cargo in cargos:
                db.session.add(cargo)
            
            print("✅ Cargos de exemplo criados")
        
        # Criar benefícios de exemplo
        if not Beneficio.query.first():
            beneficios = [
                Beneficio(nome='Plano de Saúde', descricao='Cobertura médica completa', tipo='Saúde'),
                Beneficio(nome='Vale Alimentação', descricao='Auxílio para alimentação', tipo='Alimentação'),
                Beneficio(nome='Vale Transporte', descricao='Auxílio para transporte', tipo='Transporte'),
                Beneficio(nome='Seguro de Vida', descricao='Seguro de vida em grupo', tipo='Segurança')
            ]
            
            for beneficio in beneficios:
                db.session.add(beneficio)
            
            print("✅ Benefícios de exemplo criados")
        
        db.session.commit()
        print("✅ Dados de exemplo inseridos com sucesso!")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao inserir dados de exemplo: {str(e)}")

if __name__ == '__main__':
    criar_tabelas_iamc()
