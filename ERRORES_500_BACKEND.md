# ⚠️ ERRORES 500 - BACKEND CRASHEADO

## ❌ PROBLEMA ACTUAL

Todos los endpoints del backend devuelven error 500:
- `/qr/funcionarios` → 500
- `/cv/funcionarios-con-cv` → 500  
- `/qr/funcionarios/total` → 500
- `/cv/generar` → 500

**Causa probable**: Cambios en `qr_routes.py` causaron error de sintaxis SQL.

---

## ✅ SOLUCIÓN INMEDIATA

### **Opción 1: Revertir Cambios (MÁS RÁPIDO)**

Si aplicaste cambios en `backend/routes/qr_routes.py` línea 47, **reviértelos**:

**Cambiar de**:
```python
cursor.execute("""
    SELECT contact_id FROM qr_codes
    UNION
    SELECT contact_id FROM cv_codes
""")
```

**A** (original):
```python
cursor.execute("SELECT contact_id FROM qr_codes")
```

Luego reinicia el backend.

---

### **Opción 2: Ver Logs del Backend**

Para identificar el error exacto, necesitamos ver los logs:

1. Ve al terminal donde está corriendo el backend
2. Busca el traceback del error (líneas rojas)
3. Copia el error completo

---

## 🔧 DIAGNÓSTICO

### **Paso 1: Verifica si el servidor está corriendo**

En PowerShell:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET
```

Si da error de conexión → El servidor NO está corriendo.  
Si da 500 → El servidor está corriendo pero con errores.

### **Paso 2: Reinicia el servidor**

1. Detén el servidor: `Ctrl+C` en el terminal del backend
2. Activa el entorno virtual:
   ```powershell
   .\apiqr\Scripts\Activate.ps1
   ```
3. Inicia el servidor:
   ```powershell
   cd backend
   python app.py
   ```
4. Observa los logs - **copia cualquier error que aparezca**

---

## 🎯 SOLUCIÓN DEFINITIVA (Una vez funcione de nuevo)

Para corregir el problema original (funcionarios con solo CV no aparecen), necesitamos:

### **Archivo**: `backend/routes/qr_routes.py`
### **Línea**: ~47
### **Cambio**:

```python
# ANTES (solo QR Normal)
cursor.execute("SELECT contact_id FROM qr_codes")

# DESPUÉS (QR Normal Y CV)
cursor.execute("""
    SELECT contact_id FROM qr_codes
    UNION
    SELECT contact_id FROM cv_codes
""")
```

**IMPORTANTE**: Este cambio DEBE hacerse cuando el servidor esté funcionando normalmente.

---

## 📋 CHECKLIST DE RECUPERACIÓN

- [ ] Backend está corriendo (no hay errores de conexión)
- [ ] No hay errores 500 en los endpoints básicos
- [ ] `/qr/funcionarios` devuelve datos
- [ ] `/cv/funcionarios-con-cv` devolve datos
- [ ] Tabla del Dashboard carga funcionarios

---

## 🆘 SI NADA FUNCIONA

**Guarda todos los cambios de código** y:

1. Detén todo
2. Revisa que NO hayas modificado `qr_routes.py`  
3. Reinicia el backend
4. Prueba endpoints básicos

---

**Por favor, envía los logs del backend o confirma si el servidor está corriendo.** 🔍

_Ing. Maikel Cuao • 2025-12-03_
