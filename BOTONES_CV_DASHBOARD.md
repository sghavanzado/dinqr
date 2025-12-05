# ✅ BOTONES CV AGREGADOS AL DASHBOARD

## 🎉 IMPLEMENTACIÓN COMPLETADA

**Fecha**: 2025-12-02  
**Archivo**: `frontend/src/components/MainGrid.tsx`

---

## 📊 CAMBIOS REALIZADOS

### 1. **Nuevos Estados**
```typescript
const [funcionariosConCV, setFuncionariosConCV] = useState<number[]>([]);
const [cvModalOpen, setCvModalOpen] = useState(false);
const [cvImage, setCvImage] = useState('');
```

### 2. **Nueva Función de Consulta**
```typescript
const fetchFuncionariosConCV = async () => {
  // Consulta /cv/funcionarios-con-cv
  // Guarda IDs de funcionarios con CV
}
```

### 3. **4 Nuevos Handlers**

#### a) Visualizar QR del CV
```typescript
handleViewCVQR(id)
```
- Descarga imagen del QR
- Abre modal con QR azul

#### b) Descargar QR del CV
```typescript
handleDownloadCV(id)
```
- Descarga archivo `CV{sap}.png`

#### c) Ver Cartón de Visita
```typescript
handleViewCVCard(funcionario)
```
- Obtiene firma HMAC del CV
- Abre landing page `/cartonv?sap=X&hash=Y` en nueva ventana

#### d) Eliminar CV
```typescript
handleDeleteCV(id)
```
- Confirma eliminación
- Llama endpoint `/cv/eliminar/{id}`
- Recarga lista de CVs

---

## 🎨 DISEÑO DE LA COLUMNA "AÇÕES"

### Antes:
```
┌──────────────────────────┐
│  👁️ 📥 🔗 🗑️              │
│  (solo QR normal)        │
└──────────────────────────┘
```

### Ahora:
```
┌──────────────────────────────────────┐
│  QR:  👁️ 📥 🔗 🗑️                   │
│  (negro - funcionarios con QR)      │
│                                      │
│  CV:  👁️ 📥 🔗 🗑️  ← NUEVO!        │
│  (azul/morado - solo si tiene CV)   │
└──────────────────────────────────────┘
```

---

## 🔹 CARACTERÍSTICAS

### **Visibilidad Condicional**
- Los botones de CV **solo aparecen** si el funcionario tiene CV generado
- Se consulta automáticamente al cargar el Dashboard

### **Diferenciación Visual**
- **QR Normal**: Íconos negros estándar
- **CV**: Íconos azules (#667eea) y morado (#764ba2)
- Etiqueta "QR:" y "CV:" para claridad

### **Organización**
- Disposición en columna (vertical)
- Primera fila: QR Normal (siempre visible)
- Segunda fila: CV (condicional)

---

## 📱 MODAL DIFERENCIADO

### Modal QR Normal:
- Borde estándar
- Título: "Código QR"
- Botón azul sólido

### Modal CV:
- **Borde

 azul** (#667eea)
- **Título en azul**: "QR - Cartão de Visita"
- **Botón con gradiente**: azul-morado

---

## 🔄 FLUJO DE USO

### 1. Ver QR del CV
```
Usuario click 👁️ (azul)
  → Consulta /cv/descargar/{id}
  → Abre modal con QR azul
  → Usuario cierra modal
```

### 2. Descargar CV
```
Usuario click 📥 (azul)
  → Consulta /cv/descargar/{id}
  → Descarga CV{sap}.png
```

### 3. Ver Landing Page
```
Usuario click 🔗 (azul)
  → Consulta /cv/funcionarios-con-cv
  → Obtiene firma HMAC
  → Abre /cartonv?sap=X&hash=Y en nueva pestaña
  → Usuario ve landing page del CV
```

### 4. Eliminar CV
```
Usuario click 🗑️ (morado)
  → Confirma eliminación
  → Consulta DELETE /cv/eliminar/{id}
  → Recarga lista de CVs
  → Botones CV desaparecen de esa fila
```

---

## ✅ ENDPOINTS UTILIZADOS

| Acción | Endpoint | Método |
|--------|----------|--------|
| Listar CVs | `/cv/funcionarios-con-cv` | GET |
| Ver QR | `/cv/descargar/{id}` | GET (blob) |
| Descargar | `/cv/descargar/{id}` | GET (blob) |
| Eliminar | `/cv/eliminar/{id}` | DELETE |

---

## 🎯 RESULTADO VISUAL

```
┌────────────────────────────────────────────────────────┐
│  SAP: 102                                              │
│  Nome: Helder Rangel Leite                            │
│  ...                                                   │
│                                                        │
│  Ações:                                               │
│  ┌─────────────────────────────────────────┐          │
│  │ QR: 👁️ 📥 🔗 🗑️                         │          │
│  │                                          │          │
│  │ CV: 👁️ 📥 🔗 🗑️  ← Solo si tiene CV   │          │
│  │    (azul) (azul) (azul) (morado)        │          │
│  └─────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 PARA PROBAR

1. Ir a **Dashboard** (`https://localhost/`)
2. Ver tabla "Funcionários com QR"
3. Buscar funcionario que tenga CV generado
4. Debería ver **2 filas de botones**:
   - Primera: QR (negro)
   - Segunda: CV (azul/morado)
5. Probar cada botón:
   - Visualizar QR del CV
   - Descargar CV{sap}.png
   - Ver landing page
   - Eliminar CV

---

## 📝 NOTAS

- Los botones de CV **solo se muestran** si `funcionariosConCV.includes(funcionario.id)`
- La consulta se hace automáticamente en `useEffect` al cargar
- El modal CV tiene estilo diferenciado con colors azul/morado
- La eliminación pide confirmación antes de proceder

---

**¡Implementación completada!** 🎉

_Desarrollado por: Ing. Maikel Cuao • 2025-12-02_
