#!/usr/bin/env python3
"""
Teste para verificar se a integração do campo design está funcionando
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.routes.passes_routes import criar_tabelas_configuracao, obter_conexao_local
import json

def test_design_integration():
    """Testa a integração do campo design na tabela de temas"""
    
    print("🔧 Teste de Integração do Campo Design")
    print("="*50)
    
    try:
        # Criar tabelas (incluindo migração)
        print("1. Criando/atualizando tabelas...")
        criar_tabelas_configuracao()
        print("✅ Tabelas criadas/atualizadas com sucesso")
        
        # Conectar ao banco
        conn = obter_conexao_local()
        cursor = conn.cursor()
        
        # Verificar se o campo design existe
        print("\n2. Verificando estrutura da tabela...")
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'pass_temas_avancado' 
            ORDER BY ORDINAL_POSITION
        """)
        
        columns = cursor.fetchall()
        design_column_exists = False
        
        print("Colunas da tabela pass_temas_avancado:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
            if col[0] == 'design':
                design_column_exists = True
        
        if design_column_exists:
            print("✅ Campo 'design' encontrado na tabela!")
        else:
            print("❌ Campo 'design' NÃO encontrado na tabela!")
            return False
        
        # Testar inserção com design
        print("\n3. Testando inserção de tema com design...")
        
        design_test = {
            "id": "test-design-1",
            "name": "Tema de Teste",
            "front": [
                {
                    "id": "text1",
                    "type": "text",
                    "content": "Nome do Funcionário",
                    "x": 10,
                    "y": 20
                }
            ],
            "back": [],
            "createdAt": "2024-01-01T10:00:00Z",
            "updatedAt": "2024-01-01T10:00:00Z"
        }
        
        design_json = json.dumps(design_test)
        
        # Inserir tema de teste
        cursor.execute("""
            INSERT INTO pass_temas_avancado 
            (nome, cor_primaria, design)
            VALUES (?, ?, ?)
        """, ("Tema Teste Design", "#1976d2", design_json))
        
        tema_id = cursor.lastrowid if hasattr(cursor, 'lastrowid') else 1
        conn.commit()
        print(f"✅ Tema inserido com ID: {tema_id}")
        
        # Recuperar tema e verificar design
        print("\n4. Verificando recuperação do design...")
        cursor.execute("""
            SELECT nome, design 
            FROM pass_temas_avancado 
            WHERE nome = 'Tema Teste Design'
        """)
        
        row = cursor.fetchone()
        if row:
            nome, design_str = row
            print(f"Nome recuperado: {nome}")
            
            if design_str:
                try:
                    design_recuperado = json.loads(design_str)
                    print("Design recuperado:")
                    print(json.dumps(design_recuperado, indent=2))
                    print("✅ Design recuperado com sucesso!")
                except json.JSONDecodeError as e:
                    print(f"❌ Erro ao fazer parse do JSON: {e}")
                    return False
            else:
                print("❌ Design está vazio/nulo")
                return False
        else:
            print("❌ Tema não encontrado")
            return False
        
        # Limpar dados de teste
        print("\n5. Limpando dados de teste...")
        cursor.execute("DELETE FROM pass_temas_avancado WHERE nome = 'Tema Teste Design'")
        conn.commit()
        print("✅ Dados de teste removidos")
        
        conn.close()
        
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("A integração do campo design está funcionando corretamente.")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_design_integration()
    sys.exit(0 if success else 1)
