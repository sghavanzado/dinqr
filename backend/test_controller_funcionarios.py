#!/usr/bin/env python3
"""
Test direto do controller de funcionários
"""

import sys
sys.path.append('.')

from app import create_app
from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario
import json

def test_controller_funcionarios():
    """Test direto do controller"""
    print("=" * 60)
    print("TESTE DIRETO DO CONTROLLER")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        session = IAMCSession()
        try:
            print("1. Consultando funcionários...")
            funcionarios = session.query(Funcionario).order_by(Funcionario.FuncionarioID).limit(3).all()
            print(f"   Encontrados: {len(funcionarios)}")
            
            print("2. Convertendo para dict...")
            funcionarios_dict = []
            for i, f in enumerate(funcionarios):
                print(f"   Convertendo funcionário {i+1}: {f.Nome}")
                try:
                    func_dict = f.to_dict()
                    funcionarios_dict.append(func_dict)
                    print(f"     ✅ OK - Keys: {list(func_dict.keys())}")
                except Exception as e:
                    print(f"     ❌ Erro: {e}")
                    import traceback
                    traceback.print_exc()
            
            print("3. Criando JSON...")
            try:
                json_result = json.dumps(funcionarios_dict, ensure_ascii=False, indent=2)
                print(f"   ✅ JSON criado - {len(json_result)} chars")
                print(f"   Primeira parte: {json_result[:200]}...")
            except Exception as e:
                print(f"   ❌ Erro JSON: {e}")
            
            print("4. Simulando resposta Flask...")
            try:
                from flask import jsonify
                response_data = {
                    'success': True,
                    'funcionarios': funcionarios_dict,
                    'total': len(funcionarios_dict),
                    'page': 1,
                    'per_page': 3
                }
                response = jsonify(response_data)
                print(f"   ✅ Response Flask criada")
            except Exception as e:
                print(f"   ❌ Erro Flask response: {e}")
                import traceback
                traceback.print_exc()
                
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()

if __name__ == "__main__":
    test_controller_funcionarios()
