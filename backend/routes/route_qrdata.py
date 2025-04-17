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
    cursor.execute("SELECT * FROM contactos")
    for row in cursor.fetchall():
        id_normalizado = str(row.id).strip()  # Normalizar el ID eliminando espacios
        contactos[id_normalizado] = {
            "firma": None,  # Se calculará al iniciar
            "datos": {
                "id": id_normalizado,
                "nombre": row.nombre,
                "empresa": row.empresa,
                "telefono": row.telefono,
                "email": row.email,
                "web": row.web,
                "direccion": row.direccion,
                "categoria": row.categoria,
                "numero_ext": row.numero_ext,
                "cargo": row.cargo,
                "unidad_negocio": row.unidad_negocio
            }
        }

# Precalcular firmas al iniciar el servidor
for contacto_id, contacto in contactos.items():
    contacto_id_normalizado = contacto_id.strip()  # Normalizar el ID
    contactos[contacto_id_normalizado]['firma'] = generar_firma_hmac(contacto['datos']['nombre'])

def validar_hmac(f):
    """Decorador para validar HMAC en las solicitudes"""
    def wrapper(*args, **kwargs):
        id_contacto = request.args.get('id', '').strip()  # Normalizar el ID recibido
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
    id_contacto = request.args.get('id')
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
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contacto - {datos['nombre']}</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', system-ui;
                max-width: 800px;
                margin: 2rem auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .card {{
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 15px rgba(0,0,0,0.1);
                padding: 2rem;
            }}
            h1 {{ color: #2c3e50; }}
            .info-section {{ margin: 1.5rem 0; }}
            .btn-download {{
                background: #3498db;
                color: white;
                padding: 12px 25px;
                border-radius: 25px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s;
            }}
            .btn-download:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(52,152,219,0.4);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>{datos['nombre']}</h1>
            <div class="info-section">
                <p><strong>Empresa:</strong> {datos['empresa']}</p>
                <p><strong>Teléfono:</strong> <a href="tel:{datos['telefono']}">{datos['telefono']}</a></p>
                <p><strong>Email:</strong> <a href="mailto:{datos['email']}">{datos['email']}</a></p>
                <p><strong>Sitio Web:</strong> <a href="{datos['web']}" target="_blank">{datos['web']}</a></p>
                <p><strong>Dirección:</strong> {datos['direccion']}</p>
                <p><strong>Categoría:</strong> {datos['categoria']}</p>
                <p><strong>Número de Extensión:</strong> {datos['numero_ext']}</p>
                <p><strong>Cargo:</strong> {datos['cargo']}</p>
                <p><strong>Unidad de Negocio:</strong> {datos['unidad_negocio']}</p>
            </div>
            <a href="{generar_vcard(datos)}" class="btn-download" download="contacto.vcf">
                Descargar Contacto
            </a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

def generar_vcard(datos):
    """Genera contenido vCard con validación básica"""
    vcard_content = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{datos.get('nombre', '')}",
        f"ORG:{datos.get('empresa', '')}",
        f"TEL;TYPE=WORK,VOICE:{datos.get('telefono', '')}",
        f"EMAIL;TYPE=WORK:{datos.get('email', '')}",
        f"URL:{datos.get('web', '')}",
        f"ADR;TYPE=WORK:;;{datos.get('direccion', '')}",
        f"CATEGORY:{datos.get('categoria', '')}",
        f"EXTENSION:{datos.get('numero_ext', '')}",
        f"TITLE:{datos.get('cargo', '')}",
        f"DEPARTMENT:{datos.get('unidad_negocio', '')}",
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