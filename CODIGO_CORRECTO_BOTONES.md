# 🔧 CÓDIGO CORRECTO - Sección de Botones con QR Normal y CV

## ⚠️ IMPORTANTE

El archivo `MainGrid.tsx` se ha restaurado a su versión anterior.  
Necesitas aplicar los cambios manualmente siguiendo esta guía.

---

## 📋 CAMBIOS NECESARIOS

### **CAMBIO 1: Agregar estados (línea ~52)**

```typescript
const [funcionariosConQRNormal, setFuncionariosConQRNormal] = useState<string[]>([]);
const [funcionariosConCV, setFuncionariosConCV] = useState<string[]>([]);
```

---

### **CAMBIO 2: Agregar funciones (después de línea ~130)**

```typescript
// Función para obtener funcionarios con CV
const fetchFuncionariosConCV = async () => {
  try {
    const response = await axiosInstance.get('/cv/funcionarios-con-cv');
    if (response.status === 200) {
      const idsConCV = response.data.map((f: any) => String(f.id));
      setFuncionariosConCV(idsConCV);
    }
  } catch (error) {
    console.error('Error fetching funcionarios con CV:', error);
  }
};

// Función para obtener funcionarios con QR Normal
const fetchFuncionariosConQRNormal = async () => {
  try {
    const response = await axiosInstance.get('/qr/solo-qr-normal');
    if (response.status === 200) {
      setFuncionariosConQRNormal(response.data.map((id: any) => String(id)));
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

### **CAMBIO 3: Actualizar useEffect (línea ~135)**

```typescript
useEffect(() => {
  fetchDashboardData();
  fetchFuncionarios();
  fetchFuncionariosConCV();
  fetchFuncionariosConQRNormal();
}, []);
```

---

### **CAMBIO 4: Reemplazar sección de botones (línea ~580-603)**

**BUSCA ESTE BLOQUE**:
```typescript
<TableCell align="center">
  <Box sx={{ display: 'flex', gap: 0.5 }}>
    <IconButton size="small" onClick={() => handleViewQR(funcionario.id)} title="Visualizar QR">
      <QrCodeIcon fontSize="small" />
    </IconButton>
    {/* ... más botones ... */}
  </Box>
</TableCell>
```

**REEMPLÁZALO CON**:
```typescript
<TableCell align="center">
  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
    {/* QR Normal - Solo si tiene QR Normal */}
    {funcionariosConQRNormal.includes(String(funcionario.id)) && (
      <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
        <Typography variant="caption" sx={{ mr: 1, fontWeight: 'bold', minWidth: '30px' }}>QR:</Typography>
        <IconButton size="small" onClick={() => handleViewQR(funcionario.id)} title="Visualizar QR">
          <QrCodeIcon fontSize="small" />
        </IconButton>
        <IconButton size="small" onClick={() => handleDownloadQR(funcionario.id)} title="Baixar QR">
          <DownloadIcon fontSize="small" />
        </IconButton>
        <IconButton size="small" onClick={() => handleViewContactCard(funcionario)} title="Ver Cartão">
          <OpenInNewIcon fontSize="small" />
        </IconButton>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            handleDeleteQR(funcionario.id);
          }}
          title="Eliminar QR"
          color="error"
        >
          <DeleteIcon fontSize="small" />
        </IconButton>
      </Box>
    )}

    {/* Cartón de Visita (CV) - Solo si tiene CV */}
    {funcionariosConCV.includes(String(funcionario.id)) && (
      <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
        <Typography variant="caption" sx={{ mr: 1, fontWeight: 'bold', minWidth: '30px', color: '#667eea' }}>CV:</Typography>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            handleViewCVQR(funcionario.id);
          }}
          title="Visualizar QR do CV"
          sx={{ color: '#667eea' }}
        >
          <QrCodeIcon fontSize="small" />
        </IconButton>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            handleDownloadCV(funcionario.id);
          }}
          title="Baixar QR do CV"
          sx={{ color: '#667eea' }}
        >
          <DownloadIcon fontSize="small" />
        </IconButton>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            handleViewCVCard(funcionario);
          }}
          title="Ver Cartão de Visita"
          sx={{ color: '#667eea' }}
        >
          <OpenInNewIcon fontSize="small" />
        </IconButton>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            handleDeleteCV(funcionario.id);
          }}
          title="Eliminar CV"
          sx={{ color: '#764ba2' }}
        >
          <DeleteIcon fontSize="small" />
        </IconButton>
      </Box>
    )}
  </Box>
</TableCell>
```

---

## ✅ RESULTADO FINAL

Con estos cambios:

- ✅ **Etiqueta "QR:"** en negro para botones de QR Normal
- ✅ **Etiqueta "CV:"** en azul (#667eea) para botones de CV
- ✅ **Botones en columna** (uno debajo del otro)
- ✅ **Condicionales correctos**:
  - Solo QR Normal → Solo muestra botones negros con etiqueta "QR:"
  - Solo CV → Solo muestra botones azules con etiqueta "CV:"
  - Ambos → Muestra ambas filas de botones

---

## 🎯 INSTRUCCIONES

1. Abre `frontend/src/components/MainGrid.tsx`
2. Aplica los 4 cambios en orden
3. Guarda el archivo
4. Refresca el navegador

---

_Código correcto preparado: 2025-12-04 22:27_
