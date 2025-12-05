"""
SIGA - Sistema Integral de Gestión de Accesos
Servicio de Generación de Cartones de Visita

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Servicio para generar cartones de visita digitales con código QR.
"""

import os
import qrcode
import hashlib
import hmac
import logging
from pathlib import Path
from extensions import db
from models.business_card import BusinessCard
from utils.db_utils import remote_db_connection

logger = logging.getLogger(__name__)


def generar_firma_hmac(contact_id, nombre):
    """
    Genera firma HMAC-SHA256 para seguridad del cartón de visita.
    
    Args:
        contact_id: ID del contacto
        nombre: Nombre del funcionario
    
    Returns:
        str: Firma HMAC en hexadecimal
    """
    secret_key = hashlib.sha256(nombre.encode()).digest()
    return hmac.new(secret_key, nombre.encode(), hashlib.sha256).hexdigest()


def generar_business_card(contact_id):
    """
    Genera un cartón de visita digital con código QR para un funcionario.
    
    Args:
        contact_id: ID del funcionario (SAP)
    
    Returns:
        dict: Resultado de la generación con datos del cartón
    
    Raises:
        ValueError: Si el funcionario no existe
        Exception: Si hay error en la generación
    """
    try:
        # Verificar si ya existe un cartón para este contacto
        existing_card = BusinessCard.query.filter_by(contact_id=str(contact_id)).first()
        if existing_card:
            logger.info(f"Cartón de visita ya existe para contacto {contact_id}")
            return {
                'contact_id': contact_id,
                'success': False,
                'message': 'El cartón de visita ya existe para este funcionario',
                'business_card': existing_card.to_dict()
            }
        
        # Obtener datos del funcionario desde SQL Server
        with remote_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT sap, nome, funcao, area, nif, telefone, email, unineg FROM sonacard WHERE sap = ?",
                (contact_id,)
            )
            funcionario = cursor.fetchone()
        
        if not funcionario:
            raise ValueError(f"Funcionario con ID {contact_id} no encontrado")
        
        # Extraer datos
        sap, nome, funcao, area, nif, telefone, email, unineg = funcionario
        
        # Generar firma HMAC
        firma = generar_firma_hmac(str(sap), nome)
        
        # Generar URL del cartón de visita
        base_url = os.environ.get('APP_BASE_URL', 'http://localhost:5000')
        carton_url = f"{base_url}/cartonv?sap={sap}&hash={firma}"
        
        # Crear directorio para QRs si no existe
        qr_dir = Path('static/business_cards')
        qr_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar código QR con prefijo CV
        qr_filename = f"CV-{sap}.png"
        qr_path = qr_dir / qr_filename
        
        # Configurar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(carton_url)
        qr.make(fit=True)
        
        # Crear imagen QR
        img = qr.make_image(fill_color="blue", back_color="white")
        img.save(str(qr_path))
        
        logger.info(f"QR generado para cartón de visita: {qr_path}")
        
        # Guardar en base de datos local
        business_card = BusinessCard(
            contact_id=str(sap),
            firma=firma,
            qr_code_path=str(qr_path),
            qr_code_data=carton_url,
            is_active=True
        )
        
        db.session.add(business_card)
        db.session.commit()
        
        logger.info(f"Cartón de visita generado exitosamente para {nome} (SAP: {sap})")
        
        return {
            'contact_id': sap,
            'success': True,
            'message': 'Cartón de visita generado exitosamente',
            'qr_path': str(qr_path),
            'url': carton_url,
            'business_card': business_card.to_dict()
        }
        
    except ValueError as e:
        logger.error(f"Error de validación generando cartón: {str(e)}")
        return {
            'contact_id': contact_id,
            'success': False,
            'message': str(e)
        }
    except Exception as e:
        logger.error(f"Error generando cartón de visita para {contact_id}: {str(e)}")
        db.session.rollback()
        return {
            'contact_id': contact_id,
            'success': False,
            'message': f'Error al generar cartón: {str(e)}'
        }


def generar_business_cards_multiples(contact_ids):
    """
    Genera múltiples cartones de visita.
    
    Args:
        contact_ids: Lista de IDs de contactos
    
    Returns:
        list: Lista de resultados de generación
    """
    resultados = []
    for contact_id in contact_ids:
        resultado = generar_business_card(contact_id)
        resultados.append(resultado)
    
    return resultados


def eliminar_business_card(contact_id):
    """
    Elimina un cartón de visita.
    
    Args:
        contact_id: ID del contacto
    
    Returns:
        dict: Resultado de la eliminación
    """
    try:
        business_card = BusinessCard.query.filter_by(contact_id=str(contact_id)).first()
        
        if not business_card:
            return {
                'success': False,
                'message': 'Cartón de visita no encontrado'
            }
        
        # Eliminar archivo QR
        if os.path.exists(business_card.qr_code_path):
            os.remove(business_card.qr_code_path)
            logger.info(f"Archivo QR eliminado: {business_card.qr_code_path}")
        
        # Eliminar de BD
        db.session.delete(business_card)
        db.session.commit()
        
        logger.info(f"Cartón de visita eliminado para contacto {contact_id}")
        
        return {
            'success': True,
            'message': 'Cartón de visita eliminado exitosamente'
        }
        
    except Exception as e:
        logger.error(f"Error eliminando cartón de visita {contact_id}: {str(e)}")
        db.session.rollback()
        return {
            'success': False,
            'message': f'Error al eliminar: {str(e)}'
        }


