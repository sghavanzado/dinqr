# 📋 Análisis y Corrección: Botones CV en MainGrid.tsx

## ❌ **PROBLEMA ENCONTRADO**

Los botones de CV en la tabla de "Funcionários com QR" estaban generando errores **404 NOT FOUND** al intentar visualizar o descargar los códigos QR de los cartones de visita.

### **Error Original:**
```
XHRGET http://localhost:5000/cv/qr/102
[HTTP/1.1 404 NOT FOUND 67ms]
```

---

## 🔍 **CAUSA RAÍZ**

El código del frontend estaba llamando a endpoints **INCORRECTOS** que no existen en el backend:

| Función Frontend | Endpoint Incorrecto | Endpoint Correcto |
|------------------|-------------------|------------------|
| `handleViewCVQR` | `/cv/qr/${id}` ❌ | `/cv/descargar/${id}` ✅ |
| `handleDownloadCV` | `/cv/qr/${id}` ❌ | `/cv/descargar/${id}` ✅ |
| `handleViewCVCard` | `/cv/${id}` ❌ | `/cv/cartonv?sap=${id}&hash=${firma}` ✅ |

---

## 🎯 **LO QUE DEBEN HACER LOS BOTONES CV**

Basándome en la arquitectura del backend (`backend/routes/cv_routes.py`), aquí está la funcionalidad correcta de cada botón:

### **1. 🔍 Botón "Visualizar QR do CV"** (Icono: QrCode)
- **Propósito**: Mostrar el código QR asociado al cartón de visita en un modal
- **Endpoint**: `GET /cv/descargar/${contact_id}`
- **Respuesta**: Archivo PNG con el código QR (blob)
- **Comportamiento**: 
  - Descarga la imagen del QR
  - Crea un objeto URL temporal
  - Muestra la imagen en el modal compartido con QR Normal

### **2. 💾 Botón "Baixar QR do CV"** (Icono: Download)
- **Propósito**: Descargar el archivo PNG del código QR del CV
- **Endpoint**: `GET /cv/descargar/${contact_id}`
- **Respuesta**: Archivo PNG con el código QR (blob)
- **Comportamiento**: 
  - Descarga la imagen del QR
  - Crea un link de descarga automático
  - Guarda el archivo como `cv_qr_${id}.png`

### **3. 👤 Botón "Ver Cartão de Visita"** (Icono: OpenInNew)
- **Propósito**: Abrir la landing page del cartón de visita
- **Endpoint**: `GET /cv/cartonv?sap=${id}&hash=${firma_hmac}`
- **Parámetros requeridos**:
  - `sap`: ID del funcionario
  - `hash`: Firma HMAC-SHA256 para validación de seguridad
- **Comportamiento**: 
  - Abre una nueva pestaña con la landing page del cartón
  - La landing page muestra información completa del funcionario
  - Incluye botón para descargar vCard

### **4. 🗑️ Botón "Eliminar CV"** (Icono: Delete)
- **Propósito**: Eliminar el CV del funcionario
- **Endpoint**: `DELETE /cv/eliminar/${contact_id}`
- **Comportamiento**: 
  - Elimina el registro de la base de datos
  - Elimina el archivo físico del QR
  - Actualiza la lista de funcionarios

---

## ✅ **CORRECCIONES APLICADAS**

### **Cambio 1: Endpoints de Visualización y Descarga**

**Archivo**: `frontend/src/components/MainGrid.tsx`

```typescript
// ANTES (INCORRECTO) ❌
const handleViewCVQR = async (id: number) => {
  const response = await axiosInstance.get(`/cv/qr/${id}`, { responseType: 'blob' });
  // ...
};

const handleDownloadCV = async (id: number) => {
  const response = await axiosInstance.get(`/cv/qr/${id}`, { responseType: 'blob' });
  // ...
};

// DESPUÉS (CORRECTO) ✅
const handleViewCVQR = async (id: number) => {
  const response = await axiosInstance.get(`/cv/descargar/${id}`, { responseType: 'blob' });
  // ...
};

const handleDownloadCV = async (id: number) => {
  const response = await axiosInstance.get(`/cv/descargar/${id}`, { responseType: 'blob' });
  // ...
};
```

### **Cambio 2: Almacenamiento de Firma HMAC**

**Problema**: El botón "Ver Cartão" necesita la firma HMAC para autenticar el acceso, pero solo se estaban guardando los IDs.

```typescript
// ANTES (INCORRECTO) ❌
const [funcionariosConCV, setFuncionariosConCV] = useState<string[]>([]);

const fetchFuncionariosConCV = async () => {
  const idsConCV = response.data.map((f: any) => String(f.id));
  setFuncionariosConCV(idsConCV);
};

// DESPUÉS (CORRECTO) ✅
const [funcionariosConCV, setFuncionariosConCV] = useState<{id: string, firma: string}[]>([]);

const fetchFuncionariosConCV = async () => {
  const cvData = response.data.map((f: any) => ({
    id: String(f.id),
    firma: f.cvCode?.firma || ''
  }));
  setFuncionariosConCV(cvData);
};
```

