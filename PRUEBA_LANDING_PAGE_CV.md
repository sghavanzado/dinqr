# 🧪 PRUEBA DE LANDING PAGE - Cartón de Visita

## 🔗 URL PARA PROBAR

```
https://192.168.253.5/cartonv?sap=107&hash=ef33da9f921cab6859c87a87a96b61863df18f398fb9d1e24d2fcd7727860bda
```

**Funcionario**: Andre Cabaia Eduardo  
**SAP**: 107  
**Área**: DAA

---

## ✅ ELEMENTOS A VERIFICAR

### **1. Header con SVG de Sonangol**
- [ ] Logo amarillo de Sonangol (SVG inline)
- [ ] Debe verse completo y con buena calidad
- [ ] Sin errores de carga de imagen

### **2. Subtítulo Gris**
- [ ] Texto: "Sociedade Nacional de Combustíveis de Angola"
- [ ] Fondo gris (#B8B8B8)
- [ ] Alineado a la derecha

### **3. Datos del Funcionario**
- [ ] **Nome**: "Andre Cabaia Eduardo" (grande, negrita)
- [ ] **Função**: (puede estar vacío)
- [ ] **Área**: "DAA" (en gris, más pequeño)

### **4. Información de Contacto**
- [ ] **Telefone**: "+244 226 690 495"
- [ ] **E-mail**: "andre.cabaya@isptec.co.ao"
- [ ] Con labels "Telefone:" y "E-mail:"

### **5. Footer**
- [ ] Texto: "Rua Rainha Ginga, N.º 29/31 R/C - C. Postal 1316 - Luanda - República de Angola"
- [ ] Con borde superior
- [ ] Centrado

### **6. Botón de Importar Contacto**
- [ ] Texto: "📇 Guardar Contato"
- [ ] Gradiente azul-morado
- [ ] Al hacer hover: Sube un poco
- [ ] Al hacer click: Descarga archivo .vcf

### **7. Diseño General**
- [ ] Fondo con gradiente azul-morado
- [ ] Tarjeta blanca centrada
- [ ] Bordes redondeados
- [ ] Sombra profesional
- [ ] Animación de entrada suave

---

## 🎨 COMPARACIÓN CON MODAL

El diseño debe ser **exactamente igual** al modal del Dashboard:
- Mismo SVG de Sonangol
- Misma estructura de layout
- Mismos colores y tipografía
- Mismo espaciado (padding-left: 100px)

**Única diferencia**: El botón dice "Guardar Contato" en lugar de "Fechar"

---

## 📱 RESPONSIVE

### **En Desktop**:
- Ancho máximo: 600px
- Padding left de 100px en los campos

### **En Mobile** (menor a 600px):
- Padding left reducido a 20px
- Card ocupa todo el ancho disponible

---

## 🧪 PASOS DE PRUEBA

### **Prueba 1: Diseño Visual**
1. Abre la URL en el navegador
2. Verifica que el SVG de Sonangol se vea completo
3. Verifica que todos los campos estén alineados correctamente
4. Compara con el modal del Dashboard (deben ser idénticos)

### **Prueba 2: Botón vCard**
1. Click en "📇 Guardar Contato"
2. Debería descargar archivo: `CV-107.vcf`
3. Abre el archivo con tu app de contactos
4. Verifica que importe:
   - Nombre: Andre Cabaia Eduardo
   - Función: (vacío o presente)
   - Departamento: DAA
   - Teléfono: +244 226 690 495
   - Email: andre.cabaya@isptec.co.ao

### **Prueba 3: Responsive**
1. Abre las herramientas de desarrollador (F12)
2. Cambia a vista móvil (Ctrl+Shift+M)
3. Verifica que el padding se ajuste
4. Verifica que todo sea legible

---

## 🐛 PROBLEMAS COMUNES

### **Si el SVG no se ve**:
- Verifica que el código HTML tenga el SVG inline completo
- Abre la consola del navegador (F12) y busca errores

### **Si falta el hash o SAP**:
- Error 400: Parámetros faltantes
- Verifica que la URL tenga ambos parámetros

### **Si hash es inválido**:
- Error 403: Acceso no autorizado
- El hash debe coincidir con la firma en la base de datos

### **Si el funcionario no existe**:
- Error 404: Cartón de visita no encontrado
- Verifica que el SAP esté en la tabla `cv_codes`

---

## 📊 OTRAS URLs DE PRUEBA

### **SAP 102** (Helder Rangel Leite):
```
https://192.168.253.5/cartonv?sap=102&hash=eb8c62aa2e0e61245f20e3abade62af3e716eee31cd4d95e128852c235670d76
```

### **SAP 106** (Nauria de Fatima):
```
https://192.168.253.5/cartonv?sap=106&hash=34e201e96d3d0975dbaaebc804353228390cd75b5dfa5169648459c507b0b6f5
```

### **SAP 111** (Elizangela Patricia):
```
https://192.168.253.5/cartonv?sap=111&hash=99d585a71335e0322f47cdeb2720af82de9a1c2d14a74e62646cb97cc64d8ba9
```

---

## ✅ CHECKLIST FINAL

- [ ] SVG de Sonangol se ve correctamente
- [ ] Subtítulo gris presente
- [ ] Datos del funcionario mostrados
- [ ] Telefone y email visibles
- [ ] Footer con dirección
- [ ] Botón "Guardar Contato" funciona
- [ ] Descarga vCard correctamente
- [ ] Diseño idéntico al modal
- [ ] Responsive funciona
- [ ] Sin errores en consola

---

## 🎯 RESULTADO ESPERADO

Al abrir la URL deberías ver:

```
┌────────────────────────────────────┐
│  [SVG SONANGOL AMARILLO COMPLETO] │
├────────────────────────────────────┤
│  Sociedade Nacional de Combustí... │
├────────────────────────────────────┤
│                                    │
│  ANDRE CABAIA EDUARDO              │
│  (Función si existe)               │
│  DAA                               │
│                                    │
│  Telefone: +244 226 690 495        │
│  E-mail: andre.cabaya@isptec.co.ao│
│                                    │
│  ─────────────────────────────────│
│  Rua Rainha Ginga, N.º 29/31...   │
│                                    │
│  [📇 Guardar Contato] (gradiente) │
└────────────────────────────────────┘
```

Todo con fondo degradado azul-morado! 🎨

---

**Por favor, abre la URL en tu navegador y verifica todos los puntos del checklist.** 

_Ing. Maikel Cuao • 2025-12-03_
