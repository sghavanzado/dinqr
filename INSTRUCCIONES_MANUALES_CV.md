# 📋 Instrucciones Manuales para Completar Cartón de Visita

## ⚠️ IMPORTANTE

Debido a problemas de timeout en el proxy/IIS y corrupción de archivos al editar, estas son las instrucciones **MANUALMENTE** para completar la implementación.

---

## ✅ Ya Completado (Backend)

### Files Created:
1. ✅ `backend/models/business_card.py` - Modelo de BD
2. ✅ `backend/services/business_card_service.py` - Lógica de negocio
3. ✅ `backend/routes/business_card_routes.py` - API + Landing page
4. ✅ `backend/migrations/versions/create_business_cards_table.py` - Migración
5. ✅ `backend/app.py` - Blueprint registrado

### Changes Made:
- ✅ Límite TOP 50 en consultas SQL
- ✅ Timeout 15s en conexiones
- ✅ Caché de 2 minutos
- ✅ Logging detallado

---

## ⏳ Pendiente (Frontend) - HACER MANUALMENTE

### Paso 1: Restaurar MenuContent.tsx

```bash
cd frontend
git checkout HEAD -- src/components/MenuContent.tsx
```

### Paso 2: Editar MenuContent.tsx Manualmente

Abrir `frontend/src/components/MenuContent.tsx` en el editor y buscar la línea 59-67:

**ANTES**:
```typescript
    children: [
      {
        id: '2.1',
        label: 'Gerar Code',
        icon: ReceiptLongOutlinedIcon,
        to: '/qrcode',
      },
    ],
  },
];
```

**DESPUÉS** (agregar el item 2.2):
```typescript
    children: [
      {
        id: '2.1',
        label: 'Gerar Code',
        icon: ReceiptLongOutlinedIcon,
        to: '/qrcode',
      },
      {
        id: '2.2',
        label: 'Gerar CV',
        icon: ReceiptLongOutlinedIcon,
        to: '/business-card',
      },
    ],
  },
];
```

Guardar el archivo.

---

### Paso 3: Crear BusinessCardManagement.tsx

Crear archivo `frontend/src/pages/BusinessCardManagement.tsx`:

```typescript
// BusinessCardManagement.tsx
import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Snackbar,
  Alert,
  CircularProgress,
} from '@mui/material';
import BusinessCardTable from '../components/BusinessCardTable';
import { fetchFuncionarios } from '../api/apiService';
import type { Funcionario } from '../types/Funcionario';

const BusinessCardManagement = () => {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await fetchFuncionarios(1, 10, '');
      console.log('API Response (Funcionários):', data);
      setFuncionarios(data);
    } catch (error) {
      console.error('Erro ao carregar os funcionários:', error);
      setSnackbarMessage('Erro ao carregar os funcionários.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  console.log('BusinessCardManagement rendered');

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Gestão de Cartões de Visita
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <BusinessCardTable />
        </Grid>
      </Grid>
     
      {loading && <CircularProgress />}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity={snackbarSeverity}>{snackbarMessage}</Alert>
      </Snackbar>
    </Container>
  );
};

export default BusinessCardManagement;
```

---

### Paso 4: Eliminar BusinessCardTable de QRManagement.tsx

Abrir `frontend/src/pages/QRManagement.tsx` y **ELIMINAR** las siguientes líneas:

**ELIMINAR** import:
```typescript
import BusinessCardTable from '../components/BusinessCardTable';  // BORRAR
```

**ELIMINAR** el título:
```typescript
// CAMBIAR de:
Gestão de Códigos QR e Cartões de Visita

// A:
Gestão de Códigos QR
```

**ELIMINAR** el Grid de BusinessCard:
```typescript
{/* Tabla de Cartones de Visita */}
<Grid item xs={12}>    {/* BORRAR TODO ESTE BLOQUE */}
  <BusinessCardTable />
</Grid>
```

---

### Paso 5: Agregar Ruta en App.tsx

Abrir `frontend/src/App.tsx` y agregar:

**Importar la página**:
```typescript
import BusinessCardManagement from './pages/BusinessCardManagement';
```

**Agregar ruta** (dentro de `<Routes>`):
```typescript
<Route path="/business-card" element={<BusinessCardManagement />} />
```

---

### Paso 6: Acceder Directamente a Vite

Para evitar problemas de timeout del proxy/IIS:

1. Abrir navegador
2. Ir a: **`http://localhost:5173/`** (NO https://localhost)
3. Navegar a "Funcionários → Gerar CV"

---

## 🎯 Estructura Final

```
Menu:
├── Dashboard
├── Funcionários
│   ├── Gerar Code (/qrcode)       ← Solo tabla QR
│   └── Gerar CV (/business-card)  ← Solo tabla Cartón
└── Settings
```

---

## ✅ Verificación

Después de hacer estos cambios manualmente:

1. Reiniciar Vite:
   ```bash
   cd frontend
   npm run dev
   ```

2. Acceder a: `http://localhost:5173/`

3. Verificar en el menú:
   - ✅ "Funcionários" tiene 2 items
   - ✅ "Gerar Code" muestra tabla de QR
   - ✅ "Gerar CV" muestra tabla de Cartones

---

## 🔧 Si hay Errores de TypeScript

Si hay errores en BusinessCardTable.tsx después de editar, verificar que el import del ícono sea:

```typescript
import QrCodeIcon from '@mui/icons-material/QrCode';  // ✅ Correcto
```

Y no:
```typescript
import ContactCardIcon from '@mui/icons-material/Badge';  // ❌ Incorrecto
```

Todas las referencias a `ContactCardIcon` deben cambiarse a `QrCodeIcon`.

---

_Sigue estas instrucciones paso a paso para completar la implementación correctamente._
