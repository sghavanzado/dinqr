from flask import Flask, request, render_template_string, abort, jsonify, make_response
import hmac
import hashlib
import logging
from flask_limiter import Limiter
from flask_talisman import Talisman
from utils.db_utils import obtener_conexion_local, obtener_conexion_remota
import os

app = Flask(__name__, static_folder='static')

# Configuração de segurança
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Configurar Talisman para cabeçalhos de segurança
Talisman(
    app,
    content_security_policy=None,
    force_https=False,  # Desativar HTTPS
    strict_transport_security=False,  # Não habilitar HSTS
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
    """Registar detalhes de cada pedido recebido."""
    logging.info(f"Pedido recebido: {request.method} {request.url} de {request.remote_addr}")

def obter_configuracao(chave):
    """Obter um valor de configuração da tabela settings."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = %s", (chave,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Não foi encontrada a configuração '{chave}' na tabela settings.")
        return result[0]

@app.route('/contacto')
@limiter.limit("10/minuto")  # Limite de pedidos
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
            cursor.execute("SELECT * FROM sonacard WHERE sap = ?", (id_contacto,))
            contacto = cursor.fetchone()

        if not contacto:
            logging.warning(f"ID não encontrado na base de dados remota: {id_contacto}")
            abort(404, description="Contacto não encontrado")

        # Gerar a página HTML com os dados do contacto
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
                    <p><strong>Área:</strong> {contacto.area or 'Não especificada'}</p>
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

@app.route('/contacto/vcard', methods=['GET'])
def descargar_vcard():
    """Gerar e descarregar um ficheiro vCard para o contacto."""
    id_contacto = request.args.get('sap', '').strip()
    hash_recebido = request.args.get('hash', '').strip()

    try:
        # Validar parâmetros e obter dados do contacto
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT firma FROM qr_codes WHERE contact_id = %s", (id_contacto,))
            resultado_local = cursor.fetchone()

        if not resultado_local:
            abort(404, description="ID não encontrado")

        firma_local = resultado_local[0]
        if not hmac.compare_digest(firma_local, hash_recebido):
            abort(403, description="Hash inválido")

        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sonacard WHERE sap = ?", (id_contacto,))
            contacto = cursor.fetchone()

        if not contacto:
            abort(404, description="Contacto não encontrado")

        # Gerar conteúdo vCard
        vcard_content = f"""
        BEGIN:VCARD
        VERSION:3.0
        FN:{contacto.nome}
        TITLE:{contacto.funcao or ''}
        NIKENAME:{contacto.area or ''}
        ORG:{contacto.unineg or ''}
        TEL;TYPE=WORK,VOICE:{contacto.telefone or ''}
        EMAIL:{contacto.email or ''}
        END:VCARD
        """

        # Criar resposta com o ficheiro vCard
        response = make_response(vcard_content.strip())
        response.headers['Content-Type'] = 'text/vcard'
        response.headers['Content-Disposition'] = f'attachment; filename=contacto_{id_contacto}.vcf'
        return response

    except Exception as e:
        logging.error(f"Erro ao gerar vCard para o ID {id_contacto}: {str(e)}")
        abort(500, description="Erro interno do servidor")

@app.route('/server/control', methods=['POST'])
def controlar_servidor():
    """Controla o estado do servidor (iniciar, pausar, parar)."""
    acao = request.json.get('acao', '').lower()
    if acao == 'iniciar':
        logging.info("Servidor iniciado.")
        return {"message": "Servidor iniciado."}, 200
    elif acao == 'pausar':
        logging.info("Servidor pausado.")
        return {"message": "Servidor pausado."}, 200
    elif acao == 'parar':
        logging.info("Servidor parado.")
        os._exit(0)
    else:
        return {"error": "Ação inválida."}, 400

@app.errorhandler(400)
def bad_request(error):
    return "Pedido incorreto", 400

@app.errorhandler(403)
def forbidden(error):
    return "Acesso não autorizado", 403

@app.errorhandler(404)
def not_found(error):
    return "Contacto não encontrado", 404

@app.errorhandler(429)
def ratelimit_handler(error):
    return "Demasiados pedidos. Por favor, tente mais tarde.", 429

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Gestor global para erros inesperados."""
    logging.error(f"Erro inesperado: {str(error)}")
    return "Erro interno do servidor", 500

if __name__ == '__main__':
    try:
        # Forçar o uso da porta 5678
        port = 5678

        # Inicia o servidor em localhost
        app.run(host='127.0.0.1', port=port, debug=True)
    except Exception as e:
        logging.error(f"Erro ao iniciar o servidor: {str(e)}")
        print(f"❌ Erro ao iniciar o servidor: {str(e)}")