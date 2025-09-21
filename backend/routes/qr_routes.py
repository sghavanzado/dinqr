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
from utils.db_utils import obtener_conexion_local, obtener_conexion_remota
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
    """Listado de funcionarios desde la tabla IAMC Funcionarios."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    filtro = request.args.get('filtro', '', type=str)

    try:
        # Validar parámetros
        if page < 1 or per_page < 1:
            return jsonify({"error": "Los parámetros 'page' y 'per_page' deben ser mayores a 0"}), 400

        # Consultar IDs de funcionarios con QR en la base de datos IAMC
        conn_local = None
        try:
            conn_local = obtener_conexion_local()
            cursor = conn_local.cursor()
            cursor.execute("SELECT contact_id FROM qr_codes")
            qr_generated_ids = [int(row[0]) for row in cursor.fetchall()]  # Convertir a int
            logging.info(f"IDs de funcionarios con QR obtenidos: {qr_generated_ids}")
        except Exception as e:
            logging.error(f"Error al consultar IDs de funcionarios con QR en la base de datos IAMC: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500
        finally:
            if conn_local:
                conn_local.close()
                
        # Si no hay IDs en qr_generated_ids, devolver lista vacía
        if not qr_generated_ids:
            logging.info("No se encontraron IDs de funcionarios con QR en la base de datos IAMC.")
            return jsonify([])

        # Consultar funcionarios desde la tabla IAMC Funcionarios con JOINs y paginación
        try:
            from extensions import IAMCSession
            from models.iamc_funcionarios_new import Funcionario, Cargo, Departamento
            
            session = IAMCSession()
            
            # Calcular offset
            offset = (page - 1) * per_page
            
            # Consulta con JOINs, filtro y paginación
            query = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome'),
                Funcionario.CargoID,
                Funcionario.DepartamentoID
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            ).filter(
                Funcionario.FuncionarioID.in_(qr_generated_ids)
            )
            
            # Aplicar filtro de búsqueda si existe
            if filtro:
                query = query.filter(
                    Funcionario.Nome.ilike(f"%{filtro}%") | 
                    Funcionario.Apelido.ilike(f"%{filtro}%") |
                    Cargo.Nome.ilike(f"%{filtro}%") |
                    Departamento.Nome.ilike(f"%{filtro}%")
                )
            
            funcionarios = query.order_by(Funcionario.FuncionarioID).offset(offset).limit(per_page).all()
            logging.info(f"Funcionarios obtenidos desde IAMC: {len(funcionarios)} registros")
            
        except Exception as e:
            logging.error(f"Error al consultar funcionarios desde la tabla IAMC: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500
        finally:
            if 'session' in locals():
                session.close()

        # Combinar datos y agregar estado de QR
        try:
            result = [
                {
                    "id": func.FuncionarioID,
                    "funcionarioId": func.FuncionarioID,
                    "nome": func.Nome,
                    "apelido": func.Apelido or 'Não especificado',
                    "email": func.Email or 'Não especificado',
                    "telefone": func.Telefone or 'Não especificado',
                    "cargo": func.CargoNome or 'Não especificado',
                    "cargoId": func.CargoID,
                    "departamento": func.DepartamentoNome or 'Não especificado',
                    "departamentoId": func.DepartamentoID,
                    "qrGenerated": True
                }
                for func in funcionarios
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
    """Listado de funcionarios que no tienen un código QR generado - usando tabla IAMC."""
    try:
        # Consultar IDs de funcionarios con QR en la base de datos IAMC
        conn_local = None
        try:
            conn_local = obtener_conexion_local()
            cursor = conn_local.cursor()
            cursor.execute("SELECT contact_id FROM qr_codes")
            qr_generated_ids = [int(row[0]) for row in cursor.fetchall()]  # Convertir a int
        except Exception as e:
            logging.error(f"Error al consultar QR codes: {str(e)}")
            qr_generated_ids = []
        finally:
            if conn_local:
                conn_local.close()

        # Consultar funcionarios desde la tabla IAMC que no tienen QR
        try:
            from extensions import IAMCSession
            from models.iamc_funcionarios_new import Funcionario, Cargo, Departamento
            
            session = IAMCSession()
            
            # Consulta con JOINs para funcionarios sin QR
            query = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome'),
                Funcionario.CargoID,
                Funcionario.DepartamentoID
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            )
            
            if qr_generated_ids:
                # Excluir funcionarios que ya tienen QR
                query = query.filter(~Funcionario.FuncionarioID.in_(qr_generated_ids))
            
            funcionarios = query.order_by(Funcionario.FuncionarioID).all()
            logging.info(f"Funcionarios sin QR obtenidos desde IAMC: {len(funcionarios)} registros")
            
        except Exception as e:
            logging.error(f"Error al consultar funcionarios sin QR desde IAMC: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500
        finally:
            if 'session' in locals():
                session.close()

        result = [
            {
                "id": func.FuncionarioID,
                "funcionarioId": func.FuncionarioID,
                "nome": func.Nome,
                "apelido": func.Apelido or 'Não especificado',
                "email": func.Email or 'Não especificado',
                "telefone": func.Telefone or 'Não especificado',
                "cargo": func.CargoNome or 'Não especificado',
                "cargoId": func.CargoID,
                "departamento": func.DepartamentoNome or 'Não especificado',
                "departamentoId": func.DepartamentoID,
                "qrGenerated": False
            }
            for func in funcionarios
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

@qr_bp.route('/generar/<int:funcionario_id>', methods=['POST'])
def generar_codigo_qr_individual(funcionario_id):
    """Generar código QR para un funcionario específico."""
    try:
        result = generar_qr([funcionario_id])
        return jsonify(result[0] if result else {"error": "No se pudo generar el código QR"})
    except Exception as e:
        logging.error(f"Error al generar código QR para funcionario {funcionario_id}: {str(e)}")
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
    """Obtener la cantidad total de funcionarios desde la tabla IAMC Funcionarios."""
    try:
        from extensions import IAMCSession
        from models.iamc_funcionarios_new import Funcionario
        
        session = IAMCSession()
        try:
            total = session.query(Funcionario).count()
            return jsonify({"total": total})
        finally:
            session.close()
            
    except Exception as e:
        logging.error(f"Error al obtener el total de funcionarios desde IAMC: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

@qr_bp.route('/funcionarios/total-con-qr', methods=['GET'])
def obtener_total_funcionarios_con_qr_endpoint():
    """Obtener la cantidad total de funcionarios con código QR en la base de datos IAMC."""
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
    # Conexión se libera automáticamente

@qr_bp.route('/generar-todos', methods=['POST'])
def generar_todos_codigos_qr():
    """Generar códigos QR para todos los funcionarios en la tabla IAMC Funcionarios."""
    try:
        # Obtener todos los IDs de funcionarios desde la tabla IAMC Funcionarios
        from extensions import IAMCSession
        from models.iamc_funcionarios_new import Funcionario
        
        session = IAMCSession()
        try:
            funcionarios = session.query(Funcionario.FuncionarioID).all()
            ids = [func.FuncionarioID for func in funcionarios]
        finally:
            session.close()

        if not ids:
            return jsonify({"message": "No hay funcionarios en la tabla IAMC Funcionarios."}), 200

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

@qr_bp.route('/funcionarios-com-qr', methods=['GET'])
def listar_funcionarios_com_qr():
    """Listado de funcionarios que SÍ tienen un código QR generado - usando tabla IAMC Funcionarios."""
    try:
        # Consultar IDs de funcionarios con QR en la base de datos IAMC
        conn_local = None
        try:
            conn_local = obtener_conexion_local()
            cursor = conn_local.cursor()
            cursor.execute("SELECT contact_id FROM qr_codes")
            qr_generated_ids = [int(row[0]) for row in cursor.fetchall()]  # Convertir a int
            logging.info(f"IDs de funcionarios con QR obtenidos: {qr_generated_ids}")
        except Exception as e:
            logging.error(f"Error al consultar IDs de funcionarios con QR en la base de datos IAMC: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500
        finally:
            if conn_local:
                conn_local.close()
        
        # Si no hay IDs en qr_generated_ids, devolver lista vacía
        if not qr_generated_ids:
            logging.info("No se encontraron IDs de funcionarios con QR en la base de datos IAMC.")
            return jsonify([])

        # Consultar funcionarios desde la tabla IAMC Funcionarios con JOINs
        try:
            from extensions import IAMCSession
            session = IAMCSession()
            
            # Importar modelos IAMC
            from models.iamc_funcionarios_new import Funcionario, Cargo, Departamento
            
            # Consulta con JOINs para obtener nombres de Cargo y Departamento
            query = session.query(
                Funcionario.FuncionarioID,
                Funcionario.Nome,
                Funcionario.Apelido,
                Funcionario.Email,
                Funcionario.Telefone,
                Cargo.Nome.label('CargoNome'),
                Departamento.Nome.label('DepartamentoNome'),
                Funcionario.CargoID,
                Funcionario.DepartamentoID
            ).outerjoin(
                Cargo, Funcionario.CargoID == Cargo.CargoID
            ).outerjoin(
                Departamento, Funcionario.DepartamentoID == Departamento.DepartamentoID
            ).filter(
                Funcionario.FuncionarioID.in_(qr_generated_ids)
            ).order_by(Funcionario.FuncionarioID)
            
            funcionarios = query.all()
            logging.info(f"Funcionarios con QR obtenidos desde IAMC: {len(funcionarios)} registros")
            
        except Exception as e:
            logging.error(f"Error al consultar funcionarios con QR desde la base de datos IAMC: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500
        finally:
            if 'session' in locals():
                session.close()

        # Procesar datos con la nueva estructura IAMC
        try:
            result = [
                {
                    "id": func.FuncionarioID,
                    "funcionarioId": func.FuncionarioID,
                    "nome": func.Nome,
                    "apelido": func.Apelido or 'Não especificado',
                    "email": func.Email or 'Não especificado',
                    "telefone": func.Telefone or 'Não especificado', 
                    "cargo": func.CargoNome or 'Não especificado',
                    "cargoId": func.CargoID,
                    "departamento": func.DepartamentoNome or 'Não especificado',
                    "departamentoId": func.DepartamentoID,
                    "qrGenerated": True
                }
                for func in funcionarios
            ]
        except Exception as e:
            logging.error(f"Error al procesar los datos de funcionarios con QR: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500

        return jsonify(result)

    except Exception as e:
        logging.error(f"Error inesperado al listar funcionarios com QR: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500