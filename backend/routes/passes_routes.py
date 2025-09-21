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
from controllers.iamc_funcionarios_controller_new import FuncionarioController
from utils.api_helpers import success_response, error_response

passes_bp = Blueprint('passes', __name__)

class PassRequestSchema(Schema):
    """Schema para validação de requisições de geração de passe"""
    funcionario_id = fields.Integer(required=True)
    incluir_qr = fields.Boolean(missing=True)
    data_validade = fields.Date(missing=None)
    tema = fields.String(missing='default', validate=lambda x: x in ['default', 'dark', 'green', 'orange'])
    formato_saida = fields.String(missing='pdf', validate=lambda x: x in ['pdf', 'html'])

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

def gerar_pdf_pass(template_data):
    """
    Gera PDF do passe de funcionário usando ReportLab
    Formato CR80: 85.6mm x 53.98mm
    """
    try:
        # Buffer para o PDF
        buffer = BytesIO()
        
        # Dimensões CR80 em pontos (1mm = 2.834645669 pontos)
        largura_cr80 = 85.6 * mm
        altura_cr80 = 53.98 * mm
        
        # Criar canvas
        c = canvas.Canvas(buffer, pagesize=(largura_cr80, altura_cr80))
        
        # Configurações de fonte
        c.setFont("Helvetica-Bold", 8)
        
        # Fundo branco
        c.setFillColor(colors.white)
        c.rect(0, 0, largura_cr80, altura_cr80, fill=1)
        
        # Borda
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.5)
        c.rect(2, 2, largura_cr80-4, altura_cr80-4, fill=0)
        
        # Título da empresa (topo)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        empresa_nome = template_data.get('empresa_nome', 'DINQR SYSTEM')
        text_width = c.stringWidth(empresa_nome, "Helvetica-Bold", 10)
        c.drawString((largura_cr80 - text_width) / 2, altura_cr80 - 15, empresa_nome)
        
        # Nome do funcionário
        c.setFont("Helvetica-Bold", 9)
        nome = template_data.get('funcionario_nome', 'Nome do Funcionário')
        # Quebrar nome se for muito longo
        if len(nome) > 25:
            nome = nome[:22] + "..."
        c.drawString(8, altura_cr80 - 30, nome)
        
        # ID do funcionário
        c.setFont("Helvetica", 7)
        funcionario_id = f"ID: {template_data.get('funcionario_id', 'N/A')}"
        c.drawString(8, altura_cr80 - 40, funcionario_id)
        
        # Cargo
        cargo = template_data.get('cargo', 'N/A')
        if len(cargo) > 20:
            cargo = cargo[:17] + "..."
        c.drawString(8, altura_cr80 - 48, cargo)
        
        # Data de emissão (canto inferior esquerdo)
        c.setFont("Helvetica", 6)
        data_emissao = f"Emitido: {template_data.get('data_emissao', 'N/A')}"
        c.drawString(5, 8, data_emissao)
        
        # Data de validade (canto inferior direito)
        data_validade = f"Válido até: {template_data.get('data_validade', 'N/A')}"
        text_width = c.stringWidth(data_validade, "Helvetica", 6)
        c.drawString(largura_cr80 - text_width - 5, 8, data_validade)
        
        # Área para QR Code (canto direito)
        qr_size = 35
        qr_x = largura_cr80 - qr_size - 8
        qr_y = altura_cr80 - qr_size - 15
        
        # Tentar adicionar QR code se disponível
        qr_url = template_data.get('qr_url')
        if qr_url and qr_url.startswith('data:image'):
            try:
                # Decodificar base64 do QR
                qr_data = qr_url.split(',')[1]
                qr_bytes = base64.b64decode(qr_data)
                qr_image = ImageReader(BytesIO(qr_bytes))
                c.drawImage(qr_image, qr_x, qr_y, qr_size, qr_size)
            except Exception as e:
                logging.warning(f"Erro ao adicionar QR code ao PDF: {str(e)}")
                # Desenhar placeholder para QR
                c.setStrokeColor(colors.lightgrey)
                c.rect(qr_x, qr_y, qr_size, qr_size, fill=0)
                c.setFont("Helvetica", 6)
                c.drawString(qr_x + 10, qr_y + qr_size/2, "QR")
        else:
            # Desenhar placeholder para QR
            c.setStrokeColor(colors.lightgrey)
            c.rect(qr_x, qr_y, qr_size, qr_size, fill=0)
            c.setFont("Helvetica", 6)
            c.drawString(qr_x + 10, qr_y + qr_size/2, "QR")
        
        # Finalizar PDF
        c.save()
        
        # Retornar conteúdo do buffer
        buffer.seek(0)
        return buffer.getvalue()
        
    except Exception as e:
        logging.error(f"Erro ao gerar PDF com ReportLab: {str(e)}")
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
            # Gerar PDF usando ReportLab
            try:
                # Criar arquivo temporário para o PDF
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                    
                    # Gerar PDF com ReportLab
                    pdf_content = gerar_pdf_pass(template_data)
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
        # Preparar dados para preview
        preview_data = {
            'funcionario_id': funcionario_id,
            'incluir_qr': True,
            'formato_saida': 'html'
        }
        
        # Reutilizar lógica de geração
        request.json = preview_data
        return gerar_passe()
        
    except Exception as e:
        logging.error(f"Erro ao gerar preview: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500

@passes_bp.route('/configuracao', methods=['GET'])
def obter_configuracao():
    """
    GET /api/rrhh/passes/configuracao
    Retorna configurações disponíveis para passes
    """
    try:
        configuracao = {
            'temas_disponiveis': [
                {'id': 'default', 'nome': 'Padrão', 'cor_primaria': '#1976d2'},
                {'id': 'dark', 'nome': 'Escuro', 'cor_primaria': '#37474f'},
                {'id': 'green', 'nome': 'Verde', 'cor_primaria': '#2e7d32'},
                {'id': 'orange', 'nome': 'Laranja', 'cor_primaria': '#f57722'}
            ],
            'formatos_saida': [
                {'id': 'pdf', 'nome': 'PDF', 'descricao': 'Arquivo PDF para impressão'},
                {'id': 'html', 'nome': 'HTML', 'descricao': 'Visualização HTML'}
            ],
            'dimensoes': {
                'formato': 'CR80',
                'largura_mm': 85.6,
                'altura_mm': 53.98,
                'dpi_recomendado': 300
            },
            'validade_padrao_dias': 365
        }
        
        return success_response(configuracao)
        
    except Exception as e:
        logging.error(f"Erro ao obter configuração: {str(e)}")
        return error_response(f"Erro interno do servidor: {str(e)}"), 500
