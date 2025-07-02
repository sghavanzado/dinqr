# Scripts de Despliegue para DINQR en Windows Server

Esta carpeta contiene todos los scripts necesarios para automatizar el despliegue de la aplicación DINQR en Windows Server con dos opciones de deployment:

1. **🆕 WAITRESS + IIS** (Recomendado para nuevas instalaciones)
2. **🔧 Gunicorn + IIS** (Para compatibilidad con instalaciones existentes)

## 🚀 Opción 1: Deployment con Waitress + IIS (RECOMENDADO)

### ⭐ Scripts Principales para Waitress
- `instalar_waitress_iis.bat` - **INSTALACIÓN AUTOMATIZADA COMPLETA CON WAITRESS**
- `servicio_dinqr.bat` - **GESTIÓN DEL SERVICIO DE WINDOWS**
- `monitoreo_waitress.bat` - **MONITOREO ESPECÍFICO PARA WAITRESS**
- `backup_waitress.bat` - **BACKUP Y RESTAURACIÓN COMPLETA**

### � Arquitectura Waitress + IIS
```
Cliente ↔ IIS (Puerto 80/443) ↔ Waitress (Puerto 5000) ↔ Flask App
```

**Ventajas del deployment con Waitress:**
- ✅ **Nativo para Windows** - Mejor rendimiento y estabilidad
- ✅ **Servicio de Windows** - Inicio automático y gestión nativa
- ✅ **Sin dependencias externas** - No requiere Gunicorn ni configuraciones complejas
- ✅ **Mejor manejo de memoria** - Optimizado para Windows Server
- ✅ **SSL/TLS nativo** - Soporte completo para HTTPS
- ✅ **Logs estructurados** - Integración con Event Viewer de Windows

## 🔧 Opción 2: Deployment Tradicional (Compatibilidad)

### 🎯 Scripts Principales Tradicionales
- `instalar_completo.bat` - **INSTALACIÓN AUTOMATIZADA COMPLETA** (Gunicorn)
- `desinstalar.bat` - Desinstalación completa del sistema
- `actualizar.bat` - Actualización automatizada del sistema

### 🔧 Scripts de Troubleshooting
- `solucionar_powershell.bat` - **SOLUCIONADOR AUTOMÁTICO** de problemas PowerShell
- `configurar_powershell.ps1` - Configura ExecutionPolicy de PowerShell
- `configurar_iis_features.ps1` - Habilita características de IIS (PowerShell)

### 📋 Configuración Manual de IIS
- `configurar_iis_manual.ps1` - **GUÍA COMPLETA PASO A PASO** para configurar IIS manualmente
- `configurar_iis_dism.bat` - Configuración IIS usando comandos DISM (CMD)
- `comandos_iis_copiar_pegar.txt` - **ARCHIVO DE TEXTO** con comandos para copiar/pegar

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
- `verificacion_final.bat` - **VERIFICACIÓN COMPLETA POST-INSTALACIÓN**
- `monitoreo_salud.bat` - Monitoreo completo de salud del sistema (Gunicorn)
- `reiniciar_servicios.bat` - Reinicia todos los servicios de DINQR
- `backup_aplicacion.bat` - Crea backup de la aplicación (tradicional)
- `logs_aplicacion.bat` - Monitorea logs en tiempo real

## 🚀 Uso Rápido

## 🆕 NUEVO: Instalación con Waitress + IIS (RECOMENDADO)

### Para Nueva Instalación con Waitress:
```cmd
# 1. Instalación automatizada completa (FÁCIL Y RÁPIDO)
instalar_waitress_iis.bat

# 2. Verificar el estado del sistema
monitoreo_waitress.bat

# 3. Configurar backup automático
backup_waitress.bat schedule
```

### Gestión del Servicio DINQR:
```cmd
# Controlar el servicio de Windows
servicio_dinqr.bat install    # Instalar servicio
servicio_dinqr.bat start      # Iniciar servicio
servicio_dinqr.bat stop       # Detener servicio
servicio_dinqr.bat restart    # Reiniciar servicio
servicio_dinqr.bat status     # Ver estado
servicio_dinqr.bat debug      # Ejecutar en modo debug
servicio_dinqr.bat logs       # Ver logs del servicio
```

### Monitoreo y Mantenimiento Waitress:
```cmd
# Monitoreo en tiempo real
monitoreo_waitress.bat -watch

# Reporte detallado del sistema
monitoreo_waitress.bat -report

# Backup completo
backup_waitress.bat create

# Backup solo configuración
backup_waitress.bat create-config

# Listar backups disponibles
backup_waitress.bat list

# Restaurar desde backup
backup_waitress.bat restore [archivo_backup]
```

### Solución de Problemas Waitress:
```cmd
# Diagnóstico completo
solucionador_waitress.bat

# Reparación automática
solucionador_waitress.bat -auto

# Problemas específicos
solucionador_waitress.bat -service     # Solo servicio
solucionador_waitress.bat -iis         # Solo IIS
solucionador_waitress.bat -network     # Solo red
solucionador_waitress.bat -permissions # Solo permisos
```

### Migración de Gunicorn a Waitress:
```cmd
# Verificar compatibilidad antes de migrar
migrar_gunicorn_waitress.bat -check

# Crear backup de seguridad
migrar_gunicorn_waitress.bat -backup

# Ejecutar migración completa
migrar_gunicorn_waitress.bat

# Revertir migración si es necesario
migrar_gunicorn_waitress.bat -rollback
```

