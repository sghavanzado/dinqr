"""
Script de teste para validar a conectividade com a base de dados IAMC existente
e verificar se nossos modelos SQLAlchemy estão alinhados com a estrutura da BD
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from config import Config

def testar_conexao_iamc():
    """Testa a conexão com a base de dados IAMC"""
    try:
        print("🔍 Testando conexão com a base de dados IAMC...")
        
        # Criar engine com a string de conexão IAMC
        engine = create_engine(Config.IAMC_SQLALCHEMY_DATABASE_URI)
        
        # Testar conexão
        with engine.connect() as connection:
            result = connection.execute(text("SELECT @@VERSION as version"))
            version = result.fetchone()
            print(f"✅ Conexão bem-sucedida!")
            print(f"📊 Versão do SQL Server: {version[0]}")
            
            # Verificar se a base de dados IAMC existe
            result = connection.execute(text("SELECT DB_NAME() as database_name"))
            db_name = result.fetchone()
            print(f"🗄️ Base de dados atual: {db_name[0]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

def verificar_tabelas_existentes():
    """Verifica quais tabelas existem na base de dados IAMC"""
    try:
        print("\n🔍 Verificando tabelas existentes na base de dados IAMC...")
        
        engine = create_engine(Config.IAMC_SQLALCHEMY_DATABASE_URI)
        inspector = inspect(engine)
        
        tabelas = inspector.get_table_names()
        print(f"📋 Tabelas encontradas ({len(tabelas)}):")
        
        tabelas_esperadas = [
            'Funcionarios', 'Departamentos', 'Cargos', 'HistoricoCargoFuncionario',
            'Contratos', 'Presencas', 'Licencas', 'Formacoes', 
            'AvaliacoesDesempenho', 'FolhaSalarial', 'Beneficios', 'FuncionarioBeneficio'
        ]
        
        for tabela in sorted(tabelas):
            status = "✅" if tabela in tabelas_esperadas else "⚠️"
            print(f"  {status} {tabela}")
        
        # Verificar tabelas em falta
        tabelas_em_falta = set(tabelas_esperadas) - set(tabelas)
        if tabelas_em_falta:
            print(f"\n⚠️ Tabelas esperadas não encontradas:")
            for tabela in sorted(tabelas_em_falta):
                print(f"  ❌ {tabela}")
        else:
            print(f"\n✅ Todas as tabelas esperadas foram encontradas!")
            
        return tabelas
        
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {str(e)}")
        return []

def verificar_estrutura_tabela(tabela_nome):
    """Verifica a estrutura de uma tabela específica"""
    try:
        print(f"\n🔍 Verificando estrutura da tabela '{tabela_nome}'...")
        
        engine = create_engine(Config.IAMC_SQLALCHEMY_DATABASE_URI)
        inspector = inspect(engine)
        
        # Obter colunas
        colunas = inspector.get_columns(tabela_nome)
        print(f"📋 Colunas ({len(colunas)}):")
        
        for coluna in colunas:
            tipo = str(coluna['type'])
            nullable = "NULL" if coluna['nullable'] else "NOT NULL"
            print(f"  - {coluna['name']}: {tipo} {nullable}")
        
        # Obter chaves primárias
        pk = inspector.get_pk_constraint(tabela_nome)
        if pk['constrained_columns']:
            print(f"🔑 Chave Primária: {', '.join(pk['constrained_columns'])}")
        
        # Obter chaves estrangeiras
        fks = inspector.get_foreign_keys(tabela_nome)
        if fks:
            print(f"🔗 Chaves Estrangeiras:")
            for fk in fks:
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura da tabela '{tabela_nome}': {str(e)}")
        return False

def testar_operacoes_basicas():
    """Testa operações básicas de leitura na base de dados"""
    try:
        print(f"\n🔍 Testando operações básicas...")
        
        engine = create_engine(Config.IAMC_SQLALCHEMY_DATABASE_URI)
        
        with engine.connect() as connection:
            # Contar registros em cada tabela
            tabelas = ['Funcionarios', 'Departamentos', 'Cargos']
            
            for tabela in tabelas:
                try:
                    result = connection.execute(text(f"SELECT COUNT(*) as total FROM {tabela}"))
                    count = result.fetchone()[0]
                    print(f"📊 {tabela}: {count} registros")
                except Exception as e:
                    print(f"⚠️ Erro ao contar registros em {tabela}: {str(e)}")
            
            # Testar uma consulta de exemplo
            try:
                result = connection.execute(text("""
                    SELECT TOP 5 FuncionarioID, Nome, Apelido, EstadoFuncionario 
                    FROM Funcionarios 
                    ORDER BY FuncionarioID
                """))
                funcionarios = result.fetchall()
                
                if funcionarios:
                    print(f"\n📋 Primeiros funcionários encontrados:")
                    for func in funcionarios:
                        print(f"  - ID: {func[0]}, Nome: {func[1]} {func[2]}, Estado: {func[3]}")
                else:
                    print(f"\n📋 Nenhum funcionário encontrado (tabela vazia)")
                    
            except Exception as e:
                print(f"⚠️ Erro ao consultar funcionários: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas operações básicas: {str(e)}")
        return False

def main():
    """Função principal do teste"""
    print("🚀 IAMC - Teste de Conectividade e Estrutura da Base de Dados")
    print("=" * 60)
    
    # Teste 1: Conexão
    if not testar_conexao_iamc():
        print("\n❌ Falha na conexão. Verifique a configuração da base de dados.")
        return False
    
    # Teste 2: Verificar tabelas
    tabelas = verificar_tabelas_existentes()
    if not tabelas:
        print("\n❌ Não foi possível listar as tabelas.")
        return False
    
    # Teste 3: Verificar estrutura de tabelas principais
    tabelas_principais = ['Funcionarios', 'Departamentos', 'Cargos']
    for tabela in tabelas_principais:
        if tabela in tabelas:
            verificar_estrutura_tabela(tabela)
    
    # Teste 4: Operações básicas
    testar_operacoes_basicas()
    
    print("\n" + "=" * 60)
    print("✅ Teste concluído! A base de dados IAMC está acessível.")
    print("\n📝 Próximos passos:")
    print("1. Execute: python app.py (para iniciar o servidor)")
    print("2. Importe a coleção do Postman: IAMC_Postman_Collection_Melhorada.json")
    print("3. Teste os endpoints começando por: GET /api/iamc/status")
    
    return True

if __name__ == "__main__":
    main()
