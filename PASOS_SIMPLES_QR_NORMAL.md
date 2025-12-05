# ✅ SOLUCIÓN SIMPLE - Botones de QR Normal Condicionales

## 🎯 OBJETIVO

Mostrar botones de QR Normal SOLO si el funcionario tiene QR Normal.
Los botones de CV ya funcionan correctamente, NO los toques.

---

## 📋 3 CAMBIOS SIMPLES

### **CAMBIO 1: Agregar estado (línea ~63)**

**BUSCA**:
```typescript
  const [funcionariosConCV, setFuncionariosConCV] = useState<string[]>([]); // IDs con CV (como strings)
  const [cvModalOpen, setCvModalOpen] = useState(false);
```

**AGREGA DESPUÉS DE LA LÍNEA DE funcionariosConCV**:
```typescript
  const [funcionariosConQRNormal, setFuncionariosConQRNormal] = useState<string[]>([]);
```

---

### **CAMBIO 2: Agregar función (después de línea ~131)**

**BUSCA**:
```typescript
  };

  useEffect(() => {
```

**AGREGA ANTES DEL useEffect**:
```typescript
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

### **CAMBIO 3: Actualizar useEffect (línea ~134)**

**BUSCA**:
```typescript
  useEffect(() => {
    fetchDashboardData();
    fetchFuncionarios();
    fetchFuncionariosConCV();
  }, []);
```

**CAMBIA A**:
```typescript
  useEffect(() => {
    fetchDashboardData();
    fetchFuncionarios();
    fetchFuncionariosConCV();
    fetchFuncionariosConQRNormal();
  }, []);
```

---

### **CAMBIO 4: Condicionar botones de QR Normal (línea ~597-618)**

**BUSCA ESTE BLOQUE**:
```typescript
                            {/* QR Normal */}
                            <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
                              <Typography variant="caption" sx={{ mr: 1, fontWeight: 'bold', minWidth: '30px' }}>QR:</Typography>
                              <IconButton size="small" onClick={() => handleViewQR(funcionario.id)} title="Visualizar QR">
                                <QrCodeIcon fontSize="small" />
                              </IconButton>
```

**ENVUÉLVELO EN UNA CONDICIÓN**:

Agrega `{funcionariosConQRNormal.includes(String(funcionario.id)) && (` ANTES de `<Box`

Y agrega `)}` DESPUÉS del `</Box>` que cierra los botones de QR Normal

**DEBERÍA QUEDAR ASÍ**:
```typescript
                            {/* QR Normal - Solo si tiene QR Normal */}
                            {funcionariosConQRNormal.includes(String(funcionario.id)) && (
                              <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
                                <Typography variant="caption" sx={{ mr: 1, fontWeight: 'bold', minWidth: '30px' }}>QR:</Typography>
                                <!-- TODOS LOS ICONBUTTONS DE QR NORMAL -->
                              </Box>
                            )}
```

---

## ✅ RESUMEN

1. Agregar 1 línea de estado
2. Agregar 1 función
3. Agregar 1 línea en useEffect
4. Agregar 1 condición (2 líneas) rodeando los botones de QR Normal

**NO TOQUES NADA MÁS**. Especialmente NO toques los botones de CV.

---

## 🧪 RESULTADO ESPERADO

| Tiene QR Normal | Tiene CV | Botones QR Normal | Botones CV |
|-----------------|----------|-------------------|------------|
| ✅ Sí | ❌ No | ✅ Sí | ❌ No |
| ❌ No | ✅ Sí | ❌ No | ✅ Sí |
| ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |

---

_Solución preparada: 2025-12-04 11:04_
