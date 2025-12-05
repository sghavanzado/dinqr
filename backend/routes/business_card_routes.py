"""
SIGA - Sistema Integral de Gestión de Accesos  
Rutas de Cartones de Visita

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Endpoints para gestión de cartones de visita digitales.
"""

from flask import Blueprint, request, jsonify, render_template_string, send_file, abort
import hmac
import logging
import time
from services.business_card_service import (
    generar_business_card,
    generar_business_cards_multiples,
    eliminar_business_card,
    obtener_funcionarios_sin_business_card,
    obtener_funcionarios_con_business_card
)
from models.business_card import BusinessCard
from utils.db_utils import remote_db_connection, local_db_connection
from marshmallow import Schema, fields, ValidationError

logger = logging.getLogger(__name__)

business_card_bp = Blueprint('business_card', __name__)

# Caché simple en memoria
_cache = {
    'funcionarios_sin_carton': {'data': None, 'timestamp': 0},
    'funcionarios_con_carton': {'data': None, 'timestamp': 0}
}
CACHE_TIMEOUT = 120  # 2 minutos


class BusinessCardRequestSchema(Schema):
    """Schema de validación para generación de cartones"""
    ids = fields.List(fields.Int(), required=True)


# ========== ENDPOINTS DE GESTIÓN ==========

