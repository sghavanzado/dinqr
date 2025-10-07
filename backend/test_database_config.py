#!/usr/bin/env python3
"""
Test script to check database connection and table creation for passes configuration
"""

import sys
import os
import logging

# Add the backend directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.db_utils import obtener_conexion_local

def test_database_connection():
    """Test database connection and table creation"""
    try:
        print("Testing database connection...")
        
        # Test connection
        conn = obtener_conexion_local()
        cursor = conn.cursor()
        
        print("✅ Database connection successful!")
        
        # Check if tables exist
        print("\nChecking if configuration tables exist...")
        
        # Check for pass_temas_avancado table
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'pass_temas_avancado'
        """)
        temas_table_exists = cursor.fetchone()[0] > 0
        print(f"pass_temas_avancado table exists: {temas_table_exists}")
        
        # Check for pass_formatos_avancado table
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'pass_formatos_avancado'
        """)
        formatos_table_exists = cursor.fetchone()[0] > 0
        print(f"pass_formatos_avancado table exists: {formatos_table_exists}")
        
        if not temas_table_exists or not formatos_table_exists:
            print("\n⚠️  Some tables are missing. This might be causing the 500 error.")
            print("Attempting to create tables...")
            
            try:
                # Try to create the tables
                create_tables(cursor)
                conn.commit()
                print("✅ Tables created successfully!")
            except Exception as create_error:
                print(f"❌ Error creating tables: {create_error}")
        else:
            print("\n✅ All required tables exist!")
            
            # Check if there's any data
            cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado")
            temas_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM pass_formatos_avancado")
            formatos_count = cursor.fetchone()[0]
            
            print(f"Themes in database: {temas_count}")
            print(f"Formats in database: {formatos_count}")
            
            if temas_count == 0 or formatos_count == 0:
                print("\n⚠️  No data found in tables. Adding default data...")
                add_default_data(cursor)
                conn.commit()
                print("✅ Default data added!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()

def create_tables(cursor):
    """Create the configuration tables"""
    
    # Create themes table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pass_temas_avancado' AND xtype='U')
        CREATE TABLE pass_temas_avancado (
            id INT IDENTITY(1,1) PRIMARY KEY,
            nome NVARCHAR(100) NOT NULL UNIQUE,
            cor_primaria NVARCHAR(7) NOT NULL DEFAULT '#1976d2',
            cor_secundaria NVARCHAR(7) DEFAULT '#ffffff',
            cor_texto NVARCHAR(7) DEFAULT '#000000',
            cor_borda NVARCHAR(7) DEFAULT '#cccccc',
            layout_tipo NVARCHAR(20) DEFAULT 'horizontal',
            margem_superior FLOAT DEFAULT 5.0,
            margem_inferior FLOAT DEFAULT 5.0,
            margem_esquerda FLOAT DEFAULT 5.0,
            margem_direita FLOAT DEFAULT 5.0,
            fonte_titulo NVARCHAR(50) DEFAULT 'Helvetica-Bold',
            tamanho_fonte_titulo INT DEFAULT 12,
            fonte_nome NVARCHAR(50) DEFAULT 'Helvetica-Bold',
            tamanho_fonte_nome INT DEFAULT 10,
            fonte_cargo NVARCHAR(50) DEFAULT 'Helvetica',
            tamanho_fonte_cargo INT DEFAULT 8,
            fonte_info NVARCHAR(50) DEFAULT 'Helvetica',
            tamanho_fonte_info INT DEFAULT 7,
            mostrar_logo BIT DEFAULT 1,
            posicao_logo NVARCHAR(30) DEFAULT 'superior_esquerda',
            tamanho_logo FLOAT DEFAULT 15.0,
            mostrar_qr_borda BIT DEFAULT 1,
            qr_tamanho FLOAT DEFAULT 20.0,
            qr_posicao NVARCHAR(20) DEFAULT 'direita',
            fundo_tipo NVARCHAR(20) DEFAULT 'solido',
            fundo_cor NVARCHAR(7) DEFAULT '#ffffff',
            fundo_cor_gradiente NVARCHAR(7) DEFAULT '#f0f0f0',
            fundo_imagem_url NVARCHAR(255) DEFAULT '',
            fundo_opacidade FLOAT DEFAULT 1.0,
            ativo BIT DEFAULT 1,
            data_criacao DATETIME DEFAULT GETDATE(),
            data_atualizacao DATETIME DEFAULT GETDATE()
        )
    """)
    
    # Create formats table
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pass_formatos_avancado' AND xtype='U')
        CREATE TABLE pass_formatos_avancado (
            id INT IDENTITY(1,1) PRIMARY KEY,
            nome NVARCHAR(100) NOT NULL UNIQUE,
            extensao NVARCHAR(10) NOT NULL,
            descricao NVARCHAR(255),
            largura FLOAT NOT NULL,
            altura FLOAT NOT NULL,
            dpi INT DEFAULT 300,
            orientacao NVARCHAR(20) DEFAULT 'horizontal',
            qualidade INT DEFAULT 95,
            compressao BIT DEFAULT 0,
            ativo BIT DEFAULT 1,
            data_criacao DATETIME DEFAULT GETDATE(),
            data_atualizacao DATETIME DEFAULT GETDATE()
        )
    """)

def add_default_data(cursor):
    """Add default theme and format data"""
    
    # Add default theme
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM pass_temas_avancado WHERE nome = 'Tema Padrão')
        INSERT INTO pass_temas_avancado (nome, cor_primaria, cor_secundaria, cor_texto, layout_tipo)
        VALUES ('Tema Padrão', '#1976d2', '#ffffff', '#000000', 'horizontal')
    """)
    
    # Add default format
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM pass_formatos_avancado WHERE nome = 'CR80 Padrão')
        INSERT INTO pass_formatos_avancado (nome, extensao, descricao, largura, altura, dpi, orientacao)
        VALUES ('CR80 Padrão', 'pdf', 'Formato padrão CR80 para passes de funcionários', 85.6, 53.98, 300, 'horizontal')
    """)

if __name__ == "__main__":
    test_database_connection()
