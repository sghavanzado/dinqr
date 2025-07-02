# 🚀 DINQR - Guía de Instalación Waitress + IIS para Windows Server

## 📋 Tabla de Contenidos
1. [Información General](#información-general)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Preparación del Servidor](#preparación-del-servidor)
4. [Instalación Automatizada](#instalación-automatizada)
5. [Instalación Manual Paso a Paso](#instalación-manual-paso-a-paso)
6. [Configuración Post-Instalación](#configuración-post-instalación)
7. [Gestión del Servicio](#gestión-del-servicio)
8. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
9. [Backup y Restauración](#backup-y-restauración)
10. [Solución de Problemas](#solución-de-problemas)

---

## 📚 Información General

### 🏗️ Arquitectura del Sistema

```
Cliente (Browser) 
    ↓ HTTPS/HTTP (Puerto 80/443)
IIS (Internet Information Services)
    ↓ HTTP (Reverse Proxy)
Waitress WSGI Server (Puerto 5000)
    ↓ Python WSGI
Flask Application (DINQR Backend)
    ↓ SQL
PostgreSQL Database
```

### ✅ Ventajas de Waitress + IIS

- **🔥 Rendimiento Superior**: Waitress está optimizado para Windows Server
- **🛡️ Seguridad Mejorada**: Integración nativa con Windows Security
- **🔄 Servicio de Windows**: Inicio automático y gestión nativa del SO
- **📊 Monitoreo Integrado**: Compatible con Event Viewer y herramientas de Windows
- **🔧 Mantenimiento Simplificado**: Menos dependencias externas
- **🏥 Recuperación Automática**: Reinicio automático en caso de fallos

---

## 🔧 Requisitos del Sistema

### Requisitos Mínimos
- **SO**: Windows Server 2016+ o Windows 10+ Pro
- **RAM**: 4 GB (8 GB recomendado)
- **CPU**: 2 cores (4 cores recomendado)
- **Disco**: 20 GB libres (50 GB recomendado)
- **Red**: Acceso a Internet para descarga de dependencias

### Software Requerido
- **Python**: 3.8 o superior
- **IIS**: Con Application Request Routing (ARR)
- **PostgreSQL**: 12+ (o SQL Server como alternativa)
- **Git**: Para clonar el repositorio (opcional)

### Puertos Requeridos
- **80**: HTTP (IIS)
- **443**: HTTPS (IIS) 
- **5000**: Waitress (interno)
- **5432**: PostgreSQL (si está en el mismo servidor)

---

## 🛠️ Preparación del Servidor

### 1. Habilitar IIS y Características Necesarias

**Opción A: Script Automatizado (Recomendado)**
```cmd
# Ejecutar como Administrador
cd deployment-scripts
configurar_iis_features.ps1
```

**Opción B: Manual via GUI**
1. Abrir "Activar o desactivar las características de Windows"
2. Habilitar:
   - Internet Information Services
   - Herramientas de administración web
   - Servicios World Wide Web
   - Características de aplicación
   - Desarrollo de aplicaciones (.NET, ISAPI, CGI)

**Opción C: PowerShell Manual**
```powershell
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServer
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CommonHttpFeatures
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpErrors
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpLogging
Enable-WindowsOptionalFeature -Online -FeatureName IIS-RequestFiltering
Enable-WindowsOptionalFeature -Online -FeatureName IIS-StaticContent
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DefaultDocument
Enable-WindowsOptionalFeature -Online -FeatureName IIS-DirectoryBrowsing
```

### 2. Instalar Application Request Routing (ARR)

1. Descargar ARR desde: https://www.iis.net/downloads/microsoft/application-request-routing
2. Ejecutar el instalador como administrador
3. Reiniciar IIS: `iisreset`

### 3. Instalar URL Rewrite Module

1. Descargar desde: https://www.iis.net/downloads/microsoft/url-rewrite
2. Ejecutar instalador como administrador

### 4. Configurar Python

```cmd
# Verificar instalación de Python
python --version

# Si no está instalado, descargar desde python.org
# Asegurarse de marcar "Add Python to PATH" durante la instalación

# Actualizar pip
python -m pip install --upgrade pip
```

---

## 🚀 Instalación Automatizada

### Instalación Completa con Un Solo Comando

```cmd
# 1. Abrir CMD como Administrador

# 2. Navegar al directorio del proyecto
cd C:\ruta\a\dinqr\deployment-scripts

# 3. Ejecutar instalación automatizada
instalar_waitress_iis.bat
```

### ¿Qué hace el Script Automatizado?

1. **Verificación de Prerequisitos**
   - Privilegios de administrador
   - Python instalado y en PATH
   - IIS disponible y configurado
   - ARR instalado

2. **Configuración de Parámetros**
   - Puerto para Waitress (por defecto: 5000)
   - Nombre de dominio (por defecto: dinqr.local)
   - Configuración SSL (opcional)

3. **Instalación de Dependencias**
   - Actualización de pip
   - Instalación de paquetes Python
   - Verificación de Waitress y pywin32

4. **Configuración del Servicio de Windows**
   - Instalación del servicio DINQR
   - Configuración de inicio automático

5. **Configuración de IIS**
   - Creación de Application Pool
   - Configuración del sitio web
   - Copia de web.config
   - Configuración de permisos

6. **Inicio de Servicios**
   - Inicio del servicio DINQR
   - Inicio del sitio IIS
   - Verificación de conectividad

---

## 🔧 Instalación Manual Paso a Paso

### Paso 1: Preparar el Entorno

```cmd
# Navegar al directorio del backend
cd backend

# Instalar dependencias de Python
python -m pip install -r requirements.txt

# Verificar que Waitress se instaló correctamente
python -c "import waitress; print('Waitress version:', waitress.__version__)"
```

### Paso 2: Configurar Variables de Entorno

Editar el archivo `.env` en el directorio `backend`:

```ini
# Configuración de Waitress
WAITRESS_HOST=0.0.0.0
WAITRESS_PORT=5000
WAITRESS_THREADS=4
WAITRESS_CONNECTION_LIMIT=100
WAITRESS_CLEANUP_INTERVAL=30
WAITRESS_CHANNEL_TIMEOUT=120

# Configuración de Flask
FLASK_ENV=production
DEBUG=False
SECRET_KEY=tu_clave_secreta_aqui

# Configuración de Base de Datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/dinqr
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=dinqr
POSTGRES_USER=dinqr_user
POSTGRES_PASSWORD=password_seguro

# Configuración de Logs
LOG_LEVEL=INFO
LOG_DIR=logs
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# Configuración del Servicio de Windows
WINDOWS_SERVICE_NAME=DINQRBackend
WINDOWS_SERVICE_DISPLAY_NAME=DINQR Backend Service
WINDOWS_SERVICE_DESCRIPTION=Servicio de Backend para DINQR con Waitress
```

### Paso 3: Instalar el Servicio de Windows

```cmd
# Instalar el servicio
python windows_service.py install

# Configurar inicio automático
sc config DINQRBackend start= auto

# Iniciar el servicio
python windows_service.py start
```

### Paso 4: Configurar IIS

```cmd
# Crear Application Pool
%windir%\system32\inetsrv\appcmd.exe add apppool /name:"DINQRAppPool" /managedRuntimeVersion:"" /processModel.identityType:ApplicationPoolIdentity

# Crear sitio web
%windir%\system32\inetsrv\appcmd.exe add site /name:"DINQR" /physicalPath:"C:\ruta\a\dinqr\frontend\dist" /bindings:http/*:80:

# Asignar Application Pool
%windir%\system32\inetsrv\appcmd.exe set app "DINQR/" /applicationPool:"DINQRAppPool"

# Copiar web.config
copy web.config C:\ruta\a\dinqr\frontend\dist\web.config

# Iniciar sitio
%windir%\system32\inetsrv\appcmd.exe start site "DINQR"
```

### Paso 5: Configurar SSL (Opcional)

```cmd
# Generar certificado autofirmado para desarrollo
powershell -Command "New-SelfSignedCertificate -DnsName 'dinqr.local' -CertStoreLocation Cert:\LocalMachine\My"

# Configurar binding HTTPS
%windir%\system32\inetsrv\appcmd.exe set site "DINQR" /+bindings.[protocol='https',bindingInformation='*:443:dinqr.local']
```

---

## ⚙️ Configuración Post-Instalación

### 1. Configurar DNS Local (Para Testing)

Editar `C:\Windows\System32\drivers\etc\hosts`:
```
127.0.0.1    dinqr.local
```

### 2. Configurar Firewall

```cmd
# Permitir tráfico HTTP
netsh advfirewall firewall add rule name="DINQR HTTP" dir=in action=allow protocol=TCP localport=80

# Permitir tráfico HTTPS
netsh advfirewall firewall add rule name="DINQR HTTPS" dir=in action=allow protocol=TCP localport=443
```

### 3. Verificar Instalación

```cmd
# Verificar servicio de Windows
sc query DINQRBackend

# Verificar conectividad del backend
curl http://localhost:5000/api/v1/health

# Verificar conectividad via IIS
curl http://localhost/api/v1/health

# Verificar sitio web
curl http://localhost/
```

---

## 🎛️ Gestión del Servicio

### Usar el Script de Gestión

```cmd
# Instalar servicio
servicio_dinqr.bat install

# Iniciar servicio
servicio_dinqr.bat start

# Detener servicio
servicio_dinqr.bat stop

# Reiniciar servicio
servicio_dinqr.bat restart

# Ver estado del servicio
servicio_dinqr.bat status

# Ejecutar en modo debug (consola)
servicio_dinqr.bat debug

# Ver logs del servicio
servicio_dinqr.bat logs

# Remover servicio
servicio_dinqr.bat remove
```

### Comandos Directos de Windows

```cmd
# Iniciar servicio
sc start DINQRBackend

# Detener servicio
sc stop DINQRBackend

# Ver configuración del servicio
sc qc DINQRBackend

# Ver estado del servicio
sc query DINQRBackend
```

---

## 📊 Monitoreo y Mantenimiento

### Monitoreo Básico

```cmd
# Verificación única del estado
monitoreo_waitress.bat

# Monitoreo continuo (cada 30 segundos)
monitoreo_waitress.bat -watch

# Generar reporte detallado
monitoreo_waitress.bat -report
```

### ¿Qué Monitorea el Script?

1. **Servicio de Windows**: Estado y disponibilidad
2. **Servidor Waitress**: Conectividad y tiempo de respuesta
3. **Sitio IIS**: Estado y respuesta HTTP
4. **Base de Datos**: Conectividad y queries básicos
5. **Recursos del Sistema**: CPU, memoria, disco
6. **Logs de Errores**: Análisis de logs recientes

### Ubicación de Logs

```
backend/logs/
├── app.log              # Logs de la aplicación Flask
├── server.log           # Logs del servidor Waitress
├── access.log           # Logs de acceso HTTP
└── gunicorn_error.log   # Logs de errores (si aplica)
```

### Monitoreo en Event Viewer

1. Abrir Event Viewer (`eventvwr.msc`)
2. Navegar a: `Windows Logs > Application`
3. Filtrar por Source: `DINQRBackend`

---

## 💾 Backup y Restauración

### Crear Backups

```cmd
# Backup completo del sistema
backup_waitress.bat create

# Backup solo de configuración
backup_waitress.bat create-config

# Backup solo de base de datos
backup_waitress.bat create-db
```

### Restaurar desde Backup

```cmd
# Listar backups disponibles
backup_waitress.bat list

# Restaurar desde un backup específico
backup_waitress.bat restore "backups\dinqr_full_20240115_1430"

# Verificar integridad de un backup
backup_waitress.bat verify "backups\dinqr_full_20240115_1430.zip"
```

### Programar Backups Automáticos

```cmd
# Configurar backup automático diario
backup_waitress.bat schedule

# Limpiar backups antiguos
backup_waitress.bat cleanup
```

---

## 🔧 Solución de Problemas

### Problemas Comunes y Soluciones

#### 1. Servicio no inicia

**Síntomas**: El servicio DINQR no inicia o se detiene inmediatamente

**Soluciones**:
```cmd
# Ver logs detallados
servicio_dinqr.bat debug

# Verificar configuración
python -c "from app import create_app; app = create_app(); print('Config OK')"

# Reinstalar servicio
servicio_dinqr.bat remove
servicio_dinqr.bat install
```

#### 2. IIS no puede conectar con Waitress

**Síntomas**: Error 502/503 en IIS, backend funciona directamente

**Soluciones**:
```cmd
# Verificar conectividad interna
curl http://localhost:5000/api/v1/health

# Verificar web.config
type frontend\dist\web.config

# Reiniciar IIS
iisreset

# Verificar logs de IIS
type %windir%\system32\LogFiles\W3SVC1\*.log
```

#### 3. Problemas de permisos

**Síntomas**: Errores de acceso a archivos o base de datos

**Soluciones**:
```cmd
# Configurar permisos para logs
icacls "backend\logs" /grant "IIS_IUSRS:(OI)(CI)F" /T

# Configurar permisos para uploads
icacls "backend\uploads" /grant "IIS_IUSRS:(OI)(CI)F" /T

# Verificar permisos del servicio
sc qc DINQRBackend
```

#### 4. Alto uso de recursos

**Síntomas**: CPU o memoria alta

**Soluciones**:
```cmd
# Verificar procesos
tasklist | find "python"

# Ajustar configuración de Waitress en .env
# WAITRESS_THREADS=2
# WAITRESS_CONNECTION_LIMIT=50

# Reiniciar servicio
servicio_dinqr.bat restart
```

#### 5. Base de datos desconectada

**Síntomas**: Errores de conexión a la base de datos

**Soluciones**:
```cmd
# Verificar servicio PostgreSQL
sc query postgresql-x64-12

# Probar conexión manual
python -c "import psycopg2; conn = psycopg2.connect('postgresql://user:pass@localhost/dinqr'); print('DB OK')"

# Verificar configuración en .env
type backend\.env | find "DATABASE_URL"
```

### Herramientas de Diagnóstico

```cmd
# Reporte completo del sistema
monitoreo_waitress.bat -report

# Verificar configuración de red
netstat -an | find ":5000"
netstat -an | find ":80"

# Verificar procesos relacionados
tasklist | find /i "python"
tasklist | find /i "w3wp"

# Verificar servicios
sc query DINQRBackend
sc query W3SVC
```

---

## 🚀 Comandos de Referencia Rápida

### Instalación
```cmd
instalar_waitress_iis.bat              # Instalación completa automatizada
```

### Gestión del Servicio
```cmd
servicio_dinqr.bat install             # Instalar servicio
servicio_dinqr.bat start               # Iniciar servicio
servicio_dinqr.bat stop                # Detener servicio
servicio_dinqr.bat restart             # Reiniciar servicio
servicio_dinqr.bat status              # Estado del servicio
servicio_dinqr.bat debug               # Modo debug
servicio_dinqr.bat logs                # Ver logs
servicio_dinqr.bat remove              # Remover servicio
```

### Monitoreo
```cmd
monitoreo_waitress.bat                 # Verificación única
monitoreo_waitress.bat -watch          # Monitoreo continuo
monitoreo_waitress.bat -report         # Reporte detallado
```

### Backup
```cmd
backup_waitress.bat create             # Backup completo
backup_waitress.bat create-config      # Backup configuración
backup_waitress.bat create-db          # Backup base de datos
backup_waitress.bat list               # Listar backups
backup_waitress.bat restore [archivo]  # Restaurar backup
backup_waitress.bat schedule           # Programar backups
backup_waitress.bat cleanup            # Limpiar backups antiguos
```

### Verificación
```cmd
curl http://localhost:5000/api/v1/health     # Backend directo
curl http://localhost/api/v1/health          # Via IIS
curl http://localhost/                       # Frontend
sc query DINQRBackend                        # Estado del servicio
```

---

## 📞 Soporte y Recursos Adicionales

### Logs Importantes
- **Aplicación**: `backend\logs\app.log`
- **Servidor**: `backend\logs\server.log`
- **IIS**: `%windir%\system32\LogFiles\W3SVC1\`
- **Event Viewer**: Windows Logs > Application (Source: DINQRBackend)

### Archivos de Configuración Clave
- **Aplicación**: `backend\.env`
- **IIS**: `frontend\dist\web.config`
- **Servicio**: `backend\windows_service.py`
- **Servidor**: `backend\waitress_server.py`

### Comandos de Emergencia
```cmd
# Reinicio completo de servicios
servicio_dinqr.bat restart
iisreset

# Verificación rápida de estado
monitoreo_waitress.bat

# Backup de emergencia
backup_waitress.bat create
```

---

## 🎯 Conclusión

La instalación de DINQR con Waitress + IIS proporciona una solución robusta y nativa para Windows Server, optimizada para rendimiento y facilidad de mantenimiento. Con los scripts automatizados proporcionados, la instalación y gestión del sistema se simplifica significativamente.

Para soporte adicional, consulte los logs del sistema y utilice las herramientas de monitoreo proporcionadas para diagnosticar y resolver problemas de manera eficiente.
