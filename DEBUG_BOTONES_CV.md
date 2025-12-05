# 🔍 DEBUG - Botones CV no se muestran

## ✅ VERIFICACIONES REALIZADAS

### 1. Base de Datos
```
✅ CVs en BD: 7
✅ Tabla cv_codes existe
✅ Registros válidos
```

### 2. Endpoint Backend
```
✅ GET /cv/funcionarios-con-cv funciona
✅ Retorna 200 OK
✅ Datos correctos
```

### 3. Estructura de Datos
```json
{
  "id": "102",  // ⚠️ String, no número
  "nome": "Helder Rangel Leite",
  "cvCode": {
    "archivo": "...",
    "firma": "eb8c62aa..."
  }
}
```

---

## 🔍 LOGS AGREGADOS

He agregado logging en 3 lugares:

### 1. `fetchFuncionariosConCV()`
```typescript
console.log('[DEBUG] Fetching funcionarios con CV...');
console.log('[DEBUG] Response status:', response.status);
console.log('[DEBUG] Response data:', response.data);
console.log('[DEBUG] CV ID: ${f.id} -> ${numId}');
console.log('[DEBUG] IDs con CV:', idsConCV);
```

### 2. Render Condicional
```typescript
console.log(`[DEBUG] Funcionario ${funcionario.id} tiene CV:`, tieneCV);
console.log('Array CVs:', funcionariosConCV);
```

---

## 📋 INSTRUCCIONES DE DEBUG

### PASO 1: Abrir Consola del Navegador
1. Ir a https://localhost/ (Dashboard)
2. Presionar **F12**
3. Ir a pestaña **Console**

### PASO 2: Refrescar Página
1. Presionar **Ctrl+Shift+R** (hard reload)
2. Observar mensajes `[DEBUG]` en consola

### PASO 3: Reportar Logs

Buscar y copiar:

#### a) Al cargar (useEffect):
```
[DEBUG] Fetching funcionarios con CV...
[DEBUG] Response status: ???
[DEBUG] Response data: ???
[DEBUG] CV ID: ??? -> ???
[DEBUG] IDs con CV: [...]
```

#### b) Al renderizar tabla:
```
[DEBUG] Funcionario 102 tiene CV: true/false
Array CVs: [...]
```

---

## 🔎 POSIBLES PROBLEMAS

### Problema 1: IDs diferentes tipos
- **Backend retorna**: `"102"` (string)
- **Frontend espera**: `102` (número)
- **Solución**: `Number(f.id)` ya aplicado

### Problema 2: Endpoint falla
- **Síntoma**: Error en consola
- **Solución**: Verificar CORS, autenticación

### Problema 3: Array vacío
- **S

íntoma**: `IDs con CV: []`
- **Solución**: Verificar formato de datos

### Problema 4: Comparación falla
- **Síntoma**: `tiene CV: false` pero ID está en array
- **Solución**: Verificar tipos (string vs number)

---

## 🛠️ SOLUCIÓN TEMPORAL

Si los logs muestran que `funcionariosConCV` tiene IDs pero no se muestran botones:

### Verificar tipo de `funcionario.id`:
```typescript
console.log(typeof funcionario.id);  // string o number?
console.log(typeof funcionariosConCV[0]);  // string o number?
```

### Si hay mismatch de tipos:
```typescript
// Cambiar línea 478 a:
{funcionariosConCV.includes(String(funcionario.id)) && (
// o
{funcionariosConCV.map(String).includes(String(funcionario.id)) && (
```

---

## 📊 EJEMPLO DE SALIDA ESPERADA

**Console al cargar**:
```
[DEBUG] Fetching funcionarios con CV...
[DEBUG] Response status: 200
[DEBUG] Response data: [{ id: "102", ... }, { id: "106", ... }]
[DEBUG] CV ID: 102 -> 102
[DEBUG] CV ID: 106 -> 106
[DEBUG] IDs con CV: [102, 106, 107, 108, 112, 113, 115]
```

**Console al renderizar**:
```
[DEBUG] Funcionario 102 tiene CV: true Array CVs: [102, 106, ...]
[DEBUG] Funcionario 103 tiene CV: false Array CVs: [102, 106, ...]
```

---

## ⚙️ SIGUIENTE PASO

**Por favor**:
1. Abre https://localhost/
2. Presiona F12
3. Ve a Console
4. Refresca la página (Ctrl+Shift+R)
5. Copia todos los mensajes `[DEBUG]` que aparezcan
6. Pégalos aquí

Con esa información sabré exactamente cuál es el problema.

---

_Debugging Assistant • 2025-12-02_
