#!/usr/bin/env python3
"""Script para generar QR codes para varios funcionarios IAMC."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Generating QR codes for multiple funcionarios...")

try:
    # Importar dependencies necesarias
    from utils.db_utils import obtener_conexion_local
    from extensions import IAMCSession
    from models.iamc_funcionarios_new import Funcionario
    import qrcode
    import hmac
    import hashlib
    from PIL import Image
    
    # Función de configuración directa
    def obtener_config(key):
        conn = obtener_conexion_local()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE [key] = ?", (key,))
        result = cursor.fetchone()
        conn.close()
        if not result:
            raise ValueError(f"No se encontró la configuración '{key}' en la tabla settings.")
        return result[0]
    
    def generar_firma_local(nome):
        clave_secreta = "clave_secreta_super_segura"
        key = hashlib.sha256(nome.encode()).digest()
        return hmac.new(key, nome.encode(), hashlib.sha256).hexdigest()
    
    def generar_qr_funcionario(funcionario_id):
        # Obtener configuraciones
        output_folder = obtener_config('outputFolder')
        qr_domain = obtener_config('qrdomain')
        server_port = obtener_config('serverPort')
        
        # Crear carpeta de salida si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
        
        # Obtener datos del funcionario
        session = IAMCSession()
        funcionario = session.query(Funcionario).filter(Funcionario.FuncionarioID == funcionario_id).first()
        session.close()
        
        if not funcionario:
            print(f"✗ Funcionario {funcionario_id} not found")
            return False
        
        # Generar datos
        nome = funcionario.Nome or "Desconocido"
        apelido = funcionario.Apelido or ""
        nome_completo = f"{nome} {apelido}".strip()
        
        # Generar firma
        firma = generar_firma_local(nome_completo)
        
        # Crear QR
        qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
        qr_url = f"https://{qr_domain}:{server_port}/contacto?id={funcionario_id}&hash={firma}"
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        # Crear imagen
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.convert("RGB")
        
        # Guardar imagen
        nome_arquivo = f"qr_{funcionario_id}.png"
        caminho_arquivo = os.path.join(output_folder, nome_arquivo)
        qr_img.save(caminho_arquivo)
        
        # Guardar en base de datos
        conn_local = obtener_conexion_local()
        cursor_local = conn_local.cursor()
        
        # Verificar si ya existe
        cursor_local.execute("SELECT contact_id FROM qr_codes WHERE contact_id = ?", (str(funcionario_id),))
        existe = cursor_local.fetchone()
        
        if existe:
            # Actualizar
            cursor_local.execute("""
                UPDATE qr_codes 
                SET nombre = ?, archivo_qr = ?, firma = ?, qr_path = ?, hash_value = ?
                WHERE contact_id = ?
            """, (nome_completo, nome_arquivo, firma, caminho_arquivo, firma, str(funcionario_id)))
            action = "Updated"
        else:
            # Insertar
            cursor_local.execute("""
                INSERT INTO qr_codes (contact_id, nombre, archivo_qr, firma, qr_path, hash_value) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (str(funcionario_id), nome_completo, nome_arquivo, firma, caminho_arquivo, firma))
            action = "Created"
        
        conn_local.commit()
        conn_local.close()
        
        print(f"✓ {action} QR for funcionario {funcionario_id}: {nome_completo}")
        return True
    
    # Generar QR codes para varios funcionarios
    funcionarios_ids = [5, 6, 7, 8, 9]  # IDs que sabemos que existen
    
    success_count = 0
    for funcionario_id in funcionarios_ids:
        if generar_qr_funcionario(funcionario_id):
            success_count += 1
    
    print(f"\nGenerated QR codes for {success_count}/{len(funcionarios_ids)} funcionarios")
    
    # Verificar total en base de datos
    conn = obtener_conexion_local()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM qr_codes")
    total = cursor.fetchone()[0]
    print(f"Total QR codes in database: {total}")
    conn.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
