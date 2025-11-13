# 🛠️ DINQR - Instalación de Servicio de Windows

## 📋 Métodos Disponibles

### Método 1: Servicio Nativo (Recomendado)
Utiliza el soporte integrado de Windows Services con pywin32.

### Método 2: NSSM (Alternativo)
Utiliza Non-Sucking Service Manager como wrapper.

---

## 🚀 Método 1: Servicio Nativo

### Instalación Automática
```cmd
# Ejecutar como Administrador
instalar_servicio.bat
```

### Instalación Manual
```cmd
# Como Administrador
generadorqr.exe --service install
generadorqr.exe --service start
generadorqr.exe --service status
```

### Comandos Disponibles
```cmd
generadorqr.exe --service install    # Instalar servicio
generadorqr.exe --service remove     # Remover servicio
generadorqr.exe --service start      # Iniciar servicio
generadorqr.exe --service stop       # Detener servicio
generadorqr.exe --service restart    # Reiniciar servicio
generadorqr.exe --service status     # Ver estado
```

---

## 🔧 Método 2: NSSM (Alternativo)

### Prerequisitos
1. Descargar NSSM desde: https://nssm.cc/download
2. Extraer `nssm.exe` al directorio del ejecutable
3. O instalar NSSM en el PATH del sistema

### Instalación con NSSM
```cmd
# Ejecutar como Administrador
instalar_servicio_nssm.bat
```

### Comandos NSSM
```cmd
nssm install DINQRBackend "C:\ruta\generadorqr.exe"
nssm set DINQRBackend AppDirectory "C:\ruta\"
nssm start DINQRBackend
nssm status DINQRBackend
nssm stop DINQRBackend
nssm remove DINQRBackend confirm
```

---

## 🆘 Solución de Problemas

### Error: "pywin32 no está disponible"
**Causa**: El ejecutable no incluye correctamente los módulos pywin32.

**Soluciones**:
1. **Usar NSSM**: Ejecutar `instalar_servicio_nssm.bat`
2. **Modo aplicación**: Ejecutar `generadorqr.exe` sin argumentos de servicio
3. **Recompilar**: Recompilar el ejecutable con PyInstaller

### Error: "Acceso denegado"
**Causa**: Falta de permisos de administrador.

**Solución**: Ejecutar CMD/PowerShell como Administrador.

### Error: "Puerto en uso"
**Causa**: Otro proceso está usando el puerto 5000.

**Soluciones**:
1. Cambiar puerto en `.env`: `PORT=5001`
2. Detener el proceso que usa el puerto: `netstat -ano | findstr :5000`

### Servicio no inicia
**Diagnóstico**:
```cmd
# Ver logs del servicio
type logs\windows_service.log
type logs\app.log

# Ver eventos de Windows
eventvwr.msc  # Buscar DINQRBackend en Application Log
```

---

## 📊 Comparación de Métodos

| Característica | Servicio Nativo | NSSM |
|----------------|------------------|------|
| **Instalación** | Integrada | Requiere NSSM |
| **Rendimiento** | Óptimo | Muy bueno |
| **Logs** | Event Viewer + archivos | Archivos |
| **Gestión** | services.msc + CLI | services.msc + CLI |
| **Dependencias** | pywin32 | NSSM binary |
| **Reinicio automático** | Nativo | Configurable |

---

## 🎯 Recomendaciones

### Para Producción
1. **Intentar primero**: Servicio nativo con `instalar_servicio.bat`
2. **Si falla**: Usar NSSM con `instalar_servicio_nssm.bat`
3. **Backup**: Ejecutar como aplicación normal con `iniciar_servidor.bat`

### Para Desarrollo
- Usar modo aplicación normal: `generadorqr.exe`
- O modo debug: `generadorqr.exe --debug`

### Para Troubleshooting
- Siempre revisar logs en carpeta `logs/`
- Usar Health Check: `http://127.0.0.1:5000/health`
- Verificar configuración en `.env`

---

## 📞 Soporte

### Información de Debug
```cmd
# Estado del servicio
generadorqr.exe --service status
# O con NSSM
nssm status DINQRBackend

# Logs recientes
powershell -Command "Get-Content logs\app.log -Tail 20"

# Test de conectividad
curl http://127.0.0.1:5000/health
```

### Scripts Disponibles
- `instalar_servicio.bat` - Instalación nativa automática
- `instalar_servicio_nssm.bat` - Instalación con NSSM
- `gestionar_servicio.bat` - Gestión interactiva
- `iniciar_servidor.bat` - Modo aplicación normal

---
**Última actualización**: 12 de Agosto 2025  
**Soporte**: Equipo DINQR
