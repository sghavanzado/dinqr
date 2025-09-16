#!/usr/bin/env python3
"""
Test básico de conexão SQL Server com pyodbc
"""

import pyodbc
import sys

def test_sql_server():
    """Test básico do SQL Server"""
    print("=" * 60)
    print("TESTE BÁSICO SQL SERVER")
    print("=" * 60)
    
    try:
        # 1. Listar drivers ODBC disponíveis
        print("\n1. Drivers ODBC disponíveis:")
        drivers = pyodbc.drivers()
        for driver in drivers:
            print(f"   - {driver}")
        
        # 2. Tentar conectar
        print("\n2. Tentando conectar ao SQL Server...")
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=IAMC;"
            "UID=sa;"
            "PWD=Global2020;"
            "TrustServerCertificate=yes"
        )
        
        conn = pyodbc.connect(connection_string, timeout=10)
        print("✅ Conexão estabelecida com sucesso!")
        
        # 3. Testar query simples
        print("\n3. Testando query básica...")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"✅ Query OK: {result}")
        
        # 4. Verificar se database IAMC existe
        print("\n4. Verificando database IAMC...")
        cursor.execute("SELECT DB_NAME() as current_db")
        db_name = cursor.fetchone()[0]
        print(f"✅ Database atual: {db_name}")
        
        # 5. Listar tabelas
        print("\n5. Listando tabelas...")
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = cursor.fetchall()
        print(f"Total de tabelas: {len(tables)}")
        for table in tables[:10]:  # Mostrar só as primeiras 10
            print(f"   - {table[0]}")
        
        # 6. Verificar tabela Funcionarios especificamente
        print("\n6. Verificando tabela Funcionarios...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Funcionarios'
        """)
        funcionarios_table_exists = cursor.fetchone()[0]
        
        if funcionarios_table_exists > 0:
            print("✅ Tabela Funcionarios existe")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM Funcionarios")
            count = cursor.fetchone()[0]
            print(f"✅ Total funcionários: {count}")
            
            if count > 0:
                # Listar alguns registros
                cursor.execute("""
                    SELECT TOP 3 FuncionarioID, Nome, Apelido 
                    FROM Funcionarios 
                    ORDER BY FuncionarioID
                """)
                funcionarios = cursor.fetchall()
                print("Primeiros funcionários:")
                for func in funcionarios:
                    print(f"   - {func[0]}: {func[1]} {func[2]}")
        else:
            print("❌ Tabela Funcionarios NÃO existe")
        
        conn.close()
        print("\n✅ Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sql_server()
    sys.exit(0 if success else 1)
