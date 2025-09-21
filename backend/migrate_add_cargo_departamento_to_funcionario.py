#!/usr/bin/env python3
"""
Script para agregar los campos CargoID y DepartamentoID a la tabla Funcionarios
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from config import Config

def migrate_add_cargo_departamento():
    """Agregar campos CargoID y DepartamentoID a la tabla Funcionarios"""
    
    # Crear conexión
    engine = create_engine(Config.IAMC_SQLALCHEMY_DATABASE_URI, echo=True)
    
    try:
        with engine.connect() as connection:
            print("🔄 Verificando si los campos ya existen...")
            
            # Verificar si CargoID existe
            try:
                result = connection.execute(text("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'Funcionarios' 
                    AND COLUMN_NAME = 'CargoID'
                """))
                cargo_exists = result.scalar() > 0
            except Exception as e:
                print(f"Error verificando CargoID: {e}")
                cargo_exists = False
            
            # Verificar si DepartamentoID existe
            try:
                result = connection.execute(text("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'Funcionarios' 
                    AND COLUMN_NAME = 'DepartamentoID'
                """))
                departamento_exists = result.scalar() > 0
            except Exception as e:
                print(f"Error verificando DepartamentoID: {e}")
                departamento_exists = False
            
            # Agregar CargoID si no existe
            if not cargo_exists:
                print("🔄 Agregando campo CargoID...")
                connection.execute(text("""
                    ALTER TABLE Funcionarios 
                    ADD CargoID INT NULL
                """))
                print("✅ Campo CargoID agregado exitosamente")
            else:
                print("ℹ️ Campo CargoID ya existe")
            
            # Agregar DepartamentoID si no existe
            if not departamento_exists:
                print("🔄 Agregando campo DepartamentoID...")
                connection.execute(text("""
                    ALTER TABLE Funcionarios 
                    ADD DepartamentoID INT NULL
                """))
                print("✅ Campo DepartamentoID agregado exitosamente")
            else:
                print("ℹ️ Campo DepartamentoID ya existe")
            
            # Confirmar cambios
            connection.commit()
            
            # Agregar las restricciones de clave foránea
            if not cargo_exists:
                try:
                    print("🔄 Agregando restricción de clave foránea para CargoID...")
                    connection.execute(text("""
                        ALTER TABLE Funcionarios 
                        ADD CONSTRAINT FK_Funcionarios_Cargo 
                        FOREIGN KEY (CargoID) REFERENCES Cargos(CargoID)
                    """))
                    print("✅ Restricción de clave foránea para CargoID agregada")
                except Exception as e:
                    print(f"⚠️ Error agregando FK para CargoID (puede ser normal si ya existe): {e}")
            
            if not departamento_exists:
                try:
                    print("🔄 Agregando restricción de clave foránea para DepartamentoID...")
                    connection.execute(text("""
                        ALTER TABLE Funcionarios 
                        ADD CONSTRAINT FK_Funcionarios_Departamento 
                        FOREIGN KEY (DepartamentoID) REFERENCES Departamentos(DepartamentoID)
                    """))
                    print("✅ Restricción de clave foránea para DepartamentoID agregada")
                except Exception as e:
                    print(f"⚠️ Error agregando FK para DepartamentoID (puede ser normal si ya existe): {e}")
            
            # Confirmar cambios finales
            connection.commit()
            
            print("✅ Migración completada exitosamente!")
            
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Iniciando migración para agregar CargoID y DepartamentoID a Funcionarios...")
    
    success = migrate_add_cargo_departamento()
    
    if success:
        print("✅ Migración completada exitosamente!")
        sys.exit(0)
    else:
        print("❌ Migración falló!")
        sys.exit(1)
