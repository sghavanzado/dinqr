import os
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from utils.db_utils import obtener_conexion_local  # Import database utility
import psutil

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
            cursor.execute("SELECT value FROM settings WHERE [key] = 'serverPort'")
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
            cursor.execute("SELECT value FROM settings WHERE [key] = 'serverDomain'")
            result = cursor.fetchone()
            if not result:
                raise ValueError("No se encontró la configuración 'serverDomain' en la tabla settings.")
            return result[0]  # Return as a string, not an integer
    except Exception as e:
        logger.error(f"Error al obtener el ip del servidor: {str(e)}")
        raise

def iniciar_servidor():
    """Start the Waitress server."""
    global server_process
    try:
        if server_process is None or server_process.poll() is not None:
            ip = obtener_domain_servidor()
            port = obtener_puerto_servidor()



            # Detectar automáticamente el ejecutable del entorno virtual activo
            import sys
            venv_python = sys.executable
            waitress_command = [
                venv_python, "-m", "waitress", "--host", ip, "--port", str(port), "server:app"
            ]

            logger.info(f"Iniciando Waitress con el comando: {' '.join(waitress_command)}")

            server_process = subprocess.Popen(
                waitress_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Esperar unos segundos para verificar si el proceso se inicia correctamente
            try:
                stdout, stderr = server_process.communicate(timeout=5)
                if server_process.returncode is not None and server_process.returncode != 0:
                    logger.error(f"Error al iniciar Waitress: {stderr.strip()}")
                    raise RuntimeError(f"Error al iniciar Waitress: {stderr.strip()}")
            except subprocess.TimeoutExpired:
                logger.info(f"Servidor iniciado correctamente con PID: {server_process.pid}")

            logger.info(f"Servidor {ip} iniciado en el puerto {port} con PID: {server_process.pid}")
        else:
            logger.warning("El servidor ya está en ejecución.")
    except Exception as e:
        logger.error(f"Error al iniciar el servidor: {str(e)}")
        raise

def detener_servidor():
    """Stop the Waitress server."""
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

if __name__ == '__main__':
    try:
        ip = obtener_domain_servidor()  # Obtener la IP desde la base de datos
        port = obtener_puerto_servidor()  # Obtener el puerto desde la base de datos
        logger.info("Use Waitress to run this application in producción.")
        logger.info(f"Example: python -m waitress --host {ip} --port {port} server:app")
    except Exception as e:
        logger.error(f"Error al obtener el puerto del servidor: {str(e)}")