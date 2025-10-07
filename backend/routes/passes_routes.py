"""
Employee Pass Generation Routes
Geração de passes de funcionários para impressão em formato CR80
"""

from flask import Blueprint, request, jsonify, render_template, make_response, send_file
from marshmallow import Schema, fields, ValidationError
import logging
import os
import tempfile
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from controllers.iamc_funcionarios_controller_new import FuncionarioController
from utils.api_helpers import success_response, error_response
from sqlalchemy import text
from extensions import get_iamc_session
# from utils.db_utils import obtener_conexao_local  # Temporarily commented out
import pyodbc
import os

passes_bp = Blueprint('passes', __name__)

# Local database connection function
def obtener_conexao_local():
    """Obtener una conexión a la base de datos IAMC (MSSQL)."""
    try:
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER', 'localhost')};"
            f"DATABASE=IAMC;"
            f"UID=sa;"
            f"PWD=Global2020;"
            f"TrustServerCertificate=yes",
            timeout=10
        )
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos IAMC: {str(e)}")
        raise ConnectionError(f"Error al conectar con la base de datos IAMC: {str(e)}")

class PassRequestSchema(Schema):
    """Schema para validação de requisições de geração de passe"""
    funcionario_id = fields.Integer(required=True)
    incluir_qr = fields.Boolean(load_default=True)
    data_validade = fields.Date(load_default=None, allow_none=True)
    tema_id = fields.Integer(load_default=1)  # ID do tema da base de dados
    formato_id = fields.Integer(load_default=1)  # ID do formato da base de dados

class TemaConfigSchema(Schema):
    """Schema para configuração avançada de temas"""
    nome = fields.String(required=True, validate=lambda x: len(x.strip()) > 0)
    # Cores
    cor_primaria = fields.String(required=True, validate=lambda x: x.startswith('#') and len(x) == 7)
    cor_secundaria = fields.String(load_default='#ffffff')
    cor_texto = fields.String(load_default='#000000')
    cor_borda = fields.String(load_default='#cccccc')
    # Layout
    layout_tipo = fields.String(load_default='horizontal', validate=lambda x: x in ['horizontal', 'vertical', 'compact'])
    margem_superior = fields.Float(load_default=5.0)  # mm
    margem_inferior = fields.Float(load_default=5.0)  # mm
    margem_esquerda = fields.Float(load_default=5.0)  # mm
    margem_direita = fields.Float(load_default=5.0)  # mm
    # Tipografia
    fonte_titulo = fields.String(load_default='Helvetica-Bold')
    tamanho_fonte_titulo = fields.Integer(load_default=12)
    fonte_nome = fields.String(load_default='Helvetica-Bold')
    tamanho_fonte_nome = fields.Integer(load_default=10)
    fonte_cargo = fields.String(load_default='Helvetica')
    tamanho_fonte_cargo = fields.Integer(load_default=8)
    fonte_info = fields.String(load_default='Helvetica')
    tamanho_fonte_info = fields.Integer(load_default=7)
    # Elementos gráficos
    mostrar_logo = fields.Boolean(load_default=True)
    posicao_logo = fields.String(load_default='superior_esquerda', validate=lambda x: x in ['superior_esquerda', 'superior_direita', 'superior_centro', 'inferior_esquerda', 'inferior_direita'])
    tamanho_logo = fields.Float(load_default=15.0)  # mm
    mostrar_qr_borda = fields.Boolean(load_default=True)
    qr_tamanho = fields.Float(load_default=20.0)  # mm
    qr_posicao = fields.String(load_default='direita', validate=lambda x: x in ['direita', 'esquerda', 'centro'])
    # Fundo
    fundo_tipo = fields.String(load_default='solido', validate=lambda x: x in ['solido', 'gradiente', 'imagem'])
    fundo_cor = fields.String(load_default='#ffffff')
    fundo_cor_gradiente = fields.String(load_default='#f0f0f0')
    fundo_imagem_url = fields.String(load_default='')
    fundo_opacidade = fields.Float(load_default=1.0, validate=lambda x: 0.0 <= x <= 1.0)
    # Estado
    ativo = fields.Boolean(load_default=True)
    # Design visual (CardDesigner JSON)
    design = fields.Dict(load_default=None, allow_none=True)

class FormatoConfigSchema(Schema):
    """Schema para configuração de formatos com medidas padrão"""
    nome = fields.String(required=True, validate=lambda x: len(x.strip()) > 0)
    extensao = fields.String(required=True, validate=lambda x: x in ['pdf', 'html', 'png', 'svg'])
    descricao = fields.String(load_default='')
    # Medidas padrão (mm)
    largura = fields.Float(load_default=85.6)  # CR80 padrão
    altura = fields.Float(load_default=53.98)  # CR80 padrão
    dpi = fields.Integer(load_default=300)
    orientacao = fields.String(load_default='horizontal', validate=lambda x: x in ['horizontal', 'vertical'])
    # Configurações específicas do formato
    qualidade = fields.Integer(load_default=95, validate=lambda x: 1 <= x <= 100)
    compressao = fields.Boolean(load_default=False)
    ativo = fields.Boolean(load_default=True)

# Medidas padrão para passes empresariais
MEDIDAS_PADRAO = {
    'CR80': {'largura': 85.6, 'altura': 53.98, 'descricao': 'Cartão de crédito padrão'},
    'CR100': {'largura': 98.5, 'altura': 67.0, 'descricao': 'Cartão grande'},
    'BUSINESS': {'largura': 89.0, 'altura': 51.0, 'descricao': 'Cartão de visita'},
    'BADGE': {'largura': 76.2, 'altura': 101.6, 'descricao': 'Crachá vertical'},
    'MINI': {'largura': 70.0, 'altura': 45.0, 'descricao': 'Mini cartão'},
}

def gerar_qr_funcionario(funcionario_data):
    """Gera código QR com dados do funcionário"""
    try:
        # Dados para o QR code
        qr_data = {
            'id': funcionario_data.get('funcionarioID'),
            'nome': funcionario_data.get('nome'),
            'cargo': funcionario_data.get('cargo'),
            'departamento': funcionario_data.get('departamento'),
            'data_emissao': datetime.now().strftime('%Y-%m-%d')
        }
        
        qr_string = f"FUNCIONARIO:{qr_data['id']}|{qr_data['nome']}|{qr_data['cargo']}|{qr_data['departamento']}|{qr_data['data_emissao']}"
        
        # Gerar QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_string)
        qr.make(fit=True)
        
        # Criar imagem
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para base64
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{qr_base64}"
        
    except Exception as e:
        logging.error(f"Erro ao gerar QR code: {str(e)}")
        return None

def obter_foto_funcionario(funcionario_id):
    """Obtém URL da foto do funcionário ou retorna placeholder"""
    try:
        # Verificar se existe foto personalizada
        foto_path = f"static/images/funcionarios/{funcionario_id}.jpg"
        if os.path.exists(foto_path):
            return f"/static/images/funcionarios/{funcionario_id}.jpg"
        else:
            # Retornar placeholder padrão
            return "/static/images/default-avatar.png"
    except Exception as e:
        logging.error(f"Erro ao obter foto do funcionário {funcionario_id}: {str(e)}")
        return "/static/images/default-avatar.png"

