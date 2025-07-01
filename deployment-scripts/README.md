# Scripts de Despliegue para DINQR en Windows Server

Esta carpeta contiene todos los scripts necesarios para automatizar el despliegue de la aplicación DINQR en Windows Server con IIS y PostgreSQL.

## 📁 Contenido de Scripts

### 🎯 Scripts Principales
- `instalar_completo.bat` - **INSTALACIÓN AUTOMATIZADA COMPLETA** (Recomendado)
- `desinstalar.bat` - Desinstalación completa del sistema
- `actualizar.bat` - Actualización automatizada del sistema

### 🔧 Scripts de Compilación
- `compilar_backend.bat` - Compila y prepara el backend Flask
- `compilar_frontend.bat` - Compila el frontend React/TypeScript
- `compilar_todo.bat` - Ejecuta ambas compilaciones

### 🚀 Scripts de Despliegue
- `desplegar_iis.bat` - Script principal de despliegue en IIS
- `configurar_iis.ps1` - Configuración automática de IIS (PowerShell)
- `configurar_ssl.ps1` - Configuración SSL/HTTPS para el sitio
- `instalar_dependencias.bat` - Instala todas las dependencias necesarias

### 🗄️ Scripts de Base de Datos
- `configurar_postgresql.bat` - Instala y configura PostgreSQL
- `crear_base_datos.sql` - Script SQL para crear la base de datos
- `migrar_base_datos.bat` - Ejecuta migraciones de base de datos

### 🔐 Scripts de Configuración
- `configurar_ambiente.bat` - Configura variables de entorno

### 🎯 Scripts de Operación y Mantenimiento
- `verificar_sistema.bat` - Verifica prerrequisitos del sistema
- `monitoreo_salud.bat` - Monitoreo completo de salud del sistema
- `reiniciar_servicios.bat` - Reinicia todos los servicios de DINQR
- `backup_aplicacion.bat` - Crea backup de la aplicación
- `logs_aplicacion.bat` - Monitorea logs en tiempo real
- `logs_aplicacion.bat` - Muestra logs en tiempo real

## 🚀 Uso Rápido

## 🚀 Orden de Ejecución Recomendado

### Para Instalación Nueva (RECOMENDADO):
```cmd
# Opción 1: Instalación automatizada completa (Más fácil)
instalar_completo.bat

# Opción 2: Instalación paso a paso (Más control)
verificar_sistema.bat
instalar_dependencias.bat
configurar_postgresql.bat
configurar_ambiente.bat
compilar_todo.bat
migrar_base_datos.bat
desplegar_iis.bat
```

### Para Operaciones Específicas:
```cmd
# Actualizar aplicación existente
actualizar.bat

# Monitoreo de salud
monitoreo_salud.bat

# Reiniciar servicios
reiniciar_servicios.bat

# Configurar HTTPS
configurar_ssl.ps1 -DomainName "mi-servidor.com" -SelfSigned

# Backup del sistema
backup_aplicacion.bat

# Desinstalar completamente
desinstalar.bat
```

### Actualización de Aplicación
```cmd
# Crear backup
backup_aplicacion.bat

# Compilar cambios
compilar_todo.bat

# Desplegar actualización
desplegar_iis.bat
```

## ⚠️ Requisitos Previos
- Windows Server 2019/2022 o Windows 10/11 Pro
- Permisos de Administrador
- PowerShell habilitado
- Conexión a Internet para descargas

## 🔧 Características Principales

### Instalación Automatizada
- **instalar_completo.bat**: Ejecuta todo el proceso de instalación automáticamente
- Verificación de prerrequisitos integrada
- Manejo de errores y rollback automático
- Logging detallado de todo el proceso

### Monitoreo y Mantenimiento
- **monitoreo_salud.bat**: Verifica estado completo del sistema
- Chequeo de servicios, conectividad, recursos y logs
- Reportes de salud con códigos de color
- Recomendaciones automáticas para resolución de problemas

