#!/usr/bin/env python3
"""
Script para asignar cargos y departamentos a los funcionarios existentes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from config import Config

def assign_cargo_departamento():
    """Asignar cargos y departamentos a funcionarios existentes"""
    
    engine = create_engine(Config.IAMC_SQLALCHEMY_DATABASE_URI, echo=True)
    
    try:
        with engine.connect() as connection:
            print("🔄 Asignando cargos y departamentos a funcionarios existentes...")
            
            # Obtener funcionarios
            result = connection.execute(text("SELECT FuncionarioID, Nome FROM Funcionarios"))
            funcionarios = result.fetchall()
            
            # Obtener departamentos
            result = connection.execute(text("SELECT DepartamentoID, Nome FROM Departamentos"))
            departamentos = result.fetchall()
            
            # Obtener cargos
            result = connection.execute(text("SELECT CargoID, Nome FROM Cargos"))
            cargos = result.fetchall()
            
            print(f"📋 Funcionarios: {len(funcionarios)}")
            print(f"📋 Departamentos: {len(departamentos)}")
            print(f"📋 Cargos: {len(cargos)}")
            
            if funcionarios and departamentos and cargos:
                # Asignar cada funcionario a un departamento y cargo
                for i, funcionario in enumerate(funcionarios):
                    funcionario_id = funcionario[0]
                    funcionario_nome = funcionario[1]
                    
                    # Asignar de forma rotatoria
                    dept_index = i % len(departamentos)
                    cargo_index = i % len(cargos)
                    
                    dept_id = departamentos[dept_index][0]
                    cargo_id = cargos[cargo_index][0]
                    
                    # Actualizar funcionario
                    connection.execute(text("""
                        UPDATE Funcionarios 
                        SET DepartamentoID = :dept_id, CargoID = :cargo_id 
                        WHERE FuncionarioID = :func_id
                    """), {
                        'dept_id': dept_id,
                        'cargo_id': cargo_id,
                        'func_id': funcionario_id
                    })
                    
                    print(f"✅ {funcionario_nome}: Departamento={departamentos[dept_index][1]}, Cargo={cargos[cargo_index][1]}")
                
                # Confirmar cambios
                connection.commit()
                print("✅ Asignación completada exitosamente!")
            else:
                print("⚠️ No hay datos suficientes para asignar")
                
    except Exception as e:
        print(f"❌ Error durante la asignación: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Iniciando asignación de cargos y departamentos...")
    
    success = assign_cargo_departamento()
    
    if success:
        print("✅ Asignación completada exitosamente!")
        sys.exit(0)
    else:
        print("❌ Asignación falló!")
        sys.exit(1)
