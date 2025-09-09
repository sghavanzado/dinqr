#!/usr/bin/env python3
"""
Script de prueba para verificar las importaciones del servicio de Windows
"""

def test_imports():
    """Probar las importaciones críticas"""
    
    print("=== PRUEBA DE IMPORTACIONES ===")
    
    # Test 1: Waitress Server
    try:
        from waitress_server import WaitressServer
        print("✅ WaitressServer importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando WaitressServer: {e}")
        return False
    
    # Test 2: Windows Service
    try:
        from windows_service import DINQRWindowsService, ServiceManager
        print("✅ Windows Service importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Windows Service: {e}")
        return False
    
    # Test 3: pywin32
    try:
        import win32serviceutil
        import win32service
        print("✅ pywin32 importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando pywin32: {e}")
        return False
    
    # Test 4: Configuración
    try:
        from config import ProductionConfig
        print("✅ ProductionConfig importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando ProductionConfig: {e}")
        return False
    
    # Test 5: App principal
    try:
        from app import create_app
        print("✅ create_app importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando create_app: {e}")
        return False
    
    print("\n=== PRUEBA DE INSTANCIACIÓN ===")
    
    # Test 6: Crear WaitressServer
    try:
        server = WaitressServer(ProductionConfig)
        print("✅ WaitressServer instanciado correctamente")
        print(f"   Host: {server.host}")
        print(f"   Port: {server.port}")
    except Exception as e:
        print(f"❌ Error instanciando WaitressServer: {e}")
        return False
    
    # Test 7: Crear app Flask
    try:
        app = create_app(ProductionConfig)
        print("✅ Flask app creada correctamente")
    except Exception as e:
        print(f"❌ Error creando Flask app: {e}")
        return False
    
    print("\n🎉 TODAS LAS PRUEBAS PASARON")
    return True

if __name__ == '__main__':
    import sys
    
    print("DINQR - Prueba de Importaciones")
    print("=" * 40)
    
    success = test_imports()
    
    if success:
        print("\n✅ El sistema está listo para ejecutarse como servicio")
        sys.exit(0)
    else:
        print("\n❌ Hay problemas con las importaciones")
        sys.exit(1)
