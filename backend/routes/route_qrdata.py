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

def generar_firma_hmac(nombre_contacto):
    """Genera firma HMAC-SHA256 basada en el nombre del contacto"""
    return hmac.new(
        hashlib.sha256(nombre_contacto.encode()).digest(),
        nombre_contacto.encode(),
        hashlib.sha256
    ).hexdigest()

# Cargar contactos desde la tabla IAMC Funcionarios
contactos = {}
try:
    from extensions import IAMCSession
    from models.iamc_funcionarios_new import Funcionario, Cargo, Departamento
    
    session = IAMCSession()
    
    # Consulta con JOINs para obtener información completa
    query = session.query(
        Funcionario.FuncionarioID,
        Funcionario.Nome,
        Funcionario.Apelido,
        Funcionario.Email,
        Funcionario.Telefone,
        Funcionario.BI,
        Cargo.Nome.label('CargoNome'),
        Departamento.Nome.label('DepartamentoNome'),
        Funcionario.CargoID,
        Funcionario.DepartamentoID
    ).outerjoin(
        Cargo, Funcionario.CargoID == Cargo.CargoID
    ).outerjoin(
        Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
    )
    
    for func in query.all():
        # Usar FuncionarioID como clave principal
        id_normalizado = str(func.FuncionarioID).strip()
        nome_completo = f"{func.Nome} {func.Apelido}".strip()
        contactos[id_normalizado] = {
            "firma": None,  # Se calculará al iniciar
            "datos": {
                "funcionarioId": func.FuncionarioID,
                "nome": nome_completo,
                "cargo": func.CargoNome or "Sin Cargo",
                "departamento": func.DepartamentoNome or "Sin Departamento", 
                "bi": func.BI,
                "telefone": func.Telefone or "",
                "email": func.Email or "",
                "cargoId": func.CargoID,
                "departamentoId": func.DepartamentoID
            }
        }
    
    session.close()
    logging.info(f"Cargados {len(contactos)} contactos desde la tabla IAMC Funcionarios")
    
except Exception as e:
    logging.error(f"Error al cargar contactos desde IAMC: {str(e)}")
    contactos = {}

# Precalcular firmas al iniciar el servidor
for contacto_id, contacto in contactos.items():
    contacto_id_normalizado = contacto_id.strip()  # Normalizar el ID
    contactos[contacto_id_normalizado]['firma'] = generar_firma_hmac(contacto['datos']['nome'])

def validar_hmac(f):
    """Decorador para validar HMAC en las solicitudes"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # Permitir compatibilidad: aceptar 'funcionarioId' (nuevo) o 'sap' (legacy)
        id_contacto = request.args.get('funcionarioId', '').strip() or request.args.get('sap', '').strip()
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
    # Permitir compatibilidad: aceptar 'funcionarioId' (nuevo) o 'sap' (legacy)
    id_contacto = request.args.get('funcionarioId', '').strip() or request.args.get('sap', '').strip()
    hash_recebido = request.args.get('hash', '').strip() or request.args.get('firma', '').strip()

    if not id_contacto or not hash_recebido:
        abort(400, description="Parâmetros em falta")

    try:
        # Buscar contacto en la tabla IAMC Funcionarios usando consulta específica
        from extensions import IAMCSession
        from models.iamc_funcionarios_new import Funcionario, Cargo, Departamento
        
        session = IAMCSession()
        try:
            # Consulta con JOINs para obtener información completa
            funcionario_data = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Funcionario.BI,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome')
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            ).filter(
                Funcionario.FuncionarioID == int(id_contacto)
            ).first()
        finally:
            session.close()

        if not funcionario_data:
            abort(404, description="Contacto não encontrado")

        # Construir datos para vCard usando la nueva estructura IAMC
        dados = {
            "nome": f"{funcionario_data.Nome} {funcionario_data.Apelido}".strip(),
            "cargo": funcionario_data.CargoNome or "Sin Cargo",
            "departamento": funcionario_data.DepartamentoNome or "Sin Departamento",
            "bi": funcionario_data.BI or "",
            "telefone": funcionario_data.Telefone or "",
            "email": funcionario_data.Email or "",
            "org": "SONANGOL"  # Organización fija
        }
        
        vcard_str = """BEGIN:VCARD\nVERSION:3.0\nFN:{nome}\nTITLE:{cargo}\nDEPARTMENT:{departamento}\nORG:{org}\nTEL;TYPE=WORK,VOICE:{telefone}\nEMAIL:{email}\nEND:VCARD\n""".format(**dados)

        # Enviar como archivo descargable
        from flask import Response
        response = Response(vcard_str, mimetype='text/vcard; charset=utf-8')
        response.headers['Content-Disposition'] = f'attachment; filename=contacto_{id_contacto}.vcf'
        return response
    except Exception as e:
        logging.error(f"Error al generar vCard: {str(e)}")
        abort(500, description=f"Erro ao gerar vCard: {str(e)}")

@qrdata_bp.route('/contacto')
@validar_hmac
def mostrar_contacto():
    """Devolve a informação de um contacto em formato HTML validando o ID e o hash."""
    # Permitir compatibilidad: aceptar 'funcionarioId' (nuevo) o 'sap' (legacy)
    id_contacto = request.args.get('funcionarioId', '').strip() or request.args.get('sap', '').strip()
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

        # Consultar na tabla IAMC Funcionarios
        from extensions import IAMCSession
        from models.iamc_funcionarios_new import Funcionario, Cargo, Departamento
        
        session = IAMCSession()
        try:
            # Consulta con JOINs para obtener información completa
            funcionario_data = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Funcionario.BI,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome')
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            ).filter(
                Funcionario.FuncionarioID == int(id_contacto)
            ).first()
        finally:
            session.close()

        if not funcionario_data:
            logging.warning(f"ID não encontrado na tabla IAMC Funcionarios: {id_contacto}")
            abort(404, description="Contacto não encontrado")
        
        # Crear un objeto que simule el acceso por atributo usando la nueva estructura IAMC
        class Contacto:
            def __init__(self, data):
                self.funcionarioId = data.FuncionarioID
                self.nome = f"{data.Nome} {data.Apelido}".strip()
                self.cargo = data.CargoNome or "Sin Cargo"
                self.departamento = data.DepartamentoNome or "Sin Departamento"
                self.bi = data.BI or ""
                self.telefone = data.Telefone or ""
                self.email = data.Email or ""
                self.org = "SONANGOL"  # Organización fija
        
        contacto = Contacto(funcionario_data)

        # Generar la página HTML con los datos del contacto usando estructura IAMC
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
                <div class="info-section">
                    <p><strong>ID Funcionario:</strong> {contacto.funcionarioId}</p>
                    <p><strong>Cargo:</strong> {contacto.cargo}</p>
                    <p><strong>Departamento:</strong> {contacto.departamento}</p>
                    <p><strong>BI:</strong> {contacto.bi}</p>
                    <p><strong>Telefone:</strong> {contacto.telefone}</p>
                    <p><strong>Email:</strong> {contacto.email}</p>
                    <p><strong>Organização:</strong> {contacto.org}</p>
                </div>
                <a href="/contacto/vcard?funcionarioId={id_contacto}&hash={hash_recebido}" class="import-button">
                    Importar Contacto
                </a>
            </div>
        </body>
        </html>
        """

        logging.info(f"Acesso autorizado ao ID {id_contacto} de {request.remote_addr}")
        return render_template_string(html_template)

    except Exception as e:
        logging.error(f"Erro ao mostrar contacto: {str(e)}")
        abort(500, description=f"Erro interno: {str(e)}")
