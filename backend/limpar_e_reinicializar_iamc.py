#!/usr/bin/env python3
"""
Script para limpar e reinicializar todos os dados IAMC com dados completos de exemplo.
"""

import logging
from datetime import date, time
from flask import Flask

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar modelos e configurações
from models.iamc_funcionarios_new import (
    Departamento, Cargo, Funcionario, Contrato, HistoricoCargoFuncionario
)
from models.iamc_presencas_new import (
    Presenca, FolhaSalarial, Beneficio, FuncionarioBeneficio
)
from config import Config
from extensions import init_iamc_db, IAMCSession

def limpar_dados_iamc():
    """
    Remove todos os dados IAMC existentes.
    """
    try:
        # Inicializar Flask app mínimo
        app = Flask(__name__)
        app.config.from_object(Config)
        
        with app.app_context():
            # Inicializar conexão IAMC
            success = init_iamc_db(app)
            if not success:
                print("❌ Erro ao inicializar IAMC")
                return False
            
            session = IAMCSession()
            
            print("🧹 Limpando dados existentes...")
            
            # Remover em ordem para respeitar foreign keys
            session.query(FolhaSalarial).delete()
            session.query(FuncionarioBeneficio).delete()
            session.query(Presenca).delete()
            session.query(HistoricoCargoFuncionario).delete()
            session.query(Contrato).delete()
            session.query(Funcionario).delete()
            session.query(Beneficio).delete()
            session.query(Cargo).delete()
            session.query(Departamento).delete()
            
            session.commit()
            print("   ✅ Todos os dados foram removidos!")
            
            return True
            
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao limpar dados: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()

