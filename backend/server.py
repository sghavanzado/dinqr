from flask import Flask, request, render_template_string, abort, jsonify, make_response
import hmac
import hashlib
import logging
from flask_limiter import Limiter
from flask_talisman import Talisman
from utils.db_utils import obtener_conexion_local, obtener_conexion_remota
import os

app = Flask(__name__, static_folder='static')

# Configuración de seguridad
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Configurar Talisman para cabeceras de seguridad
Talisman(
    app,
    content_security_policy=None,
    force_https=False,  # Deshabilitar HTTPS
    strict_transport_security=False,  # No habilitar HSTS
    frame_options='DENY'
)

# Configurar logging
logging.basicConfig(
    filename='logs/server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Configurar rate limiting
limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    storage_uri="memory://",
    default_limits=["200 per day", "50 per hour"]
)

@app.before_request
def log_request_details():
    """Registrar detalles de cada solicitud entrante."""
    logging.info(f"Solicitud entrante: {request.method} {request.url} desde {request.remote_addr}")

def obtener_configuracion(clave):
    """Obtener un valor de configuración desde la tabla settings."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", (clave,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"No se encontró la configuración '{clave}' en la tabla settings.")
        return result[0]

@app.route('/contacto')
@limiter.limit("10/minute")  # Límite de solicitudes
def mostrar_contacto():
    """Devuelve la información de un contacto en formato HTML validando el ID y el hash."""
    id_contacto = request.args.get('sap', '').strip()
    hash_recibido = request.args.get('hash', '').strip()

    logging.info(f"Parámetros recibidos: id_contacto={id_contacto}, hash_recibido={hash_recibido}")

    # Validar parámetros
    if not id_contacto or not hash_recibido:
        logging.warning(f"Parámetros faltantes desde {request.remote_addr}")
        abort(400, description="Parámetros faltantes")

    try:
        # Verificar en la base de datos local (localdb)
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT firma FROM qr_codes WHERE contact_id = %s", (id_contacto,))
            resultado_local = cursor.fetchone()

        if not resultado_local:
            logging.warning(f"ID no encontrado en la base de datos local: {id_contacto}")
            abort(404, description="ID no encontrado")

        firma_local = resultado_local[0]
        if not hmac.compare_digest(firma_local, hash_recibido):
            logging.warning(f"Hash no coincide para el ID {id_contacto} desde {request.remote_addr}")
            abort(403, description="Hash no válido")

        # Consultar en la base de datos remota (externaldb)
        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sonacard WHERE sap = ?", (id_contacto,))
            contacto = cursor.fetchone()

        if not contacto:
            logging.warning(f"ID no encontrado en la base de datos remota: {id_contacto}")
            abort(404, description="Contacto no encontrado")

        # Generar la página HTML con los datos del contacto
        html_template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Contacto - {contacto.nome}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 600px;
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
                .header {{
                    background-color: #F4CF0A;
                    padding: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header img {{
                    height: 50px;
                    margin-right: 10px;
                }}
                .header span {{
                    font-size: 2rem;
                    font-weight: bold;
                    color: #000;
                }}
                h1 {{
                    color: #2c3e50;
                }}
                .info-section {{
                    margin: 1.5rem 0;
                    
                }}
                .info-section p {{
                    margin: 0.5rem 0;
                }}
                .import-button {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    text-align: center;
                    cursor: pointer;
                }}
                .import-button:hover {{
                    background-color: #2980b9;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <img src="/static/images/sonangol-logo.png" alt="Sonangol Logo">
                    <span>Sonangol</span>
                </div>
                <h1>{contacto.nome}</h1>
                <div class="">
                    <p><strong>SAP:</strong> {contacto.sap or 'No especificada'}</p>
                    <p><strong>Funçao:</strong> {contacto.funcao or 'No especificada'}</p>
                    <p><strong>Area:</strong> {contacto.area or 'No especificado'}</p>
                    <p><strong>Nif:</strong> {contacto.nif or 'No especificada'}</p>
                    <p><strong>Telefone:</strong> {contacto.telefone or 'No especificada'}</p>
                </div>
                <a href="/contacto/vcard?sap={id_contacto}&hash={hash_recibido}" class="import-button">
                    Importar Contacto
                </a>
            </div>
        </body>
        </html>
        """
        logging.info(f"Acceso autorizado a {id_contacto} desde {request.remote_addr}")
        return render_template_string(html_template)

    except Exception as e:
        logging.error(f"Error al procesar la solicitud para el ID {id_contacto}: {str(e)}")
        abort(500, description="Error interno del servidor")

@app.route('/contacto/vcard', methods=['GET'])
def descargar_vcard():
    """Generar y descargar un archivo vCard para el contacto."""
    id_contacto = request.args.get('sap', '').strip()
    hash_recibido = request.args.get('hash', '').strip()

    try:
        # Validar parámetros y obtener datos del contacto
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT firma FROM qr_codes WHERE contact_id = %s", (id_contacto,))
            resultado_local = cursor.fetchone()

        if not resultado_local:
            abort(404, description="ID no encontrado")

        firma_local = resultado_local[0]
        if not hmac.compare_digest(firma_local, hash_recibido):
            abort(403, description="Hash no válido")

        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sonacard WHERE sap = ?", (id_contacto,))
            contacto = cursor.fetchone()

        if not contacto:
            abort(404, description="Contacto no encontrado")

        # Generar contenido vCard
        vcard_content = f"""
        BEGIN:VCARD
        VERSION:3.0
        FN:{contacto.nome}
        TITLE:{contacto.funcao or ''}
        ORG:{contacto.area or ''}
        TEL;TYPE=WORK,VOICE:{contacto.telefone or ''}
        END:VCARD
        """

        # Crear respuesta con el archivo vCard
        response = make_response(vcard_content.strip())
        response.headers['Content-Type'] = 'text/vcard'
        response.headers['Content-Disposition'] = f'attachment; filename=contacto_{id_contacto}.vcf'
        return response

    except Exception as e:
        logging.error(f"Error al generar vCard para el ID {id_contacto}: {str(e)}")
        abort(500, description="Error interno del servidor")

@app.route('/server/control', methods=['POST'])
def controlar_servidor():
    """Controla el estado del servidor (iniciar, pausar, detener)."""
    accion = request.json.get('accion', '').lower()
    if accion == 'iniciar':
        logging.info("Servidor iniciado.")
        return {"message": "Servidor iniciado."}, 200
    elif accion == 'pausar':
        logging.info("Servidor pausado.")
        return {"message": "Servidor pausado."}, 200
    elif accion == 'detener':
        logging.info("Servidor detenido.")
        os._exit(0)
    else:
        return {"error": "Acción no válida."}, 400

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

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Manejador global para errores inesperados."""
    logging.error(f"Error inesperado: {str(error)}")
    return "Error interno del servidor", 500

if __name__ == '__main__':
    try:
        # Forzar el uso del puerto 5678
        port = 5678

        # Inicia el servidor en localhost
        app.run(host='127.0.0.1', port=port, debug=True)
    except Exception as e:
        logging.error(f"Error al iniciar el servidor: {str(e)}")
        print(f"❌ Error al iniciar el servidor: {str(e)}")