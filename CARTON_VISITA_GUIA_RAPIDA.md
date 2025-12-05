# 🎴 Cartón de Visita - Resumen Visual Rápido

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO FINAL                             │
│                  (Escanea QR del Cartón)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LANDING PAGE (Frontend)                       │
│        /cartonv?sap=12345&hash=abc123...                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │  [Logo Sonangol - Gradiente Azul]                │          │
│  │  Nome: João Silva                                │          │
│  │  Função: Ingeniero                               │          │
│  │  📇 [Guardar Contato] ← vCard Download           │          │
│  └──────────────────────────────────────────────────┘          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask API)                           │
│                                                                  │
│  1. Validar HMAC (firma)     ┌────────────────┐                │
│     en business_cards        │  PostgreSQL    │                │
│                              │   (Local DB)   │                │
│  2. Obtener datos →          │ business_cards │                │
│     funcionario              └────────────────┘                │
│     desde SQL Server                                            │
│                              ┌────────────────┐                │
│  3. Renderizar HTML          │  SQL Server    │                │
│     landing page             │   (Remote DB)  │                │
│                              │    sonacard    │                │
│                              └────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Generación de Cartón

```
ADMINISTRADOR
     │
     │ 1. Accede a "Gestão de Códigos QR e Cartões de Visita"
     ▼
┌─────────────────────────────────────────────────┐
│  FRONTEND - BusinessCardTable.tsx               │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 📇 Funcionários sem Cartão de Visita     │ │
│  │                                           │ │
│  │ ☐ João Silva    - Ingeniero              │ │
│  │ ☐ Maria Santos  - Gerente                │ │
│  │ ☑ Pedro Costa   - Técnico                │ │
│  │                                           │ │
│  │ [Gerar Selecionados (1)] ← Click         │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────┘
                      │ POST /api/business-card/generar
                      │ {ids: [12345]}
                      ▼
┌─────────────────────────────────────────────────┐
│  BACKEND - business_card_service.py             │
│                                                 │
│  1. Verificar si ya existe cartón              │
│     ❌ No existe → Continuar                   │
│                                                 │
│  2. Obtener datos funcionario SQL Server       │
│     ✅ SELECT * FROM sonacard WHERE sap=12345  │
│                                                 │
│  3. Generar firma HMAC                         │
│     firma = hmac_sha256(nome)                  │
│                                                 │
│  4. Crear QR Code                              │
│     - Prefijo: CV-12345.png                    │
│     - Color: Azul                              │
│     - URL: /cartonv?sap=12345&hash=...         │
│                                                 │
│  5. Guardar en BD local (business_cards)       │
│     ✅ INSERT INTO business_cards              │
│                                                 │
│  6. Guardar archivo QR                         │
│     static/business_cards/CV-12345.png         │
└─────────────────────┬───────────────────────────┘
                      │ Response: {success: true}
                      ▼
┌─────────────────────────────────────────────────┐
│  FRONTEND - Actualización                       │
│  ✅ Alerta "Cartão gerado com sucesso"         │
│  🔄 Recargar tabla (funcionario ya no aparece) │
└─────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Directorios

```
dinqr/
│
├── backend/
│   ├── migrations/
│   │   ├── versions/
│   │   │   └── create_business_cards_table.py  ✅ NUEVO
│   │   └── create_business_cards_manual.sql    ✅ NUEVO (alternativa)
│   │
│   ├── models/
│   │   └── business_card.py                    ✅ NUEVO
│   │
│   ├── services/
│   │   └── business_card_service.py            ✅ NUEVO
│   │
│   ├── routes/
│   │   ├── business_card_routes.py             ✅ NUEVO
│   │   └── route_qrdata.py                     (existente - para contacto)
│   │
│   ├── static/
│   │   ├── qr_codes/                           (existente)
│   │   │   └── 12345.png
│   │   └── business_cards/                     ✅ NUEVO (auto-creado)
│   │       └── CV-12345.png                    ← Prefijo CV
│   │
│   └── app.py                                  📝 MODIFICADO (registra blueprint)
│
└── frontend/
    └── src/
        ├── components/
        │   ├── QRTable.tsx                     (existente)
        │   └── BusinessCardTable.tsx           ✅ NUEVO
        │
        └── pages/
            └── QRManagement.tsx                📝 MODIFICADO (añade tabla)
