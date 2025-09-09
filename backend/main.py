#!/usr/bin/env python3
"""
DINQR Backend - Punto de Entrada Principal
==========================================

Este archivo actúa como punto de entrada único para el backend DINQR.
Puede ejecutarse como:
1. Aplicación normal (servidor web)
2. Servicio de Windows
3. Modo debug/desarrollo

Uso:
    generadorqr.exe                    # Servidor web normal
    generadorqr.exe --service install  # Instalar como servicio
    generadorqr.exe --service start    # Iniciar servicio
    generadorqr.exe --service stop     # Detener servicio
    generadorqr.exe --service remove   # Remover servicio
    generadorqr.exe --service status   # Estado del servicio
    generadorqr.exe --debug            # Modo debug
"""

import sys
import os
import argparse
from pathlib import Path

# Añadir el directorio actual al path para importaciones
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

def main():
    """Punto de entrada principal"""
    parser = argparse.ArgumentParser(
        description='DINQR Backend - Generador de Códigos QR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--service',
        choices=['install', 'remove', 'start', 'stop', 'restart', 'status'],
        help='Operaciones del servicio de Windows'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Ejecutar en modo debug'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Puerto del servidor (por defecto: 5000)'
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host del servidor (por defecto: 127.0.0.1)'
    )
    
    # Verificar si se ejecuta sin argumentos (comportamiento por defecto)
    if len(sys.argv) == 1:
        # Verificar si se está ejecutando como servicio de Windows
        try:
            import win32serviceutil
            # Si es un servicio, manejar con Windows Service
            if hasattr(sys, 'frozen') and '--service' not in sys.argv:
                # Es un ejecutable y no tiene argumentos de servicio
                # Ejecutar como servidor normal
                run_server()
                return
        except ImportError:
            # pywin32 no disponible, ejecutar como servidor normal
            pass
        
        # Ejecutar servidor normal
        run_server()
        return
    
    args = parser.parse_args()
    
    # Manejar operaciones de servicio
    if args.service:
        handle_service_command(args.service)
        return
    
    # Manejar modo debug
    if args.debug:
        run_debug_server(args.host, args.port)
        return
    
    # Ejecutar servidor normal
    run_server(args.host, args.port)

def run_server(host='127.0.0.1', port=5000):
    """Ejecutar el servidor web normal con Waitress"""
    try:
        from waitress import serve
        from app import create_app
        
        print(f"🚀 Iniciando DINQR Backend en http://{host}:{port}")
        print("📚 Documentación API: http://127.0.0.1:5000/apidocs/")
        print("❤️  Health Check: http://127.0.0.1:5000/health")
        print("⏹️  Presiona Ctrl+C para detener el servidor")
        print("=" * 60)
        
        app = create_app()
        serve(app, host=host, port=port)
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Verifique que todas las dependencias estén instaladas")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        sys.exit(1)

def run_debug_server(host='127.0.0.1', port=5000):
    """Ejecutar el servidor en modo debug"""
    try:
        from app import create_app
        
        print(f"🐛 Iniciando DINQR Backend en modo DEBUG en http://{host}:{port}")
        print("⚠️  ADVERTENCIA: Modo debug habilitado")
        print("⏹️  Presiona Ctrl+C para detener el servidor")
        print("=" * 60)
        
        app = create_app()
        app.run(host=host, port=port, debug=True)
        
    except Exception as e:
        print(f"❌ Error al iniciar el servidor debug: {e}")
        sys.exit(1)

def handle_service_command(command):
    """Manejar comandos del servicio de Windows"""
    try:
        # Verificar si pywin32 está disponible
        import win32serviceutil
        import win32service
        
        from windows_service import ServiceManager, DINQRWindowsService
        
        print(f"🔧 Ejecutando comando de servicio: {command}")
        
        if command == 'install':
            if ServiceManager.install_service():
                print("✅ Servicio instalado correctamente")
                print("💡 Use 'generadorqr.exe --service start' para iniciarlo")
            else:
                print("❌ Error al instalar el servicio")
                sys.exit(1)
        
        elif command == 'remove':
            if ServiceManager.remove_service():
                print("✅ Servicio removido correctamente")
            else:
                print("❌ Error al remover el servicio")
                sys.exit(1)
        
        elif command == 'start':
            if ServiceManager.start_service():
                print("✅ Servicio iniciado correctamente")
            else:
                print("❌ Error al iniciar el servicio")
                sys.exit(1)
        
        elif command == 'stop':
            if ServiceManager.stop_service():
                print("✅ Servicio detenido correctamente")
            else:
                print("❌ Error al detener el servicio")
                sys.exit(1)
        
        elif command == 'restart':
            if ServiceManager.restart_service():
                print("✅ Servicio reiniciado correctamente")
            else:
                print("❌ Error al reiniciar el servicio")
                sys.exit(1)
        
        elif command == 'status':
            ServiceManager.service_status()
    
    except ImportError as e:
        print("❌ Error: Módulos de Windows Service no están disponibles")
        print(f"   Detalles: {e}")
        print("\n🔧 SOLUCIONES:")
        print("1. El ejecutable no fue compilado con soporte para servicios")
        print("2. Recompile el ejecutable con PyInstaller incluyendo pywin32")
        print("3. O use el modo servidor normal: generadorqr.exe")
        print("\n💡 ALTERNATIVA: Ejecutar como aplicación normal")
        print("   generadorqr.exe  # Servidor web normal")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error en operación de servicio: {e}")
        sys.exit(1)

def check_windows_service():
    """Verificar si se está ejecutando como servicio de Windows"""
    try:
        import win32serviceutil
        import servicemanager
        from windows_service import DINQRWindowsService
        
        # Si no hay argumentos y se está ejecutando desde el Service Manager
        if len(sys.argv) == 1:
            try:
                # Intentar inicializar como servicio
                servicemanager.Initialize()
                servicemanager.PrepareToHostSingle(DINQRWindowsService)
                servicemanager.StartServiceCtrlDispatcher()
                return True
            except:
                # No es un servicio, continuar como aplicación normal
                return False
        
        # Verificar argumentos de servicio específicos
        if len(sys.argv) > 1 and sys.argv[1] in ['install', 'remove', 'start', 'stop', 'restart', 'debug']:
            win32serviceutil.HandleCommandLine(DINQRWindowsService)
            return True
        
        return False
        
    except ImportError:
        return False

if __name__ == '__main__':
    # Verificar primero si es un servicio de Windows
    if check_windows_service():
        sys.exit(0)
    
    # Si no, ejecutar la aplicación normal
    main()
