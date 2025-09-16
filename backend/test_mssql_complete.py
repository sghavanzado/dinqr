#!/usr/bin/env python3
"""
Script de verificación completa para SQL Server (MSSQL)
Verifica todas las funcionalidades críticas y posibles incompatibilidades
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario, Departamento, Cargo, HistoricoCargoFuncionario
from models.iamc_presencas_new import Presenca, Licenca, Formacao, AvaliacaoDesempenho
from sqlalchemy import func, text
from datetime import datetime, date, time
import json

def test_database_connection():
    """Teste básico de conexão"""
    print("=== TESTE DE CONEXÃO SQL SERVER ===")
    session = IAMCSession()
    try:
        # Teste simples de conexão
        result = session.execute(text("SELECT @@VERSION")).fetchone()
        print(f"✓ Conexão SQL Server estabelecida")
        print(f"✓ Versão: {result[0][:100]}...")
        return True
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    finally:
        session.close()

def test_basic_queries():
    """Teste consultas básicas"""
    print("\n=== TESTE DE CONSULTAS BÁSICAS ===")
    session = IAMCSession()
    try:
        # Teste contagem de registros
        func_count = session.query(Funcionario).count()
        dept_count = session.query(Departamento).count()
        cargo_count = session.query(Cargo).count()
        
        print(f"✓ Funcionários: {func_count}")
        print(f"✓ Departamentos: {dept_count}")
        print(f"✓ Cargos: {cargo_count}")
        
        # Teste paginação com ORDER BY (obrigatório no SQL Server)
        funcionarios = session.query(Funcionario).order_by(Funcionario.FuncionarioID).limit(5).all()
        print(f"✓ Paginação: {len(funcionarios)} funcionários retornados")
        
        return True
    except Exception as e:
        print(f"❌ Erro em consultas básicas: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def test_date_time_functions():
    """Teste funções de data/hora específicas do SQL Server"""
    print("\n=== TESTE DE FUNÇÕES DATA/HORA ===")
    session = IAMCSession()
    try:
        # Teste func.year, func.month (compatível com SQL Server)
        test_query = session.query(
            func.year(Funcionario.DataAdmissao).label('ano'),
            func.month(Funcionario.DataAdmissao).label('mes'),
            func.count(Funcionario.FuncionarioID).label('total')
        ).group_by(
            func.year(Funcionario.DataAdmissao),
            func.month(Funcionario.DataAdmissao)
        ).all()
        
        print(f"✓ Funções YEAR/MONTH: {len(test_query)} resultados")
        for item in test_query:
            print(f"  - {item.ano}-{item.mes:02d}: {item.total} funcionários")
        
        # Teste de data atual
        current_date = session.execute(text("SELECT GETDATE()")).fetchone()
        print(f"✓ Data atual SQL Server: {current_date[0]}")
        
        return True
    except Exception as e:
        print(f"❌ Erro em funções de data: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def test_aggregation_functions():
    """Teste funções de agregação"""
    print("\n=== TESTE DE FUNÇÕES DE AGREGAÇÃO ===")
    session = IAMCSession()
    try:
        # Teste COUNT, GROUP BY
        estados = session.query(
            Funcionario.EstadoFuncionario,
            func.count(Funcionario.FuncionarioID)
        ).group_by(Funcionario.EstadoFuncionario).all()
        
        print(f"✓ GROUP BY/COUNT: {len(estados)} estados diferentes")
        for estado, count in estados:
            print(f"  - {estado}: {count}")
        
        # Teste JOINs com agregação
        departamentos = session.query(
            Departamento.Nome,
            func.count(HistoricoCargoFuncionario.FuncionarioID)
        ).join(
            HistoricoCargoFuncionario,
            Departamento.DepartamentoID == HistoricoCargoFuncionario.DepartamentoID
        ).filter(
            HistoricoCargoFuncionario.DataFim.is_(None)
        ).group_by(Departamento.Nome).all()
        
        print(f"✓ JOINs com agregação: {len(departamentos)} departamentos")
        for nome, count in departamentos:
            print(f"  - {nome}: {count}")
        
        return True
    except Exception as e:
        print(f"❌ Erro em agregações: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def test_data_types():
    """Teste tipos de dados específicos"""
    print("\n=== TESTE DE TIPOS DE DADOS ===")
    session = IAMCSession()
    try:
        # Teste tipos de dados comuns
        funcionario = session.query(Funcionario).first()
        if funcionario:
            print(f"✓ String: {funcionario.Nome} (tipo: {type(funcionario.Nome)})")
            print(f"✓ Date: {funcionario.DataAdmissao} (tipo: {type(funcionario.DataAdmissao)})")
            if funcionario.DataNascimento:
                print(f"✓ Date nullable: {funcionario.DataNascimento} (tipo: {type(funcionario.DataNascimento)})")
        
        # Teste Boolean (BIT no SQL Server)
        formacao = session.query(Formacao).first()
        if formacao:
            print(f"✓ Boolean/BIT: {formacao.Certificado} (tipo: {type(formacao.Certificado)})")
        
        # Teste Time
        presenca = session.query(Presenca).first()
        if presenca:
            if presenca.HoraEntrada:
                print(f"✓ Time: {presenca.HoraEntrada} (tipo: {type(presenca.HoraEntrada)})")
        
        return True
    except Exception as e:
        print(f"❌ Erro em tipos de dados: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def test_crud_operations():
    """Teste operações CRUD"""
    print("\n=== TESTE DE OPERAÇÕES CRUD ===")
    session = IAMCSession()
    try:
        # Teste INSERT (sem executar, apenas preparar)
        test_dept = Departamento(
            Nome='Teste MSSQL',
            Descricao='Departamento de teste para SQL Server'
        )
        
        # Verificar se a estrutura está correta
        dict_test = test_dept.to_dict()
        print(f"✓ Estrutura to_dict(): {dict_test}")
        
        # Não vamos inserir realmente para não alterar dados
        print("✓ Estruturas CRUD verificadas (sem execução real)")
        
        return True
    except Exception as e:
        print(f"❌ Erro em operações CRUD: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def test_specific_sql_server_features():
    """Teste características específicas do SQL Server"""
    print("\n=== TESTE DE CARACTERÍSTICAS ESPECÍFICAS SQL SERVER ===")
    session = IAMCSession()
    try:
        # Teste TOP (específico SQL Server, mas SQLAlchemy converte limit() automaticamente)
        top_funcionarios = session.query(Funcionario).order_by(Funcionario.FuncionarioID).limit(3).all()
        print(f"✓ TOP/LIMIT: {len(top_funcionarios)} registros")
        
        # Teste OFFSET/FETCH (SQL Server 2012+)
        offset_funcionarios = session.query(Funcionario).order_by(Funcionario.FuncionarioID).offset(1).limit(2).all()
        print(f"✓ OFFSET/FETCH: {len(offset_funcionarios)} registros")
        
        # Teste IDENTITY (auto-increment)
        max_id = session.query(func.max(Funcionario.FuncionarioID)).scalar()
        print(f"✓ IDENTITY/Auto-increment: Max ID = {max_id}")
        
        # Teste filtros com IS NULL
        null_count = session.query(Funcionario).filter(Funcionario.DataNascimento.is_(None)).count()
        print(f"✓ IS NULL: {null_count} registros com DataNascimento NULL")
        
        return True
    except Exception as e:
        print(f"❌ Erro em características SQL Server: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def main():
    """Execução principal dos testes"""
    print("VERIFICAÇÃO COMPLETA SQL SERVER (MSSQL)")
    print("=" * 50)
    
    tests = [
        ("Conexão", test_database_connection),
        ("Consultas Básicas", test_basic_queries),
        ("Funções Data/Hora", test_date_time_functions),
        ("Funções Agregação", test_aggregation_functions),
        ("Tipos de Dados", test_data_types),
        ("Operações CRUD", test_crud_operations),
        ("Características SQL Server", test_specific_sql_server_features)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} testes passaram")
    
    if passed == len(results):
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Configuração SQL Server está CORRETA")
    else:
        print(f"\n⚠️  {len(results) - passed} testes falharam")
        print("❌ Revisar configuração SQL Server")

if __name__ == '__main__':
    main()
