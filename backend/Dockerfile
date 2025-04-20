# Utiliza una imagen base oficial de Python
FROM python:3.12.5

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Expone el puerto en el que la aplicación Flask se ejecutará
EXPOSE 5050

# Define la variable de entorno para Flask (si es necesario)
# ENV FLASK_APP=main.py

# Define el comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0"]