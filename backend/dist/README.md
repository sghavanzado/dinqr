# DINQR Backend - Ejecutable Standalone

## Archivos Incluidos

- `generadorqr.exe` - Ejecutable principal del backend DINQR
- `.env.template` - Plantilla de configuración

## Instalación y Configuración

### 1. Preparación del Entorno

1. Cree una carpeta para la aplicación (ej: `C:\DINQR\Backend`)
2. Copie `generadorqr.exe` a esta carpeta
3. Copie `.env.template` como `.env` en la misma carpeta
4. Edite el archivo `.env` con sus configuraciones específicas

### 2. Configuración de Base de Datos

El backend requiere acceso a dos bases de datos:

**PostgreSQL Local (requerido):**
```
DATABASE_URL=postgresql://usuario:password@servidor:puerto/base_datos
```

**SQL Server Remoto (opcional):**
```
DB_SERVER=servidor_sql_server
DB_NAME=nombre_base_datos
DB_USERNAME=usuario
DB_PASSWORD=password
```

### 3. Configuración de Seguridad

**Claves secretas (IMPORTANTE - cambiar en producción):**
```
SECRET_KEY=genere_una_clave_secreta_unica
JWT_SECRET_KEY=genere_una_clave_jwt_unica
```

### 4. Configuración de Red

**Servidor y CORS:**
```
HOST=127.0.0.1
PORT=5000
CORS_ORIGINS=https://su-dominio.com,https://otro-dominio.com
```

## Ejecución

### Modo Manual
```cmd
cd C:\DINQR\Backend
generadorqr.exe
```

### Como Servicio de Windows (Recomendado)

#### Instalación Automática
```cmd
# Ejecutar como administrador
instalar_servicio.bat
```

#### Instalación Manual
```cmd
# Instalar servicio (requiere permisos de administrador)
generadorqr.exe --service install

# Iniciar servicio
generadorqr.exe --service start

# Ver estado
generadorqr.exe --service status

# Detener servicio
generadorqr.exe --service stop

# Remover servicio
generadorqr.exe --service remove
```

#### Gestión del Servicio
```cmd
# Script interactivo de gestión
gestionar_servicio.bat
```

### Argumentos de Línea de Comandos
```cmd
# Servidor normal en puerto personalizado
generadorqr.exe --port 8000 --host 0.0.0.0

# Modo debug (desarrollo)
generadorqr.exe --debug
```

## Estructura de Directorios

Después de la primera ejecución, se crearán automáticamente:

```
C:\DINQR\Backend\
├── generadorqr.exe
├── .env
├── logs/              # Archivos de log
│   ├── app.log
│   └── access.log
├── static/            # Archivos estáticos
├── uploads/           # Archivos subidos
└── data/              # Datos de la aplicación
```

## API Endpoints

Una vez ejecutándose, la API estará disponible en:

- Base URL: `http://127.0.0.1:5000`
- Documentación: `http://127.0.0.1:5000/apidocs/`
- Health Check: `http://127.0.0.1:5000/health`

### Principales Endpoints:
- `POST /auth/login` - Autenticación
- `GET /qr/funcionarios-sem-qr` - Funcionarios sin QR
- `GET /qr/funcionarios-com-qr` - Funcionarios con QR
- `POST /qr/generate` - Generar código QR

## Logs y Monitoreo

Los logs se guardan en la carpeta `logs/`:
- `app.log` - Log principal de la aplicación
- `access.log` - Log de accesos HTTP

## Solución de Problemas

### Error de Base de Datos
- Verifique la conexión a PostgreSQL
- Confirme que las credenciales en `.env` son correctas
- Asegúrese de que el servidor PostgreSQL esté ejecutándose

### Error de Puerto en Uso
- Cambie el puerto en `.env`: `PORT=5001`
- O termine el proceso que está usando el puerto 5000

### Error de Permisos
- Ejecute como administrador si es necesario
- Verifique permisos de escritura en la carpeta de logs

## Información Técnica

- **Versión de Python**: 3.11.8
- **Framework**: Flask
- **Servidor Web**: Waitress (incluido)
- **Base de Datos**: PostgreSQL + SQL Server
- **Autenticación**: JWT

## Soporte

Para soporte técnico, revise los logs en la carpeta `logs/` y contacte al equipo de desarrollo.
