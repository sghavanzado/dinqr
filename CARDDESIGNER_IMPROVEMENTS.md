# Mejoras Implementadas en CardDesigner

## Resumen
Se han implementado nuevas funcionalidades en el componente `CardDesigner.tsx` para mejorar la experiencia de diseño interactivo de passes, incluyendo elementos de fondo, imágenes como placeholders, y QR codes posicionables.

## Nuevas Funcionalidades Implementadas

### 1. Elemento "FONDO" para Imágenes de Fondo
- **Función**: Permite seleccionar y aplicar una imagen de fondo al pase
- **Implementación**: 
  - Nuevo componente `BackgroundElement` que maneja tanto color sólido como imagen de fondo
  - Botón "FONDO" en la barra de herramientas para seleccionar imagen de fondo
  - Soporte para opacidad y overlay de imagen sobre color de fondo
- **Ubicación**: Los elementos de fondo se renderizan primero para estar detrás de otros elementos

### 2. Elementos de Imagen como Placeholders
- **Función**: Permite agregar elementos de imagen sin necesidad de seleccionar archivo primero
- **Implementación**:
  - Botón "Imagem" que agrega un placeholder visual con texto "IMAGEM"
  - Placeholder renderizado como rectángulo con borde punteado
  - Funcionalidad para seleccionar imagen después de posicionar el placeholder
  - Capacidad de cambiar o remover imagen desde el panel de propiedades

### 3. Elementos QR Code Interactivos
- **Función**: QR codes que se pueden agregar, posicionar y redimensionar libremente
- **Implementación**:
  - Componente `QRElement` que renderiza un QR code visual
  - Posicionamiento y redimensionamiento con transformadores de Konva
  - Panel de propiedades para editar los datos del QR code
  - Tamaño mínimo de 30x30 píxeles para mantener legibilidad

### 4. Interfaz de Usuario Mejorada
- **Botones de Herramientas**:
  - `Texto`: Agrega elementos de texto
  - `Imagem`: Agrega placeholders de imagen
  - `QR Code`: Agrega elementos QR code
  - `FONDO`: Selecciona imagen de fondo
- **Panel de Propiedades Dinámico**:
  - Propiedades específicas según el tipo de elemento seleccionado
  - Controles para cambiar imágenes, colores, y datos QR
  - Botones para remover elementos o imágenes

## Estructura de Código

### Componentes Principales
```typescript
- TextElement: Maneja elementos de texto con transformación
- ImageElement: Maneja imágenes y placeholders con transformación
- QRElement: Maneja elementos QR code con transformación
- BackgroundElement: Maneja fondo con color e imagen
```

### Tipos de Elementos Soportados
```typescript
type ElementType = 'text' | 'image' | 'qr' | 'background';
```

### Propiedades de Elementos
```typescript
interface DesignElement {
  id: string;
  type: ElementType;
  x: number;
  y: number;
  width: number;
  height: number;
  rotation?: number;
  properties: {
    // Texto
    text?: string;
    fontSize?: number;
    fontFamily?: string;
    fill?: string;
    align?: string;
    
    // Imagen
    src?: string;
    placeholder?: string;
    
    // QR Code
    qrData?: string;
    
    // Fondo
    backgroundColor?: string;
    backgroundImage?: string;
  };
}
```

## Flujo de Uso

### Para Agregar Imagen de Fondo:
1. Hacer clic en botón "FONDO"
2. Seleccionar imagen desde el explorador de archivos
3. La imagen se aplica automáticamente como fondo del passe
4. Se puede cambiar o remover desde el panel de propiedades

### Para Agregar Elemento de Imagen:
1. Hacer clic en botón "Imagem"
2. Se agrega un placeholder visual posicionable
3. Posicionar y redimensionar el placeholder
4. Hacer clic en el placeholder para seleccionarlo
5. Usar panel de propiedades para seleccionar imagen
6. La imagen se aplica manteniendo la posición y tamaño

### Para Agregar QR Code:
1. Hacer clic en botón "QR Code"
2. Se agrega un elemento QR visual
3. Posicionar y redimensionar según necesidad
4. Seleccionar el elemento QR
5. Editar datos del QR en el panel de propiedades

## Archivos Modificados

### `frontend/src/components/CardDesigner.tsx`
- Agregados nuevos componentes para cada tipo de elemento
- Implementadas funciones de manejo de archivos para fondo e imágenes
- Mejorada interfaz de usuario con nuevos botones y controles
- Actualizadas funciones de renderización para todos los tipos de elementos

## Características Técnicas

### Renderización por Capas:
1. **Fondo**: BackgroundElement (color + imagen opcional)
2. **Elementos**: TextElement, ImageElement, QRElement en orden de creación
3. **Transformadores**: Solo para elemento seleccionado

### Manejo de Archivos:
- Soporte para formatos de imagen estándar (PNG, JPG, GIF, etc.)
- Conversión a Base64 para almacenamiento en el diseño
- Referencias a archivos por FileReader API

### Interactividad:
- Drag & Drop para todos los elementos
- Redimensionamiento con mantener proporción opcional
- Rotación de elementos (implementada en transformadores)
- Selección múltiple (base implementada)

## Próximas Mejoras Posibles

1. **Bibliotecas QR Reales**: Integrar generación real de QR codes con bibliotecas como `qrcode`
2. **Efectos de Imagen**: Filtros, transparencia, máscaras
3. **Plantillas**: Guardar y cargar diseños predefinidos
4. **Exportación Avanzada**: PDF, SVG con elementos vectoriales
5. **Capas**: Sistema de capas para mejor organización
6. **Alineación**: Herramientas de alineación y distribución
7. **Tipografías**: Soporte para fuentes personalizadas

## Notas de Desarrollo

- Todas las refs utilizan inicialización explícita `useRef<any>(null)` para TypeScript
- Manejo de errores implementado para carga de archivos
- Componentes optimizados para re-renderización mínima
- Código modular con separación clara de responsabilidades

## Testing

Para probar las nuevas funcionalidades:
1. Ejecutar `npm run dev` en el directorio frontend
2. Navegar a Passes Config → Novo Tema → Designer Visual
3. Probar cada tipo de elemento en el canvas
4. Verificar propiedades dinámicas en el panel lateral
5. Probar exportación y guardado de diseños
