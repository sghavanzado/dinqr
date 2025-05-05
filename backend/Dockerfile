# Utiliza una imagen base de Python específica con la versión 3.12.5
FROM python:3.12.5

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Instala las dependencias del sistema necesarias para pyodbc
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc \
    odbcinst 
# Agregar repositorio de Microsoft para msodbcsql17
# Agregar clave GPG de Microsoft de forma segura
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg

# Agregar el repositorio de Microsoft (ajustado para Debian 12 / bookworm)
RUN echo "deb [arch=amd64] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list

# Instalar msodbcsql18 (última versión estable)
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala el wheel de tu aplicación.
COPY dist/apiqr-*.whl .
RUN pip install --timeout=100 --no-cache-dir apiqr-*.whl

# Instala otras dependencias de Python que no estén en el wheel (si las hay).
# Por ejemplo, si Flask no está en el wheel por alguna razón:
# RUN pip install --no-cache-dir flask

# Copia el archivo de configuración.
COPY config.py .

# Copia los scripts de inicialización de la base de datos.
COPY initialize_roles.py .
COPY initialize_user.py .

# Copia el código fuente de tu backend al contenedor.
COPY . .


# Define el comando para ejecutar la inicialización de la base de datos y luego la aplicación principal (app.py).
CMD ["sh", "-c", "python initialize_roles.py && python initialize_user.py && python app.py"]

# Expone el puerto en el que tu aplicación escucha.
EXPOSE 5000
EXPOSE 9000
