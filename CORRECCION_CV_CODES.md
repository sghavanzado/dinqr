# ✅ CORRECCIÓN IMPLEMENTADA - Cartón de Visita

## 🔧 PROBLEMA IDENTIFICADO

El usuario reportó que:
1. La tabla mostraba "Nenhum funcionário sem Cartão de Visita encontrado"
2. La tabla debe llamarse **`cv_codes`** (NO `business_cards`)
3.  Debe ser **exactamente igual** a `qr_codes`
4. Debe consultar `sonacard` de la BD `empresadb`

## ✅ CORRECCIONES APLICADAS

### 1. Tabla Renombrada: `business_cards` → `cv_codes`

**Estructura idéntica a `qr_codes`**:
```sql
CREATE TABLE cv_codes (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    firma VARCHAR(64) NOT NULL,
    archivo_qr VARCHAR(255) NOT NULL
);
```

### 2. Modelo Actualizado

**Archivo**: `backend/models/cv_code.py` (NUEVO)
- Modelo `CVCode` con estructura idéntica a `QRCode`
- `__tablename__ = 'cv_codes'`

### 3. Servicio Actualizado

**Archivo**: `backend/services/cv_service.py` (NUEVO)
- Basado 100% en `qr_service.py`
- Usa `obtener_conexion_remota()` para SQL Server
- Usa `obtener_tabla()` para obtener nombre tabla desde settings
- QR con prefijo `CV-{sap}.png`
- QR color azul (vs negro en QR original)
- Landing page: `/cartonv`

**Diferencias con QR original**:
- Tabla: `cv_codes` (vs `qr_codes`)
- Prefijo archivo: `CV-` (vs sin prefijo)
- Color QR: `blue` (vs `black`)
- URL: `/cartonv` (vs `/contacto`)

### 4. Rutas Actualizadas

**Archivo**: `backend/routes/cv_routes.py` (NUEVO)
- Blueprint `cv_bp` (vs `business_card_bp`)
- Endpoints:
  - `GET /cv/funcionarios-sin-cv`
  - `GET /cv/funcionarios-con-cv`
  - `POST /cv/generar`
  - `GET /cv/descargar/<contact_id>`
  - `DELETE /cv/eliminar/<contact_id>`
  - `GET /cv/cartonv` (landing page)
  - `GET /cv/vcard` (descarga vCard)

**Consulta a sonacard** (líneas 39-48):
```python
query = """
    SELECT TOP 50 sap, nome, funcao, area, nif, telefone, email, unineg
    FROM sonacard
    WHERE sap NOT IN (...)
"""
```

### 5. App.py Actualizado

**Cambios**:
```python
# ANTES
from routes.business_card_routes import business_card_bp
app.register_blueprint(business_card_bp, url_prefix='/api/business-card')

# DESPUÉS
from routes.cv_routes import cv_bp
app.register_blueprint(cv_bp, url_prefix='/cv')
```

### 6. Frontend Actualizado

**Archivo**: `frontend/src/components/BusinessCardTable.tsx`

**Endpoints actualizados**:
```typescript
// ANTES
'/api/business-card/funcionarios-sin-carton'
'/api/business-card/generar'

// DESPUÉS  
'/cv/funcionarios-sin-cv'
'/cv/generar'
```

---

## 📊 NUEVA ESTRUCTURA

```
BASE DE DATOS:
├─ localdb (PostgreSQL)
│  ├─ qr_codes         (QR original)
│  └─ cv_codes         (Cartón de Visita) ✅ NUEVA
│
└─ empresadb (SQL Server)
   └─ sonacard         (Funcionarios)

BACKEND:
├─ models/
│  ├─ qrdata.py        (QRCode)
│  └─ cv_code.py       (CVCode) ✅ NUEVO
├─ services/
│  ├─ qr_service.py
│  └─ cv_service.py    ✅ NUEVO
└─ routes/
   ├─ qr_routes.py
   └─ cv_routes.py     ✅ NUEVO

FRONTEND:
└─ components/
   ├─ QRTable.tsx
   └─ BusinessCardTable.tsx ✅ (endpoints actualizados)
```

