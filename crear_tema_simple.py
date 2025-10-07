#!/usr/bin/env python3
"""
Script simple para crear un tema de prueba y verificar datos
"""

import sys
import os
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def crear_tema_simple():
    try:
        from routes.passes_routes import obter_conexao_local
        
        conn = obter_conexao_local()
        cursor = conn.cursor()
        
        # Primero, limpiar todos los temas
        logger.info("🧹 Limpiando temas existentes...")
        cursor.execute("DELETE FROM pass_temas_avancado")
        
        # Crear un tema simple con design básico
        design_basico = {
            "id": "tema-test-1",
            "name": "Tema Test",
            "front": [
                {
                    "id": "text1",
                    "type": "text",
                    "content": "NOME: {{nome}}",
                    "x": 10,
                    "y": 10,
                    "width": 200,
                    "height": 30,
                    "fontSize": 14,
                    "fontFamily": "Arial",
                    "fill": "#000000"
                }
            ],
            "back": [],
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z"
        }
        
        logger.info("➕ Creando tema de prueba...")
        cursor.execute("""
            INSERT INTO pass_temas_avancado 
            (nome, cor_primaria, cor_secundaria, cor_texto, layout_tipo, fonte_titulo, design)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "Tema Teste",
            "#1976d2", 
            "#ffffff", 
            "#000000", 
            "horizontal", 
            "Arial",
            json.dumps(design_basico)
        ))
        
        conn.commit()
        
        # Verificar que se guardó correctamente
        logger.info("🔍 Verificando tema guardado...")
        cursor.execute("SELECT id, nome, design FROM pass_temas_avancado WHERE nome = ?", ("Tema Teste",))
        row = cursor.fetchone()
        
        if row:
            tema_id, nome, design_str = row
            logger.info(f"✅ Tema encontrado: ID={tema_id}, Nome={nome}")
            
            if design_str:
                design_data = json.loads(design_str)
                logger.info(f"✅ Design encontrado: {len(design_data.get('front', []))} elementos en frente")
                logger.info(f"🎨 Design JSON: {json.dumps(design_data, indent=2)}")
            else:
                logger.error("❌ Design está vacío!")
        else:
            logger.error("❌ Tema no encontrado!")
        
        conn.close()
        
        logger.info("\n🎯 TEMA DE PRUEBA CREADO!")
        logger.info("Ahora puedes:")
        logger.info("1. Ir a https://localhost/rrhh/passes/configuracao")
        logger.info("2. Hacer clic en 'Editar' del tema 'Tema Teste'")
        logger.info("3. Verificar que CardDesigner carga con el texto 'NOME: {{nome}}'")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = crear_tema_simple()
    sys.exit(0 if success else 1)
