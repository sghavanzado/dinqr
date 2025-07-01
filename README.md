# DINQR - Sistema de Generación de Códigos QR

Una aplicación web completa para la generación y gestión de códigos QR, construida con Flask (backend) y React con TypeScript (frontend).

## 📋 Descripción del Proyecto

DINQR es un sistema que permite:
- **Gestión de usuarios** con roles y permisos
- **Generación de códigos QR** personalizados
- **Configuración del servidor** a través de interfaz web
- **Autenticación JWT** con seguridad avanzada
- **API RESTful** documentada con Swagger
- **Interfaz moderna** con Material-UI

## 🏗️ Arquitectura Técnica

### Backend (Flask)
- **Framework**: Flask 3.1.0 con extensiones
- **Base de datos local**: PostgreSQL (para configuración y usuarios)
- **Base de datos remota**: SQL Server (para datos de empleados)
- **Autenticación**: JWT con Flask-JWT-Extended
- **ORM**: SQLAlchemy con Alembic para migraciones
- **Cache**: Redis (opcional)
- **Documentación**: Swagger/Flasgger
- **Servidor**: Gunicorn con supervisión

### Frontend (React + TypeScript)
- **Framework**: React 19.0.0 con TypeScript
- **UI Library**: Material-UI 7.0.2
- **Routing**: React Router DOM 7.5.1
- **Build Tool**: Vite 6.3.1
- **HTTP Client**: Axios 1.8.4

### Estructura de Base de Datos

#### PostgreSQL (Local)
- `users`: Gestión de usuarios del sistema
- `roles`: Roles y permisos
- `settings`: Configuración del sistema
- `qr_codes`: Registro de códigos QR generados
- `audit_log`: Log de auditoría

#### SQL Server (Remoto)
- `sonacard`: Datos de empleados externos

---

## 🚀 Opciones de Despliegue

## Opción 1: IIS con PostgreSQL (Windows Server)

### 📋 Prerrequisitos

1. **Windows Server 2019/2022** o Windows 10/11 Pro
2. **IIS (Internet Information Services)** habilitado
3. **PostgreSQL 14+** instalado
4. **Python 3.10+** instalado
5. **Node.js 18+** y npm instalados
6. **Git** para clonar el repositorio

### 🔧 Instalación de Componentes

#### 1. Habilitar IIS
```powershell
# Ejecutar como Administrador
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole, IIS-WebServer, IIS-CommonHttpFeatures, IIS-HttpErrors, IIS-HttpLogging, IIS-RequestFiltering, IIS-StaticContent, IIS-DefaultDocument, IIS-DirectoryBrowsing, IIS-ASPNET45
```

#### 2. Instalar PostgreSQL
1. Descargar desde https://www.postgresql.org/download/windows/
2. Instalar con configuración por defecto
3. **Puerto**: 5432
4. **Usuario**: postgres
5. **Contraseña**: postgr3s (o la que prefieras)

#### 3. Instalar Python
1. Descargar Python 3.10+ desde https://www.python.org/
2. ✅ Marcar "Add Python to PATH"
3. Instalar pip y virtualenv:
```cmd
python -m pip install --upgrade pip
pip install virtualenv
```

#### 4. Instalar Node.js
1. Descargar desde https://nodejs.org/
2. Instalar con configuración por defecto
3. Verificar instalación:
```cmd
node --version
npm --version
```

### 🗄️ Configuración de Base de Datos

#### 1. Crear Base de Datos PostgreSQL
```sql
-- Conectar como usuario postgres
psql -U postgres

-- Crear base de datos
CREATE DATABASE localdb;

-- Crear usuario (opcional)
CREATE USER dinqr_user WITH PASSWORD 'dinqr_password';
GRANT ALL PRIVILEGES ON DATABASE localdb TO dinqr_user;

-- Salir
\q
```

#### 2. Configurar Variables de Entorno
Crear archivo `.env` en la carpeta `backend/`:
```env
# Base de datos PostgreSQL
DATABASE_URL=postgresql://postgres:postgr3s@localhost:5432/localdb
LOCAL_DB_NAME=localdb
LOCAL_DB_USER=postgres
LOCAL_DB_PASSWORD=postgr3s
LOCAL_DB_HOST=localhost
LOCAL_DB_PORT=5432

# Base de datos SQL Server (remota)
DB_SERVER=192.168.253.5
DB_NAME=empresadb
DB_USERNAME=sa
DB_PASSWORD=Global2020

# Configuración del servidor
HOST=0.0.0.0
PORT=5000
DEBUG=false
FLASK_ENV=production

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://tu-dominio.com

# Redis (opcional)
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### 🛠️ Instalación del Backend

#### 1. Clonar y Configurar Proyecto
```cmd
# Clonar repositorio
git clone <url-del-repositorio> dinqr
cd dinqr\backend

