# 🚨 Problema REAL: Timeout del Proxy/IIS en Desarrollo

## ❌ Síntoma

Errores 504 Gateway Timeout al cargar íconos de Material-UI en desarrollo:

```
GET https://localhost/node_modules/.vite/deps/@mui_icons-material_Badge.js 504
GET https://localhost/node_modules/.vite/deps/@mui_icons-material_ContactMail.js 504
```

## 🔍 Causa Raíz

El problema **NO es el backend ni los íconos específicos**. El problema es:

### IIS/Proxy con Timeout Muy Bajo

Estás accediendo a Vite dev server a través de **`https://localhost`** (puerto 443), lo que indica que hay un **proxy reverso** (probablemente IIS) entre el navegador y Vite.

**Flujo actual**:
```
Navegador → IIS (puerto 443) → Vite (puerto 5173) → node_modules
            ↑
         TIMEOUT aquí (30-60 seg)
```

Cuando Vite procesa las dependencias de MUI por primera vez, tarda más del timeout configurado en IIS/proxy, causando el error 504.

---

## ✅ Solución TEMPORAL Aplicada

**Usar QrCodeIcon** que ya está cargado en `QRTable.tsx`:

```typescript
// En BusinessCardTable.tsx
import QrCodeIcon from '@mui/icons-material/QrCode';  // ✅ Ya cargado

// En lugar de:
// import ContactCardIcon from '@mui/icons-material/ContactMail';  // ❌ Timeout
```

**Resultado**: BusinessCardTable usará el mismo ícono que QRTable temporalmente.

---

## ✅ Soluciones PERMANENTES

### Opción 1: Acceder Directamente a Vite (RECOMENDADO para desarrollo)

En lugar de `https://localhost`, accede directamente a Vite:

```
http://localhost:5173/
```

**Ventajas**:
- ✅ Sin proxy/timeout
- ✅ Hot reload más rápido
- ✅ Todos los íconos funcionan
- ✅ Mejor experiencia de desarrollo

**Cómo**:
1. Abrir navegador
2. Ir a `http://localhost:5173/`
3. Aceptar certificado autofirmado si es necesario

---

### Opción 2: Aumentar Timeout en IIS

Si DEBES usar el proxy, aumenta el timeout:

**web.config** (en el directorio del proxy IIS):
```xml
<configuration>
  <system.webServer>
    <aspNetCore requestTimeout="00:05:00" />
    <!-- Aumentar de 30seg a 5 minutos -->
    
    <rewrite>
      <outboundRules>
        <rule name="proxy-timeout">
          <action type="Rewrite" value="300000" />
          <!-- 5 minutos en milisegundos -->
        </rule>
      </outboundRules>
    </rewrite>
  </system.webServer>
</configuration>
```

---

### Opción 3: Pre-bundlear Dependencias

Forzar a Vite a procesar dependencias antes de iniciar:

**vite.config.ts**:
```typescript
export default defineConfig({
  optimizeDeps: {
    include: [
      '@mui/material',
      '@mui/icons-material',
      '@mui/icons-material/QrCode',
      '@mui/icons-material/ContactMail',
      '@mui/icons-material/Search',
      // ... otros íconos
    ],
    force: true  // Forzar re-optimización
  }
});
```

Luego:
```bash
cd frontend
rm -rf node_modules/.vite
npm run dev
```

---

### Opción 4: Usar Build en Producción

Si esto es para producción:

```bash
cd frontend
npm run build
```

Luego servir desde `dist/` con IIS (sin Vite dev server).

---

## 📊 Comparación de Soluciones

| Solución | Complejidad | Desarrollo | Producción |
|----------|-------------|------------|------------|
| **Acceso directo Vite** | Baja | ✅ Mejor | ❌ No |
| **Aumentar timeout IIS** | Media | ✅ Funciona | ⚠️ Innecesario |
| **Pre-bundlear deps** | Media | ✅ Funciona | ✅ Funciona |
| **Build producción** | Baja | ❌ Lento | ✅ Mejor |

---

## 🎯 Recomendación FINAL

### Para Desarrollo:
Usa **acceso directo a Vite** sin proxy:
```
http://localhost:5173/
```

### Para Producción:
Usa **build** y sirve con IIS:
```bash
npm run build
# Servir carpeta dist/ con IIS
```

---

## 🔧 Cambios Realizados en el Código

**Archivo**: `frontend/src/components/BusinessCardTable.tsx`

**Cambio temporal**:
```typescript
// Línea 31
import QrCodeIcon from '@mui/icons-material/QrCode';

// Líneas 269, 278, 330
<QrCodeIcon />  // En lugar de ContactCardIcon
```

**Razón**: Evitar cargar nuevo ícono mientras hay problema de timeout.

---

## ✅ Prueba Inmediata

1. **Recargar navegador** (Ctrl+R)
2. Si sigue error 504:
   - **Opción A**: Ir a `http://localhost:5173/` directamente
   - **Opción B**: Esperar a que Vite termine de procesar (puede tardar 2-3 min)

3. Una vez funcionando, considera implementar Opción 3 (pre-bundlear)

---

## 📝 Resumen

**Problema**: IIS/proxy timeout procesando dependencias MUI  
**Causa**: Vite tarda en optimizar íconos, proxy timeout <60seg  
**Solución temporal**: Usar QrCodeIcon (ya cargado)  
**Solución permanente**: Acceso directo a Vite o aumentar timeout  

---

_Desarrollado por: Ing. Maikel Cuao • 2025_