def gerar_pdf_pass_avancado(template_data, tema_config=None, formato_config=None):
    """
    Gera PDF do passe de funcionário com configurações avançadas
    """
    try:
        # Buffer para o PDF
        buffer = BytesIO()
        
        # Usar configurações do formato ou padrão CR80
        if formato_config:
            largura = formato_config['largura'] * mm
            altura = formato_config['altura'] * mm
        else:
            largura = 85.6 * mm
            altura = 53.98 * mm
        
        # Criar canvas
        c = canvas.Canvas(buffer, pagesize=(largura, altura))
        
        # Aplicar tema se fornecido
        if tema_config:
            aplicar_tema_ao_pdf(c, tema_config, template_data)
        else:
            # Fundo padrão
            c.setFillColor(colors.white)
            c.rect(0, 0, largura, altura, fill=1)
        
        # Obter configurações de tema ou usar padrões
        if tema_config:
            fonte_titulo = tema_config.get('fonte_titulo', 'Helvetica-Bold')
            tamanho_fonte_titulo = tema_config.get('tamanho_fonte_titulo', 12)
            fonte_nome = tema_config.get('fonte_nome', 'Helvetica-Bold')
            tamanho_fonte_nome = tema_config.get('tamanho_fonte_nome', 10)
            fonte_cargo = tema_config.get('fonte_cargo', 'Helvetica')
            tamanho_fonte_cargo = tema_config.get('tamanho_fonte_cargo', 8)
            fonte_info = tema_config.get('fonte_info', 'Helvetica')
            tamanho_fonte_info = tema_config.get('tamanho_fonte_info', 7)
            cor_texto = tema_config.get('cor_texto', '#000000')
            margem_esq = tema_config.get('margem_esquerda', 5.0) * mm / 10
            margem_sup = tema_config.get('margem_superior', 5.0) * mm / 10
            qr_tamanho = tema_config.get('qr_tamanho', 20.0) * mm / 10
            qr_posicao = tema_config.get('qr_posicao', 'direita')
        else:
            # Configurações padrão
            fonte_titulo = 'Helvetica-Bold'
            tamanho_fonte_titulo = 12
            fonte_nome = 'Helvetica-Bold'
            tamanho_fonte_nome = 10
            fonte_cargo = 'Helvetica'
            tamanho_fonte_cargo = 8
            fonte_info = 'Helvetica'
            tamanho_fonte_info = 7
            cor_texto = '#000000'
            margem_esq = 8
            margem_sup = 15
            qr_tamanho = 35
            qr_posicao = 'direita'
        
        # Definir cor do texto
        c.setFillColor(cor_texto)
        
        # Título da empresa (usar configurações de fonte)
        c.setFont(fonte_titulo, tamanho_fonte_titulo)
        empresa_nome = template_data.get('empresa_nome', 'DINQR SYSTEM')
        text_width = c.stringWidth(empresa_nome, fonte_titulo, tamanho_fonte_titulo)
        c.drawString((largura - text_width) / 2, altura - margem_sup, empresa_nome)
        
        # Nome do funcionário
        c.setFont(fonte_nome, tamanho_fonte_nome)
        nome = template_data.get('funcionario_nome', 'Nome do Funcionário')
        # Ajustar nome baseado na largura disponível
        max_width = largura - 2 * margem_esq - (qr_tamanho if qr_posicao == 'direita' else 0)
        while c.stringWidth(nome, fonte_nome, tamanho_fonte_nome) > max_width and len(nome) > 10:
            nome = nome[:-4] + "..."
        c.drawString(margem_esq, altura - margem_sup - 20, nome)
        
        # ID do funcionário
        c.setFont(fonte_info, tamanho_fonte_info)
        funcionario_id = f"ID: {template_data.get('funcionario_id', 'N/A')}"
        c.drawString(margem_esq, altura - margem_sup - 32, funcionario_id)
        
        # Cargo
        c.setFont(fonte_cargo, tamanho_fonte_cargo)
        cargo = template_data.get('cargo', 'N/A')
        max_cargo_width = largura - 2 * margem_esq - (qr_tamanho if qr_posicao == 'direita' else 0)
        while c.stringWidth(cargo, fonte_cargo, tamanho_fonte_cargo) > max_cargo_width and len(cargo) > 8:
            cargo = cargo[:-4] + "..."
        c.drawString(margem_esq, altura - margem_sup - 45, cargo)
        
        # Departamento
        departamento = template_data.get('departamento', 'N/A')
        while c.stringWidth(departamento, fonte_info, tamanho_fonte_info) > max_cargo_width and len(departamento) > 8:
            departamento = departamento[:-4] + "..."
        c.setFont(fonte_info, tamanho_fonte_info)
        c.drawString(margem_esq, altura - margem_sup - 55, departamento)
        
        # Data de emissão (canto inferior esquerdo)
        c.setFont(fonte_info, tamanho_fonte_info - 1)
        data_emissao = f"Emitido: {template_data.get('data_emissao', 'N/A')}"
        c.drawString(margem_esq, 8, data_emissao)
        
        # Data de validade (canto inferior direito)
        data_validade = f"Válido até: {template_data.get('data_validade', 'N/A')}"
        text_width = c.stringWidth(data_validade, fonte_info, tamanho_fonte_info - 1)
        c.drawString(largura - text_width - margem_esq, 8, data_validade)
        
        # Posicionar QR Code baseado na configuração
        if qr_posicao == 'direita':
            qr_x = largura - qr_tamanho - margem_esq
            qr_y = altura - qr_tamanho - margem_sup - 5
        elif qr_posicao == 'esquerda':
            qr_x = margem_esq
            qr_y = altura - qr_tamanho - margem_sup - 5
        else:  # centro
            qr_x = (largura - qr_tamanho) / 2
            qr_y = altura - qr_tamanho - margem_sup - 5
        
        # Adicionar QR code se disponível
        qr_url = template_data.get('qr_url')
        if qr_url and qr_url.startswith('data:image'):
            try:
                # Decodificar base64 do QR
                qr_data = qr_url.split(',')[1]
                qr_bytes = base64.b64decode(qr_data)
                qr_image = ImageReader(BytesIO(qr_bytes))
                c.drawImage(qr_image, qr_x, qr_y, qr_tamanho, qr_tamanho)
                
                # Adicionar borda ao QR se configurado
                if tema_config and tema_config.get('mostrar_qr_borda', True):
                    c.setStrokeColor(tema_config.get('cor_borda', '#cccccc'))
                    c.setLineWidth(0.5)
                    c.rect(qr_x, qr_y, qr_tamanho, qr_tamanho, fill=0, stroke=1)
                    
            except Exception as e:
                logging.warning(f"Erro ao adicionar QR code ao PDF: {str(e)}")
                # Desenhar placeholder para QR
                c.setStrokeColor(colors.lightgrey)
                c.rect(qr_x, qr_y, qr_tamanho, qr_tamanho, fill=0)
                c.setFont("Helvetica", 8)
                c.drawString(qr_x + qr_tamanho/3, qr_y + qr_tamanho/2, "QR")
        
        # Adicionar logo se configurado
        if tema_config and tema_config.get('mostrar_logo', True):
            logo_url = template_data.get('logo_url')
            if logo_url and os.path.exists(logo_url.replace('/', '\\')):
                tamanho_logo = tema_config.get('tamanho_logo', 15.0) * mm / 10
                posicao_logo = tema_config.get('posicao_logo', 'superior_esquerda')
                
                # Calcular posição do logo
                if posicao_logo == 'superior_esquerda':
                    logo_x, logo_y = margem_esq, altura - tamanho_logo - 5
                elif posicao_logo == 'superior_direita':
                    logo_x, logo_y = largura - tamanho_logo - margem_esq, altura - tamanho_logo - 5
                elif posicao_logo == 'superior_centro':
                    logo_x, logo_y = (largura - tamanho_logo) / 2, altura - tamanho_logo - 5
                else:
                    logo_x, logo_y = margem_esq, 15
                
                try:
                    c.drawImage(logo_url, logo_x, logo_y, tamanho_logo, tamanho_logo)
                except Exception as e:
                    logging.warning(f"Erro ao adicionar logo: {str(e)}")
        
        # Finalizar PDF
        c.save()
        
        # Retornar conteúdo do buffer
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        logging.error(f"Erro ao gerar PDF avançado: {str(e)}")
        raise e