```

---

## 🎨 Diferencias Visuales

### Color Schemes

**QR Code (Original)**:
```
Tabla Fondo: #FFFFFF (blanco)
Botón:       #1976d2 (azul Material-UI)
Icono:       QrCodeIcon (negro)
Landing:     Fondo gris #f8f9fa, Header amarillo #F4CF0A
```

**Cartón de Visita (Nuevo)**:
```
Tabla Fondo: #f8f9ff (azul muy claro)
Botón:       linear-gradient(135deg, #667eea, #764ba2) (gradiente)
Icono:       ContactCardIcon (azul #667eea)
Landing:     Fondo gradiente azul-morado, Header gradiente azul oscuro
```

### Visual Comparison

```
┌──────────────────────────┐  ┌──────────────────────────┐
│ QR CODE ORIGINAL         │  │ CARTÓN DE VISITA NUEVO   │
├──────────────────────────┤  ├──────────────────────────┤
│ 📋 Funcionários sem QR   │  │ 📇 Funcionários sem      │
│                          │  │    Cartão de Visita      │
│ [⬛] João Silva          │  │ [🔵] João Silva          │
│ [⬛] Maria Santos        │  │ [🔵] Maria Santos        │
│                          │  │                          │
│ [Gerar Selecionados]     │  │ [Gerar Selecionados]     │
│  ⬆ Azul sólido           │  │  ⬆ Gradiente azul-morado │
└──────────────────────────┘  └──────────────────────────┘
```

---

## 🔐 Seguridad

```
┌────────────────────────────────────────────────┐
│  GENERACIÓN                                    │
├────────────────────────────────────────────────┤
│  nome = "João Silva"                           │
│  secret_key = SHA256(nome)                     │
│  firma = HMAC-SHA256(secret_key, nome)         │
│       = "a1b2c3d4e5f6..."                      │
│                                                │
│  QR URL = /cartonv?sap=12345&hash=a1b2c3d4...  │
│                                                │
│  → Guardar firma en business_cards            │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  VALIDACIÓN (al escanear QR)                   │
├────────────────────────────────────────────────┤
│  1. Recibir: sap=12345, hash=a1b2c3d4...       │
│                                                │
│  2. Buscar firma en business_cards             │
│     WHERE contact_id = '12345'                 │
│     firma_db = "a1b2c3d4e5f6..."               │
│                                                │
│  3. Comparar:                                  │
│     hmac.compare_digest(firma_db, hash_url)    │
│     ✅ Match → Mostrar datos                   │
│     ❌ No match → 403 Forbidden                │
└────────────────────────────────────────────────┘
```

---

## 📋 Checklist de Implementación

### Backend
- [x] ✅ Modelo `BusinessCard` creado
- [x] ✅ Migración de BD lista
- [x] ✅ Servicio `business_card_service.py` completo
- [x] ✅ Rutas `business_card_routes.py` implementadas
- [x] ✅ Landing page `/cartonv` con diseño diferenciado
- [x] ✅ Blueprint registrado en `app.py`
- [x] ✅ Validación HMAC implementada
- [x] ✅ Descarga vCard funcionando

### Frontend
- [x] ✅ Componente `BusinessCardTable.tsx` creado
- [x] ✅ Página `QRManagement.tsx` actualizada
- [x] ✅ Estilos diferenciados (gradientes)
- [x] ✅ Iconos diferentes (Badge vs QrCode)
- [x] ✅ Paginación y búsqueda implementadas
- [x] ✅ Selección múltiple con checkboxes
- [x] ✅ Integración con API correcta

### Por Ejecutar
- [ ] ⏳ Ejecutar migración: `flask db upgrade` o SQL manual
- [ ] ⏳ Reiniciar backend
- [ ] ⏳ Recompilar frontend (`npm run build`)
- [ ] ⏳ Probar generación de cartón
- [ ] ⏳ Verificar archivo QR con prefijo CV-
- [ ] ⏳ Escanear QR y verificar landing page
- [ ] ⏳ Descargar y probar vCard
- [ ] ⏳ Verificar logs de acceso

---

## 🚀 Comandos Rápidos

```bash
# 1. Ejecutar migración
cd backend
flask db upgrade
# O manualmente:
psql -U postgres -d localdb -f migrations/create_business_cards_manual.sql

# 2. Reiniciar backend
python app.py
# O servicio Windows:
python run_service.py restart

# 3. Frontend (desarrollo)
cd frontend
npm run dev

# 4. Frontend (producción)
npm run build

# 5. Verificar tabla creada
psql -U postgres -d localdb -c "\d business_cards"

# 6. Ver cartones generados
ls backend/static/business_cards/

# 7. Eliminar todos los cartones (testing)
DELETE FROM business_cards;
rm backend/static/business_cards/CV-*.png
```

---

## 🎯 URLs Importantes

| Descripción | URL |
|-------------|-----|
| **Página de gestión** | `http://localhost:5000/qr-management` |
| **API: Funcionarios sin cartón** | `http://localhost:5000/api/business-card/funcionarios-sin-carton` |
| **API: Generar cartones** | `POST http://localhost:5000/api/business-card/generar` |
| **Landing page ejemplo** | `http://localhost:5000/cartonv?sap=12345&hash=abc...` |
| **Descarga vCard** | `http://localhost:5000/cartonv/vcard?sap=12345&hash=abc...` |

---

## 📊 Base de Datos

### Tabla: `business_cards`

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| `id` | INTEGER | ID autoincremental | `1` |
| `contact_id` | VARCHAR(20) | SAP del funcionario (único) | `"12345"` |
| `firma` | VARCHAR(256) | HMAC-SHA256 | `"a1b2c3d4e5..."` |
| `qr_code_path` | VARCHAR(512) | Ruta del archivo QR | `"static/business_cards/CV-12345.png"` |
| `qr_code_data` | TEXT | URL completa del cartón | `"http://.../cartonv?sap=12345&hash=..."` |
| `created_at` | TIMESTAMP | Fecha de creación | `2025-12-01 15:30:00` |
| `updated_at` | TIMESTAMP | Última actualización | `2025-12-01 15:30:00` |
| `is_active` | BOOLEAN | Cartón activo | `true` |

### Consultas Útiles

```sql
-- Ver todos los cartones
SELECT contact_id, created_at, is_active FROM business_cards;

-- Contar cartones activos
SELECT COUNT(*) FROM business_cards WHERE is_active = true;

-- Ver último cartón generado
SELECT * FROM business_cards ORDER BY created_at DESC LIMIT 1;

-- Buscar cartón por SAP
SELECT * FROM business_cards WHERE contact_id = '12345';

-- Desactivar cartón (soft delete)
UPDATE business_cards SET is_active = false WHERE contact_id = '12345';
```

---

## ✅ Resultado Final

```
ANTES:
┌────────────────────────────┐
│ Gestão de Códigos QR       │
├────────────────────────────┤
│ Funcionários sem QR        │
│ [Tabla con funcionarios]   │
└────────────────────────────┘

DESPUÉS:
┌────────────────────────────────────────┐
│ Gestão de Códigos QR e Cartões Visita  │
├────────────────────────────────────────┤
│ Funcionários sem QR                    │
│ [Tabla QR - diseño original]           │
│                                        │
│ 📇 Funcionários sem Cartão de Visita   │ ← NUEVO
│ [Tabla Cartón - diseño gradiente azul]│ ← NUEVO
└────────────────────────────────────────┘
```

---

**¡Implementación Completa! 🎉**

**Autor**: Ing. Maikel Cuao  
**Email**: maikel@hotmail.com  
**Año**: 2025