---

## 🗂️ ARCHIVOS CREADOS/MODIFICADOS

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `backend/models/cv_code.py` | ✅ NUEVO | Modelo CVCode |
| `backend/services/cv_service.py` | ✅ NUEVO | Servicio CV |
| `backend/routes/cv_routes.py` | ✅ NUEVO | Rutas CV |
| `backend/migrations/create_cv_codes_manual.sql` | ✅ NUEVO | Migración SQL |
| `backend/migrations/versions/create_cv_codes_table.py` | ✅ NUEVO | Migración Flask |
| `backend/update-app.ps1` | ✅ NUEVO | Script actualización |
| `backend/app.py` | 📝 MODIFICADO | Blueprint actualizado |
| `frontend/update-endpoints.ps1` | ✅ NUEVO | Script actualización |
| `frontend/src/components/BusinessCardTable.tsx` | 📝 MODIFICADO | Endpoints actualizados |

---

## 🚀 INSTALACIÓN

### Paso 1: Ejecutar Migración

```bash
cd backend
psql -U postgres -d localdb -f migrations/create_cv_codes_manual.sql
```

### Paso 2: Verificar Tabla

```bash
psql -U postgres -d localdb -c "\d cv_codes"
```

Debe mostrar:
```
Tabla "public.cv_codes"
  Columna    |          Tipo          
-------------+------------------------
 id          | integer               
 contact_id  | character varying(50) 
 nombre      | character varying(100)
 firma       | character varying(64) 
 archivo_qr  | character varying(255)
Índices:
    "cv_codes_pkey" PRIMARY KEY, btree (id)
    "cv_codes_contact_id_key" UNIQUE CONSTRAINT, btree (contact_id)
```

### Paso 3: Reiniciar Backend

```bash
cd backend
python app.py
```

### Paso 4: Probar

1. Ir a http://localhost:5173/
2. Navegar a "Funcionários → Gerar CV"
3. Debería mostrar la tabla con funcionarios de `sonacard`

---

## 🔍 VERIFICACIÓN

### Consulta Manual BD

```sql
-- Ver funcionarios en sonacard
SELECT COUNT(*) FROM empresadb.dbo.sonacard;

-- Ver CVs generados
SELECT COUNT(*) FROM cv_codes;

-- Ver funcionarios SIN CV (debería coincidir con la tabla frontend)
SELECT TOP 50 sap, nome
FROM empresadb.dbo.sonacard
WHERE sap NOT IN (SELECT contact_id FROM cv_codes);
```

---

## 📝 DIFERENCIAS QR vs CV

| Aspecto | QR Original | Cartón de Visita |
|---------|-------------|------------------|
| **Tabla** | `qr_codes` | `cv_codes` |
| **Modelo** | `QRCode` | `CVCode` |
| **Servicio** | `qr_service.py` | `cv_service.py` |
| **Rutas** | `qr_routes.py` | `cv_routes.py` |
| **Blueprint** | `qr_bp` | `cv_bp` |
| **URL Prefix** | `/qr` | `/cv` |
| **Archivo QR** | `{sap}.png` | `CV-{sap}.png` |
| **Color QR** | Negro | Azul |
| **Landing** | `/contacto` | `/cartonv` |
| **Carpeta** | `outputFolder` (settings) | `static/business_cards` |

---

## ✅ RESUMEN

- ✅ Tabla `cv_codes` creada (idéntica a `qr_codes`)
- ✅ Modelo, servicio y rutas basados 100% en QR
- ✅ Consulta a `sonacard` de `empresadb` (vs BD local)
- ✅ Prefijo `CV-` en archivos
- ✅ QR color azul
- ✅ Landing page `/cartonv`
- ✅ Endpoints actualizados en frontend

**El problema de "Nenhum funcionário encontrado" debería estar resuelto.**

---

_Desarrollado por: Ing. Maikel Cuao • 2025-12-02_
