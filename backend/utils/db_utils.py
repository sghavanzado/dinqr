import pyodbc
import os
import logging

def obtener_conexion_local():
    """Obtener una conexión a la base de datos IAMC (MSSQL)."""
    try:
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER', 'localhost')};"
            f"DATABASE=IAMC;"
            f"UID=sa;"
            f"PWD=Global2020;"
            f"TrustServerCertificate=yes",
            timeout=10
        )
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos IAMC: {str(e)}")
        raise ConnectionError(f"Error al conectar con la base de datos IAMC: {str(e)}")

def obtener_conexion_remota():
    """Obtener una conexión a la base de datos empresadb (donde está la tabla sonacard)."""
    try:
        return pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.environ.get('DB_SERVER', 'localhost')};"
            f"DATABASE=empresadb;"
            f"UID=sa;"
            f"PWD=Global2020;"
            f"TrustServerCertificate=yes",
            timeout=10
        )
    except Exception as e:
        logging.error(f"Error al conectar con la base de datos empresadb: {str(e)}")
        raise ConnectionError(f"Error al conectar con la base de datos empresadb: {str(e)}")
