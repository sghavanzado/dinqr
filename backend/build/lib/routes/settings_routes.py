from flask import Blueprint, request, jsonify
from models.settings import Settings
from extensions import db
import os
import logging
import subprocess
import signal
import psutil  # Para manejar procesos
from server_manager import iniciar_servidor, detener_servidor, status_servidor
from utils.db_utils import obtener_conexion_local  # Importar la función para obtener conexión local
from werkzeug.utils import secure_filename

settings_bp = Blueprint('settings', __name__)

UPLOAD_FOLDER = 'uploads/logos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear la carpeta si no existe

server_process = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@settings_bp.route('/', methods=['GET'])
def get_settings():
    """Retrieve all settings."""
    settings = Settings.query.all()
    return jsonify({setting.key: setting.value for setting in settings})

@settings_bp.route('/', methods=['POST'])
def save_settings():
    """Save or update settings."""
    data = request.json
    for key, value in data.items():
        setting = Settings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            new_setting = Settings(key=key, value=value)
            db.session.add(new_setting)
    db.session.commit()
    return jsonify({"message": "Settings saved successfully."})

@settings_bp.route('/server-control', methods=['POST'])
def server_control():
    """Controla el estado del servidor (iniciar, pausar, detener)."""
    global server_process
    accion = request.json.get('accion', '').lower()

    try:
        if accion == 'iniciar':
            if server_process is None or server_process.poll() is not None:  # Use poll to check process status
                server_process = subprocess.Popen(['python', 'server_manager.py'])
                logging.info(f"Servidor iniciado con PID: {server_process.pid}")
                return jsonify({"message": "Servidor iniciado."}), 200
            else:
                logging.warning("Intento de iniciar el servidor, pero ya está en ejecución.")
                return jsonify({"message": "El servidor ya está en ejecución."}), 400

        elif accion == 'pausar':
            if server_process and server_process.poll() is None:  # Use poll to check process status
                server_process.terminate()
                server_process.wait()
                logging.info("Servidor pausado correctamente.")
                return jsonify({"message": "Servidor pausado."}), 200
            else:
                logging.warning("Intento de pausar el servidor, pero no está en ejecución.")
                return jsonify({"message": "El servidor no está en ejecución."}), 400

        elif accion == 'detener':
            if server_process and server_process.poll() is None:  # Use poll to check process status
                server_process.terminate()
                server_process.wait()
                logging.info("Servidor detenido correctamente.")
                return jsonify({"message": "Servidor detenido."}), 200
            else:
                logging.warning("Intento de detener el servidor, pero no está en ejecución.")
                return jsonify({"message": "El servidor no está en ejecución."}), 400

        else:
            logging.error(f"Acción no válida recibida: {accion}")
            return jsonify({"error": "Acción no válida."}), 400

    except Exception as e:
        logging.error(f"Error al realizar la acción '{accion}' en el servidor: {str(e)}")
        return jsonify({"error": f"Error al realizar la acción '{accion}' en el servidor."}), 500

@settings_bp.route('/server/start', methods=['POST'])
def start_server():
    """Start the server."""
    try:
        iniciar_servidor()
        return jsonify({"message": "Servidor iniciado."}), 200
    except Exception as e:
        logging.error(f"Error al iniciar el servidor: {str(e)}")
        return jsonify({"error": "Error al iniciar el servidor."}), 500

@settings_bp.route('/server/stop', methods=['POST'])
def stop_server():
    """Stop the server."""
    try:
        detener_servidor()
        return jsonify({"message": "Servidor detenido."}), 200
    except Exception as e:
        logging.error(f"Error al detener el servidor: {str(e)}")
        return jsonify({"error": "Error al detener el servidor."}), 500
    
@settings_bp.route('/server/status', methods=['GET'])
def status_servidor():
    """Consultar o estado do servidor."""
    global server_process
    try:
        if server_process and server_process.poll() is None:
            return jsonify({"status": "em execução", "pid": server_process.pid}), 200
        return jsonify({"status": "parado"}), 200
    except Exception as e:
        logging.error(f"Erro ao consultar o estado do servidor: {str(e)}")
        return jsonify({"error": "Erro ao consultar o estado do servidor."}), 500


def obtener_configuracion_servidor():
    """Obtener configuración del servidor desde la base de datos."""
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM settings WHERE key IN ('serverDomain', 'serverPort')")
        config = {row[0]: row[1] for row in cursor.fetchall()}
        return config.get('serverDomain', '127.0.0.1'), int(config.get('serverPort', 5000))

@settings_bp.route('/server/config', methods=['GET'])
def get_server_config():
    """Obtener configuración del servidor."""
    try:
        domain, port = obtener_configuracion_servidor()
        return jsonify({"serverDomain": domain, "serverPort": port}), 200
    except Exception as e:
        logging.error(f"Error al obtener la configuración del servidor: {str(e)}")
        return jsonify({"error": "Error al obtener la configuración del servidor"}), 500

@settings_bp.route('/upload-logo', methods=['POST'])
def upload_logo():
    """Subir un logo desde la PC."""
    if 'logo' not in request.files:
        return jsonify({"error": "No se encontró el archivo."}), 400

    file = request.files['logo']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Guardar la ruta del logo en la base de datos
        setting = Settings.query.filter_by(key='logoUrl').first()
        if setting:
            setting.value = filepath
        else:
            new_setting = Settings(key='logoUrl', value=filepath)
            db.session.add(new_setting)
        db.session.commit()

        return jsonify({"message": "Logo cargado exitosamente.", "logoUrl": filepath}), 200

    return jsonify({"error": "Formato de archivo no permitido."}), 400