def criar_dados_completos():
    """
    Cria um conjunto completo de dados de exemplo.
    """
    try:
        # Inicializar Flask app mínimo
        app = Flask(__name__)
        app.config.from_object(Config)
        
        with app.app_context():
            # Inicializar conexão IAMC
            success = init_iamc_db(app)
            if not success:
                print("❌ Erro ao inicializar IAMC")
                return False
            logger.info("✅ Conexão IAMC (SQL Server) inicializada com sucesso")
            
            session = IAMCSession()
            
            print("🏢 1. Criando Departamentos...")
            departamentos = [
                Departamento(Nome="Recursos Humanos", Descricao="Gestão de pessoal e recursos humanos"),
                Departamento(Nome="Tecnologia da Informação", Descricao="Desenvolvimento e manutenção de sistemas"),
                Departamento(Nome="Contabilidade", Descricao="Gestão financeira e contabilística")
            ]
            
            for dept in departamentos:
                session.add(dept)
            session.commit()
            print(f"   ✅ {len(departamentos)} departamentos criados!")
            
            print("\n👔 2. Criando Cargos...")
            cargos = [
                Cargo(Nome="Analista de RH", Descricao="Responsável pela gestão de pessoal", Nivel="Júnior"),
                Cargo(Nome="Desenvolvedor de Software", Descricao="Desenvolvimento de aplicações", Nivel="Pleno"),
                Cargo(Nome="Contador", Descricao="Responsável pela contabilidade", Nivel="Sénior")
            ]
            
            for cargo in cargos:
                session.add(cargo)
            session.commit()
            print(f"   ✅ {len(cargos)} cargos criados!")
            
            print("\n👥 3. Criando Funcionários...")
            funcionarios = [
                Funcionario(
                    Nome="Ana",
                    Apelido="Silva",
                    BI="123456789LA041", 
                    DataNascimento=date(1990, 5, 15),
                    Sexo="F",
                    EstadoCivil="Casada",
                    Email="ana.silva@empresa.com",
                    Telefone="+244 923 456 789",
                    Endereco="Rua da Paz, 123, Luanda",
                    DataAdmissao=date(2022, 3, 1),
                    EstadoFuncionario="Activo"
                ),
                Funcionario(
                    Nome="João",
                    Apelido="Santos",
                    BI="987654321LA042", 
                    DataNascimento=date(1985, 8, 22),
                    Sexo="M",
                    EstadoCivil="Solteiro",
                    Email="joao.santos@empresa.com",
                    Telefone="+244 912 345 678",
                    Endereco="Avenida Marginal, 456, Luanda",
                    DataAdmissao=date(2021, 7, 15),
                    EstadoFuncionario="Activo"
                ),
                Funcionario(
                    Nome="Carlos",
                    Apelido="Mendes",
                    BI="456789123LA043", 
                    DataNascimento=date(1988, 12, 3),
                    Sexo="M",
                    EstadoCivil="Solteiro",
                    Email="carlos.mendes@empresa.com",
                    Telefone="+244 934 567 890",
                    Endereco="Rua dos Coqueiros, 789, Luanda",
                    DataAdmissao=date(2023, 9, 5),
                    EstadoFuncionario="Activo"
                )
            ]
            
            for funcionario in funcionarios:
                session.add(funcionario)
            session.commit()
            print(f"   ✅ {len(funcionarios)} funcionários criados!")
            
            print("\n🔗 Criando histórico de cargos e departamentos...")
            # Criar relacionamentos funcionário-cargo-departamento
            historicos = []
            for i, funcionario in enumerate(funcionarios):
                historico = HistoricoCargoFuncionario(
                    FuncionarioID=funcionario.FuncionarioID,
                    CargoID=cargos[i].CargoID,
                    DepartamentoID=departamentos[i].DepartamentoID,
                    DataInicio=funcionario.DataAdmissao,
                    DataFim=None  # Cargo atual
                )
                historicos.append(historico)
            
            for historico in historicos:
                session.add(historico)
            session.commit()
            print(f"   ✅ {len(historicos)} registros de histórico criados!")
            
            print("\n⏰ 4. Criando Presenças...")
            presencas = []
            for i, funcionario in enumerate(funcionarios):
                # Criar 3 registros de presença para cada funcionário
                for dia in range(1, 4):
                    presenca = Presenca(
                        FuncionarioID=funcionario.FuncionarioID,
                        Data=date(2024, 9, dia),
                        HoraEntrada=time(8, 0, 0),
                        HoraSaida=time(17, 0, 0),
                        Observacao=f"Presença normal - Dia {dia}"
                    )
                    presencas.append(presenca)
            
            for presenca in presencas:
                session.add(presenca)
            session.commit()
            print(f"   ✅ {len(presencas)} registros de presença criados!")
            
            print("\n🎁 5. Criando Benefícios...")
            beneficios = [
                Beneficio(
                    Nome="Seguro de Saúde",
                    Descricao="Seguro médico e hospitalar",
                    Tipo="Saúde"
                ),
                Beneficio(
                    Nome="Vale Refeição",
                    Descricao="Subsídio para alimentação",
                    Tipo="Alimentação"
                ),
                Beneficio(
                    Nome="Subsídio de Transporte",
                    Descricao="Subsídio para transporte público",
                    Tipo="Transporte"
                )
            ]
            
            for beneficio in beneficios:
                session.add(beneficio)
            session.commit()
            print(f"   ✅ {len(beneficios)} tipos de benefícios criados!")
            
            print("\n🔗 Associando benefícios aos funcionários...")
            funcionario_beneficios = []
            for i, funcionario in enumerate(funcionarios):
                beneficio = beneficios[i]  # Associar cada funcionário a um benefício diferente
                
                func_ben = FuncionarioBeneficio(
                    FuncionarioID=funcionario.FuncionarioID,
                    BeneficioID=beneficio.BeneficioID,
                    DataInicio=date(2024, 1, 1),
                    DataFim=date(2024, 12, 31),
                    Estado="Activo"
                )
                funcionario_beneficios.append(func_ben)
            
            for fb in funcionario_beneficios:
                session.add(fb)
            session.commit()
            print(f"   ✅ {len(funcionario_beneficios)} associações funcionário-benefício criadas!")
            
            print("\n💰 6. Criando Folhas Salariais...")
            folhas = []
            salarios_base = [120000.00, 180000.00, 200000.00]  # Salários diferentes por nível
            
            for i, funcionario in enumerate(funcionarios):
                salario_base = salarios_base[i]
                
                folha = FolhaSalarial(
                    FuncionarioID=funcionario.FuncionarioID,
                    PeriodoInicio=date(2024, 9, 1),
                    PeriodoFim=date(2024, 9, 30),
                    SalarioBase=salario_base,
                    Bonificacoes=salario_base * 0.1,  # 10% de bonificações
                    Descontos=salario_base * 0.15,  # 15% de descontos
                    DataPagamento=date(2024, 10, 5)
                )
                folhas.append(folha)
            
            for folha in folhas:
                session.add(folha)
            session.commit()
            print(f"   ✅ {len(folhas)} folhas salariais criadas!")
            
            print("\n🎉 Dados completos criados com sucesso!")
            print("\n📊 Resumo final dos dados:")
            print(f"   • Departamentos: {session.query(Departamento).count()}")
            print(f"   • Cargos: {session.query(Cargo).count()}")
            print(f"   • Funcionários: {session.query(Funcionario).count()}")
            print(f"   • Histórico Cargo-Funcionário: {session.query(HistoricoCargoFuncionario).count()}")
            print(f"   • Presenças: {session.query(Presenca).count()}")
            print(f"   • Benefícios: {session.query(Beneficio).count()}")
            print(f"   • Funcionário-Benefícios: {session.query(FuncionarioBeneficio).count()}")
            print(f"   • Folhas Salariais: {session.query(FolhaSalarial).count()}")
            
            return True
            
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao criar dados: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()

if __name__ == "__main__":
    print("🔄 Limpeza e Reinicialização Completa IAMC")
    print("=" * 60)
    
    # 1. Limpar dados existentes
    if limpar_dados_iamc():
        print("\n🔄 Limpeza concluída! Criando novos dados...")
        
        # 2. Criar dados completos
        if criar_dados_completos():
            print("\n✅ Reinicialização concluída com sucesso!")
            print("\n🧪 Agora você pode testar todos os endpoints IAMC:")
            print("   • GET /api/iamc/funcionarios")
            print("   • GET /api/iamc/departamentos") 
            print("   • GET /api/iamc/cargos")
            print("   • GET /api/iamc/presencas")
            print("   • GET /api/iamc/beneficios")
            print("   • GET /api/iamc/funcionario-beneficios")
            print("   • GET /api/iamc/folha-salarial")
        else:
            print("\n❌ Falha na criação dos novos dados!")
    else:
        print("\n❌ Falha na limpeza dos dados!")
    
    print("\n" + "=" * 60)
