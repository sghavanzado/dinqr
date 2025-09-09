#!/usr/bin/env python3
"""
Script para agregar la columna Foto a la tabla Funcionarios.
"""

from flask import Flask
from config import Config
from extensions import init_iamc_db, IAMCSession
import pyodbc
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def adicionar_coluna_foto():
    """
    Adiciona a coluna Foto à tabela Funcionarios no SQL Server.
    """
    try:
        # Inicializar Flask app
        app = Flask(__name__)
        app.config.from_object(Config)
        
        with app.app_context():
            # Inicializar conexão IAMC
            success = init_iamc_db(app)
            if not success:
                print("❌ Erro ao inicializar IAMC")
                return False
            
            session = IAMCSession()
            
            print("🔧 Adicionando coluna Foto à tabela Funcionarios...")
            
            # Executar ALTER TABLE para adicionar a coluna
            sql_add_column = """
            ALTER TABLE Funcionarios 
            ADD Foto NVARCHAR(255) NULL
            """
            
            # Executar diretamente no SQL Server
            connection = session.get_bind().raw_connection()
            cursor = connection.cursor()
            
            try:
                cursor.execute(sql_add_column)
                connection.commit()
                print("   ✅ Coluna Foto adicionada com sucesso!")
                
                # Verificar se a coluna foi criada
                cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'Funcionarios' AND COLUMN_NAME = 'Foto'
                """)
                
                result = cursor.fetchone()
                if result:
                    print(f"   📋 Detalhes da coluna: {result[0]} ({result[1]}, Nullable: {result[2]})")
                else:
                    print("   ⚠️ Não foi possível verificar a coluna criada")
                
                return True
                
            except pyodbc.Error as e:
                if "already exists" in str(e) or "duplicate column name" in str(e).lower():
                    print("   ℹ️ Coluna Foto já existe na tabela!")
                    return True
                else:
                    raise e
            finally:
                cursor.close()
                connection.close()
            
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_estrutura_tabela():
    """
    Verifica a estrutura atual da tabela Funcionarios.
    """
    try:
        app = Flask(__name__)
        app.config.from_object(Config)
        
        with app.app_context():
            success = init_iamc_db(app)
            if not success:
                print("❌ Erro ao inicializar IAMC")
                return False
            
            session = IAMCSession()
            connection = session.get_bind().raw_connection()
            cursor = connection.cursor()
            
            print("\n📋 Estrutura atual da tabela Funcionarios:")
            cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'Funcionarios'
            ORDER BY ORDINAL_POSITION
            """)
            
            columns = cursor.fetchall()
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                max_length = f"({col[3]})" if col[3] else ""
                print(f"   • {col[0]}: {col[1]}{max_length} {nullable}")
            
            cursor.close()
            connection.close()
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Migração IAMC - Adição da Coluna Foto")
    print("=" * 50)
    
    # 1. Verificar estrutura atual
    print("1️⃣ Verificando estrutura atual...")
    verificar_estrutura_tabela()
    
    # 2. Adicionar coluna
    print("\n2️⃣ Adicionando coluna Foto...")
    if adicionar_coluna_foto():
        print("\n3️⃣ Verificando estrutura após migração...")
        verificar_estrutura_tabela()
        
        print("\n✅ Migração concluída com sucesso!")
        print("\n🧪 Agora você pode testar:")
        print("   • Upload de fotos via POST /api/iamc/funcionarios/{id}/foto")
        print("   • Visualização de dados com campo Foto")
        print("   • Todos os endpoints de funcionários incluindo foto")
    else:
        print("\n❌ Falha na migração!")
    
    print("\n" + "=" * 50)
