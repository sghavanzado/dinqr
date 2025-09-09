"""
Script para inicializar tabelas IAMC com dados de exemplo
"""

from flask import Flask
from config import Config
from extensions import init_iamc_db, IAMCSession
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo
from models.iamc_presencas_new import Presenca, Licenca, Beneficio, FolhaSalarial, FuncionarioBeneficio
from datetime import datetime, date, time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def criar_dados_exemplo():
    """Criar dados de exemplo nas tabelas IAMC"""
    
    print("🚀 Inicializando dados de exemplo IAMC...")
    
    # Configurar Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    with app.app_context():
        # Inicializar IAMC
        success = init_iamc_db(app)
        if not success:
            print("❌ Erro ao inicializar IAMC")
            return False
        
        session = IAMCSession()
        
        try:
            print("\n📋 1. Criando Departamentos...")
            
            # Verificar se já existem departamentos
            departamentos_existentes = session.query(Departamento).count()
            if departamentos_existentes > 0:
                print(f"   ℹ️ {departamentos_existentes} departamentos já existem. Pulando criação.")
            else:
                departamentos = [
                    Departamento(
                        Nome="Tecnologia da Informação",
                        Descricao="Departamento responsável pela gestão de sistemas e infraestrutura tecnológica"
                    ),
                    Departamento(
                        Nome="Recursos Humanos", 
                        Descricao="Departamento responsável pela gestão de pessoal e benefícios"
                    ),
                    Departamento(
                        Nome="Financeiro",
                        Descricao="Departamento responsável pela gestão financeira e contabilidade"
                    )
                ]
                
                for dept in departamentos:
                    session.add(dept)
                
                session.commit()
                print(f"   ✅ {len(departamentos)} departamentos criados!")
            
            print("\n👔 2. Criando Cargos...")
            
            # Verificar se já existem cargos
            cargos_existentes = session.query(Cargo).count()
            if cargos_existentes > 0:
                print(f"   ℹ️ {cargos_existentes} cargos já existem. Pulando criação.")
            else:
                cargos = [
                    Cargo(
                        Nome="Desenvolvedor Senior",
                        Descricao="Responsável pelo desenvolvimento de sistemas e aplicações",
                        Nivel="Senior"
                    ),
                    Cargo(
                        Nome="Analista de RH",
                        Descricao="Responsável por processos de recursos humanos e recrutamento",
                        Nivel="Pleno"
                    ),
                    Cargo(
                        Nome="Contador",
                        Descricao="Responsável pela contabilidade e gestão financeira",
                        Nivel="Pleno"
                    )
                ]
                
                for cargo in cargos:
                    session.add(cargo)
                
                session.commit()
                print(f"   ✅ {len(cargos)} cargos criados!")
            
            print("\n👥 3. Criando Funcionários...")
            
            # Verificar se já existem funcionários
            funcionarios_existentes = session.query(Funcionario).count()
            if funcionarios_existentes > 0:
                print(f"   ℹ️ {funcionarios_existentes} funcionários já existem. Pulando criação.")
            else:
                # Buscar departamentos e cargos criados
                dept_ti = session.query(Departamento).filter(Departamento.Nome == "Tecnologia da Informação").first()
                dept_rh = session.query(Departamento).filter(Departamento.Nome == "Recursos Humanos").first()
                dept_fin = session.query(Departamento).filter(Departamento.Nome == "Financeiro").first()
                
                cargo_dev = session.query(Cargo).filter(Cargo.Nome == "Desenvolvedor Senior").first()
                cargo_rh = session.query(Cargo).filter(Cargo.Nome == "Analista de RH").first()
                cargo_cont = session.query(Cargo).filter(Cargo.Nome == "Contador").first()
                
                funcionarios = [
                    Funcionario(
                        Nome="João Silva",
                        Apelido="Silva",
                        BI="123456789LA041",
                        DataNascimento=date(1990, 5, 15),
                        Sexo="M",
                        EstadoCivil="Solteiro",
                        Email="joao.silva@empresa.com",
                        Telefone="+244 923 456 789",
                        Endereco="Rua da Paz, 123, Luanda",
                        DataAdmissao=date(2024, 1, 15),
                        EstadoFuncionario="Activo"
                    ),
                    Funcionario(
                        Nome="Maria Santos",
                        Apelido="Santos", 
                        BI="987654321LA042",
                        DataNascimento=date(1985, 8, 22),
                        Sexo="F",
                        EstadoCivil="Casada",
                        Email="maria.santos@empresa.com",
                        Telefone="+244 912 345 678",
                        Endereco="Avenida Marginal, 456, Luanda",
                        DataAdmissao=date(2023, 6, 10),
                        EstadoFuncionario="Activo"
                    ),
                    Funcionario(
                        Nome="Carlos Mendes",
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
            
            print("\n⏰ 4. Criando Presenças...")
            
            # Verificar se já existem presenças
            presencas_existentes = session.query(Presenca).count()
            if presencas_existentes > 0:
                print(f"   ℹ️ {presencas_existentes} presenças já existem. Pulando criação.")
            else:
                # Buscar funcionários criados
                funcionarios = session.query(Funcionario).limit(3).all()
                
                if funcionarios:
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
                else:
                    print("   ⚠️ Nenhum funcionário encontrado para criar presenças")
            
            print("\n🎁 5. Criando Benefícios...")
            
            # Verificar se já existem benefícios
            beneficios_existentes = session.query(Beneficio).count()
            if beneficios_existentes > 0:
                print(f"   ℹ️ {beneficios_existentes} benefícios já existem. Pulando criação.")
            else:
                # Primeiro criar os tipos de benefícios
                beneficios = [
                    Beneficio(
                        Nome="Seguro de Saúde",
                        Descricao="Seguro de saúde completo para funcionários",
                        Tipo="Saúde"
                    ),
                    Beneficio(
                        Nome="Vale Alimentação",
                        Descricao="Vale alimentação mensal",
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
                
                # Agora associar benefícios aos funcionários
                funcionarios = session.query(Funcionario).limit(3).all()
                if funcionarios:
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
                else:
                    print("   ⚠️ Nenhum funcionário encontrado para associar benefícios")
            
            print("\n💰 6. Criando Folhas Salariais...")
            
            # Verificar se já existem folhas salariais
            folhas_existentes = session.query(FolhaSalarial).count()
            if folhas_existentes > 0:
                print(f"   ℹ️ {folhas_existentes} folhas salariais já existem. Pulando criação.")
            else:
                funcionarios = session.query(Funcionario).limit(3).all()
                
                if funcionarios:
                    folhas = []
                    for funcionario in funcionarios:
                        # Definir salário base fixo
                        salario_base = 150000.00
                        
                        folha = FolhaSalarial(
                            FuncionarioID=funcionario.FuncionarioID,
                            PeriodoInicio=date(2024, 9, 1),
                            PeriodoFim=date(2024, 9, 30),
                            SalarioBase=salario_base,
                            Bonificacoes=salario_base * 0.1,  # 10% de bonificações
                            Descontos=salario_base * 0.15,  # 15% de descontos (impostos, etc.)
                            DataPagamento=date(2024, 10, 5)  # Pagamento em 5 de outubro
                        )
                        folhas.append(folha)
                    
                    for folha in folhas:
                        session.add(folha)
                    
                    session.commit()
                    print(f"   ✅ {len(folhas)} folhas salariais criadas!")
                else:
                    print("   ⚠️ Nenhum funcionário encontrado para criar folhas salariais")
            
            print("\n🎉 Dados de exemplo criados com sucesso!")
            print("\n📊 Resumo dos dados criados:")
            print(f"   • Departamentos: {session.query(Departamento).count()}")
            print(f"   • Cargos: {session.query(Cargo).count()}")
            print(f"   • Funcionários: {session.query(Funcionario).count()}")
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
    print("🔄 Inicializador de Dados IAMC")
    print("=" * 50)
    
    sucesso = criar_dados_exemplo()
    
    if sucesso:
        print("\n✅ Inicialização concluída com sucesso!")
        print("\n🧪 Agora você pode testar os endpoints IAMC:")
        print("   • GET /api/iamc/funcionarios")
        print("   • GET /api/iamc/departamentos")
        print("   • GET /api/iamc/presencas")
        print("   • GET /api/iamc/beneficios")
        print("   • GET /api/iamc/folha-salarial")
    else:
        print("\n❌ Falha na inicialização!")
    
    print("\n" + "=" * 50)
