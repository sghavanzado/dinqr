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
            qr_generated_ids = {row[0] for row in cursor.fetchall()}
        finally:
            liberar_conexion_local(conn_local)

        # Si no hay IDs en qr_generated_ids, devolver lista vacía
        if not qr_generated_ids:
            return jsonify([])

        # Consultar funcionarios desde la base de datos remota
        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            query = """
                SELECT sap, nome, funcao, area, nif, telefone, email, uo
                FROM sonacard
                WHERE sap IN ({})
                AND nome LIKE ?
                ORDER BY sap
                OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
            """.format(",".join("?" for _ in qr_generated_ids))
            cursor.execute(query, (*qr_generated_ids, f"%{filtro}%", (page - 1) * per_page, per_page))
            funcionarios = cursor.fetchall()

        # Combinar datos y agregar estado de QR
        result = [
            {
                "id": funcionario.sap,
                "nome": funcionario.nome,
                "funcao": funcionario.funcao,
                "area": funcionario.area,
                "nif": funcionario.nif,
                "telefone": funcionario.telefone,
                "email": funcionario.email,
                "uo": funcionario.uo,
                "qrGenerated": True  # Todos los funcionarios en esta lista tienen QR
            }
            for funcionario in funcionarios
        ]

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error al listar funcionarios: {str(e)}")
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
            qr_generated_ids = {row[0] for row in cursor.fetchall()}
        finally:
            liberar_conexion_local(conn_local)

        # Consultar funcionarios desde la base de datos remota que no tienen QR
        with obtener_conexion_remota() as conn:
            cursor = conn.cursor()
            if qr_generated_ids:
                query = """
                    SELECT sap, nome, funcao, area, nif, telefone, email, uo
                    FROM sonacard
                    WHERE sap NOT IN ({})
                """.format(",".join("?" for _ in qr_generated_ids))
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
                "id": funcionario.sap,
                "nome": funcionario.nome,
                "funcao": funcionario.funcao,
                "area": funcionario.area,
                "nif": funcionario.nif,
                "telefone": funcionario.telefone,
                "email": funcionario.email,
                "uo": funcionario.uo,
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
    try:
        total_con_qr = obtener_total_funcionarios_con_qr()
        return jsonify({"total": total_con_qr})
    except Exception as e:
        logging.error(f"Error al obtener el total de funcionarios con QR: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500