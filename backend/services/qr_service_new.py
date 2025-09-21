def obtener_tabela():
    """Obtener el nombre de la tabla a consultar en la base de datos IAMC (campo 'tabela' en settings)."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE [key] = ?", ('tabela',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'tabela' en la tabla settings.")
        return result[0]

from utils.db_utils import obtener_conexion_local, obtener_conexion_remota
import qrcode
import os
import zipfile
import hmac
import hashlib
from PIL import Image
from vobject import vCard
import logging

def obtener_carpeta_salida():
    """Obtener la carpeta de salida desde la tabla settings de la base de datos IAMC."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE [key] = ?", ('outputFolder',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'outputFolder' en la tabla settings.")
        return os.path.abspath(result[0])  # Convertir a ruta absoluta

def obtener_server_domain():
    """Obtener ip/dominio servidor Web."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE [key] = ?", ('serverDomain',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'serverDomain' en la tabla settings.")
        return result[0]

def obtener_qr_domain():
    """Obtener el dominio/ip que se mostrará en el QR (qrdomain)."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE [key] = ?", ('qrdomain',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'qrdomain' en la tabla settings.")
        return result[0]

def obtener_server_port():
    """Obtener puerto servidor Web."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE [key] = ?", ('serverPort',))
        result = cursor.fetchone()
        if not result:
            raise ValueError("No se encontró la configuración 'serverPort' en la tabla settings.")
        return result[0]

def listar_funcionarios(page=1, per_page=10, filtro=""):
    """Listar funcionarios con paginación y filtro."""
    offset = (page - 1) * per_page
    
    tabela = obtener_tabela()
    base_query = f"SELECT sap, nome, funcao, area FROM {tabela}"
    
    params = []
    if filtro:
        base_query += " WHERE nome LIKE ? OR funcao LIKE ? OR area LIKE ?"
        params = [f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"]
    
    # Agregar orden y paginación
    query = f"{base_query} ORDER BY sap OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.extend([offset, per_page])
    
    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        funcionarios = cursor.fetchall()
    
    return [
        {
            "sap": funcionario.sap,
            "nome": funcionario.nome,
            "funcao": funcionario.funcao,
            "area": funcionario.area
        }
        for funcionario in funcionarios
    ]

def obtener_total_funcionarios():
    """Obtener el número total de funcionarios."""
    tabela = obtener_tabela()
    query = f"SELECT COUNT(*) FROM {tabela}"
    
    with obtener_conexion_remota() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()[0]

def obtener_total_funcionarios_con_qr():
    """Obtener el número total de funcionarios con QR generado."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM qr_codes")
        return cursor.fetchone()[0]

def generar_firma(nome):
    """Generar una firma HMAC-SHA256 para un nombre dado."""
    # Clave secreta para HMAC (debería estar en un archivo de configuración)
    clave_secreta = "clave_secreta_super_segura"  # ¡Cambiar en producción!
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
    query = f"SELECT sap, nome, funcao, area, nif, telefone, unineg FROM {tabela} WHERE sap IN ({placeholders})"

    with obtener_conexion_remota() as conn:  # empresadb para sonacard
        cursor = conn.cursor()
        cursor.execute(query, ids)
        contactos = cursor.fetchall()

    for contacto in contactos:
        try:
            # Crear el vCard
            vcard = vCard()
            vcard.add('fn').value = contacto.nome
            vcard.add('org').value = contacto.area
            vcard.add('title').value = contacto.funcao
            if contacto.telefone:
                vcard.add('tel').value = contacto.telefone
            
            # Crear el código QR con los datos del vCard
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(vcard.serialize())
            qr.make(fit=True)
            
            # Crear imagen y guardar
            arquivo_qr = os.path.join(output_folder, f"qr_estatico_{contacto.sap}.png")
            qr.make_image(fill_color="black", back_color="white").save(arquivo_qr)
            
            resultados.append({
                "sap": contacto.sap,
                "arquivo": arquivo_qr,
                "dados": vcard.serialize()
            })
        except Exception as e:
            logging.error(f"Error al generar QR estático para {contacto.sap}: {str(e)}")
            resultados.append({"sap": contacto.sap, "error": str(e)})

    return resultados

def generar_qr(ids):
    """Generar códigos QR dinámicos para una lista de IDs de funcionarios IAMC."""
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
    
    # Conectar a IAMC para obtener datos de funcionarios
    try:
        from extensions import IAMCSession
        from models.iamc_funcionarios_new import Funcionario
        
        session = IAMCSession()
        
        # Consultar funcionarios desde IAMC
        funcionarios = session.query(Funcionario).filter(Funcionario.FuncionarioID.in_(ids)).all()
        
        if not funcionarios:
            logging.warning(f"No se encontraron funcionarios con IDs: {ids}")
            return []
            
        # Conectar a base local para guardar QR codes
        with obtener_conexion_local() as conn_local:
            cursor_local = conn_local.cursor()
            
            for funcionario in funcionarios:
                try:
                    # Usar datos de funcionario IAMC
                    funcionario_id = funcionario.FuncionarioID
                    nome = funcionario.Nome or "Desconocido"
                    apelido = funcionario.Apelido or ""
                    nome_completo = f"{nome} {apelido}".strip()

                    # Generar firma HMAC-SHA256
                    firma = generar_firma(nome_completo)

                    # Crear el código QR con la URL segura
                    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
                    qr_url = f"https://{server_domain}:{server_port}/contacto?id={funcionario_id}&hash={firma}"
                    qr.add_data(qr_url)
                    qr.make(fit=True)

                    # Crear imagen del QR
                    qr_img = qr.make_image(fill_color="black", back_color="white")
                    qr_img = qr_img.convert("RGB")

                    # Guardar imagen QR
                    nome_arquivo = f"qr_{funcionario_id}.png"
                    caminho_arquivo = os.path.join(output_folder, nome_arquivo)
                    qr_img.save(caminho_arquivo)

                    # Verificar si ya existe un registro en qr_codes para este funcionario
                    cursor_local.execute("SELECT contact_id FROM qr_codes WHERE contact_id = ?", (funcionario_id,))
                    existe = cursor_local.fetchone()
                    
                    if existe:
                        # Actualizar registro existente
                        cursor_local.execute("""
                            UPDATE qr_codes 
                            SET qr_path = ?, hash_value = ?, generated_at = GETDATE()
                            WHERE contact_id = ?
                        """, (caminho_arquivo, firma, funcionario_id))
                        logging.info(f"QR actualizado para funcionario ID {funcionario_id}")
                    else:
                        # Insertar nuevo registro
                        cursor_local.execute("""
                            INSERT INTO qr_codes (contact_id, qr_path, hash_value, generated_at) 
                            VALUES (?, ?, ?, GETDATE())
                        """, (funcionario_id, caminho_arquivo, firma))
                        logging.info(f"QR creado para funcionario ID {funcionario_id}")
                    
                    conn_local.commit()

                    resultados.append({
                        "id": funcionario_id,
                        "nome": nome_completo,
                        "message": "Código QR generado exitosamente",
                        "qr_path": caminho_arquivo,
                        "qr_url": qr_url
                    })

                except Exception as e:
                    logging.error(f"Error al generar QR para funcionario ID {funcionario_id}: {str(e)}")
                    resultados.append({
                        "id": funcionario_id,
                        "nome": nome_completo if 'nome_completo' in locals() else f"ID {funcionario_id}",
                        "error": f"Error al generar QR: {str(e)}"
                    })
                    
    except Exception as e:
        logging.error(f"Error al conectar con IAMC para generar QR: {str(e)}")
        return []
    finally:
        if 'session' in locals():
            session.close()

    return resultados

def descargar_qr(contact_id):
    """Descargar un código QR específico."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT qr_path FROM qr_codes WHERE contact_id = ?", (str(contact_id),))
        result = cursor.fetchone()
        if not result:
            raise FileNotFoundError("QR no encontrado")
        return result[0]

def descargar_multiples_qr(ids):
    """Descargar múltiples códigos QR como archivo ZIP."""
    archivos = []
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(ids))
        query = f"SELECT qr_path FROM qr_codes WHERE contact_id IN ({placeholders})"
        cursor.execute(query, ids)
        archivos = [row[0] for row in cursor.fetchall()]

    zip_filename = "qr_codes.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for archivo in archivos:
            if os.path.exists(archivo):
                zipf.write(archivo, os.path.basename(archivo))
    return zip_filename

def eliminar_qr(contact_id):
    """Eliminar un código QR específico."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        # Primero obtener el archivo antes de eliminar
        cursor.execute("SELECT qr_path FROM qr_codes WHERE contact_id = ?", (str(contact_id),))
        result = cursor.fetchone()
        if not result:
            raise FileNotFoundError("QR no encontrado")
        archivo_qr = result[0]
        
        # Eliminar el registro
        cursor.execute("DELETE FROM qr_codes WHERE contact_id = ?", (str(contact_id),))
        conn.commit()
        
        # Eliminar el archivo físico
        if os.path.exists(archivo_qr):
            os.remove(archivo_qr)
        
        return {"message": "QR eliminado exitosamente"}
