from psycopg2 import pool as pg_pool
import psycopg2
import pyodbc
import os
import logging

# Pool de conexiones para PostgreSQL
pg_connection_pool = pg_pool.SimpleConnectionPool(
    1, 200,  # Min y max conexiones (incrementado a 200)
    dbname=os.environ.get('LOCAL_DB_NAME', 'localdb'),
    user=os.environ.get('LOCAL_DB_USER', 'postgres'),
    password=os.environ.get('LOCAL_DB_PASSWORD', 'postgr3s'),
    host=os.environ.get('LOCAL_DB_HOST', 'localhost'),
    port=os.environ.get('LOCAL_DB_PORT', 5432)
)

# Manual tracking of active and idle connections
active_connections = 0
idle_connections = 200  # Start with the max pool size

def obtener_conexion_local():
    """Obtener una conexión del pool de PostgreSQL."""
    global active_connections, idle_connections
    try:
        conn = pg_connection_pool.getconn()
        active_connections += 1
        idle_connections -= 1
        logging.info(f"Conexión obtenida del pool. Activas: {active_connections}, Inactivas: {idle_connections}")
        conn.set_session(autocommit=True)
        return conn
    except Exception as e:
        logging.error(f"Error al obtener conexión local: {str(e)}")
        raise

def liberar_conexion_local(conn):
    """Liberar una conexión al pool de PostgreSQL."""
    global active_connections, idle_connections
    try:
        if conn:
            pg_connection_pool.putconn(conn)
            active_connections -= 1
            idle_connections += 1
            logging.info(f"Conexión liberada al pool. Activas: {active_connections}, Inactivas: {idle_connections}")
    except Exception as e:
        logging.error(f"Error al liberar conexión local: {str(e)}")
        raise

# Conexión directa para SQL Server
def obtener_conexion_remota():
    """Obtener una conexión a SQL Server."""
    try:
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER', '10.7.74.80')};"
            f"DATABASE={os.environ.get('DB_NAME', 'empresadb')};"
            f"UID={os.environ.get('DB_USERNAME', 'sonacarduser')};"
            f"PWD={os.environ.get('DB_PASSWORD', 'Angola2025')};"
            f"TrustServerCertificate=yes",
            timeout=10  # Timeout in seconds
        )
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos remota: {str(e)}")
        raise ConnectionError(f"Error al conectar con la base de datos remota: {str(e)}")
