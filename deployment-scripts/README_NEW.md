# Scripts de Despliegue DINQR

Este directorio contiene todos los scripts necesarios para el despliegue completo de la aplicación DINQR desde Mac (desarrollo) a Windows Server con IIS + Waitress.

## 🎯 INICIO RÁPIDO

### Para Mac (Desarrollo)
```bash
# Compilar backend para Windows
./compilar_backend_mac.sh
# Resultado: deployment-package.zip listo para transferir
```

### Para Windows Server (Producción)
```cmd
# 1. Verificar sistema
verificar_sistema.bat

# 2. Instalación completa automatizada
desplegar_completo.bat

# 3. Verificación final
verificacion_final.bat
```

## 📁 ESTRUCTURA DE ARCHIVOS

### 🔧 Scripts de Verificación
- `verificar_sistema.bat` - **Verificación completa del sistema**
- `verificacion_final.bat` - Verificación post-instalación

### 🏗️ Scripts de Compilación
- `compilar_backend_mac.sh` - **Compilar en Mac (PRINCIPAL)**
- `compilar_backend.bat` - Compilar en Windows
- `compilar_backend_whl.bat` - Compilar a paquete .whl
- `compilar_frontend.bat` - Compilar frontend React
- `compilar_todo.bat` - Compilación completa

### ⚙️ Scripts de Instalación
- `instalar_dependencias.bat` - Instalar software base (Python, Node.js, etc.)
- `instalar_whl_windows.bat` - **Instalar paquete .whl generado en Mac**
- `instalar_completo.bat` - Instalación completa automatizada
- `instalacion_rapida.bat` - Instalación express

### 🚀 Scripts de Despliegue
- `desplegar_completo.bat` - **Despliegue automatizado completo**
- `desplegar_iis.bat` - Despliegue solo en IIS
- `migrar_base_datos.bat` - Migrar base de datos

### 🔧 Scripts de Configuración
- `configurar_ambiente.bat` - Configuración inicial del ambiente
- `configurar_postgresql.bat` - Configuración de PostgreSQL
- `configurar_iis_proxy.bat` - **Configurar IIS como proxy reverso**
- `configurar_iis.ps1` - Configuración avanzada de IIS
- `configurar_ssl.ps1` - Configuración de SSL/HTTPS
- `configurar_powershell.ps1` - Configurar PowerShell para scripts

### 🔄 Scripts de Mantenimiento
- `reiniciar_servicios.bat` - Reiniciar todos los servicios
- `backup_aplicacion.bat` - Backup completo de la aplicación
- `backup_waitress.bat` - Backup específico de Waitress
- `logs_aplicacion.bat` - Ver logs de aplicación
- `monitoreo_waitress.bat` - Monitoreo de Waitress
- `monitoreo_salud.bat` - Monitoreo de salud general

### 🛠️ Scripts de Solución de Problemas
- `solucionador_waitress.bat` - Solucionar problemas de Waitress
- `solucionar_powershell.bat` - Solucionar problemas de PowerShell
- `migrar_gunicorn_waitress.bat` - Migrar de Gunicorn a Waitress

### 📋 Scripts de Servicios
- `servicio_dinqr.bat` - Gestión del servicio DINQR
- `instalar_waitress_iis.bat` - Configurar Waitress con IIS

## 📚 DOCUMENTACIÓN

### Documentos Principales
- `GUIA_DESPLIEGUE_WINDOWS.md` - **Guía completa de despliegue**
- `GUIA_WAITRESS_IIS.md` - Guía específica de Waitress + IIS
- `CHECKLIST_DESPLIEGUE.md` - **Checklist paso a paso**

### Archivos de Configuración
- `env-production-template` - Plantilla de variables de entorno
- `crear_base_datos.sql` - Script SQL para crear BD
- `comandos_iis_copiar_pegar.txt` - Comandos IIS útiles

## 🚦 PROCESO COMPLETO

### FASE 1: Mac (Desarrollo)
1. **Compilar**: `./compilar_backend_mac.sh`
2. **Transferir**: `deployment-package.zip` → Windows Server

### FASE 2: Windows Server (Preparación)
1. **Verificar**: `verificar_sistema.bat`
2. **Instalar**: `instalar_dependencias.bat`
3. **Configurar**: `configurar_postgresql.bat`

### FASE 3: Windows Server (Despliegue)
1. **Extraer**: `deployment-package.zip`
2. **Instalar**: `instalar_whl_windows.bat`
3. **Desplegar**: `desplegar_completo.bat`
4. **Verificar**: `verificacion_final.bat`

## ⚡ COMANDOS ESENCIALES

```cmd
# Verificación inicial
verificar_sistema.bat

# Instalación desde cero
instalar_completo.bat

# Despliegue automatizado
desplegar_completo.bat

# Reiniciar todo
reiniciar_servicios.bat

# Ver logs
logs_aplicacion.bat

# Backup
backup_aplicacion.bat
```

## 🔧 CONFIGURACIÓN CLAVE

### Sin Redis (Solo Memoria)
- Rate limiting configurado para usar solo memoria
- No requiere instalación de Redis
- Configuración en `config.py` y `.env`

### Puertos
- **5000**: Waitress (interno)
- **8080**: IIS (externo)
- **5432**: PostgreSQL

### Directorios
- `C:\Apps\DINQR\` - Aplicación backend
- `C:\inetpub\wwwroot\dinqr\` - Frontend
- `C:\Apps\DINQR\logs\` - Logs

## 🆘 SOLUCIÓN RÁPIDA DE PROBLEMAS

```cmd
# Problema: Servicio no inicia
solucionador_waitress.bat

# Problema: Base de datos
configurar_postgresql.bat

# Problema: IIS
configurar_iis_proxy.bat

# Problema: PowerShell
solucionar_powershell.bat

# Verificar todo
verificar_sistema.bat
```

## 📞 SOPORTE

### Archivos de Log
- `C:\Apps\DINQR\logs\` - Logs de aplicación
- `%SystemRoot%\System32\LogFiles\HTTPERR\` - Logs de IIS

### Comandos de Diagnóstico
```cmd
# Estado de servicios
sc query | findstr dinqr

# Puertos en uso
netstat -an | findstr "5000\|8080\|5432"

# Procesos Python
tasklist | findstr python
```

## 🔄 ACTUALIZACIONES

Para actualizar la aplicación:
1. Compilar nueva versión en Mac
2. Transferir `deployment-package.zip`
3. Ejecutar `actualizar.bat`
4. Verificar con `verificacion_final.bat`

## ⚠️ REQUISITOS

### Sistema
- Windows Server 2016+ / Windows 10+
- RAM: 4GB mínimo, 8GB recomendado
- Espacio: 10GB libres mínimo

### Software
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- IIS con URL Rewrite Module

### Permisos
- **Administrador** requerido para instalación
- Acceso a internet para descargas
- Permisos de escritura en `C:\Apps\` y `C:\inetpub\`

---

**Última Actualización**: Diciembre 2024  
**Versión**: 2.0  
**Estado**: ✅ Producción Ready
