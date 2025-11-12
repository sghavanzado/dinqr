"""
SIGA - Sistema Integral de Gestión de Accesos
Rutas de Gestión de QR y Contactos

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Endpoints para visualización y descarga de tarjetas vCard.
"""

from flask import Blueprint, request, render_template_string, abort, send_file, jsonify
import hmac
import hashlib
import logging
import os
import csv
import pyodbc
from utils.db_utils import obtener_conexion_local, obtener_conexion_remota
import zipfile
import flask
import functools


qrdata_bp = Blueprint('qrdata_bp', __name__)

# Configurar logging
logging.basicConfig(
    filename='access.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
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
with obtener_conexion_remota() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT sap, nome, funcao, area, nif, telefone, email, unineg FROM sonacard") # Asegúrate de seleccionar las columnas en el orden correcto
    for row in cursor.fetchall():
        # Acceder a los datos por índice
        id_normalizado = str(row[0]).strip()  # sap es el primer elemento (índice 0)
        contactos[id_normalizado] = {
            "firma": None,  # Se calculará al iniciar
            "datos": {
                "sap": id_normalizado,
                "nome": row[1],      # nome es el segundo elemento (índice 1)
                "funcao": row[2],    # funcao es el tercer elemento (índice 2)
                "area": row[3],      # area es el cuarto elemento (índice 3)
                "nif": row[4],       # nif es el quinto elemento (índice 4)
                "telefone": row[5],  # telefone es el sexto elemento (índice 5)
                "email": row[6],     # email es el séptimo elemento (índice 6)
                "unineg": row[7]     # unineg es el octavo elemento (índice 7)
            }
        }

# Precalcular firmas al iniciar el servidor
for contacto_id, contacto in contactos.items():
    contacto_id_normalizado = contacto_id.strip()  # Normalizar el ID
    contactos[contacto_id_normalizado]['firma'] = generar_firma_hmac(contacto['datos']['nome'])

def validar_hmac(f):
    """Decorador para validar HMAC en las solicitudes"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        id_contacto = request.args.get('sap', '').strip()  # Normalizar el ID recibido
        # Permitir compatibilidad: aceptar 'hash' o 'firma' como parámetro
        firma_recibida = request.args.get('hash', '').strip()
        if not firma_recibida:
            firma_recibida = request.args.get('firma', '').strip()

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

def get_logger():
    if flask.has_app_context():
        return flask.current_app.logger
    else:
        return logging.getLogger('qrdata_bp')

@qrdata_bp.route('/contacto/vcard')
@validar_hmac
def descargar_vcard():
    """Devuelve la vCard del contacto si la firma es válida."""
    id_contacto = request.args.get('sap', '').strip()
    hash_recebido = request.args.get('hash', '').strip() or request.args.get('firma', '').strip()

    if not id_contacto or not hash_recebido:
        abort(400, description="Parâmetros em falta")

    try:
        # Buscar contacto en la base de datos remota usando consulta específica
        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sap, nome, funcao, area, nif, telefone, email, unineg FROM sonacard WHERE sap = ?", (id_contacto,))
            contacto_data = cursor.fetchone()

        if not contacto_data:
            abort(404, description="Contacto não encontrado")

        # Construir datos para vCard usando acceso por índice
        dados = {
            "nome": contacto_data[1],      # nome es el segundo elemento (índice 1)
            "funcao": contacto_data[2],    # funcao es el tercer elemento (índice 2)
            "area": contacto_data[3],      # area es el cuarto elemento (índice 3)
            "nif": contacto_data[4],       # nif es el quinto elemento (índice 4)
            "telefone": contacto_data[5],  # telefone es el sexto elemento (índice 5)
            "email": contacto_data[6],     # email es el séptimo elemento (índice 6)
            "unineg": contacto_data[7]     # unineg es el octavo elemento (índice 7)
        }
        
        vcard_str = """BEGIN:VCARD\nVERSION:3.0\nFN:{nome}\nTITLE:{funcao}\nDEPARTMENT:{area}\nORG:{unineg}\nTEL;TYPE=WORK,VOICE:{telefone}\nEMAIL:{email}\nEND:VCARD\n""".format(**dados)

        # Enviar como archivo descargable
        from flask import Response
        response = Response(vcard_str, mimetype='text/vcard; charset=utf-8')
        response.headers['Content-Disposition'] = f'attachment; filename=contacto_{id_contacto}.vcf'
        return response
    except Exception as e:
        abort(500, description=f"Erro ao gerar vCard: {str(e)}")

@qrdata_bp.route('/contacto')
@validar_hmac
def mostrar_contacto():
    """Devolve a informação de um contacto em formato HTML validando o ID e o hash."""
    id_contacto = request.args.get('sap', '').strip()
    hash_recebido = request.args.get('hash', '').strip()

    logging.info(f"Parâmetros recebidos: id_contacto={id_contacto}, hash_recebido={hash_recebido}")

    # Validar parâmetros
    if not id_contacto or not hash_recebido:
        logging.warning(f"Parâmetros em falta de {request.remote_addr}")
        abort(400, description="Parâmetros em falta")

    try:
        # Verificar na base de dados local (localdb)
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT firma FROM qr_codes WHERE contact_id = %s", (id_contacto,))
            resultado_local = cursor.fetchone()

        if not resultado_local:
            logging.warning(f"ID não encontrado na base de dados local: {id_contacto}")
            abort(404, description="ID não encontrado")

        firma_local = resultado_local[0]
        if not hmac.compare_digest(firma_local, hash_recebido):
            logging.warning(f"Hash não coincide para o ID {id_contacto} de {request.remote_addr}")
            abort(403, description="Hash inválido")

        # Consultar na base de dados remota (externaldb)
        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            # Asegúrate de seleccionar las columnas en el mismo orden que las usas
            cursor.execute("SELECT sap, nome, funcao, area, nif, telefone, email, unineg FROM sonacard WHERE sap = ?", (id_contacto,))
            contacto_data = cursor.fetchone() # Cambiado el nombre de la variable para evitar confusión

        if not contacto_data: # Comprobar si se encontró el contacto
            logging.warning(f"ID não encontrado na base de dados remota: {id_contacto}")
            abort(404, description="Contacto não encontrado")
        
        # Crear un objeto o diccionario que simule el acceso por atributo
        # Esto es útil para mantener la legibilidad del HTML template
        class Contacto:
            def __init__(self, data):
                self.sap = data[0]
                self.nome = data[1]
                self.funcao = data[2]
                self.area = data[3]
                self.nif = data[4]
                self.telefone = data[5]
                self.email = data[6]
                self.unineg = data[7]
        
        contacto = Contacto(contacto_data) # Instanciar la clase Contacto con los datos

        # Generar la página HTML con los datos del contacto
        html_template = f"""
        <!DOCTYPE html>
        <html lang="pt">
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
                    <p><strong>SAP:</strong> {contacto.sap or 'Não especificado'}</p>
                    <p><strong>Função:</strong> {contacto.funcao or 'Não especificada'}</p>
                    <p><strong>Direção:</strong> {contacto.area or 'Não especificada'}</p>
                    <p><strong>U.Neg:</strong> {contacto.unineg or 'Não especificada'}</p>
                    <p><strong>NIF:</strong> {contacto.nif or 'Não especificado'}</p>
                    <p><strong>Telefone:</strong> {contacto.telefone or 'Não especificado'}</p>
                    <p><strong>Email:</strong> {contacto.email or 'Não especificado'}</p>
                </div>
                <a href="/contacto/vcard?sap={id_contacto}&hash={hash_recebido}" class="import-button">
                    Importar Contacto
                </a>
            </div>
        </body>
        </html>
        """
        logging.info(f"Acesso autorizado ao ID {id_contacto} de {request.remote_addr}")
        return render_template_string(html_template)

    except Exception as e:
        logging.error(f"Erro ao processar o pedido para o ID {id_contacto}: {str(e)}")
        abort(500, description="Erro interno do servidor")


def generar_vcard(datos):
    """Genera contenido vCard con validación básica"""
    vcard_content = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{datos.get('nome', '')}",
        f"TITLE:{datos.get('funcao', '')}",
        f"DEPARTMENT:{datos.get('area', '')}",
        f"ORG:{datos.get('unineg', '')}",
        f"TEL;TYPE=WORK,VOICE:{datos.get('telefone', '')}",
        f"EMAIL:{datos.get('email', '')}",  # Adicionar email
        "END:VCARD"
    ]
    return "data:text/vcard;charset=utf-8," + "%0A".join(vcard_content)

@qrdata_bp.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    """Listado paginado de funcionarios desde externaldb"""
    # ...consultar externaldb y locadb para verificar QR generado...
    # ...return JSON con datos paginados...

@qrdata_bp.route('/qr/generar', methods=['POST'])
def generar_qr():
    """Generar códigos QR para uno o varios funcionarios"""
    ids = request.json.get('ids', [])
    from services.qr_service import generar_qr as generar_qr_service
    try:
        resultados = generar_qr_service(ids)
        return jsonify({"resultados": resultados}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@qrdata_bp.route('/qr/descargar/<int:contact_id>', methods=['GET'])
def descargar_qr(contact_id):
    """Descargar un código QR específico"""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT archivo_qr FROM qr_codes WHERE contact_id = %s", (str(contact_id),))
        result = cursor.fetchone()
        if not result:
            abort(404)
        return send_file(result[0], as_attachment=True)

@qrdata_bp.route('/qr/descargar-multiples', methods=['POST'])
def descargar_multiples_qr():
    """Descargar múltiples códigos QR como archivo ZIP"""
    ids = request.json.get('ids', [])
    archivos = []
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        # Asegúrate de que tu base de datos y pyodbc soporten 'ANY' o usa un enfoque diferente para multiples IDs
        # Si no, tendrás que construir la consulta dinámicamente o hacer múltiples consultas.
        # Por ejemplo, para PostgreSQL: WHERE contact_id = ANY(%s)
        # Para SQL Server: WHERE contact_id IN (?) con una tupla de IDs
        # Aquí, por simplicidad, asumiré que 'ANY' o 'IN' funciona.
        placeholders = ','.join(['?'] * len(ids))
        cursor.execute(f"SELECT archivo_qr FROM qr_codes WHERE contact_id IN ({placeholders})", tuple(str(id) for id in ids))
        archivos = [row[0] for row in cursor.fetchall()]
    
    zip_filename = "qr_codes.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for archivo in archivos:
            zipf.write(archivo)
    return send_file(zip_filename, as_attachment=True)

@qrdata_bp.route('/qr/eliminar/<int:contact_id>', methods=['DELETE'])
def eliminar_qr(contact_id):
    """Eliminar un código QR específico"""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM qr_codes WHERE contact_id = %s RETURNING archivo_qr", (str(contact_id),))
        result = cursor.fetchone()
        if not result:
            abort(404)
        os.remove(result[0])
        conn.commit()
    return jsonify({"message": "QR eliminado exitosamente"})