# Crear entorno virtual
python -m virtualenv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. Configurar Base de Datos
```cmd
# Ejecutar migraciones
flask db upgrade

# Crear usuario administrador
python create_admin.py

# Inicializar roles y permisos
python initialize_roles.py
```

#### 3. Probar Backend Localmente
```cmd
# Ejecutar servidor de desarrollo
python app.py
```
Verificar en: http://localhost:5000

### 🎨 Instalación del Frontend

#### 1. Instalar y Compilar
```cmd
cd ..\frontend

# Instalar dependencias
npm install

# Compilar para producción
npm run build
```

### 🌐 Configuración de IIS

#### 1. Crear Sitio Web en IIS
1. Abrir **IIS Manager**
2. Click derecho en **Sites** > **Add Website**
3. **Site name**: DINQR
4. **Physical path**: `C:\inetpub\wwwroot\dinqr`
5. **Port**: 80 (o el que prefieras)

#### 2. Copiar Archivos
```cmd
# Crear directorio
mkdir C:\inetpub\wwwroot\dinqr

# Copiar frontend compilado
xcopy /E /I frontend\dist\* C:\inetpub\wwwroot\dinqr\

# Crear directorio para API
mkdir C:\inetpub\wwwroot\dinqr\api
```

#### 3. Configurar Proxy Reverso para API
Instalar **Application Request Routing (ARR)**:
1. Descargar desde https://www.iis.net/downloads/microsoft/application-request-routing
2. Instalar y reiniciar IIS

Configurar proxy en `web.config`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <rewrite>
            <rules>
                <rule name="ReactRouter" stopProcessing="true">
                    <match url=".*" />
                    <conditions logicalGrouping="MatchAll">
                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
                        <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
                        <add input="{REQUEST_URI}" pattern="^/api" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="/" />
                </rule>
                <rule name="Flask API" stopProcessing="true">
                    <match url="^api/(.*)" />
                    <action type="Rewrite" url="http://localhost:5000/{R:1}" />
                </rule>
            </rules>
        </rewrite>
    </system.webServer>
</configuration>
```

#### 4. Configurar Servicio Windows para Flask
Crear archivo `dinqr_service.py`:
```python
import win32serviceutil
import win32service
import win32event
import subprocess
import os
import sys

class DINQRService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DINQRBackend"
    _svc_display_name_ = "DINQR Backend Service"
    _svc_description_ = "DINQR Flask Backend Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        os.chdir(r'C:\ruta\a\tu\proyecto\backend')
        self.process = subprocess.Popen([
            r'C:\ruta\a\tu\proyecto\backend\venv\Scripts\python.exe',
            'app.py'
        ])
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DINQRService)
```

Instalar servicio:
```cmd
# Instalar pywin32
pip install pywin32

# Instalar servicio
python dinqr_service.py install

# Iniciar servicio
python dinqr_service.py start
```

---

## Opción 2: Servidor XAMPP (Desarrollo)

### 📋 Prerrequisitos

1. **XAMPP** con Apache, MySQL y PHP
2. **Python 3.10+**
3. **Node.js 18+**
4. **PostgreSQL** (recomendado) o **MySQL** (alternativo)

### 🔧 Instalación de XAMPP

#### 1. Descargar e Instalar XAMPP
1. Descargar desde https://www.apachefriends.org/
2. Instalar en `C:\xampp`
3. Iniciar **Apache** y **MySQL** desde el panel de control

#### 2. Configurar PostgreSQL
```bash
# Instalar PostgreSQL
# Seguir los pasos de la Opción 1 para PostgreSQL
```

#### 3. Alternativa: Usar MySQL
Si prefieres usar MySQL en lugar de PostgreSQL:

Crear archivo `.env` para MySQL:
```env
# Base de datos MySQL
DATABASE_URL=mysql+pymysql://root:@localhost:3306/dinqr_db
LOCAL_DB_NAME=dinqr_db
LOCAL_DB_USER=root
LOCAL_DB_PASSWORD=
LOCAL_DB_HOST=localhost
LOCAL_DB_PORT=3306