### Gestión de Actualizaciones
- **actualizar.bat**: Actualización automatizada desde repositorio Git
- Backup automático antes de actualizar
- Detección de cambios en dependencias y configuración
- Migración automática de base de datos si es necesaria

### Configuración SSL/HTTPS
- **configurar_ssl.ps1**: Configuración completa de SSL
- Soporte para certificados auto-firmados o existentes
- Configuración automática de redirecciones HTTP→HTTPS
- Configuración de firewall integrada

### Operaciones de Mantenimiento
- **reiniciar_servicios.bat**: Reinicio inteligente de servicios
- **desinstalar.bat**: Desinstalación completa con opciones
- **backup_aplicacion.bat**: Backup completo (código, DB, configuración)
- **logs_aplicacion.bat**: Monitoreo de logs en tiempo real

## 📊 Características Avanzadas

### Logging Inteligente
- Logs separados por operación y fecha
- Códigos de color para fácil identificación
- Backup automático de logs críticos
- Integración con Event Viewer de Windows

### Validaciones de Seguridad
- Verificación de permisos de administrador
- Validación de servicios críticos
- Chequeo de conectividad y puertos
- Verificación de integridad de archivos

### Recuperación de Errores
- Rollback automático en caso de errores críticos
- Backup automático antes de operaciones importantes
- Mensajes de error detallados con sugerencias
- Documentación de troubleshooting integrada

## 🚦 Estados del Sistema

El sistema de monitoreo clasifica la salud en:
- **🎉 EXCELENTE**: Todo funcionando perfectamente
- **⚠️ BUENO**: Funcionando con advertencias menores
- **❌ PROBLEMAS**: Requiere atención inmediata

## 🔐 Configuraciones de Seguridad

### Variables de Entorno Seguras
- Generación automática de claves secretas
- Configuración de CORS apropiada
- Configuración de cookies seguras
- Rate limiting configurado

### Configuración de IIS
- Pool de aplicaciones dedicado
- Configuración de timeouts optimizada
- Compresión y cache configurados
- Headers de seguridad implementados

## 📈 Monitoreo de Performance

### Métricas Incluidas
- Uso de CPU y memoria
- Espacio en disco disponible
- Tiempo de respuesta de aplicación
- Estado de conexiones de base de datos

### Alertas Automáticas
- Advertencias por alto uso de recursos
- Detección de errores en logs
- Verificación de conectividad de servicios
- Alertas de espacio en disco bajo

## 🛠️ Resolución de Problemas

### Comandos de Diagnóstico
```cmd
# Verificación completa del sistema
monitoreo_salud.bat

# Ver logs en tiempo real
logs_aplicacion.bat

# Reiniciar todos los servicios
reiniciar_servicios.bat

# Verificar prerrequisitos
verificar_sistema.bat
```

### Archivos de Log Importantes
- `deployment-logs/` - Logs de despliegue y operaciones
- `backend/logs/` - Logs de aplicación
- `%WINDIR%\System32\LogFiles\W3SVC1\` - Logs de IIS

## 📞 Soporte y Mantenimiento

### Para Problemas Comunes
1. Ejecutar `monitoreo_salud.bat` para diagnóstico
2. Revisar logs específicos de la operación fallida
3. Verificar Event Viewer de Windows
4. Consultar la documentación de troubleshooting en cada script

### Para Actualizaciones
1. Siempre crear backup antes: `backup_aplicacion.bat`
2. Usar script de actualización: `actualizar.bat`
3. Verificar salud post-actualización: `monitoreo_salud.bat`

### Para Restauración
1. Detener servicios: `reiniciar_servicios.bat`
2. Restaurar desde backup
3. Ejecutar verificaciones: `verificar_sistema.bat`

---

**Nota**: Todos los scripts están diseñados para Windows Server y requieren permisos de administrador. Revisa y personaliza las configuraciones según tu entorno específico antes de la ejecución.