## 🔧 Instalación Tradicional (Gunicorn)

### Para Instalación Nueva (Tradicional):
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

# Verificación final (IMPORTANTE)
verificacion_final.bat
```

### Para Operaciones Específicas:
```cmd
# Actualizar aplicación existente
actualizar.bat

# Monitoreo de salud (Gunicorn)
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

## 🔧 Solución de Problemas Comunes

### ❌ Error: "Scripts PowerShell No Pueden Ejecutarse"

**Síntoma**: `configurar_iis.ps1 cannot be loaded because running scripts is disabled`

**Solución RÁPIDA**:
```cmd
# Ejecutar solucionador automático
solucionar_powershell.bat
```

**Soluciones Manuales**:
```powershell
# Método 1: Cambiar ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Método 2: Ejecutar con Bypass
PowerShell -ExecutionPolicy Bypass -File configurar_iis_features.ps1

# Método 3: Desbloquear archivo
Unblock-File -Path "configurar_iis_features.ps1"
```

### ❌ Error: "IIS No Se Instala Correctamente"

**Síntomas**: Error en instalación de características de IIS

**Solución AUTOMÁTICA**:
```cmd
# Verificar prerrequisitos
verificar_sistema.bat

# Instalar dependencias completas
instalar_dependencias.bat
```

**Solución MANUAL**:
```cmd
# Opción 1: Script PowerShell paso a paso
configurar_iis_manual.ps1

# Opción 2: Solo comandos DISM (CMD)
configurar_iis_dism.bat

# Opción 3: Copiar/pegar desde archivo de texto
# Abrir: comandos_iis_copiar_pegar.txt
# Copiar comandos en PowerShell o CMD
```

**Configuración Manual Completa**:
Si los scripts automáticos fallan completamente:
1. Abrir `comandos_iis_copiar_pegar.txt`
2. Copiar sección por sección en PowerShell/CMD
3. Verificar que cada comando se ejecute sin errores
4. Continuar con la siguiente sección
5. Al final ejecutar verificación

### ❌ Error: "Base de Datos No Se Conecta"

**Síntomas**: Error de conexión a PostgreSQL

**Solución**:
```cmd
# Verificar PostgreSQL
configurar_postgresql.bat

# Verificar configuración
verificar_sistema.bat

# Revisar variables de entorno
configurar_ambiente.bat
```

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

## 📊 Comparación de Métodos de Deployment

| Característica | Waitress + IIS (🆕 Recomendado) | Gunicorn + IIS (🔧 Tradicional) |
|---------------|--------------------------------|--------------------------------|
| **Compatibilidad Windows** | ✅ Nativo para Windows | ⚠️ Originalmente para Linux |
| **Rendimiento** | ✅ Optimizado para Windows | ⚠️ Bueno, pero no optimizado |
| **Facilidad de instalación** | ✅ 1 comando: `instalar_waitress_iis.bat` | ⚠️ Múltiples pasos manuales |
| **Servicio de Windows** | ✅ Integración nativa completa | ⚠️ Requiere configuración adicional |
| **Mantenimiento** | ✅ Scripts especializados incluidos | ⚠️ Herramientas genéricas |
| **Logs** | ✅ Event Viewer + archivos | ✅ Solo archivos |
| **Monitoreo** | ✅ `monitoreo_waitress.bat` | ✅ `monitoreo_salud.bat` |
| **Backup/Restore** | ✅ `backup_waitress.bat` completo | ✅ `backup_aplicacion.bat` básico |
| **Solución de problemas** | ✅ `solucionador_waitress.bat` | ⚠️ Manual |
| **Migración** | ✅ `migrar_gunicorn_waitress.bat` | N/A |
| **Memoria utilizada** | ✅ Menor uso de memoria | ⚠️ Mayor uso de memoria |
| **Estabilidad Windows** | ✅ Muy estable | ⚠️ Puede tener problemas ocasionales |
| **SSL/HTTPS** | ✅ Soporte nativo completo | ✅ Soporte funcional |
| **Escalabilidad** | ✅ Excelente en Windows | ✅ Buena |

## 🎯 Recomendaciones de Uso

### ✅ Usar Waitress + IIS cuando:
- **Nueva instalación** en Windows Server
- Se requiere **máximo rendimiento** en Windows
- Se necesita **integración nativa** con Windows Services
- Se busca **facilidad de mantenimiento** a largo plazo
- Equipo de IT prefiere **herramientas nativas de Windows**
- Se requiere **monitoreo avanzado** con Event Viewer
- Se necesita **recuperación automática** ante fallos

### ⚠️ Mantener Gunicorn + IIS cuando:
- **Instalación existente** funcionando correctamente
- Equipo familiarizado con el **setup actual**
- **Restricciones de tiempo** para migración
- Aplicación tiene **dependencias específicas** de Gunicorn
- **Ambiente híbrido** (Linux + Windows) donde se requiere consistencia

### 🔄 Migrar de Gunicorn a Waitress cuando:
- Se experimenten **problemas de estabilidad** con Gunicorn
- Se requiera **mejor rendimiento** en Windows
- Se necesiten **herramientas de monitoreo avanzadas**
- Se busque **simplificar el mantenimiento**
- Se planee **escalamiento** futuro
