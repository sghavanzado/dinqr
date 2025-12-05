# 🎯 INSTALACIÓN FINAL - Cartón de Visita Corregido

## ✅ CORRECCIONES COMPLETADAS

Se reemplazó completamente la implementación anterior con una nueva **100% basada en el sistema QR existente**:

- ✅ Tabla `cv_codes` (NO `business_cards`)
- ✅ Estructura idéntica a `qr_codes`
- ✅ Consulta a `sonacard` de `empresadb`
- ✅ Basado en `qr_service.py` y `qr_routes.py`

---

## 🚀 PASOS DE INSTALACIÓN

### Paso 1: Crear Tabla `cv_codes`

**Opción A - pgAdmin** (Recomendado):
1. Abrir **pgAdmin**
2. Conectar a `localdb`
3. Click derecho en `Schemas` → `public` → `Query Tool`
4. Pegar el siguiente SQL:

```sql
-- Crear tabla cv_codes
CREATE TABLE IF NOT EXISTS cv_codes (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    firma VARCHAR(64) NOT NULL,
    archivo_qr VARCHAR(255) NOT NULL
);

-- Crear índice
CREATE INDEX IF NOT EXISTS idx_cv_codes_contact_id ON cv_codes(contact_id);

-- Comentarios
COMMENT ON TABLE cv_codes IS 'Almacena información de cartones de visita generados';
COMMENT ON COLUMN cv_codes.contact_id IS 'SAP del funcionario (único)';
COMMENT ON COLUMN cv_codes.nombre IS 'Nombre completo del funcionario';
COMMENT ON COLUMN cv_codes.firma IS 'Firma HMAC-SHA256 para seguridad';
COMMENT ON COLUMN cv_codes.archivo_qr IS 'Ruta del archivo QR generado';
```

5. Ejecutar (F5)
6. Verificar que aparece mensaje "CREATE TABLE"

**Opción B - psql** (Si está en PATH):
```bash
cd backend
psql -U postgres -d localdb -f migrations/create_cv_codes_manual.sql
```

---

### Paso 2: Verificar Tabla Creada

**En pgAdmin**:
1. Expandir `localdb` → `Schemas` → `public` → `Tables`
2. Debería aparecer `cv_codes`
3. Click derecho → `Properties` → Ver columnas

**En Query Tool**:
```sql
\d cv_codes
```

**Debe mostrar**:
```
Tabla "public.cv_codes"
  Columna    |          Tipo          
-------------+------------------------
 id          | integer               
 contact_id  | character varying(50) 
 nombre      | character varying(100)
 firma       | character varying(64) 
 archivo_qr  | character varying(255)
```

---

### Paso 3: Crear Carpeta para QRs

```powershell
cd c:\Users\administrator.GTS\Develop\dinqr\backend
mkdir static\business_cards -Force
```

---

### Paso 4: Reiniciar Backend

```powershell
cd c:\Users\administrator.GTS\Develop\dinqr\backend

# Detener proceso Python existente
taskkill /F /IM python.exe /T

# Esperar 2 segundos
Start-Sleep -Seconds 2

# Iniciar backend
python app.py
```

---

### Paso 5: Acceder a la Aplicación

1. Abrir navegador
2. Ir a: **`http://localhost:5173/`**
3. Login
4. Navegar a: **Funcionários → Gerar CV**
5. Debería mostrar tabla con funcionarios de `sonacard`

---

## 🔍 SOLUCIÓN DE PROBLEMAS

### Problema: "Nenhum funcionário encontrado"

**Verificar**:
1. Tabla `cv_codes` existe en `localdb`
2. Backend está ejecutándose
3. Conexión a `empresadb` funciona

**Consulta de prueba** (en pgAdmin connected to empresadb):
```sql
SELECT TOP 10 sap, nome FROM sonacard;
```

Si retorna datos, la conexión funciona.

### Problema: Error al generar CV

**Verificar**:
1. Carpeta `static/business_cards` existe
2. Backend tiene permisos de escritura
3. Revisar logs del backend

---

## 📊 ARCHIVOS ACTUALIZADOS

| Archivo | Estado | Descripción |
|---------|--------|-------------|
| `backend/models/cv_code.py` | ✅ NUEVO | Modelo CVCode |
| `backend/services/cv_service.py` | ✅ NUEVO | Servicio (basado en qr_service) |
| `backend/routes/cv_routes.py` | ✅ NUEVO | Rutas (basado en qr_routes) |
| `backend/app.py` | 📝 ACTUALIZADO | Nuevo blueprint |
| `backend/migrations/create_cv_codes_manual.sql` | ✅ NUEVO | Migración SQL |
| `frontend/src/components/BusinessCardTable.tsx` | 📝 ACTUALIZADO | Nuevos endpoints |

---

## ✅ VERIFICACIÓN FINAL

### Test 1: Verificar tabla existe
```sql
SELECT COUNT(*) FROM cv_codes;
-- Debe retornar: 0 (inicialmente)
```

### Test 2: Verificar funcionarios disponibles
```sql
SELECT COUNT(*) FROM empresadb.dbo.sonacard;
-- Debe retornar: número > 0
```

### Test 3: Generar un CV

1. En la tabla frontend, seleccionar un funcionario
2. Click "Gerar Selecionados"
3. Esperar mensaje de éxito
4. Verificar archivo creado: `backend/static/business_cards/CV-{sap}.png`
5. Verificar registro en BD:
```sql
SELECT * FROM cv_codes;
```

---

## 🎯 ENDPOINTS API

```
GET  /cv/funcionarios-sin-cv       ← Funcionarios sin CV
GET  /cv/funcionarios-con-cv       ← Funcionarios con CV
POST /cv/generar                   ← Generar CVs
GET  /cv/descargar/<id>            ← Descargar QR
DELETE /cv/eliminar/<id>           ← Eliminar CV
GET  /cv/cartonv?sap=X&hash=Y      ← Landing page
GET  /cv/vcard?sap=X&hash=Y        ← Descargar vCard
```

---

## 📝 COMPARACIÓN QR vs CV

| Aspecto | QR Original | Cartón de Visita |
|---------|-------------|------------------|
| Tabla | `qr_codes` | `cv_codes` |
| Archivo | `{sap}.png` | `CV-{sap}.png` |
| Color | Negro | Azul |
| URL | `/contacto` | `/cartonv` |
| Carpeta | `{outputFolder}` | `static/business_cards` |

---

## ✅ CHECKLIST

- [ ] Tabla `cv_codes` creada en `localdb`
- [ ] Carpeta `static/business_cards` creada
- [ ] Backend reiniciado (con nuevo blueprint)
- [ ] Frontend accesible en http://localhost:5173/
- [ ] Tabla muestra funcionarios de `sonacard`
- [ ] Generación de CV funciona
- [ ] Archivo QR azul creado con prefijo `CV-`
- [ ] Landing page `/cartonv` funciona

---

**¡Listo para usar!** 🎉

_Desarrollado por: Ing. Maikel Cuao • 2025-12-02_
