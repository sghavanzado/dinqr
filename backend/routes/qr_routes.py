# qr_routes.py
from flask import Blueprint, request, jsonify, send_file, abort
from marshmallow import Schema, fields, ValidationError
from services.qr_service import (
    generar_qr,
    generar_qr_estatico,
    listar_funcionarios,
    eliminar_qr,
    descargar_qr,
    descargar_multiples_qr,
    obtener_total_funcionarios,
    obtener_total_funcionarios_con_qr
)
from utils.db_utils import obtener_conexion_remota, obtener_conexion_local, liberar_conexion_local
import logging
import csv
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

qr_bp = Blueprint('qr', __name__)

class QRRequestSchema(Schema):
    ids = fields.List(fields.Int(), required=True)

@qr_bp.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    """Listado de funcionarios desde la base de datos remota."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    filtro = request.args.get('filtro', '', type=str)

    try:
        # Validar parámetros
        if page < 1 or per_page < 1:
            return jsonify({"error": "Los parámetros 'page' y 'per_page' deben ser mayores a 0"}), 400

        # Consultar IDs de funcionarios con QR en la base de datos local
        conn_local = None
        try:
            conn_local = obtener_conexion_local()
            cursor = conn_local.cursor()
            cursor.execute("SELECT contact_id FROM qr_codes")
            qr_generated_ids = [row[0] for row in cursor.fetchall()]
            logging.info(f"IDs de funcionarios con QR obtenidos: {qr_generated_ids}")
        except Exception as e:
            logging.error(f"Error al consultar IDs de funcionarios con QR en la base de datos local: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500
        finally:
            if conn_local:
                liberar_conexion_local(conn_local)

        # Si no hay IDs en qr_generated_ids, devolver lista vacía
        if not qr_generated_ids:
            logging.info("No se encontraron IDs de funcionarios con QR en la base de datos local.")
            return jsonify([])

        # Consultar funcionarios desde la base de datos remota
        try:
            with obtener_conexion_remota() as conn:
                cursor = conn.cursor()
                placeholders = ",".join("?" for _ in qr_generated_ids)  # Crear placeholders dinámicos
                query = f"""
                    SELECT sap, nome, funcao, area, nif, telefone, email, uo
                    FROM sonacard
                    WHERE sap IN ({placeholders})
                    AND nome LIKE ?
                    ORDER BY sap
                    OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """
                logging.info(f"Ejecutando consulta SQL: {query}")
                cursor.execute(query, (*qr_generated_ids, f"%{filtro}%", (page - 1) * per_page, per_page))
                funcionarios = cursor.fetchall()
                logging.info(f"Funcionarios obtenidos: {len(funcionarios)} registros")
        except Exception as e:
            logging.error(f"Error al consultar funcionarios desde la base de datos remota: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500

        # Combinar datos y agregar estado de QR
        try:
            result = [
                {
                    "id": funcionario[0],
                    "nome": funcionario[1],
                    "funcao": funcionario[2],
                    "area": funcionario[3],
                    "nif": funcionario[4],
                    "telefone": funcionario[5],
                    "email": funcionario[6],
                    "uo": funcionario[7],
                    "qrGenerated": True
                }
                for funcionario in funcionarios
            ]
        except Exception as e:
            logging.error(f"Error al procesar los datos de funcionarios: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error inesperado al listar funcionarios: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@qr_bp.route('/funcionarios-sin-qr', methods=['GET'])
def listar_funcionarios_sin_qr():
    """Listado de funcionarios que no tienen un código QR generado."""
    try:
        # Consultar IDs de funcionarios con QR en la base de datos local
        conn_local = None
        try:
            conn_local = obtener_conexion_local()
            cursor = conn_local.cursor()
            cursor.execute("SELECT contact_id FROM qr_codes")
            qr_generated_ids = [row[0] for row in cursor.fetchall()]
        finally:
            liberar_conexion_local(conn_local)

        # Consultar funcionarios desde la base de datos remota que no tienen QR
        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            if qr_generated_ids:
                placeholders = ",".join("?" for _ in qr_generated_ids)
                query = f"""
                    SELECT sap, nome, funcao, area, nif, telefone, email, uo
                    FROM sonacard
                    WHERE sap NOT IN ({placeholders})
                """
                logging.info(f"Ejecutando consulta SQL: {query}")
                cursor.execute(query, tuple(qr_generated_ids))
            else:
                # Si no hay IDs en qr_generated_ids, devolver todos los funcionarios
                query = """
                    SELECT sap, nome, funcao, area, nif, telefone, email, uo
                    FROM sonacard
                """
                cursor.execute(query)
            funcionarios = cursor.fetchall()

        result = [
            {
                "id": funcionario[0],
                "nome": funcionario[1],
                "funcao": funcionario[2],
                "area": funcionario[3],
                "nif": funcionario[4],
                "telefone": funcionario[5],
                "email": funcionario[6],
                "uo": funcionario[7],
            }
            for funcionario in funcionarios
        ]

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error al listar funcionarios sin QR: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@qr_bp.route('/generar', methods=['POST'])
def generar_codigos_qr():
    """Generar códigos QR para funcionarios."""
    try:
        data = QRRequestSchema().load(request.json)
        ids = data['ids']
        return jsonify(generar_qr(ids))
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logging.error(f"Error al generar códigos QR: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@qr_bp.route('/generar-estatico', methods=['POST'])
def generar_codigos_qr_estaticos():
    """Generar códigos QR estáticos para funcionarios."""
    try:
        data = QRRequestSchema().load(request.json)
        ids = data['ids']
        return jsonify(generar_qr_estatico(ids))
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logging.error(f"Error al generar códigos QR estáticos: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@qr_bp.route('/descargar/<int:contact_id>', methods=['GET'])
def descargar_codigo_qr(contact_id):
    """Descargar un código QR específico."""
    return send_file(descargar_qr(contact_id), as_attachment=True)

@qr_bp.route('/descargar-multiples', methods=['POST'])
def descargar_codigos_qr_multiples():
    """Descargar múltiples códigos QR como archivo ZIP."""
    ids = request.json.get('ids', [])
    return send_file(descargar_multiples_qr(ids), as_attachment=True)

@qr_bp.route('/eliminar/<int:contact_id>', methods=['DELETE'])
def eliminar_codigo_qr(contact_id):
    """Eliminar un código QR específico."""
    return jsonify(eliminar_qr(contact_id))

@qr_bp.route('/funcionarios/total', methods=['GET'])
def obtener_total_funcionarios_endpoint():
    """Obtener la cantidad total de funcionarios desde la base de datos remota."""
    try:
        total = obtener_total_funcionarios()
        return jsonify({"total": total})
    except Exception as e:
        logging.error(f"Error al obtener el total de funcionarios: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@qr_bp.route('/funcionarios/total-con-qr', methods=['GET'])
def obtener_total_funcionarios_con_qr_endpoint():
    """Obtener la cantidad total de funcionarios con código QR en la base de datos local."""
    conn_local = None
    try:
        conn_local = obtener_conexion_local()
        cursor = conn_local.cursor()
        cursor.execute("SELECT COUNT(*) FROM qr_codes")
        total_con_qr = cursor.fetchone()[0]
        return jsonify({"total": total_con_qr})
    except Exception as e:
        logging.error(f"Error al obtener el total de funcionarios con QR: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        if conn_local:
            liberar_conexion_local(conn_local)  # Ensure the connection is released

@qr_bp.route('/generar-todos', methods=['POST'])
def generar_todos_codigos_qr():
    """Generar códigos QR para todos los funcionarios en la base de datos externa."""
    conn_remota = None
    try:
        # Obtener todos los IDs de funcionarios desde la base de datos remota
        conn_remota = obtener_conexion_remota()
        cursor = conn_remota.cursor()
        cursor.execute("SELECT sap FROM sonacard")
        ids = [row[0] for row in cursor.fetchall()]

        if not ids:
            return jsonify({"message": "No hay funcionarios en la base de datos externa."}), 200

        # Procesar en lotes de 200 para evitar problemas de memoria o tiempo de ejecución
        batch_size = 200  # Tamaño del lote
        resultados = []
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            resultados.extend(generar_qr(batch_ids))
            logging.info(f"Lote {i + 1}/{(len(ids) + batch_size - 1) // batch_size} procesado con éxito.")

        return jsonify({"message": "Códigos QR generados con éxito.", "resultados": resultados})
    except Exception as e:
        logging.error(f"Error al generar códigos QR para todos los funcionarios: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        if conn_remota:
            conn_remota.close()  # Asegurar que la conexión remota se cierre correctamente