#!/usr/bin/env python3
"""
Test IAMC Database Connection
"""

import sys
import os
sys.path.append('.')

from app import create_app
from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario

def test_iamc_connection():
    """Test IAMC database connection"""
    print("=" * 50)
    print("TESTE DE CONEXÃO IAMC")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        try:
            print("1. Criando sessão IAMC...")
            session = IAMCSession()
            
            print("2. Contando funcionários...")
            count = session.query(Funcionario).count()
            print(f"✅ Conexão IAMC OK - Total funcionários: {count}")
            
            if count > 0:
                print("3. Listando primeiros 5 funcionários...")
                funcionarios = session.query(Funcionario).limit(5).all()
                for f in funcionarios:
                    print(f"  - {f.FuncionarioID}: {f.Nome} {f.Apelido} ({f.EstadoFuncionario})")
            else:
                print("3. Nenhum funcionário encontrado na base de dados")
            
            session.close()
            return True
            
        except Exception as e:
            print(f"❌ Erro IAMC: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_iamc_connection()
    if success:
        print("\n✅ Teste de conexão passou!")
    else:
        print("\n❌ Teste de conexão falhou!")
    sys.exit(0 if success else 1)
