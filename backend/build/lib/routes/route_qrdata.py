from flask import Flask, request, render_template_string, abort, send_file, jsonify
import hmac
import hashlib
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os
import csv
import pyodbc
from db_config import obtener_conexion, obtener_conexion_local
import zipfile

app = Flask(__name__)

# Configuración de seguridad
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'clave_secreta_por_defecto').encode('utf-8')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Configurar Talisman para cabeceras de seguridad
Talisman(
    app,
    content_security_policy=None,
    force_https=True,
    strict_transport_security=True,
    frame_options='DENY'
)

# Configurar logging
logging.basicConfig(
    filename='access.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Configurar rate limiting
limiter = Limiter(
    app=app,
    key_func=lambda: request.args.get('id', 'global'),
    storage_uri="memory://",
    default_limits=["200 per day", "50 per hour"]
)

def generar_firma_hmac(nombre_contacto):
    """Genera firma HMAC-SHA256 basada en el nombre del contacto"""
    return hmac.new(
        hashlib.sha256(nombre_contacto.encode()).digest(),
        nombre_contacto.encode(),
        hashlib.sha256
    ).hexdigest()

# Cargar contactos desde la base de datos
contactos = {}
with obtener_conexion() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sonacard")
    for row in cursor.fetchall():
        id_normalizado = str(row.sap).strip()  # Normalizar el ID eliminando espacios
        contactos[id_normalizado] = {
            "firma": None,  # Se calculará al iniciar
            "datos": {
                "sap": id_normalizado,
                "nome": row.nome,
                "funcao": row.funcao,
                "area": row.area,
                "nif": row.nif,
                "telefone": row.telefone
            }
        }

# Precalcular firmas al iniciar el servidor
for contacto_id, contacto in contactos.items():
    contacto_id_normalizado = contacto_id.strip()  # Normalizar el ID
    contactos[contacto_id_normalizado]['firma'] = generar_firma_hmac(contacto['datos']['nome'])

def validar_hmac(f):
    """Decorador para validar HMAC en las solicitudes"""
    def wrapper(*args, **kwargs):
        id_contacto = request.args.get('sap', '').strip()  # Normalizar el ID recibido
        firma_recibida = request.args.get('firma', '').strip()  # Normalizar la firma recibida
        
        # Validar parámetros básicos
        if not id_contacto or not firma_recibida:
            logging.warning(f"Parámetros faltantes desde {request.remote_addr}")
            abort(400)
            
        # Validar formato del ID
        if not id_contacto.isalnum() or len(id_contacto) > 20:
            logging.warning(f"ID inválido recibido: {id_contacto}")
            abort(400)
        
        # Validar firma HMAC
        contacto = contactos.get(id_contacto)
        if not contacto:
            logging.warning(f"ID de contacto no encontrado: {id_contacto}")
            abort(404)
        
        firma_correcta = contacto['firma']
        if not hmac.compare_digest(firma_correcta, firma_recibida):
            logging.warning(f"Intento de acceso no autorizado a {id_contacto} desde {request.remote_addr}")
            abort(403)
            
        return f(*args, **kwargs)
    return wrapper

@app.route('/contacto')
@validar_hmac
@limiter.limit("10/minute")  # Límite adicional para este endpoint
def mostrar_contacto():
    id_contacto = request.args.get('sap')
    contacto = contactos.get(id_contacto)
    
    if not contacto:
        logging.error(f"Contacto no encontrado: {id_contacto}")
        abort(404)
        
    logging.info(f"Acceso autorizado a {id_contacto} desde {request.remote_addr}")
    return generar_pagina_contacto(contacto['datos'])

def generar_pagina_contacto(datos):
    """Genera la página HTML con los datos del contacto"""
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">

    </html>
    """
    return render_template_string(html_template)

def generar_vcard(datos):
    """Genera contenido vCard con validación básica"""
    vcard_content = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{datos.get('nome', '')}",
        f"TITLE:{datos.get('funcao', '')}",
        f"DEPARTMENT:{datos.get('area', '')}",
        f"ORG:{datos.get('uo', '')}",  # Adicionar unidad organizacional
        f"TEL;TYPE=WORK,VOICE:{datos.get('telefone', '')}",
        f"EMAIL:{datos.get('email', '')}",  # Adicionar email
        "END:VCARD"
    ]
    return "data:text/vcard;charset=utf-8," + "%0A".join(vcard_content)

@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    """Listado paginado de funcionarios desde externaldb"""
    # ...consultar externaldb y locadb para verificar QR generado...
    # ...return JSON con datos paginados...

@app.route('/qr/generar', methods=['POST'])
def generar_qr():
    """Generar códigos QR para uno o varios funcionarios"""
    ids = request.json.get('ids', [])
    # ...consultar externaldb, generar QR, guardar en locadb...
    # ...return JSON con resultados...

@app.route('/qr/descargar/<int:contact_id>', methods=['GET'])
def descargar_qr(contact_id):
    """Descargar un código QR específico"""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT archivo_qr FROM qr_codes WHERE contact_id = %s", (contact_id,))
        result = cursor.fetchone()
        if not result:
            abort(404)
        return send_file(result[0], as_attachment=True)

@app.route('/qr/descargar-multiples', methods=['POST'])
def descargar_multiples_qr():
    """Descargar múltiples códigos QR como archivo ZIP"""
    ids = request.json.get('ids', [])
    archivos = []
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT archivo_qr FROM qr_codes WHERE contact_id = ANY(%s)", (ids,))
        archivos = [row[0] for row in cursor.fetchall()]
    
    zip_filename = "qr_codes.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for archivo in archivos:
            zipf.write(archivo)
    return send_file(zip_filename, as_attachment=True)

@app.route('/qr/eliminar/<int:contact_id>', methods=['DELETE'])
def eliminar_qr(contact_id):
    """Eliminar un código QR específico"""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM qr_codes WHERE contact_id = %s RETURNING archivo_qr", (contact_id,))
        result = cursor.fetchone()
        if not result:
            abort(404)
        os.remove(result[0])
        conn.commit()
    return jsonify({"message": "QR eliminado exitosamente"})

@app.errorhandler(400)
def bad_request(error):
    return "Solicitud incorrecta", 400

@app.errorhandler(403)
def forbidden(error):
    return "Acceso no autorizado", 403

@app.errorhandler(404)
def not_found(error):
    return "Contacto no encontrado", 404

@app.errorhandler(429)
def ratelimit_handler(error):
    return "Demasiadas solicitudes. Por favor intente más tarde.", 429

if __name__ == '__main__':
    app.run(
        host=os.environ.get('FLASK_HOST', '192.168.253.133'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    )