# Resto de configuración igual que la Opción 1
```

Modificar `requirements.txt` para MySQL:
```txt
# Agregar estas líneas
PyMySQL==1.1.0
cryptography==41.0.7
```

### 🛠️ Configuración del Proyecto

#### 1. Clonar Proyecto
```bash
# Clonar en htdocs de XAMPP
cd C:\xampp\htdocs
git clone <url-del-repositorio> dinqr
cd dinqr
```

#### 2. Configurar Backend
```bash
cd backend

# Crear entorno virtual
python -m virtualenv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate
# O en macOS/Linux
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Para MySQL (si es necesario)
pip install PyMySQL cryptography
```

#### 3. Configurar Base de Datos

**Para PostgreSQL:**
```sql
-- Seguir los pasos de la Opción 1
```

**Para MySQL:**
```sql
-- Conectar a MySQL
mysql -u root -p

-- Crear base de datos
CREATE DATABASE dinqr_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario (opcional)
CREATE USER 'dinqr_user'@'localhost' IDENTIFIED BY 'dinqr_password';
GRANT ALL PRIVILEGES ON dinqr_db.* TO 'dinqr_user'@'localhost';
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

#### 4. Ejecutar Migraciones
```bash
# Migrar base de datos
flask db upgrade

# Crear usuario administrador
python create_admin.py

# Inicializar roles
python initialize_roles.py
```

#### 5. Configurar Frontend
```bash
cd ../frontend

# Instalar dependencias
npm install

# Crear build de producción
npm run build

# Copiar archivos a directorio web
cp -r dist/* ../public/
```

#### 6. Configurar Apache

Crear archivo `.htaccess` en `C:\xampp\htdocs\dinqr\public\`:
```apache
RewriteEngine On

# Manejar rutas de React
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} !^/api
RewriteRule . /index.html [L]

# Proxy para API (requiere mod_proxy)
RewriteCond %{REQUEST_URI} ^/api
RewriteRule ^api/(.*)$ http://localhost:5000/$1 [P,L]
```

### 🚀 Ejecutar Aplicación

#### 1. Iniciar Backend
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

python app.py
```

#### 2. Acceder a la Aplicación
- **Frontend**: http://localhost/dinqr/public
- **API**: http://localhost:5000
- **Documentación API**: http://localhost:5000/apidocs

---

## 🔐 Configuración de Seguridad

### Configuración de Producción

#### 1. Variables de Entorno Seguras
```env
# Generar clave secreta fuerte
FLASK_SECRET_KEY=tu_clave_secreta_muy_fuerte_aqui

# JWT
JWT_SECRET_KEY=otra_clave_secreta_para_jwt

# Configuración HTTPS
ENABLE_HTTPS=true
SESSION_COOKIE_SECURE=true
JWT_COOKIE_SECURE=true

# CORS restringido
CORS_ORIGINS=https://tu-dominio.com
```

#### 2. Configurar HTTPS
Para IIS:
1. Obtener certificado SSL
2. Configurar binding HTTPS en IIS
3. Redirigir HTTP a HTTPS

Para XAMPP:
1. Habilitar mod_ssl en Apache
2. Configurar certificado SSL
3. Actualizar configuración

#### 3. Firewall y Puertos
```bash
# Abrir solo puertos necesarios
# Puerto 80/443 (HTTP/HTTPS)
# Puerto 5432 (PostgreSQL) - solo local
# Puerto 5000 (Flask) - solo local
```

---

## 📊 Monitoreo y Logs

### Ubicación de Logs
```
backend/logs/
├── app.log              # Log principal de la aplicación
├── access.log           # Log de acceso HTTP
├── gunicorn_access.log  # Log de Gunicorn
├── gunicorn_error.log   # Errores de Gunicorn
└── server_manager.log   # Log del administrador de servidor
```

### Configuración de Rotación de Logs
Los logs se rotan automáticamente:
- **Tamaño máximo**: 10 MB por archivo
- **Archivos de backup**: 10
- **Nivel de log**: INFO (configurable)

---

## 🛠️ Mantenimiento

### Comandos Útiles

#### Backend
```bash
# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Crear nueva migración
flask db migrate -m "descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Backup de base de datos
pg_dump -U postgres localdb > backup_$(date +%Y%m%d).sql

# Restaurar backup
psql -U postgres localdb < backup_20250630.sql
```