def obtener_funcionarios_sin_business_card():
    """
    Obtiene lista de funcionarios que NO tienen cartón de visita.
    Limitado a 50 registros para evitar timeouts.
    
    Returns:
        list: Lista de funcionarios sin cartón (máximo 50)
    """
    try:
        logger.info("Obteniendo funcionarios sin cartón de visita...")
        
        # Obtener IDs con cartón
        cards_ids = [bc.contact_id for bc in BusinessCard.query.filter_by(is_active=True).all()]
        logger.info(f"Cartones existentes: {len(cards_ids)}")
        
        # Consultar funcionarios sin cartón (LÍMITE REDUCIDO A 50)
        with remote_db_connection(timeout=15) as conn:  # Reduced timeout to 15s
            cursor = conn.cursor()
            
            if cards_ids:
                # Si hay muchos IDs, limitar la exclusión
                if len(cards_ids) > 100:
                    logger.warning(f"Muchos cartones ({len(cards_ids)}), solo excluyendo primeros 100")
                    cards_ids = cards_ids[:100]
                
                placeholders = ','.join('?' * len(cards_ids))
                query = f"""
                    SELECT TOP 50 sap, nome, funcao, area, nif, telefone, email, unineg
                    FROM sonacard
                    WHERE sap NOT IN ({placeholders})
                    ORDER BY nome
                """
                logger.info(f"Ejecutando query con {len(cards_ids)} exclusiones...")
                cursor.execute(query, tuple(cards_ids))
            else:
                query = """
                    SELECT TOP 50 sap, nome, funcao, area, nif, telefone, email, unineg
                    FROM sonacard
                    ORDER BY nome
                """
                logger.info("Ejecutando query sin exclusiones...")
                cursor.execute(query)
            
            funcionarios = cursor.fetchall()
            logger.info(f"Funcionarios obtenidos: {len(funcionarios)}")
        
        # Formatear resultados
        resultado = []
        for func in funcionarios:
            resultado.append({
                'id': func[0],
                'nome': func[1],
                'funcao': func[2],
                'area': func[3],
                'nif': func[4],
                'telefone': func[5],
                'email': func[6],
                'unineg': func[7],
                'hasBusinessCard': False
            })
        
        logger.info(f"Retornando {len(resultado)} funcionarios sin cartón")
        return resultado
        
    except Exception as e:
        logger.error(f"Error obteniendo funcionarios sin cartón: {str(e)}", exc_info=True)
        # Retornar array vacío en lugar de fallar
        return []



def obtener_funcionarios_con_business_card():
    """
    Obtiene lista de funcionarios que SÍ tienen cartón de visita.
    
    Returns:
        list: Lista de funcionarios con cartón
    """
    try:
        logger.info("Obteniendo funcionarios con cartón de visita...")
        
        # Obtener IDs con cartón
        cards = BusinessCard.query.filter_by(is_active=True).all()
        if not cards:
            logger.info("No hay cartones de visita generados")
            return []
        
        cards_ids = [bc.contact_id for bc in cards]
        logger.info(f"Cartones a buscar: {len(cards_ids)}")
        
        # Consultar funcionarios con cartón
        with remote_db_connection(timeout=30) as conn:
            cursor = conn.cursor()
            
            placeholders = ','.join('?' * len(cards_ids))
            query = f"""
                SELECT sap, nome, funcao, area, nif, telefone, email, unineg
                FROM sonacard
                WHERE sap IN ({placeholders})
                ORDER BY nome
            """
            logger.info("Ejecutando query para funcionarios con cartón...")
            cursor.execute(query, tuple(cards_ids))
            funcionarios = cursor.fetchall()
            logger.info(f"Funcionarios encontrados: {len(funcionarios)}")
        
        # Formatear resultados
        resultado = []
        for func in funcionarios:
            # Buscar el cartón correspondiente
            card = next((bc for bc in cards if bc.contact_id == str(func[0])), None)
            
            resultado.append({
                'id': func[0],
                'nome': func[1],
                'funcao': func[2],
                'area': func[3],
                'nif': func[4],
                'telefone': func[5],
                'email': func[6],
                'unineg': func[7],
                'hasBusinessCard': True,
                'businessCard': card.to_dict() if card else None
            })
        
        logger.info(f"Retornando {len(resultado)} funcionarios con cartón")
        return resultado
        
    except Exception as e:
        logger.error(f"Error obteniendo funcionarios con cartón: {str(e)}", exc_info=True)
        return []

