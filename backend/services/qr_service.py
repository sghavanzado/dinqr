from utils.db_utils import obtener_conexion_remota, obtener_conexion_local
import qrcode
import os
import zipfile
import hmac
import hashlib

def obtener_carpeta_salida():
    """Obtener la carpeta de salida desde la tabla settings de la base de datos local."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('outputFolder',))  # PostgreSQL usa %s
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'outputFolder' en la tabla settings.")
        return os.path.abspath(result[0])  # Convertir a ruta absoluta

def obtener_server_domain():
    """Obtener ip/dominio servidor Web."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('serverDomain',))  # PostgreSQL usa %s
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'serverDomain' en la tabla settings.")
        return result[0]

def obtener_server_port():
    """Obtener port servidor Web."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('serverPort',))  # PostgreSQL usa %s
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'serverPort' en la tabla settings.")
        return result[0]

def listar_funcionarios(page, per_page, filtro):
    """Listar funcionarios desde la base de datos remota."""
    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM contactos WHERE nombre LIKE ? ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"  # SQL Server usa ?
        cursor.execute(query, (f"%{filtro}%", (page - 1) * per_page, per_page))
        funcionarios = cursor.fetchall()
    return [{"id": row.id, "nombre": row.nombre} for row in funcionarios]

def generar_firma(nombre):
    """Generar HMAC-SHA256 basado en el nombre del contacto."""
    secret_key = b'secret_key'  # Cambiar por una clave segura
    return hmac.new(secret_key, nombre.encode('utf-8'), hashlib.sha256).hexdigest()

def generar_qr(ids):
    """Generar códigos QR para una lista de IDs."""
    if not ids:
        raise ValueError("La lista de IDs está vacía.")

    # Obtener configuraciones desde la base de datos
    output_folder = obtener_carpeta_salida()
    server_domain = obtener_server_domain()
    server_port = obtener_server_port()

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    resultados = []
    placeholders = ','.join(['?'] * len(ids))  # SQL Server usa ?
    query = f"SELECT * FROM contactos WHERE id IN ({placeholders})"

    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        cursor.execute(query, ids)
        contactos = cursor.fetchall()

    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        for contacto in contactos:
            # Generar firma HMAC-SHA256
            firma = generar_firma(contacto.nombre)

            # Crear el código QR con la URL segura
            qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
            qr_url = f"http://{server_domain}:{server_port}/contacto?id={contacto.id}&hash={firma}"
            qr.add_data(qr_url)
            qr.make(fit=True)
            archivo_qr = os.path.join(output_folder, f"qr_{contacto.id}.png")
            qr.make_image(fill_color="black", back_color="white").save(archivo_qr)

            # Guardar datos en la tabla qr_codes
            cursor.execute("""
                INSERT INTO qr_codes (contact_id, nombre, firma, archivo_qr)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (contact_id) DO UPDATE SET
                nombre = EXCLUDED.nombre,
                firma = EXCLUDED.firma,
                archivo_qr = EXCLUDED.archivo_qr
            """, (contacto.id, contacto.nombre, firma, archivo_qr))  # PostgreSQL usa %s
            conn.commit()

            resultados.append({"id": contacto.id, "archivo": archivo_qr, "url": qr_url})
    return resultados

def descargar_qr(contact_id):
    """Descargar un código QR específico."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        # Convertir contact_id a cadena de texto para evitar conflictos de tipos
        cursor.execute("SELECT archivo_qr FROM qr_codes WHERE contact_id = %s", (str(contact_id),))  # PostgreSQL usa %s
        result = cursor.fetchone()
        if not result:
            raise FileNotFoundError("QR no encontrado")
        return result[0]

def descargar_multiples_qr(ids):
    """Descargar múltiples códigos QR como archivo ZIP."""
    archivos = []
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT archivo_qr FROM qr_codes WHERE contact_id = ANY(%s)", (ids,))  # PostgreSQL usa %s
        archivos = [row[0] for row in cursor.fetchall()]

    zip_filename = "qr_codes.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for archivo in archivos:
            zipf.write(archivo)
    return zip_filename

def eliminar_qr(contact_id):
    """Eliminar un código QR específico."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        # Convertir contact_id a cadena de texto para evitar conflictos de tipos
        cursor.execute("DELETE FROM qr_codes WHERE contact_id = %s RETURNING archivo_qr", (str(contact_id),))  # PostgreSQL usa %s
        result = cursor.fetchone()
        if not result:
            raise FileNotFoundError("QR no encontrado")
        os.remove(result[0])
    return {"message": "QR eliminado exitosamente"}