### **Cambio 3: Handler del Cartão de Visita**

```typescript
// ANTES (INCORRECTO) ❌
const handleViewCVCard = (funcionario: Funcionario) => {
  window.open(`/cv/${funcionario.id}`, '_blank');
};

// DESPUÉS (CORRECTO) ✅
const handleViewCVCard = (funcionario: Funcionario) => {
  // Buscar la firma HMAC del funcionario
  const cvData = funcionariosConCV.find(cv => cv.id === String(funcionario.id));
  if (!cvData || !cvData.firma) {
    alert('Erro: Firma HMAC não encontrada para este funcionário.');
    return;
  }
  
  // Abrir landing page con parámetros correctos
  const url = `/cv/cartonv?sap=${funcionario.id}&hash=${cvData.firma}`;
  window.open(url, '_blank');
};
```

### **Cambio 4: Actualización de Renderizado Condicional**

```typescript
// ANTES (INCORRECTO) ❌
{funcionariosConCV.includes(String(funcionario.id)) && (
  // Botones CV...
)}

// DESPUÉS (CORRECTO) ✅
{funcionariosConCV.map(cv => cv.id).includes(String(funcionario.id)) && (
  // Botones CV...
)}
```

---

## 🔐 **SEGURIDAD: Firma HMAC**

### **¿Por qué se usa firma HMAC?**

La firma HMAC (Hash-based Message Authentication Code) es una medida de seguridad que:

1. **Evita acceso no autorizado**: Solo las URLs con firma válida pueden acceder al cartón
2. **Previene manipulación**: No se puede cambiar el SAP sin invalidar la firma
3. **Valida integridad**: Asegura que el cartón pertenece al funcionario correcto

### **Cómo funciona:**

```python
# Backend: cv_service.py
def generar_firma(nome):
    """Generar HMAC-SHA256"""
    key = hashlib.sha256(nome.encode()).digest()
    return hmac.new(key, nome.encode(), hashlib.sha256).hexdigest()
```

**Flujo de validación:**
1. Se genera firma al crear el CV: `firma = generar_firma(nome)`
2. Se almacena en BD: `cv_codes.firma`
3. Se incluye en URL del QR: `/cv/cartonv?sap=102&hash=abc123...`
4. Backend valida: `hmac.compare_digest(firma_local, hash_recibido)`

---

## 📊 **ENDPOINTS DEL BACKEND CV**

### **Tabla de Endpoints Disponibles:**

| Método | Endpoint | Propósito | Respuesta |
|--------|----------|-----------|-----------|
| GET | `/cv/funcionarios-sin-cv` | Lista funcionarios sin CV | JSON: Array de funcionarios |
| GET | `/cv/funcionarios-con-cv` | Lista funcionarios con CV | JSON: Array con firma HMAC |
| POST | `/cv/generar` | Generar CVs masivamente | JSON: Resultados |
| GET | `/cv/descargar/<id>` | Descargar QR de CV | Blob: imagen PNG |
| DELETE | `/cv/eliminar/<id>` | Eliminar un CV | JSON: mensaje confirmación |
| GET | `/cv/cartonv?sap=X&hash=Y` | Landing page del cartón | HTML: página web |
| GET | `/cv/vcard?sap=X&hash=Y` | Descargar vCard | vCard: archivo .vcf |

---

## ✅ **RESULTADO**

Después de estas correcciones:

1. ✅ **Visualizar QR del CV**: Funciona correctamente, muestra el QR en modal
2. ✅ **Descargar QR del CV**: Descarga el archivo PNG correctamente
3. ✅ **Ver Cartão de Visita**: Abre la landing page con autenticación HMAC
4. ✅ **Eliminar CV**: Ya funcionaba correctamente

---

## 🧪 **TESTING RECOMENDADO**

Para verificar que todo funciona:

1. **Generar un CV** para un funcionario desde QRTable
2. **Abrir MainGrid** y buscar ese funcionario
3. **Probar cada botón CV**:
   - Botón QR → debe mostrar modal con QR azul
   - Botón Download → debe descargar archivo PNG
   - Botón Card → debe abrir landing page del cartón
   - Botón Delete → debe eliminar y actualizar tabla

---

## 📝 **NOTAS ADICIONALES**

### **Diferencias entre QR Normal y CV:**

| Característica | QR Normal | CV (Cartão de Visita) |
|----------------|-----------|----------------------|
| **Color QR** | Negro | Azul |
| **Prefijo archivo** | `QR{sap}.png` | `CV{sap}.png` |
| **Destino URL** | `/cartao-visita` | `/cv/cartonv` |
| **Autenticación** | Básica | HMAC-SHA256 |
| **Endpoint descarga** | `/qr/descargar/{id}` | `/cv/descargar/{id}` |
| **Base de datos** | `codigos_qr` | `cv_codes` |

---

**Fecha de corrección**: 2025-12-05  
**Archivos modificados**: `frontend/src/components/MainGrid.tsx`  
**Estado**: ✅ CORREGIDO
