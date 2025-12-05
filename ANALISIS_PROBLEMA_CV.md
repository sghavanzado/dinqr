# 🔍 ANÁLISIS COMPLETO - Problema Dashboard CV

## ✅ DIAGNÓSTICO REALIZADO

### **Base de Datos**
```
QR normales (qr_codes): 7 registros
CVs generados (cv_codes): 7 registros
Total único (UNION): 8 registros
```

**Funcionarios en cada tabla**:

**qr_codes (QR Normal)**:
- SAP 107: Andre Cabaia Eduardo
- SAP 102: Helder Rangel Leite
- SAP 106: Nauria de Fatima Cordeiro Escorcio
- SAP 109: Claudia Patricia Sequeira de Andrade
- SAP 13: Jose Joao Gaspar
- SAP 111: Elizangela Patricia Silvestre Paulino
- SAP 11: Ndemofiapo Nasser Augusto

**cv_codes (CV)**:
- SAP 107: Andre Cabaia Eduardo
- SAP 102: Helder Rangel Leite
- SAP 109: Claudia Patricia Sequeira de Andrade
- SAP 106: Nauria de Fatima Cordeiro Escorcio
- **SAP 128: Antonio Andre Chivanga Barros** ← SOLO CV
- SAP 13: Jose Joao Gaspar
- SAP 111: Elizangela Patricia Silvestre Paulino

### **UNION Results**:
```sql
SELECT contact_id FROM qr_codes
UNION
SELECT contact_id FROM cv_codes
```
**Devuelve 8 IDs**: ['13', '109', '102', '11', '111', '128', '107', '106']

---

## 🎯 CASO DE PRUEBA: SAP 128

**Antonio Andre Chivanga Barros (SAP 128)**:
- ❌ NO tiene QR Normal (no está en qr_codes)
- ✅ SÍ tiene CV (está en cv_codes)

**Resultado esperado**: DEBE aparecer en Dashboard porque tiene CV

---

## 🔧 CÓDIGO MODIFICADO (CORRECTO)

### **Archivo**: `backend/routes/qr_routes.py`

**Función `listar_funcionarios()` - Líneas 47-52**:
```python
# UNION de ambas tablas: qr_codes (QR Normal) y cv_codes (CV)
cursor.execute("""
    SELECT contact_id FROM qr_codes
    UNION
    SELECT contact_id FROM cv_codes
""")
qr_generated_ids = [row[0] for row in cursor.fetchall()]
logging.info(f"IDs de funcionarios con QR o CV obtenidos: {qr_generated_ids}")
```

**Función `listar_funcionarios_com_qr()` - Líneas 277-282**:
```python
# UNION de ambas tablas: qr_codes (QR Normal) y cv_codes (CV)
cursor.execute("""
    SELECT contact_id FROM qr_codes
    UNION
    SELECT contact_id FROM cv_codes
""")
qr_generated_ids = [row[0] for row in cursor.fetchall()]
logging.info(f"IDs de funcionarios con QR o CV obtenidos: {qr_generated_ids}")
```

---

## 🧪 FLUJO CUANDO GENERAS UN CV

### **1. Frontend: Click en "Gerar Cartão de Visita"**
```typescript
// BusinessCardTable.tsx - handleGenerateBusinessCard()
const response = await axiosInstance.post('/cv/generar', {
  ids: selectedIds
});
```

### **2. Backend: Endpoint /cv/generar**
```python
# cv_routes.py línea 131
@cv_bp.route('/generar', methods=['POST'])
def generar_cvs():
    data = request.get_json()
    ids = data.get('ids', [])
    resultados = generar_cv(ids)  # ← Llama al servicio
```

### **3. Servicio: generar_cv()**
```python
# cv_service.py línea 129-136
cursor.execute("""
    INSERT INTO cv_codes (contact_id, nombre, firma, archivo_qr)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (contact_id) DO UPDATE SET
    nombre = EXCLUDED.nombre,
    firma = EXCLUDED.firma,
    archivo_qr = EXCLUDED.archivo_qr
""", (sap, nome, firma, archivo_qr))
conn.commit()
```

**Resultado**: ✅ Registro insertado/actualizado en tabla `cv_codes`

### **4. Frontend: Dashboard carga funcionarios**
```typescript
// MainGrid.tsx - fetchFuncionarios()
const response = await axiosInstance.get('/qr/funcionarios', {
  params: { page, per_page: 10, filtro: '' }
});
```

### **5. Backend: Endpoint /qr/funcionarios**
```python
# qr_routes.py línea 47-52
cursor.execute("""
    SELECT contact_id FROM qr_codes
    UNION
    SELECT contact_id FROM cv_codes
""")
qr_generated_ids = [row[0] for row in cursor.fetchall()]
```

**Resultado esperado**: ✅ Devuelve lista con SAP 128 incluido

---

## ❌ POSIBLES PROBLEMAS

### **1. Backend no reiniciado después del cambio**
**Síntoma**: Cambios en código no se aplican  
**Solución**: ✅ Backend YA fue reiniciado (proceso actual)

### **2. Frontend cacheado**
**Síntoma**: Frontend usa código antiguo  
**Solución**: Refrescar navegador con Ctrl + Shift + R

### **3. Datos no actualizados en MainGrid**
**Síntoma**: `funcionariosConCV` no tiene SAP 128  
**Causa**: Endpoint `/cv/funcionarios-con-cv` también necesita UNION  

---

## 🔍 VERIFICACIÓN ADICIONAL NECESARIA

Voy a revisar el endpoint `/cv/funcionarios-con-cv` que también se usa en MainGrid:

**Archivo**: `backend/routes/cv_routes.py`

Buscar función `listar_funcionarios_com_cv()` y verificar si usa UNION o solo cv_codes.

---

## ✅ CONCLUSIÓN DEL ANÁLISIS

### **Lo que está BIEN**:
1. ✅ Tabla cv_codes existe y tiene datos
2. ✅ SAP 128 está en cv_codes (solo CV, sin QR normal)
3. ✅ Consulta UNION funciona en base de datos
4. ✅ Código modificado correctamente en `qr_routes.py`
5. ✅ Backend reiniciado con cambios

### **Lo que FALTA verificar**:
1. ⏳ Endpoint `/cv/funcionarios-con-cv` (usado por `fetchFuncionariosConCV`)
2. ⏳ Logs del backend cuando Dashboard carga

---

## 🚀 PRÓXIMOS PASOS

1. Verificar endpoint `/cv/funcionarios-con-cv`
2. Ver logs del backend durante carga de Dashboard
3. Confirmar que frontend está refrescado
4. Probar crear nuevo CV para funcionario sin QR

---

_Diagnóstico ejecutado: 2025-12-04 10:17_
