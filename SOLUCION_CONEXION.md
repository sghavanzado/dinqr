# 🔧 SOLUCIÓN - Conexión Rechazada

## ❌ PROBLEMA

El error `ERR_CONNECTION_REFUSED` en `https://192.168.253.5` indica que:
- El servidor backend Flask está corriendo en `localhost:5000`
- Pero NO está corriendo en la IP `192.168.253.5`

---

## ✅ SOLUCIÓN

### **Opción 1: Usar Localhost (Rápida)**

Cambia la URL a:
```
http://localhost:5000/cv/cartonv?sap=107&hash=ef33da9f921cab6859c87a87a96b61863df18f398fb9d1e24d2fcd7727860bda
```

**Nota**: Usa `http://` no `https://`

---

### **Opción 2: Iniciar Servidor de Producción (Waitress)**

Si necesitas usar `https://192.168.253.5`, debes iniciar el servidor de producción:

#### **Paso 1: Detener el servidor actual**
Presiona `Ctrl+C` en la terminal donde está corriendo Flask

#### **Paso 2: Iniciar Waitress**
```powershell
cd C:\Users\administrator.GTS\Develop\dinqr\backend
.\apiqr\Scripts\Activate.ps1
python waitress_server.py
```

---

### **Opción 3: Configurar IIS**

Si tienes IIS configurado, verifica que:
1. El servicio esté corriendo
2. El reverse proxy apunte a `localhost:5000`
3. Los certificados SSL estén configurados

---

## 🧪 URLS DE PRUEBA

### **Localhost (HTTP)**:
```
http://localhost:5000/cv/cartonv?sap=107&hash=ef33da9f921cab6859c87a87a96b61863df18f398fb9d1e24d2fcd7727860bda
```

### **Localhost (HTTPS)** - Si Waitress está corriendo:
```
https://localhost/cv/cartonv?sap=107&hash=ef33da9f921cab6859c87a87a96b61863df18f398fb9d1e24d2fcd7727860bda
```

### **IP Externa (HTTPS)** - Si IIS/Waitress está corriendo:
```
https://192.168.253.5/cv/cartonv?sap=107&hash=ef33da9f921cab6859c87a87a96b61863df18f398fb9d1e24d2fcd7727860bda
```

---

## ⚡ PRUEBA RÁPIDA

**Abre esta URL ahora** (debería funcionar):
```
http://localhost:5000/cv/cartonv?sap=107&hash=ef33da9f921cab6859c87a87a96b61863df18f398fb9d1e24d2fcd7727860bda
```

Si funciona, verás el cartón de visita con el diseño de Sonangol.

---

## 📊 ESTADO ACTUAL

| Servidor | Estado | Puerto | URL |
|----------|--------|--------|-----|
| Flask Dev | ✅ RUNNING | 5000 | http://localhost:5000 |
| Waitress | ❌ NO RUNNING | - | - |
| IIS | ❓ DESCONOCIDO | 443 | https://192.168.253.5 |

---

## 🎯 RECOMENDACIÓN

Para desarrollo, usa:
```
http://localhost:5000
```

Para producción/QR codes, necesitas iniciar Waitress o IIS.

_Ing. Maikel Cuao • 2025-12-03_
