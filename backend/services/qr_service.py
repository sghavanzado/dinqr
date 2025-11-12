"""
SIGA - Sistema Integral de Gestión de Accesos
Servicios de Generación de QR

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Lógica de negocio para la generación de códigos QR.
"""

def obtener_tabela():
    """Obtener el nombre de la tabla a consultar en la base de datos remota (campo 'tabela' en settings)."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('tabela',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'tabela' en la tabla settings.")
        return result[0]
from utils.db_utils import obtener_conexion_remota, obtener_conexion_local
import qrcode
import os
import zipfile
import hmac
import hashlib
from PIL import Image
from vobject import vCard
import logging

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

def obtener_qr_domain():
    """Obtener el dominio/ip que se mostrará en el QR (qrdomain)."""
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
        cursor.execute("SELECT value FROM settings WHERE key = %s", ('serverPort',))  # PostgreSQL usa %s
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'serverPort' en la tabla settings.")
        return result[0]

def listar_funcionarios(page, per_page, filtro):
    """Listar funcionarios desde la base de datos remota."""
    try:
        tabela = obtener_tabela()
        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT sap, nome, funcao, area, nif, telefone, email, unineg
                FROM {tabela}
                WHERE nome LIKE ?
                ORDER BY sap
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
            """
            cursor.execute(query, (f"%{filtro}%", (page - 1) * per_page, per_page))
            funcionarios = cursor.fetchall()
            logging.info(f"Funcionarios obtenidos: {len(funcionarios)} registros")
        return [{"sap": row.sap, "nome": row.nome} for row in funcionarios]
    except Exception as e:
        logging.error(f"Error al listar funcionarios: {str(e)}")
        raise

def obtener_total_funcionarios():
    """Obtener la cantidad total de funcionarios desde la base de datos remota."""
    tabela = obtener_tabela()
    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")  # Contar todos los registros en la tabla definida
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se pudo obtener la cantidad total de funcionarios.")
        return result[0]

def obtener_total_funcionarios_con_qr():
    """Obtener la cantidad total de funcionarios con código QR en la base de datos local."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM qr_codes")  # Contar todos los registros en la tabla qr_codes
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se pudo obtener la cantidad total de funcionarios con QR.")
        return result[0]

def generar_firma(nome):
    """Generar HMAC-SHA256 igual que el backend (clave = sha256(nombre), mensaje = nombre)."""
    key = hashlib.sha256(nome.encode()).digest()
    return hmac.new(key, nome.encode(), hashlib.sha256).hexdigest()

def generar_qr_estatico(ids):
    """Generar códigos QR estáticos para una lista de IDs."""
    if not ids:
        raise ValueError("La lista de IDs está vacía.")

    # Obtener configuraciones desde la base de datos
    output_folder = obtener_carpeta_salida()

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    resultados = []
    tabela = obtener_tabela()
    placeholders = ','.join(['?'] * len(ids))  # SQL Server usa ?
    query = f"SELECT * FROM {tabela} WHERE sap IN ({placeholders})"

    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        cursor.execute(query, *ids)
        contactos = cursor.fetchall()

    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        for contacto in contactos:
            try:
                # Crear vCard
                vcard = vCard()
                vcard.add("tel").value = contacto.telefone
                vcard.add("email").value = contacto.email
                vcard.add("fn").value = contacto.nome
                vcard.add("title").value = contacto.funcao
                vcard.add("org").value = contacto.unineg
                vcard.add("nickname").value = contacto.area
                vcard.add("uid").value = contacto.sap

                # Serializar vCard
                vcard_data = vcard.serialize()

                # Generar código QR
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(vcard_data)
                qr.make(fit=True)
                img = qr.make_image(fill="black", back_color="white")

                # Guardar el código QR
                qr_file_name = f"{contacto.sap}.png"
                qr_file_path = os.path.join(output_folder, qr_file_name)
                img.save(qr_file_path)

                # Guardar datos en la tabla qr_codes
                cursor.execute("""
                    INSERT INTO qr_codes (contact_id, nombre, firma, archivo_qr)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (contact_id) DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    firma = EXCLUDED.firma,
                    archivo_qr = EXCLUDED.archivo_qr
                """, (contacto.sap, contacto.nome, "static", qr_file_path))  # "static" indica QR estático
                conn.commit()

                resultados.append({"sap": contacto.sap, "archivo": qr_file_path})
            except Exception as e:
                resultados.append({"sap": contacto.sap, "error": str(e)})

    return resultados

def generar_qr(ids):
    """Generar códigos QR dinámicos para una lista de IDs."""
    if not ids:
        raise ValueError("La lista de IDs está vacía.")

    # Obtener configuraciones desde la base de datos
    output_folder = obtener_carpeta_salida()
    try:
        server_domain = obtener_qr_domain()
    except Exception:
        server_domain = obtener_server_domain()
    server_port = obtener_server_port()

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    resultados = []
    tabela = obtener_tabela()
    placeholders = ','.join(['?'] * len(ids))  # SQL Server usa ?
    query = f"SELECT sap, nome, funcao, area, nif, telefone, unineg FROM {tabela} WHERE sap IN ({placeholders})"

    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        cursor.execute(query, ids)
        contactos = cursor.fetchall()

    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        for contacto in contactos:
            try:
                # Proveer valores por defecto para datos faltantes
                sap = contacto.sap or "N/A"
                nome = contacto.nome or "Desconocido"
                funcao = contacto.funcao or "No especificada"
                area = contacto.area or "No especificada"
                nif = contacto.nif or "No especificado"
                telefone = contacto.telefone or "No especificado"
                unineg = contacto.unineg or "No especificada"

                # Generar firma HMAC-SHA256
                firma = generar_firma(nome)

                # Crear el código QR con la URL segura (solo 'hash' en la URL)
                qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
                qr_url = f"https://{server_domain}:{server_port}/contacto?sap={sap}&hash={firma}"
                qr.add_data(qr_url)
                qr.make(fit=True)
                archivo_qr = os.path.join(output_folder, f"{sap}.png")
                qr.make_image(fill_color="black", back_color="white").save(archivo_qr)

                # Guardar datos en la tabla qr_codes
                cursor.execute("""
                    INSERT INTO qr_codes (contact_id, nombre, firma, archivo_qr)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (contact_id) DO UPDATE SET
                    nombre = EXCLUDED.nombre,
                    firma = EXCLUDED.firma,
                    archivo_qr = EXCLUDED.archivo_qr
                """, (sap, nome, firma, archivo_qr))  # PostgreSQL usa %s
                conn.commit()

                resultados.append({
                    "sap": sap,
                    "archivo": archivo_qr,
                    "url": qr_url,
                    "unineg": unineg  # Incluir el campo uo en los resultados
                })
            except Exception as e:
                logging.error(f"Error al procesar el contacto {contacto.sap}: {str(e)}")
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
