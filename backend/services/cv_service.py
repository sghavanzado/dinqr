"""
SIGA - Sistema Integral de Gestión de Accesos
Servicios de Generación de Cartón de Visita

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Lógica de negocio para la generación de cartones de visita.
             Basado en qr_service.py con adaptaciones para CV.
"""

from utils.db_utils import obtener_conexion_remota, obtener_conexion_local
import qrcode
import os
import hmac
import hashlib
import logging

def obtener_tabela():
    """Obtener el nombre de la tabla a consultar en la base de datos remota."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('tabela',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'tabela' en la tabla settings.")
        return result[0]

def obtener_carpeta_salida_cv():
    """Obtener la carpeta de salida para cartones de visita (misma que QR)."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('outputFolder',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'outputFolder' en la tabla settings.")
        return os.path.abspath(result[0])

def obtener_server_domain():
    """Obtener ip/dominio servidor Web."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('serverDomain',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'serverDomain' en la tabla settings.")
        return result[0]

def obtener_qr_domain():
    """Obtener el dominio/ip que se mostrará en el QR."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('qrdomain',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'qrdomain' en la tabla settings.")
        return result[0]

def obtener_server_port():
    """Obtener port servidor Web."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('serverPort',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'serverPort' en la tabla settings.")
        return result[0]

def generar_firma(nome):
    """Generar HMAC-SHA256 igual que el backend (clave = sha256(nombre), mensaje = nombre)."""
    key = hashlib.sha256(nome.encode()).digest()
    return hmac.new(key, nome.encode(), hashlib.sha256).hexdigest()

def generar_cv(ids):
    """Generar cartones de visita para una lista de IDs."""
    if not ids:
        raise ValueError("La lista de IDs está vacía.")

    # Obtener configuraciones
    output_folder = obtener_carpeta_salida_cv()
    try:
        server_domain = obtener_qr_domain()
    except Exception:
        server_domain = obtener_server_domain()
    server_port = obtener_server_port()

    # Crear carpeta si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    resultados = []
    tabela = obtener_tabela()
    placeholders = ','.join(['?'] * len(ids))
    query = f"SELECT sap, nome, funcao, area, nif, telefone, unineg FROM {tabela} WHERE sap IN ({placeholders})"

    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        cursor.execute(query, ids)
        contactos = cursor.fetchall()

    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        for contacto in contactos:
            try:
                # Proveer valores por defecto
                sap = contacto.sap or "N/A"
                nome = contacto.nome or "Desconocido"
                funcao = contacto.funcao or "No especificada"
                area = contacto.area or "No especificada"
                nif = contacto.nif or "No especificado"
                telefone = contacto.telefone or "No especificado"
                unineg = contacto.unineg or "No especificada"

                # Generar firma HMAC-SHA256
                firma = generar_firma(nome)

                # Crear el código QR con la URL segura
                qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
                qr_url = f"https://{server_domain}:{server_port}/cv/cartonv?sap={sap}&hash={firma}"
                qr.add_data(qr_url)
                qr.make(fit=True)
                
                # Guardar con prefijo CV (sin guión)
                archivo_qr = os.path.join(output_folder, f"CV{sap}.png")
                # QR color azul (diferente al QR original que es negro)
                qr.make_image(fill_color="blue", back_color="white").save(archivo_qr)

                # Guardar datos en la tabla cv_codes
                cursor.execute("""
                    INSERT INTO cv_codes (contact_id, nombre, firma, archivo_qr)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (contact_id) DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    firma = EXCLUDED.firma,
                    archivo_qr = EXCLUDED.archivo_qr
                """, (sap, nome, firma, archivo_qr))
                conn.commit()

                resultados.append({
                    "sap": sap,
                    "archivo": archivo_qr,
                    "url": qr_url,
                    "unineg": unineg
                })
            except Exception as e:
                logging.error(f"Error al procesar el contacto {contacto.sap}: {str(e)}")
                resultados.append({"sap": contacto.sap, "error": str(e)})
    
    return resultados

def descargar_cv(contact_id):
    """Descargar un cartón de visita específico."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT archivo_qr FROM cv_codes WHERE contact_id = %s", (str(contact_id),))
        result = cursor.fetchone()
        if not result:
            raise FileNotFoundError("Cartón de visita no encontrado")
        return result[0]

def eliminar_cv(contact_id):
    """Eliminar un cartón de visita específico."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cv_codes WHERE contact_id = %s RETURNING archivo_qr", (str(contact_id),))
        result = cursor.fetchone()
        if not result:
            raise FileNotFoundError("Cartón de visita no encontrado")
        # Eliminar archivo físico
        if os.path.exists(result[0]):
            os.remove(result[0])
        conn.commit()
    return {"message": "Cartón de visita eliminado exitosamente"}
