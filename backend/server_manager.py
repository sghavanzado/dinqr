import os
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from utils.db_utils import obtener_conexion_local  # Import database utility
import psutil
import socket

# Importar la aplicación Flask desde server.py
from server import app

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')
log_file = 'logs/server_manager.log'
access_log_file = 'logs/gunicorn_access.log'
error_log_file = 'logs/gunicorn_error.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10240, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

server_process = None

def obtener_puerto_servidor():
    """Obtain the server port from the settings table."""
    try:
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = 'serverPort'")
            result = cursor.fetchone()
            if not result:
                raise ValueError("No se encontró la configuración 'serverPort' en la tabla settings.")
            return int(result[0])
    except Exception as e:
        logger.error(f"Error al obtener el puerto del servidor: {str(e)}")
        raise

def obtener_domain_servidor():
    """Obtain the server domain from the settings table."""
    try:
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = 'serverDomain'")
            result = cursor.fetchone()
            if not result:
                raise ValueError("No se encontró la configuración 'serverDomain' en la tabla settings.")
            return result[0]  # Return as a string, not an integer
    except Exception as e:
        logger.error(f"Error al obtener el ip del servidor: {str(e)}")
        raise

def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('0.0.0.0', port)) == 0

def iniciar_servidor():
    """Start the Gunicorn server."""
    global server_process
    try:
        port = 9000  # Puerto fijo
        if is_port_in_use(port):
            logger.warning(f"El puerto {port} ya está en uso. No se puede iniciar Gunicorn.")
            return

        if server_process is None or server_process.poll() is not None:
            # Construir el comando de Gunicorn
            gunicorn_command = [
                "gunicorn",
                "-w", os.environ.get("GUNICORN_WORKERS", "4"),  # Número de trabajadores
                "-k", os.environ.get("GUNICORN_WORKER_CLASS", "sync"),  # Tipo de worker
                "-b", f"0.0.0.0:{port}",  # Escuchar en todas las IPs y puerto 9000
                "--timeout", os.environ.get("GUNICORN_TIMEOUT", "120"),  # Tiempo de espera
                "--graceful-timeout", os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", "120"),
                "--access-logfile", "logs/gunicorn_access.log",
                "--error-logfile", "logs/gunicorn_error.log",
                "server:app"  # Nombre del módulo y la aplicación Flask
            ]

            # Registrar el comando en los logs
            logger.info(f"Iniciando Gunicorn con el comando: {' '.join(gunicorn_command)}")

            # Iniciar el proceso de Gunicorn
            server_process = subprocess.Popen(
                gunicorn_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            logger.info(f"Servidor iniciado en el puerto {port} con PID: {server_process.pid}")
        else:
            logger.warning("El servidor ya está en ejecución.")
    except Exception as e:
        logger.error(f"Error al iniciar el servidor: {str(e)}")
        raise

def detener_servidor():
    """Stop the Gunicorn server."""
    global server_process
    try:
        if server_process and server_process.poll() is None:
            logger.info(f"Intentando detener el servidor con PID: {server_process.pid}")
            
            # Enviar señal de terminación al proceso
            server_process.terminate()
            
            # Esperar a que el proceso termine
            server_process.wait(timeout=10)
            
            # Verificar si el proceso sigue activo
            if server_process.poll() is None:
                logger.warning(f"El proceso con PID {server_process.pid} no se detuvo. Forzando terminación.")
                server_process.kill()
                server_process.wait()

            logger.info("Servidor detenido correctamente.")
        else:
            logger.warning("El servidor no está en ejecución.")
    except subprocess.TimeoutExpired:
        logger.error(f"El proceso con PID {server_process.pid} no respondió a tiempo. Forzando terminación.")
        server_process.kill()
        server_process.wait()
    except Exception as e:
        logger.error(f"Error al detener el servidor: {str(e)}")
        raise
    finally:
        server_process = None  # Asegurarse de que la variable global se reinicie

def status_servidor():
    """Consultar o estado do servidor."""
    global server_process
    try:
        if server_process and server_process.poll() is None:
            return {"status": "em execução", "pid": server_process.pid}
        return {"status": "parado"}
    except Exception as e:
        logger.error(f"Erro ao consultar o estado do servidor: {str(e)}")
        raise RuntimeError("Erro ao consultar o estado do servidor.")

@app.before_request
def log_request_info():
    """Registrar información de cada solicitud entrante."""
    logger.info(f"Solicitud: {request.method} {request.path} desde {request.remote_addr}")

@app.after_request
def log_response_info(response):
    """Registrar información de la respuesta de cada solicitud."""
    logger.info(f"Respuesta: {response.status_code} para {request.method} {request.path}")
    return response

@app.route('/server/start', methods=['POST'])
def api_iniciar_servidor():
    iniciar_servidor()
    return jsonify({"message": "Servidor iniciado."}), 200

@app.route('/server/stop', methods=['POST'])
def api_detener_servidor():
    detener_servidor()
    return jsonify({"message": "Servidor detenido."}), 200

@app.route('/server/exit', methods=['POST'])
def api_salir():
    detener_servidor()
    return jsonify({"message": "Gestor del servidor cerrado."}), 200

@app.route('/server/status', methods=['GET'])
def server_status():
    """Consultar el estado del servidor."""
    global server_process
    if server_process and server_process.poll() is None:
        return jsonify({"status": "running", "pid": server_process.pid}), 200
    return jsonify({"status": "stopped"}), 200
