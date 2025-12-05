"""
SIGA - Sistema Integral de Gestión de Accesos
Utilidades de Base de Datos - Versión Mejorada con Context Managers

Desarrollado por: Ing. Maikel Cuao
Email: maikel@hotmail.com
Fecha: 2025
Descripción: Gestión mejorada de conexiones a bases de datos con context managers.
"""

from psycopg2 import pool as pg_pool
from contextlib import contextmanager
import psycopg2
import pyodbc
import os
import logging
from typing import Generator

# Pool de conexiones para PostgreSQL
pg_connection_pool = pg_pool.SimpleConnectionPool(
    1, 200,  # Min y max conexiones
    dbname=os.environ.get('LOCAL_DB_NAME', 'localdb'),
    user=os.environ.get('LOCAL_DB_USER', 'postgres'),
    password=os.environ.get('LOCAL_DB_PASSWORD', 'p0stgr3s'),
    host=os.environ.get('LOCAL_DB_HOST', 'localhost'),
    port=os.environ.get('LOCAL_DB_PORT', 5432)
)

# Manual tracking of active and idle connections
active_connections = 0
idle_connections = 200


# ========== FUNCIONES LEGACY (Mantener para compatibilidad) ==========

def obtener_conexion_local():
    """
    Obtener una conexión del pool de PostgreSQL.
    
    DEPRECATED: Use local_db_connection() context manager instead.
    """
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
    """
    Liberar una conexión al pool de PostgreSQL.
    
    DEPRECATED: Use local_db_connection() context manager instead.
    """
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


def obtener_conexion_remota():
    """
    Obtener una conexión a SQL Server.
    
    DEPRECATED: Use remote_db_connection() context manager instead.
    """
    try:
        return pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER', 'localhost')};"
            f"DATABASE={os.environ.get('DB_NAME', 'empresadb')};"
            f"UID={os.environ.get('DB_USERNAME', 'sa')};"
            f"PWD={os.environ.get('DB_PASSWORD', 'Global2020')};"
            f"TrustServerCertificate=yes",
            timeout=10
        )
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos remota: {str(e)}")
        raise ConnectionError(f"Error al conectar con la base de datos remota: {str(e)}")


# ========== NUEVOS CONTEXT MANAGERS (Recomendado) ==========

@contextmanager
def local_db_connection(autocommit: bool = True) -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Context manager para conexión PostgreSQL local con manejo automático de recursos.
    
    Uso:
        with local_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    
    Args:
        autocommit: Si True, activa autocommit. Si False, usa transacciones manuales.
    
    Yields:
        psycopg2.connection: Conexión a PostgreSQL
    
    Raises:
        Exception: Si hay error al obtener o usar la conexión
    """
    global active_connections, idle_connections
    conn = None
    try:
        # Obtener conexión del pool
        conn = pg_connection_pool.getconn()
        active_connections += 1
        idle_connections -= 1
        logging.debug(f"[Pool] Conexión obtenida. Activas: {active_connections}, Disponibles: {idle_connections}")
        
        # Configurar autocommit
        conn.set_session(autocommit=autocommit)
        
        yield conn
        
        # Si no está en autocommit y no hubo excepciones, hacer commit
        if not autocommit and conn and not conn.closed:
            conn.commit()
            logging.debug("[PostgreSQL] Transacción confirmada")
            
    except Exception as e:
        # En caso de error, hacer rollback si la conexión existe
        if conn and not conn.closed and not autocommit:
            conn.rollback()
            logging.warning(f"[PostgreSQL] Rollback ejecutado debido a: {str(e)}")
        raise
        
    finally:
        # Siempre liberar la conexión al pool
        if conn:
            pg_connection_pool.putconn(conn)
            active_connections -= 1
            idle_connections += 1
            logging.debug(f"[Pool] Conexión liberada. Activas: {active_connections}, Disponibles: {idle_connections}")


@contextmanager
def remote_db_connection(timeout: int = 10) -> Generator[pyodbc.Connection, None, None]:
    """
    Context manager para conexión SQL Server remota con manejo automático de recursos.
    
    Uso:
        with remote_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sonacard")
            results = cursor.fetchall()
    
    Args:
        timeout: Tiempo de espera para la conexión en segundos
    
    Yields:
        pyodbc.Connection: Conexión a SQL Server
    
    Raises:
        ConnectionError: Si no se puede establecer la conexión
    """
    conn = None
    try:
        # Crear conexión a SQL Server
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER', 'localhost')};"
            f"DATABASE={os.environ.get('DB_NAME', 'empresadb')};"
            f"UID={os.environ.get('DB_USERNAME', 'sa')};"
            f"PWD={os.environ.get('DB_PASSWORD', 'Global2020')};"
            f"TrustServerCertificate=yes",
            timeout=timeout
        )
        logging.debug("[SQL Server] Conexión establecida")
        
        yield conn
        
        # Commit al final si no hubo excepciones
        if conn:
            conn.commit()
            logging.debug("[SQL Server] Transacción confirmada")
            
    except pyodbc.Error as e:
        # Rollback en caso de error
        if conn:
            conn.rollback()
            logging.warning(f"[SQL Server] Rollback ejecutado debido a: {str(e)}")
        logging.error(f"[SQL Server] Error de conexión: {str(e)}")
        raise ConnectionError(f"Error al conectar con SQL Server: {str(e)}")
        
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"[SQL Server] Error inesperado: {str(e)}")
        raise
        
    finally:
        # Cerrar conexión
        if conn:
            conn.close()
            logging.debug("[SQL Server] Conexión cerrada")


@contextmanager
def transaction(conn, isolation_level: str = None):
    """
    Context manager para manejo explícito de transacciones.
    
    Uso:
        with local_db_connection(autocommit=False) as conn:
            with transaction(conn):
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET...")
                # Auto-commit al salir, rollback en caso de excepción
    
    Args:
        conn: Conexión de base de datos
        isolation_level: Nivel de aislamiento (para PostgreSQL)
    
    Yields:
        connection: La misma conexión para uso en el bloque
    """
    try:
        if isolation_level and hasattr(conn, 'set_isolation_level'):
            conn.set_isolation_level(isolation_level)
        
        yield conn
        
        # Commit si todo salió bien
        if conn and not conn.closed:
            conn.commit()
            logging.debug("[Transaction] Commit exitoso")
            
    except Exception as e:
        # Rollback en caso de error
        if conn and not conn.closed:
            conn.rollback()
            logging.warning(f"[Transaction] Rollback ejecutado: {str(e)}")
        raise


def get_pool_stats() -> dict:
    """
    Obtiene estadísticas del pool de conexiones.
    
    Returns:
        dict: Estadísticas del pool (activas, disponibles, etc.)
    """
    return {
        'active_connections': active_connections,
        'idle_connections': idle_connections,
        'total_capacity': 200,
        'usage_percentage': (active_connections / 200) * 100
    }


def close_all_connections():
    """
    Cierra todas las conexiones del pool (para shutdown de aplicación).
    """
    global pg_connection_pool
    try:
        pg_connection_pool.closeall()
        logging.info("[Pool] Todas las conexiones cerradas")
    except Exception as e:
        logging.error(f"[Pool] Error al cerrar conexiones: {str(e)}")
