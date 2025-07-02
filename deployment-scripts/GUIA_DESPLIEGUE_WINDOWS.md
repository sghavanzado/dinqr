# DINQR - Guía de Despliegue en Windows Server

## Índice
1. [Resumen del Proceso](#resumen-del-proceso)
2. [Prerrequisitos](#prerrequisitos)
3. [Compilación del Backend](#compilación-del-backend)
4. [Despliegue Automático](#despliegue-automático)
5. [Despliegue Manual](#despliegue-manual)
6. [Configuración](#configuración)
7. [Solución de Problemas](#solución-de-problemas)
8. [Mantenimiento](#mantenimiento)

## Resumen del Proceso

Este proyecto ha sido adaptado para ejecutarse en Windows Server usando:
- **IIS** como servidor web y proxy reverso
- **Waitress** como servidor WSGI para Python
- **Almacenamiento en memoria** para rate limiting (sin Redis)
- **PostgreSQL** como base de datos
- **Servicio Windows** para ejecutar el backend automáticamente

### Arquitectura de Despliegue

```
Internet → IIS (Puerto 80/443) → Waitress (Puerto 5000) → Flask App
                ↓
            Frontend estático
```

## Prerrequisitos

### Software Requerido

1. **Windows Server 2016 o superior**
2. **Python 3.12**
   - Descargar desde: https://www.python.org/downloads/windows/
   - Instalar para todos los usuarios en `C:\Python312`
   - Agregar Python al PATH del sistema

3. **IIS con características adicionales**
   - Usar script: `configurar_iis.ps1`
   - O instalar manualmente desde "Características de Windows"

4. **IIS URL Rewrite Module**
   - Descargar desde: https://www.iis.net/downloads/microsoft/url-rewrite

5. **IIS Application Request Routing**
   - Descargar desde: https://www.iis.net/downloads/microsoft/application-request-routing

6. **PostgreSQL**
   - Descargar desde: https://www.postgresql.org/download/windows/

### Verificación de Prerrequisitos

```cmd
# Verificar Python
C:\Python312\python.exe --version

# Verificar IIS
where appcmd

# Verificar PostgreSQL
where psql
```

## Compilación del Backend

### 1. Preparar el Entorno de Desarrollo

En el directorio del proyecto backend:

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install build wheel
```

### 2. Compilar el Paquete .whl

Ejecutar el script de compilación:

```cmd
# En el directorio deployment-scripts
compilar_backend_whl.bat
```

Este script:
- Activa el entorno virtual
- Instala dependencias de compilación
- Construye el paquete .whl
- Lo coloca en `dist/`

### 3. Verificar la Compilación

```cmd
dir dist\*.whl
```

Debería mostrar un archivo como: `dinqr-1.0.0-py3-none-any.whl`

## Despliegue Automático

### Opción 1: Despliegue Completo Automatizado

1. Copiar los siguientes archivos al servidor Windows:
   - `desplegar_completo.bat`
   - `instalar_whl_windows.bat`
   - `configurar_iis_proxy.bat`
   - `configurar_iis.ps1`
   - `env-production-template`
   - El archivo `.whl` compilado

2. Ejecutar como administrador:
   ```cmd
   desplegar_completo.bat
   ```

Este script realizará automáticamente:
- Verificación de prerrequisitos
- Instalación del backend
- Configuración de IIS
- Creación del servicio Windows
- Configuración inicial

### Opción 2: Pasos Individuales

Si prefiere control granular:

```cmd
# 1. Instalar backend
instalar_whl_windows.bat

# 2. Configurar IIS
configurar_iis_proxy.bat

# 3. Configurar variables de entorno
copy env-production-template C:\inetpub\dinqr\.env
# Editar .env con sus configuraciones
```

## Despliegue Manual

### 1. Crear Estructura de Directorios

```cmd
mkdir C:\inetpub\dinqr
mkdir C:\inetpub\dinqr\logs
mkdir C:\inetpub\dinqr\uploads
mkdir C:\inetpub\dinqr\data
```

### 2. Crear Entorno Virtual

```cmd
cd C:\inetpub\dinqr
C:\Python312\python.exe -m venv venv
venv\Scripts\activate
```

### 3. Instalar Backend

```cmd
pip install dinqr-1.0.0-py3-none-any.whl
pip install waitress pywin32
```

### 4. Configurar Servicio Windows

Crear `dinqr_service.py` (ver contenido en script de instalación) y ejecutar:

```cmd
python dinqr_service.py install
```

### 5. Configurar IIS

Usar el script `configurar_iis_proxy.bat` o configurar manualmente los sitios y reglas de reescritura.

## Configuración

### Variables de Entorno (.env)

Editar `C:\inetpub\dinqr\.env`:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/dinqr_db

# Seguridad (GENERAR CLAVES ÚNICAS)
SECRET_KEY=clave_secreta_unica_aqui
JWT_SECRET_KEY=clave_jwt_unica_aqui

# Entorno
FLASK_ENV=production
DEBUG=false

# Rate limiting (sin Redis)
RATELIMIT_STORAGE_URL=memory://

# HTTPS (recomendado)
ENABLE_HTTPS=true
SESSION_COOKIE_SECURE=true
```

### Base de Datos

1. Crear base de datos PostgreSQL:
   ```sql
   CREATE DATABASE dinqr_db;
   CREATE USER dinqr_user WITH PASSWORD 'password_segura';
   GRANT ALL PRIVILEGES ON DATABASE dinqr_db TO dinqr_user;
   ```

2. Ejecutar migraciones:
   ```cmd
   cd C:\inetpub\dinqr
   venv\Scripts\activate
   set FLASK_APP=app.py
   flask db upgrade
   ```

3. Crear usuario administrador:
   ```cmd
   python create_admin.py
   ```

### Frontend

1. Compilar frontend en el entorno de desarrollo:
   ```cmd
   cd frontend
   npm run build
   ```

2. Copiar archivos compilados:
   ```cmd
   xcopy /s /e dist\* C:\inetpub\wwwroot\dinqr\frontend\
   ```

## Gestión de Servicios

### Comandos del Servicio Windows

```cmd
# Iniciar servicio
sc start DINQR_Backend

# Detener servicio
sc stop DINQR_Backend

# Reiniciar servicio
sc stop DINQR_Backend && sc start DINQR_Backend

# Ver estado
sc query DINQR_Backend

# Ver logs del servicio
eventvwr.msc
```

### Comandos de IIS

```cmd
# Reiniciar IIS
iisreset

# Ver sitios
appcmd list sites

# Ver application pools
appcmd list apppools

# Reiniciar application pool
appcmd recycle apppool "DINQR_AppPool"
```

### Inicio Manual (para debugging)

```cmd
cd C:\inetpub\dinqr
venv\Scripts\activate
set FLASK_APP=app.py
set FLASK_ENV=production
waitress-serve --host=127.0.0.1 --port=5000 --threads=4 --call app:create_app
```

## Solución de Problemas

### Servicio no inicia

1. Verificar logs:
   - Event Viewer: Windows Logs > Application
   - `C:\inetpub\dinqr\logs\app.log`

2. Verificar configuración:
   ```cmd
   cd C:\inetpub\dinqr
   venv\Scripts\python -c "from config import Config; print('Config OK')"
   ```

3. Verificar base de datos:
   ```cmd
   venv\Scripts\python -c "import psycopg2; print('PostgreSQL OK')"
   ```

### Error 500 en IIS

1. Verificar que el servicio DINQR_Backend esté ejecutándose
2. Verificar conectividad al puerto 5000:
   ```cmd
   telnet 127.0.0.1 5000
   ```
3. Revisar logs de IIS: `C:\inetpub\logs\LogFiles\`

### Error 502 Bad Gateway

1. El servicio backend no está ejecutándose
2. Puerto 5000 está siendo usado por otro proceso
3. Firewall bloqueando conexiones locales

### Problemas de Permisos

```cmd
# Verificar permisos en directorio de aplicación
icacls C:\inetpub\dinqr

# Otorgar permisos a IIS
icacls C:\inetpub\dinqr /grant "IIS_IUSRS:(OI)(CI)RX" /T
icacls C:\inetpub\dinqr /grant "IUSR:(OI)(CI)RX" /T
```

## Mantenimiento

### Backup

1. **Base de datos**:
   ```cmd
   pg_dump -h localhost -U dinqr_user dinqr_db > backup_dinqr_%date%.sql
   ```

2. **Archivos de aplicación**:
   ```cmd
   xcopy /s /e C:\inetpub\dinqr C:\Backups\dinqr_%date%\
   ```

### Actualizaciones

1. Detener servicio:
   ```cmd
   sc stop DINQR_Backend
   ```

2. Activar entorno virtual:
   ```cmd
   cd C:\inetpub\dinqr
   venv\Scripts\activate
   ```

3. Instalar nueva versión:
   ```cmd
   pip install --upgrade dinqr-nueva-version.whl
   ```

4. Ejecutar migraciones si es necesario:
   ```cmd
   flask db upgrade
   ```

5. Reiniciar servicio:
   ```cmd
   sc start DINQR_Backend
   ```

### Monitoreo

1. **Logs de aplicación**: `C:\inetpub\dinqr\logs\app.log`
2. **Logs de IIS**: `C:\inetpub\logs\LogFiles\`
3. **Event Viewer**: Windows Logs > Application
4. **Performance Monitor**: Monitorear CPU, memoria, y red

### Scripts de Mantenimiento

Crear tareas programadas para:
- Backup automático de base de datos
- Rotación de logs
- Reinicio programado del servicio
- Monitoreo de salud de la aplicación

## Seguridad

### Configuración de Firewall

```cmd
# Bloquear acceso directo al puerto 5000 desde exterior
netsh advfirewall firewall add rule name="DINQR Block External 5000" dir=in action=block protocol=TCP localport=5000 remoteip=!127.0.0.1

# Permitir tráfico HTTP/HTTPS en IIS
netsh advfirewall firewall set rule group="World Wide Web Services (HTTP)" new enable=yes
netsh advfirewall firewall set rule group="World Wide Web Services (HTTPS)" new enable=yes
```

### Certificado SSL

1. Obtener certificado SSL válido (Let's Encrypt, CA comercial)
2. Instalar en IIS Manager
3. Configurar redirección HTTP → HTTPS
4. Actualizar .env: `ENABLE_HTTPS=true`

### Actualizaciones de Seguridad

- Mantener Windows Server actualizado
- Actualizar Python regularmente
- Revisar dependencias con `pip audit`
- Monitorear alertas de seguridad

## Contacto y Soporte

Para problemas específicos de despliegue:
1. Revisar logs detallados
2. Verificar configuración paso a paso
3. Consultar documentación oficial de IIS y Waitress
4. Contactar al equipo de desarrollo con logs específicos

---

**Nota**: Esta documentación asume un entorno de Windows Server estándar. Algunos pasos pueden variar según la configuración específica del servidor.
