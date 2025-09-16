"""
Script para criar e inicializar as tabelas IAMC para o sistema RRHH
"""

from extensions import IAMCSession, iamc_engine
from models.iamc_funcionarios_new import Base as FuncionariosBase
from models.iamc_presencas_new import Base as PresencasBase
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario, Contrato
from models.iamc_presencas_new import Presenca, Licenca, Beneficio, FolhaSalarial
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def criar_tabelas_iamc():
    """Criar todas as tabelas necessárias para o IAMC"""
    try:
        print("🔧 Criando tabelas IAMC...")
        
        # Criar tabelas de funcionários
        FuncionariosBase.metadata.create_all(iamc_engine)
        print("✅ Tabelas de funcionários criadas")
        
        # Criar tabelas de presenças
        PresencasBase.metadata.create_all(iamc_engine)
        print("✅ Tabelas de presenças criadas")
        
        print("🎉 Todas as tabelas IAMC foram criadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {str(e)}")
        return False

def inicializar_dados_basicos():
    """Inicializar dados básicos (departamentos, cargos, etc.)"""
    session = IAMCSession()
    try:
        print("📊 Inicializando dados básicos...")
        
        # Departamentos padrão
        departamentos_default = [
            {"Nome": "Recursos Humanos", "Descricao": "Gestão de pessoal e desenvolvimento organizacional"},
            {"Nome": "Tecnologia da Informação", "Descricao": "Desenvolvimento e manutenção de sistemas"},
            {"Nome": "Finanças", "Descricao": "Gestão financeira e contabilidade"},
            {"Nome": "Operações", "Descricao": "Operações e logística"},
            {"Nome": "Comercial", "Descricao": "Vendas e relacionamento com clientes"},
        ]
        
        for dept_data in departamentos_default:
            existing = session.query(Departamento).filter(Departamento.Nome == dept_data["Nome"]).first()
            if not existing:
                dept = Departamento(**dept_data)
                session.add(dept)
                print(f"  ➕ Departamento criado: {dept_data['Nome']}")
        
        # Cargos padrão
        cargos_default = [
            {"Nome": "Diretor", "Descricao": "Direção executiva", "Nivel": "Executivo"},
            {"Nome": "Gerente", "Descricao": "Gestão de equipe", "Nivel": "Gestão"},
            {"Nome": "Coordenador", "Descricao": "Coordenação de projetos", "Nivel": "Coordenação"},
            {"Nome": "Analista Sênior", "Descricao": "Análise especializada", "Nivel": "Sênior"},
            {"Nome": "Analista", "Descricao": "Análise técnica", "Nivel": "Pleno"},
            {"Nome": "Assistente", "Descricao": "Apoio operacional", "Nivel": "Júnior"},
        ]
        
        for cargo_data in cargos_default:
            existing = session.query(Cargo).filter(Cargo.Nome == cargo_data["Nome"]).first()
            if not existing:
                cargo = Cargo(**cargo_data)
                session.add(cargo)
                print(f"  ➕ Cargo criado: {cargo_data['Nome']}")
        
        # Benefícios padrão
        beneficios_default = [
            {"Nome": "Plano de Saúde", "Descricao": "Assistência médica e hospitalar", "Valor": 150.00},
            {"Nome": "Vale Refeição", "Descricao": "Auxílio alimentação", "Valor": 25.00},
            {"Nome": "Vale Transporte", "Descricao": "Auxílio transporte", "Valor": 8.00},
            {"Nome": "Seguro de Vida", "Descricao": "Seguro de vida em grupo", "Valor": 50.00},
        ]
        
        for ben_data in beneficios_default:
            existing = session.query(Beneficio).filter(Beneficio.Nome == ben_data["Nome"]).first()
            if not existing:
                beneficio = Beneficio(**ben_data)
                session.add(beneficio)
                print(f"  ➕ Benefício criado: {ben_data['Nome']}")
        
        session.commit()
        print("✅ Dados básicos inicializados com sucesso!")
        return True
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao inicializar dados básicos: {str(e)}")
        return False
    finally:
        session.close()

def verificar_iamc():
    """Verificar se a conexão IAMC está funcionando"""
    session = IAMCSession()
    try:
        # Teste simples de conexão
        total_funcionarios = session.query(Funcionario).count()
        total_departamentos = session.query(Departamento).count()
        total_cargos = session.query(Cargo).count()
        
        print("🔍 Status da base de dados IAMC:")
        print(f"  📊 Funcionários: {total_funcionarios}")
        print(f"  🏢 Departamentos: {total_departamentos}")
        print(f"  💼 Cargos: {total_cargos}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar IAMC: {str(e)}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("🚀 Inicializando sistema RRHH IAMC...")
    
    # Criar aplicação Flask para contexto
    from app import create_app
    app = create_app()
    
    with app.app_context():
        # Passo 1: Criar tabelas
        if criar_tabelas_iamc():
            # Passo 2: Inicializar dados básicos
            if inicializar_dados_basicos():
                # Passo 3: Verificar status
                verificar_iamc()
                print("🎉 Sistema RRHH IAMC inicializado com sucesso!")
            else:
                print("❌ Falha na inicialização dos dados básicos")
        else:
            print("❌ Falha na criação das tabelas")
