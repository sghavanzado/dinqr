# Utiliza una imagen base ligera para servir archivos estáticos.
# Puedes usar Nginx, httpd o una imagen base de Node.js con un servidor estático.
# Ejemplo usando Nginx:
    FROM nginx:stable-alpine

    # Copia los archivos construidos de tu frontend a la carpeta de archivos estáticos de Nginx.
    # Asegúrate de que la ruta 'dist' coincida con la carpeta de salida de tu comando 'npm run build'.
    COPY dist /usr/share/nginx/html
    
    # Expone el puerto en el que Nginx sirve el contenido (por defecto es el puerto 80).
    EXPOSE 80
    
    # Nginx ya se ejecuta por defecto en la imagen base, así que no necesitamos un CMD explícito.
