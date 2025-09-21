# Verificación de la nueva estructura del menú

## Cambios realizados:

✅ **ANTES:**
```
- Impressão (independiente)
  - Impressão Dashboard
  - Gerar Code
- RRHH (independiente)
  - Dashboard RRHH
  - Funcionários
  - ... (otros items)
```

✅ **DESPUÉS:**
```
- RRHH
  - Impressão
    - Impressão Dashboard (/dashboard)
    - Gerar Code (/qrcode)
  - Dashboard RRHH (/rrhh/dashboard)
  - Funcionários (/rrhh/funcionarios)
  - ... (otros items)
```

## Configuración actualizada:

- **defaultExpandedItems**: `['3', '3.0']` - Expande RRHH y la subsección Impressão
- **defaultSelectedItems**: `'3.0.1'` - Selecciona por defecto "Impressão Dashboard"

## Estructura de IDs:

- `3` = RRHH (nivel principal)
- `3.0` = Impressão (subsección dentro de RRHH)
- `3.0.1` = Impressão Dashboard
- `3.0.2` = Gerar Code
- `3.1` = Dashboard RRHH
- `3.2` = Funcionários
- ... etc

## Resultado esperado:

Al cargar la aplicación, el menú debería mostrar:
- RRHH expandido
- Impressão expandido dentro de RRHH
- "Impressão Dashboard" seleccionado por defecto
- Navegación a /dashboard cuando se hace clic en "Impressão Dashboard"
