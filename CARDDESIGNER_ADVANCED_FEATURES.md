# Mejoras Avanzadas del CardDesigner - Sistema de Nomenclatura y Asociación de Campos

## Resumen de Nuevas Funcionalidades

Se han implementado mejoras significativas al CardDesigner para incluir:

1. **Sistema de nomenclatura automática** para elementos
2. **Asociación de elementos con campos de funcionarios**
3. **Panel de gestión de elementos mejorado**
4. **Lista visual de elementos en la interfaz**

## 🏷️ Sistema de Nomenclatura Automática

### Funcionamiento
- Cada elemento añadido recibe automáticamente un nombre único
- Los nombres siguen el patrón: `Tipo + Número`
- Ejemplos:
  - `Texto 1`, `Texto 2`, `Texto 3`
  - `Imagen 1`, `Imagen 2`, `Imagen 3`
  - `QR Code 1`, `QR Code 2`, `QR Code 3`

### Implementación
```typescript
const generateElementName = (type: DesignElement['type']) => {
  const elementsOfType = currentElements.filter(el => 
    el.type === type && !el.id.startsWith('bg_')
  );
  const count = elementsOfType.length + 1;
  
  switch (type) {
    case 'text': return `Texto ${count}`;
    case 'image': return `Imagen ${count}`;
    case 'qr': return `QR Code ${count}`;
    case 'background': return `Fondo ${count}`;
    default: return `Elemento ${count}`;
  }
};
```

## 🔗 Sistema de Asociación con Campos de Funcionarios

### Campos Disponibles para Asociación
```typescript
const EMPLOYEE_FIELDS = {
  nombre_completo: 'Nombre Completo',
  nombre: 'Nombre',
  apellidos: 'Apellidos', 
  documento: 'Documento ID',
  email: 'Email',
  telefono: 'Teléfono',
  departamento: 'Departamento',
  cargo: 'Cargo',
  fecha_ingreso: 'Fecha de Ingreso',
  codigo_empleado: 'Código Empleado',
  foto: 'Foto del Empleado',
  qr_empleado: 'QR del Empleado',
  empresa: 'Empresa',
  sede: 'Sede/Sucursal',
  nivel_acceso: 'Nivel de Acceso'
};
```

### Funcionalidades de Asociación
- **Asociación Flexible**: Cualquier elemento puede asociarse con cualquier campo
- **Sin Restricciones**: `Texto 1` puede ser nombre, cargo, email, etc.
- **Configurable**: El usuario decide qué elemento representa qué campo
- **Opcional**: Los elementos pueden no tener campo asociado

## 🎛️ Interfaz de Usuario Mejorada

### Panel de Propiedades Dinámico
Cada elemento seleccionado muestra:

1. **Nombre del Elemento**
   - Campo editable para cambiar el nombre
   - Se actualiza en tiempo real

2. **Campo Asociado**
   - Dropdown con todos los campos disponibles
   - Opción "Ningún campo asociado"
   - Solo visible para elementos no-background

3. **Propiedades Específicas**
   - Texto: contenido, fuente, tamaño, color, alineación
   - Imagen: selección/cambio de imagen, placeholder
   - QR Code: datos del QR code
   - Fondo: color, imagen de fondo

### Lista de Elementos
- **Vista General**: Muestra todos los elementos en la cara actual
- **Información Detallada**: Nombre del elemento y campo asociado
- **Selección Rápida**: Clic para seleccionar elemento
- **Indicador Visual**: Elemento seleccionado se resalta
- **Scroll**: Lista con scroll para muchos elementos

## 📋 Estructura de Datos Actualizada

### Interfaz DesignElement
```typescript
interface DesignElement {
  id: string;
  type: 'text' | 'image' | 'qr' | 'background';
  name: string; // Nuevo: nombre del elemento
  associatedField?: string; // Nuevo: campo asociado
  x: number;
  y: number;
  width: number;
  height: number;
  rotation?: number;
  properties: {
    // ... propiedades existentes
  };
}
```

## 🎯 Flujo de Uso

### Para Agregar y Asociar Elementos:

1. **Agregar Elemento**
   ```
   Usuario hace clic en "Texto" → Se crea "Texto 1"
   Usuario hace clic en "Texto" → Se crea "Texto 2"  
   Usuario hace clic en "Imagen" → Se crea "Imagen 1"
   ```

2. **Seleccionar Elemento**
   - Clic en el elemento en el canvas
   - O clic en la lista de elementos del sidebar

3. **Configurar Elemento**
   - Cambiar nombre si se desea
   - Seleccionar campo asociado del dropdown
   - Ajustar propiedades específicas

4. **Asociar con Campo de Funcionario**
   ```
   "Texto 1" → Campo: "Nombre Completo"
   "Texto 2" → Campo: "Departamento"  
   "Imagen 1" → Campo: "Foto del Empleado"
   "QR Code 1" → Campo: "QR del Empleado"
   ```

## 🔄 Flexibilidad del Sistema

### Reasociación Dinámica
- Los elementos pueden cambiar de asociación en cualquier momento
- No hay restricciones predefinidas
- El usuario tiene control total sobre las asociaciones

### Ejemplos de Uso Flexible
```
Escenario 1:
- Texto 1 → Nombre Completo
- Texto 2 → Cargo
- Texto 3 → Departamento

Escenario 2:  
- Texto 1 → Email
- Texto 2 → Teléfono
- Texto 3 → Código Empleado

Escenario 3:
- Texto 1 → Departamento
- Texto 2 → Nombre Completo  
- Texto 3 → Fecha Ingreso
```

## 🎨 Características Visuales

### Lista de Elementos
- **Header**: "Elementos na Tela (N)" donde N es el número de elementos
- **Elemento Seleccionado**: Fondo azul con texto blanco
- **Elemento Normal**: Fondo transparente con hover gris
- **Campo Asociado**: Se muestra como "→ Nombre del Campo" en texto pequeño
- **Scroll**: Lista scrolleable si hay muchos elementos

### Panel de Propiedades
- **Título Dinámico**: Muestra "Propiedades: [Nombre del Elemento]"
- **Campo de Nombre**: Input editable en la parte superior
- **Dropdown de Asociación**: Select con todos los campos disponibles
- **Separación Visual**: Cada sección claramente diferenciada

## 🚀 Beneficios del Sistema

1. **Organización Clara**: Nombres automáticos evitan confusión
2. **Flexibilidad Total**: Asociaciones completamente configurables  
3. **Gestión Visual**: Lista de elementos para navegación rápida
4. **Escalabilidad**: Funciona con cualquier cantidad de elementos
5. **Usabilidad**: Interfaz intuitiva y fácil de usar
6. **Futuro**: Base sólida para generación automática de passes

## 🔮 Próximas Mejoras Sugeridas

1. **Preview con Datos**: Mostrar vista previa con datos reales de funcionarios
2. **Plantillas**: Guardar configuraciones de asociaciones como plantillas
3. **Validación**: Alertas si faltan asociaciones importantes
4. **Duplicación**: Duplicar elementos con sus asociaciones
5. **Importación**: Importar datos de funcionarios para testing
6. **Exportación**: Exportar configuración de asociaciones

## 📝 Notas Técnicas

- Los elementos de fondo (`background`) no tienen asociación de campos
- La numeración se reinicia por cada cara (frente/verso)
- Los nombres son editables pero deben ser únicos (recomendado)
- Las asociaciones se almacenan en el campo `associatedField`
- La interfaz se actualiza automáticamente al cambiar elementos
