#!/usr/bin/env python3
"""
Test direto da base de dados IAMC passo a passo
"""

import os, sys
sys.path.append('.')

from config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def test_iamc_direct():
    """Test direto da base IAMC"""
    print("=" * 60)
    print("TESTE DIRETO DA BASE IAMC")
    print("=" * 60)
    
    try:
        # 1. Criar engine
        print("\n1. Criando engine SQL Server...")
        engine = create_engine(
            Config.IAMC_SQLALCHEMY_DATABASE_URI,
            echo=True,  # Mostrar SQL
            pool_pre_ping=True,
            pool_recycle=3600
        )
        print("✅ Engine criado")
        
        # 2. Testar conexão básica
        print("\n2. Testando conexão...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            print(f"✅ Conexão OK: {result.fetchone()}")
        
        # 3. Verificar se tabela existe
        print("\n3. Verificando tabela Funcionarios...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) as table_exists 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'Funcionarios'
            """))
            count = result.fetchone()[0]
            if count > 0:
                print("✅ Tabela Funcionarios existe")
            else:
                print("❌ Tabela Funcionarios NÃO existe")
                return False
        
        # 4. Contar registros
        print("\n4. Contando funcionários...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM Funcionarios"))
            count = result.fetchone()[0]
            print(f"✅ Total funcionários: {count}")
        
        # 5. Buscar alguns registros
        if count > 0:
            print("\n5. Listando primeiros 3 funcionários...")
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT TOP 3 FuncionarioID, Nome, Apelido, EstadoFuncionario 
                    FROM Funcionarios 
                    ORDER BY FuncionarioID
                """))
                for row in result:
                    print(f"   - {row[0]}: {row[1]} {row[2]} ({row[3]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_iamc_direct()
    print(f"\n{'✅ Teste passou!' if success else '❌ Teste falhou!'}")
