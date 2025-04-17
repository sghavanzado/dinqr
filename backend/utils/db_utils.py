from psycopg2 import pool as pg_pool
import pyodbc
import os
import logging

# Pool de conexiones para PostgreSQL
pg_connection_pool = pg_pool.SimpleConnectionPool(
    1, 20,  # Min y max conexiones
    dbname=os.environ.get('LOCAL_DB_NAME', 'localdb'),
    user=os.environ.get('LOCAL_DB_USER', 'postgres'),
    password=os.environ.get('LOCAL_DB_PASSWORD', 'localpassword'),
    host=os.environ.get('LOCAL_DB_HOST', 'localhost'),
    port=os.environ.get('LOCAL_DB_PORT', 5432)
)

def obtener_conexion_local():
    """Obtener una conexión del pool de PostgreSQL."""
    try:
        return pg_connection_pool.getconn()
    except Exception as e:
        logging.error(f"Error al obtener conexión local: {str(e)}")
        raise

def liberar_conexion_local(conn):
    """Liberar una conexión al pool de PostgreSQL."""
    try:
        if conn:
            pg_connection_pool.putconn(conn)
    except Exception as e:
        logging.error(f"Error al liberar conexión local: {str(e)}")
        raise

# Conexión directa para SQL Server
def obtener_conexion_remota():
    """Obtener una conexión a SQL Server."""
    try:
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER', '192.168.253.5')};"
            f"DATABASE={os.environ.get('DB_NAME', 'externaldb')};"
            f"UID={os.environ.get('DB_USERNAME', 'sa')};"
            f"PWD={os.environ.get('DB_PASSWORD', 'Global2020')};"
            f"TrustServerCertificate=yes"
        )
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos remota: {str(e)}")
        raise ConnectionError(f"Error al conectar con la base de datos remota: {str(e)}")
