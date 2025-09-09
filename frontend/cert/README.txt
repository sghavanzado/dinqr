Coloca aquí tus archivos de certificado SSL para desarrollo local:
- localhost-key.pem
- localhost-cert.pem

Puedes generarlos con:
openssl req -x509 -newkey rsa:2048 -nodes -keyout localhost-key.pem -out localhost-cert.pem -days 365 -subj "/CN=localhost"
