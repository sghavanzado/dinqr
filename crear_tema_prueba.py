#!/usr/bin/env python3
"""
Script para crear un tema de prueba con design para testing
"""

import sys
import os
import json
from datetime import datetime

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def crear_tema_prueba_con_design():
    """Crear tema de prueba con design para testing"""
    print("🔧 Creando tema de prueba con design para testing...")
    
    try:
        from routes.passes_routes import criar_tabelas_configuracao, obter_conexao_local
        
        # Crear tablas
        criar_tabelas_configuracao()
        
        # Conectar
        conn = obter_conexao_local()
        cursor = conn.cursor()
        
        # Design de ejemplo
        design_ejemplo = {
            "id": "passe-global-test",
            "name": "Passe Global Test",
            "front": [
                {
                    "id": "text-nome",
                    "type": "text",
                    "content": "{{nome}}",
                    "x": 20,
                    "y": 30,
                    "width": 200,
                    "height": 40,
                    "fontSize": 16,
                    "fontFamily": "Helvetica-Bold",
                    "fill": "#000000",
                    "asociation": "nome"
                },
                {
                    "id": "text-cargo",
                    "type": "text",
                    "content": "{{cargo}}",
                    "x": 20,
                    "y": 80,
                    "width": 180,
                    "height": 30,
                    "fontSize": 12,
                    "fontFamily": "Helvetica",
                    "fill": "#666666",
                    "asociation": "cargo"
                },
                {
                    "id": "image-logo",
                    "type": "image",
                    "x": 10,
                    "y": 10,
                    "width": 60,
                    "height": 40,
                    "src": "/static/images/sonangol-logo.png",
                    "asociation": "logo"
                },
                {
                    "id": "qr-code",
                    "type": "qr",
                    "content": "{{qr_data}}",
                    "x": 270,
                    "y": 10,
                    "size": 50,
                    "asociation": "qr_code"
                }
            ],
            "back": [
                {
                    "id": "background",
                    "type": "background",
                    "fill": "#f0f0f0"
                }
            ],
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        # Verificar si ya existe
        cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado WHERE nome = ?", ("Passe Global",))
        if cursor.fetchone()[0] > 0:
            # Actualizar
            cursor.execute("""
                UPDATE pass_temas_avancado 
                SET design = ?, data_atualizacao = GETDATE()
                WHERE nome = ?
            """, (json.dumps(design_ejemplo), "Passe Global"))
            print("✅ Tema 'Passe Global' actualizado con design de prueba")
        else:
            # Crear
            cursor.execute("""
                INSERT INTO pass_temas_avancado 
                (nome, cor_primaria, cor_secundaria, cor_texto, layout_tipo, fonte_titulo, design)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, ("Passe Global", "#1976d2", "#ffffff", "#000000", "horizontal", "Helvetica-Bold", json.dumps(design_ejemplo)))
            print("✅ Tema 'Passe Global' creado con design de prueba")
        
        conn.commit()
        conn.close()
        
        print("\n🎯 TEMA DE PRUEBA LISTO!")
        print("\nPara probar:")
        print("1. Ir a https://localhost/rrhh/passes/configuracao")
        print("2. Hacer clic en 'Editar' del tema 'Passe Global'")
        print("3. Debería abrir el CardDesigner con los elementos cargados:")
        print("   - Texto: Nome (Helvetica-Bold, 16px)")
        print("   - Texto: Cargo (Helvetica, 12px)")
        print("   - Imagen: Logo de Sonangol")
        print("   - QR Code: Código QR")
        print("   - Fondo: Color gris claro")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = crear_tema_prueba_con_design()
    sys.exit(0 if success else 1)