#### Frontend
```bash
# Actualizar dependencias
npm update

# Lint del código
npm run lint

# Build de producción
npm run build
```

### Monitoreo del Sistema
```bash
# Verificar estado de servicios
systemctl status postgresql  # Linux
sc query postgresql-x64-14   # Windows

# Verificar logs en tiempo real
tail -f backend/logs/app.log

# Verificar uso de recursos
top    # Linux
taskmgr  # Windows
```

---

## 🚨 Resolución de Problemas

### Problemas Comunes

#### 1. Error de Conexión a Base de Datos
```bash
# Verificar estado de PostgreSQL
sudo systemctl status postgresql  # Linux
net start postgresql-x64-14       # Windows

# Verificar conectividad
psql -U postgres -h localhost -p 5432 -d localdb
```

#### 2. Error de Módulos Python
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Verificar entorno virtual
which python  # Debe apuntar al venv
```

#### 3. Error de Permisos en IIS
```powershell
# Dar permisos al directorio
icacls "C:\inetpub\wwwroot\dinqr" /grant "IIS_IUSRS:(OI)(CI)F"
```

#### 4. Error CORS
```env
# Verificar configuración CORS en .env
CORS_ORIGINS=http://localhost:3000,http://tu-dominio.com
```

### Logs de Debug
```bash
# Habilitar debug en .env
DEBUG=true
LOG_LEVEL=DEBUG

# Reiniciar aplicación
```

---

## 📞 Soporte

### Información del Sistema
- **Versión Flask**: 3.1.0
- **Versión React**: 19.0.0
- **Versión Python**: 3.10+
- **Base de datos**: PostgreSQL 14+ / MySQL 8.0+

### Contacto
Para soporte técnico, consultar la documentación de la API en `/apidocs` o revisar los logs del sistema.

---

## 📄 Licencia

[Especificar licencia del proyecto]

---

**Última actualización**: Junio 2025

---

## 🚀 Despliegue Automatizado en Windows Server (RECOMENDADO)

### 📋 Proceso Simplificado

**IMPORTANTE**: Los scripts de automatización ya están incluidos en el proyecto. Simplemente:

1. **Copiar proyecto a Windows Server**:
   ```cmd
   # Copiar toda la carpeta dinqr a C:\dinqr\
   # La estructura debe quedar:
   C:\dinqr\
   ├── backend/
   ├── frontend/ 
   ├── deployment-scripts/    # ← Scripts de automatización
   └── otros archivos...
   ```

2. **Ejecutar instalación automatizada**:
   ```cmd
   # Abrir PowerShell/CMD como Administrador
   cd C:\dinqr\deployment-scripts\
   
   # Opción A: Instalación completa automatizada (RECOMENDADO)
   instalar_completo.bat
   
   # Opción B: Instalación rápida (solo preparar código)
   instalacion_rapida.bat
   ```

3. **Verificar funcionamiento**:
   ```cmd
   # Verificar estado del sistema
   monitoreo_salud.bat
   
   # Ver logs en tiempo real
   logs_aplicacion.bat
   ```

### 🎯 Scripts Disponibles

Los scripts en `deployment-scripts/` automatizan todo el proceso:

- **`instalar_completo.bat`** - Instalación completa automatizada (Python, Node.js, PostgreSQL, IIS, compilación, despliegue)
- **`instalacion_rapida.bat`** - Preparación rápida del código y dependencias básicas
- **`monitoreo_salud.bat`** - Verificación completa del estado del sistema
- **`actualizar.bat`** - Actualización automatizada del sistema
- **`configurar_ssl.ps1`** - Configuración HTTPS/SSL
- **`backup_aplicacion.bat`** - Backup completo del sistema
- **`desinstalar.bat`** - Desinstalación completa

### ⚡ URLs de Acceso Post-Instalación

Después de la instalación automatizada:
- **Frontend**: http://localhost:8080
- **API**: http://localhost:8080/api
- **Documentación**: http://localhost:8080/api/apidocs

### 🔧 Resolución de Problemas Comunes

```cmd
# Si hay errores durante la instalación
monitoreo_salud.bat

# Para reiniciar servicios
reiniciar_servicios.bat

# Para ver logs detallados
logs_aplicacion.bat

# Para generar reporte del sistema
generar_documentacion.bat
```

**⚠️ Nota**: Para instalación manual paso a paso, consulta las secciones siguientes.