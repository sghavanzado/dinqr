# DINQR Backend - Información del Ejecutable

## 📋 Información General

**Nombre del Ejecutable**: `generadorqr.exe`  
**Versión**: 1.0.0  
**Fecha de Compilación**: 12 de Agosto 2025  
**Tamaño**: 43.7 MB (43,724,939 bytes)  
**Plataforma**: Windows x64  
**Tipo**: Standalone (sin dependencias externas)  

## 🔧 Detalles Técnicos

### Herramientas de Compilación
- **PyInstaller**: 6.15.0
- **Python**: 3.11.8
- **Entorno**: Virtual Environment
- **SO de Compilación**: Windows 10 (10.0.17763)

### Punto de Entrada
- **Archivo Principal**: `app.py`
- **Función**: `create_app()`
- **Servidor Web**: Waitress (incluido)

### Dependencias Principales Incluidas
```
Flask==3.1.0
flask-cors==5.0.1
Flask-JWT-Extended==4.5.3
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.10
pyodbc==5.2.0
waitress==3.0.2
qrcode==8.1
flasgger==0.9.7.1
alembic==1.14.0
```

### Archivos y Directorios Incluidos
```
📂 Datos Estáticos:
├── static/          # Archivos estáticos web
├── migrations/      # Scripts de migración Alembic
├── data/           # Datos de configuración
└── config.py       # Configuración principal

📂 Módulos de Aplicación:
├── routes/         # Rutas de la API
├── models/         # Modelos de base de datos
├── services/       # Servicios de negocio
└── utils/          # Utilidades compartidas
```

## 🚀 Configuración de Ejecución

### Variables de Entorno Requeridas
```bash
DATABASE_URL=postgresql://user:pass@host:port/database
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
```

### Variables de Entorno Opcionales
```bash
# Servidor
HOST=127.0.0.1
PORT=5000
DEBUG=false

# Base de datos SQL Server (opcional)
DB_SERVER=sql_server_host
DB_NAME=database_name
DB_USERNAME=username
DB_PASSWORD=password

# CORS
CORS_ORIGINS=https://localhost:9000,https://127.0.0.1:9000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 📊 Rendimiento y Recursos

### Uso de Memoria
- **Memoria inicial**: ~50-80 MB
- **Memoria en ejecución**: ~100-200 MB (dependiendo de la carga)
- **Tiempo de inicio**: 2-5 segundos

### Puertos Utilizados
- **Puerto principal**: 5000 (configurable)
- **Base de datos PostgreSQL**: 5432 (configurable)
- **Base de datos SQL Server**: 1433 (configurable)

## 🔐 Seguridad

### Características de Seguridad Incluidas
- ✅ JWT Authentication
- ✅ CORS Protection
- ✅ Rate Limiting
- ✅ Security Headers (Talisman)
- ✅ SQL Injection Protection (SQLAlchemy ORM)
- ✅ XSS Protection
- ✅ CSRF Protection

### Archivos de Log
```
logs/
├── app.log         # Log principal de la aplicación
├── access.log      # Log de accesos HTTP
└── audit.log       # Log de auditoría (si está habilitado)
```

## 🌐 API Endpoints

### Autenticación
- `POST /auth/login` - Iniciar sesión
- `POST /auth/logout` - Cerrar sesión
- `POST /auth/refresh` - Renovar token

### QR Codes
- `GET /qr/funcionarios-sem-qr` - Funcionarios sin QR
- `GET /qr/funcionarios-com-qr` - Funcionarios con QR
- `POST /qr/generate` - Generar código QR
- `DELETE /qr/{id}` - Eliminar código QR

### Usuarios
- `GET /users` - Listar usuarios
- `POST /users` - Crear usuario
- `PUT /users/{id}` - Actualizar usuario
- `DELETE /users/{id}` - Eliminar usuario

### Sistema
- `GET /health` - Verificación de salud
- `GET /apidocs/` - Documentación de la API

## 🛠️ Solución de Problemas

### Problemas Comunes

**Error: "No se puede conectar a la base de datos"**
- Verificar `DATABASE_URL` en el archivo `.env`
- Confirmar que PostgreSQL está ejecutándose
- Verificar credenciales y permisos

**Error: "Puerto 5000 en uso"**
- Cambiar `PORT=5001` en el archivo `.env`
- O detener el proceso que usa el puerto 5000

**Error: "Archivo .env no encontrado"**
- Copiar `.env.template` como `.env`
- Configurar las variables necesarias

### Logs de Depuración
```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Ver errores específicos
grep "ERROR" logs/app.log
```

## 📞 Soporte

Para soporte técnico:
1. Revisar los logs en `logs/app.log`
2. Verificar la configuración en `.env`
3. Contactar al equipo de desarrollo con la información del error

---
**Última actualización**: 12 de Agosto 2025  
**Compilado por**: Sistema DINQR - Equipo de Desarrollo
