# 🏗️ DINQR Backend - Servicio de Windows

## 📋 Información del Servicio

**Nombre del Servicio**: `DINQRBackend`  
**Nombre para mostrar**: `DINQR Backend Service`  
**Descripción**: `DINQR Flask Backend Service with Waitress`  
**Tipo de inicio**: Automático (se inicia con Windows)  
**Cuenta de ejecución**: LocalSystem  

## 🚀 Instalación como Servicio

### Método 1: Instalación Automática (Recomendado)
1. **Ejecutar como Administrador** el archivo `instalar_servicio.bat`
2. Seguir las instrucciones en pantalla
3. Configurar el archivo `.env` si es necesario
4. El servicio se instalará y opcionalmente se iniciará

### Método 2: Instalación Manual
```cmd
# Abrir PowerShell o CMD como Administrador
# Navegar al directorio del ejecutable
cd "C:\ruta\a\tu\directorio"

# Instalar el servicio
generadorqr.exe --service install

# Iniciar el servicio
generadorqr.exe --service start

# Verificar estado
generadorqr.exe --service status
```

## 🔧 Gestión del Servicio

### Scripts de Gestión
- **`instalar_servicio.bat`** - Instalación automática del servicio
- **`gestionar_servicio.bat`** - Menú interactivo de gestión
- **`iniciar_servidor.bat`** - Ejecutar en modo servidor normal (no servicio)

### Comandos Manuales
```cmd
# Ver estado
generadorqr.exe --service status

# Iniciar servicio
generadorqr.exe --service start

# Detener servicio
generadorqr.exe --service stop

# Reiniciar servicio
generadorqr.exe --service restart

# Remover servicio (requiere admin)
generadorqr.exe --service remove
```

### Administrador de Servicios de Windows
1. Presionar `Win + R` y escribir `services.msc`
2. Buscar "DINQR Backend Service"
3. Click derecho para opciones (Iniciar, Detener, Propiedades, etc.)

## 📊 Monitoreo y Logs

### Archivos de Log
```
logs/
├── windows_service.log    # Log específico del servicio
├── app.log               # Log principal de la aplicación
└── access.log            # Log de accesos HTTP
```

### Verificación de Estado
```cmd
# Health Check HTTP
curl http://127.0.0.1:5000/health

# O abrir en navegador
http://127.0.0.1:5000/health
```

### Event Viewer de Windows
1. Abrir Event Viewer (`eventvwr.msc`)
2. Ir a `Windows Logs > Application`
3. Filtrar por fuente: `DINQRBackend`

## ⚙️ Configuración del Servicio

### Variables de Entorno
El servicio lee la configuración del archivo `.env` en el mismo directorio del ejecutable:

```env
# Configuración obligatoria
DATABASE_URL=postgresql://user:pass@host:port/database
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_key

# Configuración del servidor
HOST=127.0.0.1
PORT=5000
DEBUG=false

# Base de datos SQL Server (opcional)
DB_SERVER=sql_server_host
DB_NAME=database_name
DB_USERNAME=username
DB_PASSWORD=password
```

### Directorio de Trabajo
El servicio utiliza como directorio de trabajo el mismo directorio donde está ubicado `generadorqr.exe`.

## 🔐 Seguridad y Permisos

### Permisos Requeridos
- **Instalación/Remoción**: Permisos de Administrador
- **Inicio/Detención**: Usuario normal (si ya está instalado)
- **Ejecución**: LocalSystem (automático)

### Puertos de Red
- **Puerto principal**: 5000 (configurable en `.env`)
- **Base de datos**: PostgreSQL (5432), SQL Server (1433)

### Firewall
Si es necesario acceso externo, configurar reglas de firewall:
```cmd
# Permitir puerto 5000 (ejecutar como admin)
netsh advfirewall firewall add rule name="DINQR Backend" dir=in action=allow protocol=TCP localport=5000
```

## 🆘 Solución de Problemas

### Problemas Comunes

**Error: "Acceso denegado al instalar"**
- Ejecutar como Administrador
- Verificar permisos UAC

**Error: "No se puede conectar a la base de datos"**
- Verificar configuración en `.env`
- Confirmar que PostgreSQL está ejecutándose
- Revisar logs en `logs/app.log`

**Error: "Puerto en uso"**
- Cambiar puerto en `.env`
- Verificar que no hay otro servicio en el puerto 5000

**Servicio no inicia automáticamente**
- Verificar configuración de inicio automático en services.msc
- Revisar dependencias del servicio

### Comandos de Diagnóstico
```cmd
# Ver servicios en ejecución
sc query DINQRBackend

# Ver configuración del servicio
sc qc DINQRBackend

# Ver logs del sistema
powershell -Command "Get-EventLog -LogName Application -Source DINQRBackend -Newest 10"
```

### Reinstalación Completa
```cmd
# 1. Detener y remover servicio
generadorqr.exe --service stop
generadorqr.exe --service remove

# 2. Limpiar logs (opcional)
rmdir /s logs

# 3. Reinstalar
generadorqr.exe --service install
generadorqr.exe --service start
```

## 🎯 Ventajas del Servicio de Windows

### ✅ Beneficios
- **Inicio automático** con Windows
- **Ejecución en segundo plano** sin interfaz visible
- **Gestión centralizada** desde services.msc
- **Logs integrados** con Event Viewer
- **Reinicio automático** en caso de falla
- **Ejecución con privilegios** de sistema

### 📈 Rendimiento
- **Tiempo de inicio**: 3-7 segundos
- **Memoria base**: ~60-100 MB
- **CPU en reposo**: <1%
- **Disponibilidad**: 24/7

## 📞 Soporte

### Información de Debug
Antes de reportar problemas, recopile:
1. Estado del servicio: `generadorqr.exe --service status`
2. Logs: `logs/windows_service.log` y `logs/app.log`
3. Configuración: contenido de `.env` (sin passwords)
4. Event Viewer: eventos relacionados con DINQRBackend

---
**Documentación actualizada**: 12 de Agosto 2025  
**Versión del servicio**: 1.0.0  
**Soporte**: Equipo DINQR