@business_card_bp.route('/funcionarios-sin-carton', methods=['GET'])
def listar_funcionarios_sin_carton():
    """
    Lista funcionarios que NO tienen cartón de visita.
    Implementa caché de 2 minutos para evitar consultas repetidas.
    ---
    tags:
      - Cartones de Visita
    responses:
      200:
        description: Lista de funcionarios sin cartón
    """
    try:
        # Verificar caché
        now = time.time()
        cache_entry = _cache['funcionarios_sin_carton']
        
        if cache_entry['data'] is not None and (now - cache_entry['timestamp']) < CACHE_TIMEOUT:
            logger.info("Retornando datos desde caché")
            return jsonify(cache_entry['data']), 200
        
        # Obtener datos frescos
        logger.info("Caché expirado, consultando BD...")
        funcionarios = obtener_funcionarios_sin_business_card()
        
        # Actualizar caché
        _cache['funcionarios_sin_carton'] = {
            'data': funcionarios,
            'timestamp': now
        }
        
        return jsonify(funcionarios), 200
    except Exception as e:
        logger.error(f"Error listando funcionarios sin cartón: {str(e)}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor', 'details': str(e)}), 500


@business_card_bp.route('/funcionarios-con-carton', methods=['GET'])
def listar_funcionarios_con_carton():
    """
    Lista funcionarios que SÍ tienen cartón de visita.
    ---
    tags:
      - Cartones de Visita
    responses:
      200:
        description: Lista de funcionarios con cartón
    """
    try:
        funcionarios = obtener_funcionarios_con_business_card()
        return jsonify(funcionarios), 200
    except Exception as e:
        logger.error(f"Error listando funcionarios con cartón: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@business_card_bp.route('/generar', methods=['POST'])
def generar_cartones():
    """
    Genera cartones de visita para uno o varios funcionarios.
    ---
    tags:
      - Cartones de Visita
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - ids
          properties:
            ids:
              type: array
              items:
                type: integer
              example: [1, 2, 3]
    responses:
      200:
        description: Cartones generados exitosamente
      400:
        description: Error de validación
    """
    try:
        data = BusinessCardRequestSchema().load(request.json)
        ids = data['ids']
        resultados = generar_business_cards_multiples(ids)
        
        exitosos = sum(1 for r in resultados if r.get('success'))
        fallidos = len(resultados) - exitosos
        
        return jsonify({
            'message': f'{exitosos} cartones generados, {fallidos} fallidos',
            'resultados': resultados
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    except Exception as e:
        logger.error(f"Error generando cartones: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@business_card_bp.route('/descargar/<int:contact_id>', methods=['GET'])
def descargar_carton_qr(contact_id):
    """
    Descarga el código QR del cartón de visita.
    ---
    tags:
      - Cartones de Visita
    parameters:
      - name: contact_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Archivo QR descargado
      404:
        description: Cartón no encontrado
    """
    try:
        business_card = BusinessCard.query.filter_by(contact_id=str(contact_id)).first()
        
        if not business_card:
            return jsonify({'error': 'Cartón de visita no encontrado'}), 404
        
        return send_file(business_card.qr_code_path, as_attachment=True, download_name=f'CV-{contact_id}.png')
        
    except Exception as e:
        logger.error(f"Error descargando cartón QR {contact_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@business_card_bp.route('/eliminar/<int:contact_id>', methods=['DELETE'])
def eliminar_carton(contact_id):
    """
    Elimina un cartón de visita.
    ---
    tags:
      - Cartones de Visita
    parameters:
      - name: contact_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cartón eliminado
      404:
        description: Cartón no encontrado
    """
    try:
        resultado = eliminar_business_card(contact_id)
        
        if resultado['success']:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 404
            
    except Exception as e:
        logger.error(f"Error eliminando cartón {contact_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500


# ========== LANDING PAGE DEL CARTÓN DE VISITA ==========

@business_card_bp.route('/cartonv', methods=['GET'])
def mostrar_carton_visita():
    """
    Muestra la landing page del cartón de visita con validación HMAC.
    
    URL: /cartonv?sap=12345&hash=abc123...
    """
    sap = request.args.get('sap', '').strip()
    hash_recibido = request.args.get('hash', '').strip()
    
    logger.info(f"Acceso a cartón de visita - SAP: {sap}")
    
    # Validar parámetros
    if not sap or not hash_recibido:
        logger.warning(f"Parámetros faltantes desde {request.remote_addr}")
        abort(400, description="Parámetros faltantes")
    
    try:
        # Verificar en base de datos local
        with local_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT firma FROM business_cards WHERE contact_id = %s", (sap,))
            resultado = cursor.fetchone()
        
        if not resultado:
            logger.warning(f"Cartón no encontrado para SAP: {sap}")
            abort(404, description="Cartón de visita no encontrado")
        
        firma_local = resultado[0]
        
        # Validar firma HMAC
        if not hmac.compare_digest(firma_local, hash_recibido):
            logger.warning(f"Hash inválido para SAP {sap} desde {request.remote_addr}")
            abort(403, description="Acceso no autorizado")
        
        # Obtener datos del funcionario
        with remote_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT sap, nome, funcao, area, nif, telefone, email, unineg FROM sonacard WHERE sap = ?",
                (sap,)
            )
            contacto_data = cursor.fetchone()
        
        if not contacto_data:
            logger.warning(f"Funcionario no encontrado en BD remota: {sap}")
            abort(404, description="Funcionario no encontrado")
        
        # Crear objeto contacto
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
        
        contacto = Contacto(contacto_data)
        
        # Generar HTML del cartón de visita con diseño diferenciado
        html_template = f"""
        <!DOCTYPE html>
        <html lang="pt">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Cartão de Visita - {contacto.nome}</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                
                .business-card {{
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    max-width: 500px;
                    width: 100%;
                    overflow: hidden;
                    animation: slideIn 0.6s ease-out;
                }}
                
                @keyframes slideIn {{
                    from {{
                        opacity: 0;
                        transform: translateY(30px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
                
                .card-header {{
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    padding: 30px 20px;
                    text-align: center;
                    position: relative;
                }}
                
                .card-header::after {{
                    content: '';
                    position: absolute;
                    bottom: -20px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 40px;
                    height: 40px;
                    background: white;
                    border-radius: 50%;
                }}
                
                .logo-container {{
                    background: white;
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    margin: 0 auto 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                }}
                
                .logo-container img {{
                    height: 50px;
                }}
                
                .company-name {{
                    color: white;
                    font-size: 1.5rem;
                    font-weight: 700;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }}
                
                .card-body {{
                    padding: 40px 30px 30px;
                }}
                
                .employee-name {{
                    font-size: 2rem;
                    font-weight: 700;
                    color: #1e3c72;
                    margin-bottom: 10px;
                    text-align: center;
                }}
                
                .employee-title {{
                    font-size: 1.1rem;
                    color: #667eea;
                    text-align: center;
                    margin-bottom: 30px;
                    font-weight: 600;
                }}
                
                .info-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                
                .info-item {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 4px solid #667eea;
                }}
                
                .info-label {{
                    font-size: 0.85rem;
                    color: #6c757d;
                    font-weight: 600;
                    text-transform: uppercase;
                    margin-bottom: 5px;
                }}
                
                .info-value {{
                    font-size: 1rem;
                    color: #212529;
                    font-weight: 500;
                }}
                
                .action-button {{
                    display: block;
                    width: 100%;
                    padding: 15px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 10px;
                    text-align: center;
                    font-weight: 600;
                    font-size: 1.1rem;
                    transition: transform 0.3s ease, box-shadow 0.3s ease;
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }}
                
                .action-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
                }}
                
                .vcard-icon {{
                    margin-right: 10px;
                }}
                
                @media (max-width: 600px) {{
                    .employee-name {{
                        font-size: 1.5rem;
                    }}
                    
                    .info-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="business-card">
                <div class="card-header">
                    <div class="logo-container">
                        <img src="/static/images/sonangol-logo.png" alt="Logo" onerror="this.style.display='none'">
                    </div>
                    <div class="company-name">Sonangol</div>
                </div>
                
                <div class="card-body">
                    <h1 class="employee-name">{contacto.nome}</h1>
                    <p class="employee-title">{contacto.funcao or 'Funcionário'}</p>
                    
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">SAP</div>
                            <div class="info-value">{contacto.sap or 'N/A'}</div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">Direção</div>
                            <div class="info-value">{contacto.area or 'N/A'}</div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">U. Negócio</div>
                            <div class="info-value">{contacto.unineg or 'N/A'}</div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">NIF</div>
                            <div class="info-value">{contacto.nif or 'N/A'}</div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">Telefone</div>
                            <div class="info-value">{contacto.telefone or 'N/A'}</div>
                        </div>
                        
                        <div class="info-item">
                            <div class="info-label">Email</div>
                            <div class="info-value" style="word-break: break-all;">{contacto.email or 'N/A'}</div>
                        </div>
                    </div>
                    
                    <a href="/cartonv/vcard?sap={sap}&hash={hash_recibido}" class="action-button">
                        <span class="vcard-icon">📇</span>
                        Guardar Contato
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        
        logger.info(f"Acceso autorizado al cartón SAP {sap} desde {request.remote_addr}")
        return render_template_string(html_template)
        
    except Exception as e:
        logger.error(f"Error procesando cartón SAP {sap}: {str(e)}")
        abort(500, description="Error interno del servidor")


@business_card_bp.route('/cartonv/vcard', methods=['GET'])
def descargar_vcard_carton():
    """
    Descarga vCard del cartón de visita.
    
    URL: /cartonv/vcard?sap=12345&hash=abc123...
    """
    sap = request.args.get('sap', '').strip()
    hash_recibido = request.args.get('hash', '').strip()
    
    if not sap or not hash_recibido:
        abort(400, description="Parámetros faltantes")
    
    try:
        # Validar firma
        with local_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT firma FROM business_cards WHERE contact_id = %s", (sap,))
            resultado = cursor.fetchone()
        
        if not resultado:
            abort(404, description="Cartón no encontrado")
        
        if not hmac.compare_digest(resultado[0], hash_recibido):
            abort(403, description="Acceso no autorizado")
        
        # Obtener datos
        with remote_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nome, funcao, area, unineg, telefone, email FROM sonacard WHERE sap = ?",
                (sap,)
            )
            data = cursor.fetchone()
        
        if not data:
            abort(404, description="Funcionario no encontrado")
        
        # Generar vCard
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{data[0]}
TITLE:{data[1]}
DEPARTMENT:{data[2]}
ORG:{data[3]}
TEL;TYPE=WORK,VOICE:{data[4]}
EMAIL:{data[5]}
END:VCARD
"""
        
        from flask import Response
        response = Response(vcard, mimetype='text/vcard; charset=utf-8')
        response.headers['Content-Disposition'] = f'attachment; filename=CV-{sap}.vcf'
        return response
        
    except Exception as e:
        logger.error(f"Error generando vCard para SAP {sap}: {str(e)}")
        abort(500, description="Error interno del servidor")
