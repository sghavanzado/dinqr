# CHECKLIST DE DESPLIEGUE - DINQR

## Proceso Completo: Mac → Windows Server

### FASE 1: PREPARACIÓN EN MAC (Desarrollo)

#### ✅ Configuración del Proyecto
- [ ] Verificar que Redis ha sido deshabilitado en `config.py`
- [ ] Confirmar que `requirements.txt` no incluye Redis
- [ ] Verificar que `.env` usa `RATELIMIT_STORAGE_URL=memory://`
- [ ] Probar que la aplicación funciona sin Redis

#### ✅ Compilación del Backend
- [ ] Ejecutar: `./deployment-scripts/compilar_backend_mac.sh`
- [ ] Verificar que se generó el archivo `.whl` en `dist/`
- [ ] Verificar que se creó `deployment-package.zip`
- [ ] Transferir `deployment-package.zip` a Windows Server

### FASE 2: PREPARACIÓN EN WINDOWS SERVER

#### ✅ Verificación del Sistema
- [ ] Ejecutar como Administrador: `verificar_sistema.bat`
- [ ] Resolver errores críticos mostrados
- [ ] Revisar advertencias importantes
- [ ] Confirmar que el sistema está listo

#### ✅ Instalación de Dependencias
- [ ] Ejecutar: `instalar_dependencias.bat`
- [ ] Verificar instalación de Python 3.8+
- [ ] Verificar instalación de Node.js 16+
- [ ] Verificar instalación de PostgreSQL 12+
- [ ] Configurar IIS con características necesarias

#### ✅ Configuración de Base de Datos
- [ ] Ejecutar: `configurar_postgresql.bat`
- [ ] Crear base de datos `dinqr`
- [ ] Crear usuario de aplicación
- [ ] Verificar conectividad

### FASE 3: DESPLIEGUE DE LA APLICACIÓN

#### ✅ Instalación del Backend
- [ ] Extraer `deployment-package.zip`
- [ ] Ejecutar: `instalar_whl_windows.bat`
- [ ] Configurar archivo `.env` de producción
- [ ] Ejecutar migraciones de base de datos

#### ✅ Compilación del Frontend
- [ ] Ejecutar: `compilar_frontend.bat`
- [ ] Verificar generación de archivos en `dist/`
- [ ] Copiar archivos a directorio de IIS

#### ✅ Configuración de IIS
- [ ] Ejecutar: `configurar_iis_proxy.bat`
- [ ] Configurar Application Pool
- [ ] Configurar sitio web
- [ ] Configurar proxy reverso para API

### FASE 4: PUESTA EN MARCHA

#### ✅ Inicio de Servicios
- [ ] Iniciar servicio Waitress
- [ ] Iniciar servicio PostgreSQL
- [ ] Iniciar sitio en IIS
- [ ] Verificar todos los servicios están corriendo

#### ✅ Verificación Final
- [ ] Ejecutar: `verificacion_final.bat`
- [ ] Probar acceso web a la aplicación
- [ ] Probar login de usuario
- [ ] Probar funciones principales
- [ ] Verificar logs sin errores

### FASE 5: CONFIGURACIÓN POST-DESPLIEGUE

#### ✅ Seguridad
- [ ] Configurar SSL/HTTPS
- [ ] Configurar firewall
- [ ] Configurar backup automático
- [ ] Crear usuario administrador

#### ✅ Monitoreo
- [ ] Configurar logs de aplicación
- [ ] Configurar logs de IIS
- [ ] Configurar alertas de sistema
- [ ] Documentar procedimientos

## ARCHIVOS IMPORTANTES

### Scripts de Compilación
- `compilar_backend_mac.sh` - Compilar en Mac
- `compilar_backend_whl.bat` - Compilar en Windows
- `compilar_frontend.bat` - Compilar frontend
- `compilar_todo.bat` - Compilar todo

### Scripts de Instalación
- `instalar_dependencias.bat` - Instalar software base
- `instalar_whl_windows.bat` - Instalar paquete Python
- `configurar_postgresql.bat` - Configurar base de datos
- `configurar_iis_proxy.bat` - Configurar IIS

### Scripts de Despliegue
- `desplegar_completo.bat` - Despliegue automatizado
- `migrar_base_datos.bat` - Migrar datos
- `verificacion_final.bat` - Verificar instalación

### Scripts de Mantenimiento
- `verificar_sistema.bat` - Verificar estado
- `reiniciar_servicios.bat` - Reiniciar servicios
- `backup_aplicacion.bat` - Backup de aplicación
- `logs_aplicacion.bat` - Ver logs

## CONFIGURACIÓN DE PRODUCCIÓN

### Variables de Entorno Críticas
```env
FLASK_ENV=production
DATABASE_URL=postgresql://dinqr_user:password@localhost:5432/dinqr
SECRET_KEY=clave-super-secreta-para-produccion
RATELIMIT_STORAGE_URL=memory://
```

### Puertos Utilizados
- **5000**: Flask/Waitress (interno)
- **8080**: IIS (externo)
- **5432**: PostgreSQL
- **443**: HTTPS (recomendado)

### Directorios Importantes
- `C:\inetpub\wwwroot\dinqr\` - Frontend
- `C:\Apps\DINQR\` - Backend
- `C:\Apps\DINQR\logs\` - Logs de aplicación
- `C:\Windows\System32\LogFiles\HTTPERR\` - Logs de IIS

## SOLUCIÓN DE PROBLEMAS COMUNES

### Error: "No se puede conectar a la base de datos"
1. Verificar que PostgreSQL está ejecutándose
2. Verificar credenciales en `.env`
3. Verificar conectividad de red
4. Revisar logs de PostgreSQL

### Error: "Aplicación no responde"
1. Verificar que Waitress está ejecutándose
2. Verificar configuración de IIS
3. Revisar logs de aplicación
4. Verificar puertos no están bloqueados

### Error: "Archivos estáticos no cargan"
1. Verificar archivos en directorio IIS
2. Verificar permisos de archivos
3. Verificar configuración de IIS
4. Verificar rutas en configuración

### Error: "Rate limiting no funciona"
1. Verificar configuración sin Redis
2. Verificar `RATELIMIT_STORAGE_URL=memory://`
3. Reiniciar aplicación Waitress

## CONTACTOS DE SOPORTE

- **Desarrollo**: Equipo de desarrollo DINQR
- **Infraestructura**: Administrador de Windows Server
- **Base de Datos**: Administrador de PostgreSQL

## ÚLTIMA ACTUALIZACIÓN

Fecha: $(date)
Versión: 1.0
Responsable: GitHub Copilot Assistant