@passes_bp.route('/gerar', methods=['POST'])
def gerar_passe():
    """
    POST /api/rrhh/passes/gerar
    Gera passe de funcionário em PDF ou HTML
    """
    try:
        # Validar dados de entrada
        schema = PassRequestSchema()
        try:
            data = schema.load(request.json or {})
        except ValidationError as err:
            return error_response("Dados inválidos", details=err.messages), 400

        funcionario_id = data['funcionario_id']
        
        # Obter dados do funcionário
        funcionario_response = FuncionarioController.obter_por_id(funcionario_id)
        
        if funcionario_response[1] != 200:
            return error_response("Funcionário não encontrado"), 404
            
        funcionario_data = funcionario_response[0].json.get('data', {})
        
        # Preparar dados para o template
        template_data = {
            'funcionario_id': funcionario_data.get('funcionarioID'),
            'funcionario_nome': f"{funcionario_data.get('nome', '')} {funcionario_data.get('apelido', '')}".strip(),
            'cargo': funcionario_data.get('cargo', 'N/A'),
            'departamento': funcionario_data.get('departamento', 'N/A'),
            'empresa_nome': 'DINQR SYSTEM',  # Pode ser configurável
            'data_emissao': datetime.now().strftime('%d/%m/%Y'),
            'data_validade': (data.get('data_validade') or (datetime.now() + timedelta(days=365))).strftime('%d/%m/%Y'),
            'foto_url': obter_foto_funcionario(funcionario_id),
            'logo_url': '/static/images/sonangol-logo.png',  # Logo da empresa
            'tema': f"theme-{data['tema']}" if data['tema'] != 'default' else ''
        }
        
        # Gerar QR code se solicitado
        if data['incluir_qr']:
            qr_url = gerar_qr_funcionario(funcionario_data)
            if qr_url:
                template_data['qr_url'] = qr_url
            else:
                template_data['qr_url'] = '/static/images/qr-placeholder.png'
        else:
            template_data['qr_url'] = '/static/images/qr-placeholder.png'
        
        # Renderizar template HTML
        html_content = render_template('employee_pass_template.html', **template_data)
        
        if data['formato_saida'] == 'html':
            # Retornar HTML diretamente
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
        
        else:
            # Gerar PDF usando ReportLab com configurações avançadas
            try:
                # Criar tabelas se não existirem
                criar_tabelas_configuracao()
                
                # Obter configurações de tema e formato
                tema_config = None
                formato_config = None
                
                if 'tema_id' in data:
                    tema_config = obter_tema_por_id(data['tema_id'])
                
                if 'formato_id' in data:
                    formato_config = obter_formato_por_id(data['formato_id'])
                
                # Criar arquivo temporário para o PDF
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                    
                    # Gerar PDF com configurações avançadas
                    pdf_content = gerar_pdf_pass_avancado(template_data, tema_config, formato_config)
                    temp_file.write(pdf_content)
                    temp_file.flush()
                    
                    # Retornar PDF
                    response = make_response(pdf_content)
                    response.headers['Content-Type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = f'attachment; filename="passe_funcionario_{funcionario_id}.pdf"'
                    
                    # Limpar arquivo temporário
                    os.unlink(temp_file.name)
                    
                    return response
                    
            except Exception as pdf_error:
                logging.error(f"Erro ao gerar PDF: {str(pdf_error)}")
                return error_response(f"Erro ao gerar PDF: {str(pdf_error)}"), 500
        
    except Exception as e:
        logging.error(f"Erro ao gerar passe: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/lote', methods=['POST'])
def gerar_passes_lote():
    """
    POST /api/rrhh/passes/lote
    Gera passes para múltiplos funcionários
    """
    try:
        data = request.json or {}
        funcionario_ids = data.get('funcionario_ids', [])
        opcoes = data.get('opcoes', {})
        
        if not funcionario_ids:
            return error_response("Lista de funcionários é obrigatória"), 400
        
        passes_gerados = []
        erros = []
        
        for funcionario_id in funcionario_ids:
            try:
                # Preparar dados para geração individual
                pass_data = {
                    'funcionario_id': funcionario_id,
                    'incluir_qr': opcoes.get('incluir_qr', True),
                    'tema': opcoes.get('tema', 'default'),
                    'formato_saida': 'pdf'  # Sempre PDF para lotes
                }
                
                # Simular request para reutilizar lógica
                request.json = pass_data
                response = gerar_passe()
                
                if response[1] == 200:
                    passes_gerados.append({
                        'funcionario_id': funcionario_id,
                        'status': 'sucesso'
                    })
                else:
                    erros.append({
                        'funcionario_id': funcionario_id,
                        'erro': 'Falha na geração'
                    })
                    
            except Exception as e:
                erros.append({
                    'funcionario_id': funcionario_id,
                    'erro': str(e)
                })
        
        return success_response({
            'passes_gerados': len(passes_gerados),
            'total_solicitados': len(funcionario_ids),
            'sucessos': passes_gerados,
            'erros': erros
        })
        
    except Exception as e:
        logging.error(f"Erro ao gerar passes em lote: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/preview/<int:funcionario_id>', methods=['GET'])
def preview_passe(funcionario_id):
    """
    GET /api/rrhh/passes/preview/{funcionario_id}
    Gera pré-visualização do passe em HTML
    """
    try:
        # Validar entrada
        schema = PassRequestSchema()
        
        # Preparar dados para preview com valores padrão
        preview_data = {
            'funcionario_id': funcionario_id,
            'incluir_qr': True,
            'tema_id': 1,  # Tema padrão
            'formato_id': 1  # Formato padrão
        }
        
        # Validar dados
        try:
            data = schema.load(preview_data)
        except ValidationError as err:
            return error_response("Dados inválidos para preview", details=err.messages), 400

        # Obter dados do funcionário
        funcionario_response = FuncionarioController.obter_por_id(funcionario_id)
        
        if funcionario_response[1] != 200:
            return error_response("Funcionário não encontrado"), 404
            
        funcionario_data = funcionario_response[0].json.get('data', {})
        
        # Preparar dados para o template
        template_data = {
            'funcionario_id': funcionario_data.get('funcionarioID'),
            'funcionario_nome': f"{funcionario_data.get('nome', '')} {funcionario_data.get('apelido', '')}".strip(),
            'cargo': funcionario_data.get('cargo', 'N/A'),
            'departamento': funcionario_data.get('departamento', 'N/A'),
            'empresa_nome': 'DINQR SYSTEM',
            'data_emissao': datetime.now().strftime('%d/%m/%Y'),
            'data_validade': (datetime.now() + timedelta(days=365)).strftime('%d/%m/%Y'),
            'foto_url': obter_foto_funcionario(funcionario_id),
            'logo_url': '/static/images/sonangol-logo.png',
            'tema': f"theme-{data['tema_id']}" if data['tema_id'] != 1 else ''
        }
        
        # Gerar QR code se solicitado
        if data['incluir_qr']:
            qr_url = gerar_qr_funcionario(funcionario_data)
            if qr_url:
                template_data['qr_url'] = qr_url
            else:
                template_data['qr_url'] = '/static/images/qr-placeholder.png'
        else:
            template_data['qr_url'] = '/static/images/qr-placeholder.png'
        
        # Renderizar template HTML para preview
        html_content = render_template('employee_pass_template.html', **template_data)
        
        # Retornar HTML diretamente
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
        
    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        logging.error(f"Erro ao gerar preview: {str(e)}")
        logging.error(f"Stack trace completo: {full_error}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/preview-new/<int:funcionario_id>', methods=['GET'])
def preview_passe_new(funcionario_id):
    """
    GET /api/iamc/passes/preview-new/{funcionario_id}
    Nova versão do endpoint de pré-visualização do passe em HTML
    """
    try:
        # Validar entrada
        schema = PassRequestSchema()
        
        # Preparar dados para preview com valores padrão
        preview_data = {
            'funcionario_id': funcionario_id,
            'incluir_qr': True,
            'tema_id': 1,  # Tema padrão
            'formato_id': 1  # Formato padrão
        }
        
        # Validar dados
        try:
            data = schema.load(preview_data)
        except ValidationError as err:
            return error_response("Dados inválidos para preview", details=err.messages), 400

        # Obter dados do funcionário
        funcionario_response = FuncionarioController.obter_por_id(funcionario_id)
        
        if funcionario_response[1] != 200:
            return error_response("Funcionário não encontrado"), 404
            
        funcionario_data = funcionario_response[0].json.get('data', {})
        
        # Preparar dados para o template
        template_data = {
            'funcionario_id': funcionario_data.get('funcionarioID'),
            'funcionario_nome': f"{funcionario_data.get('nome', '')} {funcionario_data.get('apelido', '')}".strip(),
            'cargo': funcionario_data.get('cargo', 'N/A'),
            'departamento': funcionario_data.get('departamento', 'N/A'),
            'empresa_nome': 'DINQR SYSTEM',
            'data_emissao': datetime.now().strftime('%d/%m/%Y'),
            'data_validade': (datetime.now() + timedelta(days=365)).strftime('%d/%m/%Y'),
            'foto_url': obter_foto_funcionario(funcionario_id),
            'logo_url': '/static/images/sonangol-logo.png',
            'tema': f"theme-{data['tema_id']}" if data['tema_id'] != 1 else ''
        }
        
        # Gerar QR code se solicitado
        if data['incluir_qr']:
            qr_url = gerar_qr_funcionario(funcionario_data)
            if qr_url:
                template_data['qr_url'] = qr_url
            else:
                template_data['qr_url'] = '/static/images/qr-placeholder.png'
        else:
            template_data['qr_url'] = '/static/images/qr-placeholder.png'
        
        # Renderizar template HTML para preview
        html_content = render_template('employee_pass_template.html', **template_data)
        
        # Retornar HTML diretamente
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
        
    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        logging.error(f"Erro ao gerar preview novo: {str(e)}")
        logging.error(f"Stack trace completo: {full_error}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/configuracao', methods=['GET'])
def obter_configuracao():
    """
    GET /api/iamc/passes/configuracao
    Retorna configurações dinâmicas disponíveis para passes
    """
    try:
        criar_tabelas_configuracao()
        
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Obter temas ativos
        cursor.execute("""
            SELECT id, nome, cor_primaria, cor_secundaria, cor_texto, layout_tipo
            FROM pass_temas_avancado
            WHERE ativo = 1
            ORDER BY nome
        """)
        
        temas_disponiveis = []
        for row in cursor.fetchall():
            temas_disponiveis.append({
                'id': row[0],
                'nome': row[1],
                'cor_primaria': row[2],
                'cor_secundaria': row[3],
                'cor_texto': row[4],
                'layout_tipo': row[5]
            })
        
        # Obter formatos ativos
        cursor.execute("""
            SELECT id, nome, extensao, descricao, largura, altura, dpi
            FROM pass_formatos_avancado
            WHERE ativo = 1
            ORDER BY nome
        """)
        
        formatos_saida = []
        for row in cursor.fetchall():
            formatos_saida.append({
                'id': row[0],
                'nome': row[1],
                'extensao': row[2],
                'descricao': row[3],
                'largura': row[4],
                'altura': row[5],
                'dpi': row[6]
            })
        
        conn.close()
        
        configuracao = {
            'temas_disponiveis': temas_disponiveis,
            'formatos_saida': formatos_saida,
            'dimensoes': {
                'formato': 'CR80',
                'largura_mm': 85.6,
                'altura_mm': 54.0,
                'dpi_recomendado': 300
            },
            'medidas_padrao': MEDIDAS_PADRAO,
            'opcoes_layout': [
                {'id': 'horizontal', 'nome': 'Horizontal', 'descricao': 'Layout tradicional'},
                {'id': 'vertical', 'nome': 'Vertical', 'descricao': 'Layout em crachá'},
                {'id': 'compact', 'nome': 'Compacto', 'descricao': 'Layout compacto'}
            ],
            'opcoes_fonte': [
                {'id': 'Helvetica', 'nome': 'Helvetica'},
                {'id': 'Helvetica-Bold', 'nome': 'Helvetica Bold'},
                {'id': 'Times-Roman', 'nome': 'Times'},
                {'id': 'Times-Bold', 'nome': 'Times Bold'},
                {'id': 'Courier', 'nome': 'Courier'},
                {'id': 'Courier-Bold', 'nome': 'Courier Bold'}
            ],
            'opcoes_fundo': [
                {'id': 'solido', 'nome': 'Cor Sólida'},
                {'id': 'gradiente', 'nome': 'Gradiente'},
                {'id': 'imagem', 'nome': 'Imagem de Fundo'}
            ],
            'validade_padrao_dias': 365,
            'versao_api': '2.0'
        }
        
        return success_response(configuracao)
        
    except Exception as e:
        logging.error(f"Erro ao obter configuração: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/configuracao-safe', methods=['GET'])
def obter_configuracao_safe():
    """
    GET /api/iamc/passes/configuracao-safe
    Safe version of configuration endpoint with better error handling
    """
    try:
        # Return a minimal configuration to get the frontend working
        configuracao = {
            'temas_disponiveis': [
                {
                    'id': 1,
                    'nome': 'Tema Padrão',
                    'cor_primaria': '#1976d2',
                    'cor_secundaria': '#ffffff',
                    'cor_texto': '#000000',
                    'layout_tipo': 'horizontal'
                }
            ],
            'formatos_saida': [
                {
                    'id': 1,
                    'nome': 'PDF Padrão',
                    'extensao': 'pdf',
                    'descricao': 'Formato padrão PDF',
                    'largura': 85.6,
                    'altura': 53.98,
                    'dpi': 300
                }
            ],
            'dimensoes': {
                'formato': 'CR80',
                'largura_mm': 85.6,
                'altura_mm': 54.0,
                'dpi_recomendado': 300
            },
            'medidas_padrao': {
                'CR80': {'largura': 85.6, 'altura': 53.98, 'descricao': 'Cartão de crédito padrão'},
                'A4': {'largura': 210.0, 'altura': 297.0, 'descricao': 'Papel A4'}
            },
            'opcoes_layout': [
                {'id': 'horizontal', 'nome': 'Horizontal', 'descricao': 'Layout tradicional'},
                {'id': 'vertical', 'nome': 'Vertical', 'descricao': 'Layout em crachá'}
            ],
            'opcoes_fonte': [
                {'id': 'Helvetica', 'nome': 'Helvetica'},
                {'id': 'Helvetica-Bold', 'nome': 'Helvetica Bold'}
            ],
            'opcoes_fundo': [
                {'id': 'solido', 'nome': 'Cor Sólida'},
                {'id': 'gradiente', 'nome': 'Gradiente'}
            ],
            'validade_padrao_dias': 365,
            'versao_api': '2.0'
        }
        
        logging.info("Configuração safe retornada com sucesso")
        return success_response(configuracao)
        
    except Exception as e:
        import traceback
        full_error = traceback.format_exc()
        logging.error(f"Erro na configuração safe: {str(e)}")
        logging.error(f"Stack trace: {full_error}")
        return error_response(f"Erro interno: {str(e)}"), 500

# Funções auxiliares para configurações avançadas
def criar_tabelas_configuracao():
    """Cria tabelas de configuração avançada se não existirem"""
    try:
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Tabela para temas avançados
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pass_temas_avancado' AND xtype='U')
            CREATE TABLE pass_temas_avancado (
                id INT IDENTITY(1,1) PRIMARY KEY,
                nome NVARCHAR(100) NOT NULL UNIQUE,
                -- Cores
                cor_primaria NVARCHAR(7) NOT NULL DEFAULT '#1976d2',
                cor_secundaria NVARCHAR(7) DEFAULT '#ffffff',
                cor_texto NVARCHAR(7) DEFAULT '#000000',
                cor_borda NVARCHAR(7) DEFAULT '#cccccc',
                -- Layout
                layout_tipo NVARCHAR(20) DEFAULT 'horizontal',
                margem_superior FLOAT DEFAULT 5.0,
                margem_inferior FLOAT DEFAULT 5.0,
                margem_esquerda FLOAT DEFAULT 5.0,
                margem_direita FLOAT DEFAULT 5.0,
                -- Tipografia
                fonte_titulo NVARCHAR(50) DEFAULT 'Helvetica-Bold',
                tamanho_fonte_titulo INT DEFAULT 12,
                fonte_nome NVARCHAR(50) DEFAULT 'Helvetica-Bold',
                tamanho_fonte_nome INT DEFAULT 10,
                fonte_cargo NVARCHAR(50) DEFAULT 'Helvetica',
                tamanho_fonte_cargo INT DEFAULT 8,
                fonte_info NVARCHAR(50) DEFAULT 'Helvetica',
                tamanho_fonte_info INT DEFAULT 7,
                -- Elementos gráficos
                mostrar_logo BIT DEFAULT 1,
                posicao_logo NVARCHAR(30) DEFAULT 'superior_esquerda',
                tamanho_logo FLOAT DEFAULT 15.0,
                mostrar_qr_borda BIT DEFAULT 1,
                qr_tamanho FLOAT DEFAULT 20.0,
                qr_posicao NVARCHAR(20) DEFAULT 'direita',
                -- Fundo
                fundo_tipo NVARCHAR(20) DEFAULT 'solido',
                fundo_cor NVARCHAR(7) DEFAULT '#ffffff',
                fundo_cor_gradiente NVARCHAR(7) DEFAULT '#f0f0f0',
                fundo_imagem_url NVARCHAR(255) DEFAULT '',
                fundo_opacidade FLOAT DEFAULT 1.0,
                -- Estado
                ativo BIT DEFAULT 1,
                data_criacao DATETIME DEFAULT GETDATE(),
                data_atualizacao DATETIME DEFAULT GETDATE(),
                -- Design visual (CardDesigner JSON)
                design NVARCHAR(MAX) DEFAULT NULL
            )
        """)
        
        # Tabela para formatos avançados
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pass_formatos_avancado' AND xtype='U')
            CREATE TABLE pass_formatos_avancado (
                id INT IDENTITY(1,1) PRIMARY KEY,
                nome NVARCHAR(100) NOT NULL UNIQUE,
                extensao NVARCHAR(10) NOT NULL,
                descricao NVARCHAR(255),
                -- Medidas
                largura FLOAT DEFAULT 85.6,
                altura FLOAT DEFAULT 53.98,
                dpi INT DEFAULT 300,
                orientacao NVARCHAR(20) DEFAULT 'horizontal',
                -- Configurações
                qualidade INT DEFAULT 95,
                compressao BIT DEFAULT 0,
                ativo BIT DEFAULT 1,
                data_criacao DATETIME DEFAULT GETDATE(),
                data_atualizacao DATETIME DEFAULT GETDATE()
            )
        """)
        
        # Migração: Adicionar campo design se não existir
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS 
                              WHERE TABLE_NAME = 'pass_temas_avancado' AND COLUMN_NAME = 'design')
                BEGIN
                    ALTER TABLE pass_temas_avancado ADD design NVARCHAR(MAX) DEFAULT NULL
                END
            """)
            conn.commit()
        except Exception as e:
            logging.warning(f"Erro ao adicionar campo design: {e}")
        
        # Comentado: Inserir temas padrão automaticamente causa problemas
        # quando o usuário borra todos os temas, eles se recrean automáticamente
        # cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado")
        # if cursor.fetchone()[0] == 0:
        #     # Solo insertar temas por defecto en primera instalación, no automáticamente
        
        # Inserir formatos padrão se a tabela está vazia
        cursor.execute("SELECT COUNT(*) FROM pass_formatos_avancado")
        if cursor.fetchone()[0] == 0:
            formatos_padrao = [
                ('PDF Padrão CR80', 'pdf', 'Cartão padrão para impressão', 85.6, 53.98, 300, 'horizontal', 95),
                ('PDF Crachá Vertical', 'pdf', 'Crachá vertical para funcionários', 76.2, 101.6, 300, 'vertical', 95),
                ('HTML Preview', 'html', 'Visualização no navegador', 85.6, 53.98, 72, 'horizontal', 100),
                ('PNG Alta Qualidade', 'png', 'Imagem para uso digital', 85.6, 53.98, 300, 'horizontal', 100),
                ('PDF Business Card', 'pdf', 'Formato cartão de visita', 89.0, 51.0, 300, 'horizontal', 95)
            ]
            
            for formato in formatos_padrao:
                cursor.execute("""
                    INSERT INTO pass_formatos_avancado 
                    (nome, extensao, descricao, largura, altura, dpi, orientacao, qualidade)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, formato)
        
        conn.commit()
        conn.close()
        logging.info("Tabelas de configuração avançada criadas/verificadas com sucesso")
        
    except Exception as e:
        logging.error(f"Erro ao criar tabelas de configuração: {str(e)}")
        raise e

def aplicar_tema_ao_pdf(canvas_obj, tema_config, template_data):
    """Aplica configurações avançadas de tema ao PDF"""
    try:
        # Definir dimensões baseadas no tema
        largura = 85.6 * mm  # Pode ser configurável futuramente
        altura = 53.98 * mm
        
        # Aplicar fundo
        if tema_config.get('fundo_tipo') == 'solido':
            canvas_obj.setFillColor(tema_config.get('fundo_cor', '#ffffff'))
            canvas_obj.rect(0, 0, largura, altura, fill=1, stroke=0)
        elif tema_config.get('fundo_tipo') == 'gradiente':
            # Simular gradiente com retângulos sobrepostos
            cor_base = tema_config.get('fundo_cor', '#ffffff')
            cor_gradiente = tema_config.get('fundo_cor_gradiente', '#f0f0f0')
            canvas_obj.setFillColor(cor_base)
            canvas_obj.rect(0, 0, largura, altura, fill=1, stroke=0)
            # Adicionar efeito de gradiente (simplificado)
            canvas_obj.setFillColor(cor_gradiente)
            canvas_obj.setFillAlpha(tema_config.get('fundo_opacidade', 0.5))
            canvas_obj.rect(0, altura/2, largura, altura/2, fill=1, stroke=0)
            canvas_obj.setFillAlpha(1.0)  # Restaurar opacidade
        
        # Aplicar borda se configurada
        if tema_config.get('mostrar_qr_borda', True):
            canvas_obj.setStrokeColor(tema_config.get('cor_borda', '#cccccc'))
            canvas_obj.setLineWidth(1)
            margem = 2
            canvas_obj.rect(margem, margem, largura-2*margem, altura-2*margem, fill=0, stroke=1)
        
        return True
        
    except Exception as e:
        logging.error(f"Erro ao aplicar tema: {str(e)}")
        return False

def obter_tema_por_id(tema_id):
    """Obtém configuração completa de um tema por ID"""
    try:
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nome, cor_primaria, cor_secundaria, cor_texto, cor_borda,
                   layout_tipo, margem_superior, margem_inferior, margem_esquerda, margem_direita,
                   fonte_titulo, tamanho_fonte_titulo, fonte_nome, tamanho_fonte_nome,
                   fonte_cargo, tamanho_fonte_cargo, fonte_info, tamanho_fonte_info,
                   mostrar_logo, posicao_logo, tamanho_logo, mostrar_qr_borda, qr_tamanho, qr_posicao,
                   fundo_tipo, fundo_cor, fundo_cor_gradiente, fundo_imagem_url, fundo_opacidade, design
            FROM pass_temas_avancado 
            WHERE id = ? AND ativo = 1
        """, (tema_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Parse design JSON se existir
            design = None
            if row[29]:  # design column
                try:
                    import json
                    design = json.loads(row[29])
                except:
                    design = None
            
            return {
                'nome': row[0], 'cor_primaria': row[1], 'cor_secundaria': row[2], 'cor_texto': row[3], 'cor_borda': row[4],
                'layout_tipo': row[5], 'margem_superior': row[6], 'margem_inferior': row[7], 'margem_esquerda': row[8], 'margem_direita': row[9],
                'fonte_titulo': row[10], 'tamanho_fonte_titulo': row[11], 'fonte_nome': row[12], 'tamanho_fonte_nome': row[13],
                'fonte_cargo': row[14], 'tamanho_fonte_cargo': row[15], 'fonte_info': row[16], 'tamanho_fonte_info': row[17],
                'mostrar_logo': bool(row[18]), 'posicao_logo': row[19], 'tamanho_logo': row[20], 'mostrar_qr_borda': bool(row[21]), 
                'qr_tamanho': row[22], 'qr_posicao': row[23], 'fundo_tipo': row[24], 'fundo_cor': row[25], 
                'fundo_cor_gradiente': row[26], 'fundo_imagem_url': row[27], 'fundo_opacidade': row[28], 'design': design
            }
        return None
        
    except Exception as e:
        logging.error(f"Erro ao obter tema: {str(e)}")
        return None

def obter_formato_por_id(formato_id):
    """Obtém configuração completa de um formato por ID"""
    try:
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nome, extensao, descricao, largura, altura, dpi, orientacao, qualidade, compressao
            FROM pass_formatos_avancado 
            WHERE id = ? AND ativo = 1
        """, (formato_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'nome': row[0], 'extensao': row[1], 'descricao': row[2], 'largura': row[3], 'altura': row[4],
                'dpi': row[5], 'orientacao': row[6], 'qualidade': row[7], 'compressao': bool(row[8])
            }
        return None
        
    except Exception as e:
        logging.error(f"Erro ao obter formato: {str(e)}")
        return None

# ===== ENDPOINTS PARA TEMAS AVANÇADOS =====

@passes_bp.route('/temas', methods=['GET'])
def listar_temas():
    """
    GET /api/iamc/passes/temas
    Lista todos os temas avançados disponíveis
    """
    try:
        criar_tabelas_configuracao()
        
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nome, cor_primaria, cor_secundaria, cor_texto, cor_borda,
                   layout_tipo, fonte_titulo, tamanho_fonte_titulo, fundo_tipo, 
                   fundo_cor, ativo, data_criacao, data_atualizacao, design
            FROM pass_temas_avancado
            ORDER BY nome
        """)
        
        temas = []
        for row in cursor.fetchall():
            # Parse design JSON se existir
            design = None
            if row[14]:  # design column
                try:
                    import json
                    design = json.loads(row[14])
                except:
                    design = None
            
            temas.append({
                'id': row[0], 'nome': row[1], 'cor_primaria': row[2], 'cor_secundaria': row[3], 
                'cor_texto': row[4], 'cor_borda': row[5], 'layout_tipo': row[6], 
                'fonte_titulo': row[7], 'tamanho_fonte_titulo': row[8], 'fundo_tipo': row[9],
                'fundo_cor': row[10], 'ativo': bool(row[11]),
                'data_criacao': row[12].isoformat() if row[12] else None,
                'data_atualizacao': row[13].isoformat() if row[13] else None,
                'design': design
            })
        
        conn.close()
        
        return success_response({
            'temas': temas,
            'total': len(temas)
        })
        
    except Exception as e:
        logging.error(f"Erro ao listar temas: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/temas', methods=['POST'])
def criar_tema():
    """
    POST /api/iamc/passes/temas
    Cria um novo tema avançado
    """
    try:
        schema = TemaConfigSchema()
        try:
            data = schema.load(request.json or {})
        except ValidationError as err:
            return error_response("Dados inválidos", details=err.messages), 400
        
        criar_tabelas_configuracao()
        
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Verificar se nome já existe
        cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado WHERE nome = ?", (data['nome'],))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return error_response("Já existe um tema com este nome"), 400
        
        # Preparar design JSON se fornecido
        design_json = None
        if 'design' in data and data['design']:
            import json
            design_json = json.dumps(data['design'])

        # Inserir novo tema
        cursor.execute("""
            INSERT INTO pass_temas_avancado 
            (nome, cor_primaria, cor_secundaria, cor_texto, cor_borda, layout_tipo,
             margem_superior, margem_inferior, margem_esquerda, margem_direita,
             fonte_titulo, tamanho_fonte_titulo, fonte_nome, tamanho_fonte_nome,
             fonte_cargo, tamanho_fonte_cargo, fonte_info, tamanho_fonte_info,
             mostrar_logo, posicao_logo, tamanho_logo, mostrar_qr_borda, qr_tamanho, qr_posicao,
             fundo_tipo, fundo_cor, fundo_cor_gradiente, fundo_imagem_url, fundo_opacidade, ativo, design)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['nome'], data['cor_primaria'], data['cor_secundaria'], data['cor_texto'], data['cor_borda'],
            data['layout_tipo'], data['margem_superior'], data['margem_inferior'], data['margem_esquerda'], data['margem_direita'],
            data['fonte_titulo'], data['tamanho_fonte_titulo'], data['fonte_nome'], data['tamanho_fonte_nome'],
            data['fonte_cargo'], data['tamanho_fonte_cargo'], data['fonte_info'], data['tamanho_fonte_info'],
            data['mostrar_logo'], data['posicao_logo'], data['tamanho_logo'], data['mostrar_qr_borda'], 
            data['qr_tamanho'], data['qr_posicao'], data['fundo_tipo'], data['fundo_cor'], 
            data['fundo_cor_gradiente'], data['fundo_imagem_url'], data['fundo_opacidade'], data['ativo'], design_json
        ))
        
        tema_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return success_response({
            'id': tema_id,
            'message': 'Tema criado com sucesso'
        }), 201
        
    except Exception as e:
        logging.error(f"Erro ao criar tema: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/temas/<int:tema_id>', methods=['PUT'])
def atualizar_tema(tema_id):
    """
    PUT /api/iamc/passes/temas/{id}
    Atualiza um tema existente
    """
    try:
        logging.info(f"🔧 Atualizando tema {tema_id} com dados: {request.json}")
        
        schema = TemaConfigSchema()
        try:
            data = schema.load(request.json or {})
        except ValidationError as err:
            logging.error(f"❌ Erro de validação para tema {tema_id}: {err.messages}")
            return error_response("Dados inválidos", details=err.messages), 400
        
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Verificar se tema existe
        cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado WHERE id = ?", (tema_id,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return error_response("Tema não encontrado"), 404
        
        # Verificar se nome já existe em outro tema
        cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado WHERE nome = ? AND id != ?", (data['nome'], tema_id))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return error_response("Já existe um tema com este nome"), 400
        
        # Preparar design JSON se fornecido
        design_json = None
        if 'design' in data and data['design']:
            import json
            design_json = json.dumps(data['design'])

        # Atualizar tema
        cursor.execute("""
            UPDATE pass_temas_avancado 
            SET nome = ?, cor_primaria = ?, cor_secundaria = ?, cor_texto = ?, cor_borda = ?,
                layout_tipo = ?, margem_superior = ?, margem_inferior = ?, margem_esquerda = ?, margem_direita = ?,
                fonte_titulo = ?, tamanho_fonte_titulo = ?, fonte_nome = ?, tamanho_fonte_nome = ?,
                fonte_cargo = ?, tamanho_fonte_cargo = ?, fonte_info = ?, tamanho_fonte_info = ?,
                mostrar_logo = ?, posicao_logo = ?, tamanho_logo = ?, mostrar_qr_borda = ?, qr_tamanho = ?, qr_posicao = ?,
                fundo_tipo = ?, fundo_cor = ?, fundo_cor_gradiente = ?, fundo_imagem_url = ?, fundo_opacidade = ?,
                ativo = ?, design = ?, data_atualizacao = GETDATE()
            WHERE id = ?
        """, (
            data['nome'], data['cor_primaria'], data['cor_secundaria'], data['cor_texto'], data['cor_borda'],
            data['layout_tipo'], data['margem_superior'], data['margem_inferior'], data['margem_esquerda'], data['margem_direita'],
            data['fonte_titulo'], data['tamanho_fonte_titulo'], data['fonte_nome'], data['tamanho_fonte_nome'],
            data['fonte_cargo'], data['tamanho_fonte_cargo'], data['fonte_info'], data['tamanho_fonte_info'],
            data['mostrar_logo'], data['posicao_logo'], data['tamanho_logo'], data['mostrar_qr_borda'], 
            data['qr_tamanho'], data['qr_posicao'], data['fundo_tipo'], data['fundo_cor'], 
            data['fundo_cor_gradiente'], data['fundo_imagem_url'], data['fundo_opacidade'], data['ativo'], design_json, tema_id
        ))
        
        conn.commit()
        conn.close()
        
        return success_response({
            'message': 'Tema atualizado com sucesso'
        })
        
    except Exception as e:
        logging.error(f"Erro ao atualizar tema: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/temas/<int:tema_id>', methods=['DELETE'])
def deletar_tema(tema_id):
    """
    DELETE /api/iamc/passes/temas/{id}
    Deleta um tema
    """
    try:
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Verificar se tema existe
        cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado WHERE id = ?", (tema_id,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return error_response("Tema não encontrado"), 404
        
        # Deletar tema
        cursor.execute("DELETE FROM pass_temas_avancado WHERE id = ?", (tema_id,))
        conn.commit()
        conn.close()
        
        return success_response({
            'message': 'Tema deletado com sucesso'
        })
        
    except Exception as e:
        logging.error(f"Erro ao deletar tema: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/temas/<int:tema_id>', methods=['GET'])
def obter_tema_endpoint(tema_id):
    """
    GET /api/iamc/passes/temas/{id}
    Obtém um tema específico com todas as configurações
    """
    try:
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nome, cor_primaria, cor_secundaria, cor_texto, cor_borda,
                   layout_tipo, margem_superior, margem_inferior, margem_esquerda, margem_direita,
                   fonte_titulo, tamanho_fonte_titulo, fonte_nome, tamanho_fonte_nome,
                   fonte_cargo, tamanho_fonte_cargo, fonte_info, tamanho_fonte_info,
                   mostrar_logo, posicao_logo, tamanho_logo, mostrar_qr_borda, qr_tamanho, qr_posicao,
                   fundo_tipo, fundo_cor, fundo_cor_gradiente, fundo_imagem_url, fundo_opacidade,
                   ativo, data_criacao, data_atualizacao, design
            FROM pass_temas_avancado
            WHERE id = ?
        """, (tema_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return error_response("Tema não encontrado"), 404
        
        # Parse design JSON se existir
        design = None
        if row[33]:  # design column
            try:
                import json
                design = json.loads(row[33])
            except:
                design = None
        
        tema = {
            'id': row[0], 'nome': row[1], 'cor_primaria': row[2], 'cor_secundaria': row[3], 'cor_texto': row[4], 'cor_borda': row[5],
            'layout_tipo': row[6], 'margem_superior': row[7], 'margem_inferior': row[8], 'margem_esquerda': row[9], 'margem_direita': row[10],
            'fonte_titulo': row[11], 'tamanho_fonte_titulo': row[12], 'fonte_nome': row[13], 'tamanho_fonte_nome': row[14],
            'fonte_cargo': row[15], 'tamanho_fonte_cargo': row[16], 'fonte_info': row[17], 'tamanho_fonte_info': row[18],
            'mostrar_logo': bool(row[19]), 'posicao_logo': row[20], 'tamanho_logo': row[21], 'mostrar_qr_borda': bool(row[22]), 
            'qr_tamanho': row[23], 'qr_posicao': row[24], 'fundo_tipo': row[25], 'fundo_cor': row[26], 
            'fundo_cor_gradiente': row[27], 'fundo_imagem_url': row[28], 'fundo_opacidade': row[29],
            'ativo': bool(row[30]),
            'data_criacao': row[31].isoformat() if row[31] else None,
            'data_atualizacao': row[32].isoformat() if row[32] else None,
            'design': design
        }
        
        conn.close()
        
        return success_response(tema)
        
    except Exception as e:
        logging.error(f"Erro ao obter tema: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

# ===== ENDPOINTS PARA FORMATOS AVANÇADOS =====

@passes_bp.route('/formatos', methods=['GET'])
def listar_formatos():
    """
    GET /api/iamc/passes/formatos
    Lista todos os formatos avançados disponíveis
    """
    try:
        criar_tabelas_configuracao()
        
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nome, extensao, descricao, largura, altura, dpi, orientacao, 
                   qualidade, compressao, ativo, data_criacao, data_atualizacao
            FROM pass_formatos_avancado
            ORDER BY nome
        """)
        
        formatos = []
        for row in cursor.fetchall():
            formatos.append({
                'id': row[0], 'nome': row[1], 'extensao': row[2], 'descricao': row[3],
                'largura': row[4], 'altura': row[5], 'dpi': row[6], 'orientacao': row[7],
                'qualidade': row[8], 'compressao': bool(row[9]), 'ativo': bool(row[10]),
                'data_criacao': row[11].isoformat() if row[11] else None,
                'data_atualizacao': row[12].isoformat() if row[12] else None
            })
        
        conn.close()
        
        return success_response({
            'formatos': formatos,
            'total': len(formatos),
            'medidas_padrao': MEDIDAS_PADRAO
        })
        
    except Exception as e:
        logging.error(f"Erro ao listar formatos: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/formatos', methods=['POST'])
def criar_formato():
    """
    POST /api/iamc/passes/formatos
    Cria um novo formato avançado
    """
    try:
        schema = FormatoConfigSchema()
        try:
            data = schema.load(request.json or {})
        except ValidationError as err:
            return error_response("Dados inválidos", details=err.messages), 400
        
        criar_tabelas_configuracao()
        
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Verificar se nome já existe
        cursor.execute("SELECT COUNT(*) FROM pass_formatos_avancado WHERE nome = ?", (data['nome'],))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return error_response("Já existe um formato com este nome"), 400
        
        # Inserir novo formato
        cursor.execute("""
            INSERT INTO pass_formatos_avancado 
            (nome, extensao, descricao, largura, altura, dpi, orientacao, qualidade, compressao, ativo)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['nome'], data['extensao'], data['descricao'], data['largura'], data['altura'],
            data['dpi'], data['orientacao'], data['qualidade'], data['compressao'], data['ativo']
        ))
        
        formato_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        return success_response({
            'id': formato_id,
            'message': 'Formato criado com sucesso'
        }), 201
        
    except Exception as e:
        logging.error(f"Erro ao criar formato: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/formatos/<int:formato_id>', methods=['PUT'])
def atualizar_formato(formato_id):
    """
    PUT /api/iamc/passes/formatos/{id}
    Atualiza um formato existente
    """
    try:
        schema = FormatoConfigSchema()
        try:
            data = schema.load(request.json or {})
        except ValidationError as err:
            return error_response("Dados inválidos", details=err.messages), 400
        
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Verificar se formato existe
        cursor.execute("SELECT COUNT(*) FROM pass_formatos_avancado WHERE id = ?", (formato_id,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return error_response("Formato não encontrado"), 404
        
        # Verificar se nome já existe em outro formato
        cursor.execute("SELECT COUNT(*) FROM pass_formatos_avancado WHERE nome = ? AND id != ?", (data['nome'], formato_id))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return error_response("Já existe um formato com este nome"), 400
        
        # Atualizar formato
        cursor.execute("""
            UPDATE pass_formatos_avancado 
            SET nome = ?, extensao = ?, descricao = ?, largura = ?, altura = ?, dpi = ?, 
                orientacao = ?, qualidade = ?, compressao = ?, ativo = ?, data_atualizacao = GETDATE()
            WHERE id = ?
        """, (
            data['nome'], data['extensao'], data['descricao'], data['largura'], data['altura'],
            data['dpi'], data['orientacao'], data['qualidade'], data['compressao'], data['ativo'], formato_id
        ))
        
        conn.commit()
        conn.close()
        
        return success_response({
            'message': 'Formato atualizado com sucesso'
        })
        
    except Exception as e:
        logging.error(f"Erro ao atualizar formato: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/formatos/<int:formato_id>', methods=['DELETE'])
def deletar_formato(formato_id):
    """
    DELETE /api/iamc/passes/formatos/{id}
    Deletar um formato
    """
    try:
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        # Verificar se formato existe
        cursor.execute("SELECT COUNT(*) FROM pass_formatos_avancado WHERE id = ?", (formato_id,))
        if cursor.fetchone()[0] == 0:
            conn.close()
            return error_response("Formato não encontrado"), 404
        
        # Deletar formato
        cursor.execute("DELETE FROM pass_formatos_avancado WHERE id = ?", (formato_id,))
        conn.commit()
        conn.close()
        
        return success_response({
            'message': 'Formato deletado com sucesso'
        })
        
    except Exception as e:
        logging.error(f"Erro ao deletar formato: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/formatos/<int:formato_id>', methods=['GET'])
def obter_formato_endpoint(formato_id):
    """
    GET /api/iamc/passes/formatos/{id}
    Obtém um formato específico
    """
    try:
        conn = obtener_conexao_local()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nome, extensao, descricao, largura, altura, dpi, orientacao,
                   qualidade, compressao, ativo, data_criacao, data_atualizacao
            FROM pass_formatos_avancado
            WHERE id = ?
        """, (formato_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return error_response("Formato não encontrado"), 404
        
        formato = {
            'id': row[0], 'nome': row[1], 'extensao': row[2], 'descricao': row[3],
            'largura': row[4], 'altura': row[5], 'dpi': row[6], 'orientacao': row[7],
            'qualidade': row[8], 'compressao': bool(row[9]), 'ativo': bool(row[10]),
            'data_criacao': row[11].isoformat() if row[11] else None,
            'data_atualizacao': row[12].isoformat() if row[12] else None
        }
        
        conn.close()
        
        return success_response(formato)
        
    except Exception as e:
        logging.error(f"Erro ao obter formato: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500
