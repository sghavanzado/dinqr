"""
SIGA - Sistema Integral de Gestión de Accesos
CLI Command para ejecutar Seeders

Desarrollado por: Ing. Maikel Cuao
Fecha: 2025
Descripción: Comando CLI para ejecutar los seeders de la base de datos.
"""

from app import create_app
from extensions import db
from seeders.database_seeders import run_all_seeders, RolePermissionSeeder, UserSeeder, PrestadorSeeder
import logging
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Función principal para ejecutar seeders"""
    app = create_app()
    
    with app.app_context():
        print("\n=== SIGA Database Seeder ===\n")
        print("Opciones:")
        print("1. Ejecutar todos los seeders (sin limpiar)")
        print("2. Ejecutar todos los seeders (LIMPIANDO datos existentes)")
        print("3. Solo Roles y Permisos")
        print("4. Solo Usuarios")
        print("5. Solo Prestadores y Empresas")
        print("0. Salir")
        
        choice = input("\nSeleccione una opción: ").strip()
        
        try:
            if choice == '1':
                print("\n✓ Ejecutando todos los seeders (conservando datos existentes)...")
                run_all_seeders(clear_existing=False)
                
            elif choice == '2':
                confirm = input("\n⚠ ADVERTENCIA: Esto eliminará datos existentes. ¿Continuar? (s/n): ")
                if confirm.lower() == 's':
                    print("\n✓ Ejecutando todos los seeders (LIMPIANDO datos)...")
                    run_all_seeders(clear_existing=True)
                else:
                    print("Operación cancelada.")
                    return
                    
            elif choice == '3':
                print("\n✓ Ejecutando RolePermissionSeeder...")
                RolePermissionSeeder.run(clear_existing=False)
                
            elif choice == '4':
                count = input("¿Cuántos usuarios crear? (default: 10): ").strip()
                count = int(count) if count else 10
                print(f"\n✓ Ejecutando UserSeeder ({count} usuarios)...")
                UserSeeder.run(count=count, clear_existing=False)
                
            elif choice == '5':
                empresas = input("¿Cuántas empresas crear? (default: 5): ").strip()
                prestadores = input("¿Cuántos prestadores crear? (default: 20): ").strip()
                empresas = int(empresas) if empresas else 5
                prestadores = int(prestadores) if prestadores else 20
                print(f"\n✓ Ejecutando PrestadorSeeder ({empresas} empresas, {prestadores} prestadores)...")
                PrestadorSeeder.run(count_empresas=empresas, count_prestadores=prestadores, clear_existing=False)
                
            elif choice == '0':
                print("Saliendo...")
                return
                
            else:
                print("Opción inválida.")
                return
            
            print("\n✓ Proceso completado exitosamente!\n")
            
        except Exception as e:
            print(f"\n✗ Error: {e}\n")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()
