"""
SIGA - Script de Prueba para Funcionalidad Cartón de Visita
============================================================

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025

Descripción:
Este script prueba todas las funcionalidades del sistema de Cartón de Visita.
"""

import requests
import json
from colorama import init, Fore, Style

# Inicializar colorama para colores en terminal
init(autoreset=True)

# Configuración
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api/business-card"

def print_header(text):
    """Imprime encabezado formateado"""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}{text}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
    """Imprime mensaje de error"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
    """Imprime mensaje informativo"""
    print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")

def test_1_listar_funcionarios_sin_carton():
    """Prueba 1: Listar funcionarios sin cartón de visita"""
    print_header("PRUEBA 1: Listar Funcionarios SIN Cartón de Visita")
    
    try:
        response = requests.get(f"{API_BASE}/funcionarios-sin-carton")
        
        if response.status_code == 200:
            funcionarios = response.json()
            print_success(f"Respuesta exitosa. Funcionarios encontrados: {len(funcionarios)}")
            
            if funcionarios:
                print_info(f"Primeros 3 funcionarios:")
                for func in funcionarios[:3]:
                    print(f"  - SAP: {func.get('id')}, Nome: {func.get('nome')}, Função: {func.get('funcao')}")
                return funcionarios[0]['id']  # Retornar primer ID para siguientes pruebas
            else:
                print_info("No hay funcionarios sin cartón")
                return None
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return None

def test_2_generar_carton(sap_id):
    """Prueba 2: Generar cartón de visita"""
    print_header(f"PRUEBA 2: Generar Cartón de Visita para SAP {sap_id}")
    
    if not sap_id:
        print_error("No hay SAP ID para probar")
        return None
    
    try:
        payload = {"ids": [sap_id]}
        response = requests.post(f"{API_BASE}/generar", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"Respuesta exitosa: {result.get('message')}")
            
            if result.get('resultados'):
                for res in result['resultados']:
                    if res.get('success'):
                        print_success(f"Cartón generado para SAP {res.get('contact_id')}")
                        print_info(f"  QR Path: {res.get('qr_path')}")
                        print_info(f"  URL: {res.get('url')}")
                        return res
                    else:
                        print_error(f"Error: {res.get('message')}")
            return result
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return None

def test_3_listar_funcionarios_con_carton():
    """Prueba 3: Listar funcionarios CON cartón de visita"""
    print_header("PRUEBA 3: Listar Funcionarios CON Cartón de Visita")
    
    try:
        response = requests.get(f"{API_BASE}/funcionarios-con-carton")
        
        if response.status_code == 200:
            funcionarios = response.json()
            print_success(f"Respuesta exitosa. Funcionarios con cartón: {len(funcionarios)}")
            
            if funcionarios:
                print_info(f"Primeros 3 funcionarios con cartón:")
                for func in funcionarios[:3]:
                    print(f"  - SAP: {func.get('id')}, Nome: {func.get('nome')}")
                    if func.get('businessCard'):
                        print(f"    Cartón creado: {func['businessCard'].get('created_at')}")
            else:
                print_info("No hay funcionarios con cartón aún")
                
            return funcionarios
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return None

def test_4_descargar_qr(sap_id):
    """Prueba 4: Descargar QR del cartón"""
    print_header(f"PRUEBA 4: Descargar QR para SAP {sap_id}")
    
    if not sap_id:
        print_error("No hay SAP ID para probar")
        return False
    
    try:
        response = requests.get(f"{API_BASE}/descargar/{sap_id}")
        
        if response.status_code == 200:
            filename = f"CV-{sap_id}_test.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print_success(f"QR descargado exitosamente: {filename}")
            return True
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def test_5_landing_page(business_card_data):
    """Prueba 5: Acceder a landing page del cartón"""
    print_header("PRUEBA 5: Verificar Landing Page")
    
    if not business_card_data or 'url' not in business_card_data:
        print_error("No hay URL del cartón para probar")
        return False
    
    try:
        url = business_card_data['url']
        print_info(f"URL del cartón: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            print_success("Landing page accesible")
            
            # Verificar contenido HTML
            if "Cartão de Visita" in response.text:
                print_success("Contenido HTML correcto (título 'Cartão de Visita' encontrado)")
            else:
                print_error("HTML no contiene título esperado")
            
            if "Guardar Contato" in response.text:
                print_success("Botón vCard presente")
            else:
                print_error("Botón vCard no encontrado")
                
            return True
        else:
            print_error(f"Error HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def test_6_eliminar_carton(sap_id):
    """Prueba 6: Eliminar cartón (opcional)"""
    print_header(f"PRUEBA 6: Eliminar Cartón para SAP {sap_id}")
    
    if not sap_id:
        print_error("No hay SAP ID para probar")
        return False
    
    print_info("¿Desea eliminar el cartón de prueba? (s/n): ")
    confirmacion = input().strip().lower()
    
    if confirmacion != 's':
        print_info("Eliminación cancelada")
        return False
    
    try:
        response = requests.delete(f"{API_BASE}/eliminar/{sap_id}")
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"Cartón eliminado: {result.get('message')}")
            return True
        elif response.status_code == 404:
            print_error("Cartón no encontrado")
            return False
        else:
            print_error(f"Error HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Excepción: {str(e)}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print(f"\n{Fore.MAGENTA}{'=' * 60}")
    print(f"{Fore.MAGENTA}SIGA - PRUEBAS DE CARTÓN DE VISITA")
    print(f"{Fore.MAGENTA}{'=' * 60}{Style.RESET_ALL}\n")
    
    print_info(f"URL Base: {BASE_URL}")
    print_info(f"API Base: {API_BASE}\n")
    
    # Prueba 1: Listar funcionarios sin cartón
    sap_id = test_1_listar_funcionarios_sin_carton()
    
    # Prueba 2: Generar cartón
    if sap_id:
        business_card_data = test_2_generar_carton(sap_id)
    else:
        print_error("No se puede continuar sin SAP ID")
        return
    
    # Prueba 3: Listar funcionarios CON cartón
    test_3_listar_funcionarios_con_carton()
    
    # Prueba 4: Descargar QR
    if sap_id:
        test_4_descargar_qr(sap_id)
    
    # Prueba 5: Landing page
    if business_card_data:
        test_5_landing_page(business_card_data)
    
    # Prueba 6: Eliminar cartón (opcional)
    if sap_id:
        test_6_eliminar_carton(sap_id)
    
    # Resumen final
    print_header("RESUMEN DE PRUEBAS")
    print_success("Todas las pruebas completadas")
    print_info("Revise los resultados arriba para ver el estado de cada prueba")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Pruebas interrumpidas por el usuario{Style.RESET_ALL}")
    except Exception as e:
        print_error(f"Error general: {str(e)}")
        import traceback
        traceback.print_exc()
