# INSTRUCCIONES PARA CORREGIR qr_routes.py

## ARCHIVO: backend/routes/qr_routes.py
## FUNCIÓN: listar_funcionarios()  
## LÍNEAS: 46-49

### CÓDIGO ACTUAL (INCORRECTO):
```python
cursor = conn_local.cursor()
cursor.execute("SELECT contact_id FROM qr_codes")
qr_generated_ids = [row[0] for row in cursor.fetchall()]
logging.info(f"IDs de funcionarios con QR obtenidos: {qr_generated_ids}")
```

### CÓDIGO NUEVO (CORRECTO):
```python
cursor = conn_local.cursor()
# UNION de ambas tablas para obtener funcionarios con QR Normal O CV
cursor.execute("""
    SELECT contact_id FROM qr_codes
    UNION
    SELECT contact_id FROM cv_codes
""")
qr_generated_ids = [row[0] for row in cursor.fetchall()]
logging.info(f"IDs de funcionarios con QR o CV obtenidos: {qr_generated_ids}")
```

## EXPLICACIÓN:

El problema es que la consulta solo busca en `qr_codes`, ignorando `cv_codes`.

Con UNION, obtenemos IDs de AMBAS tablas:
- QR Normal (tabla `qr_codes`)
- CV (tabla `cv_codes`)

Así, un funcionario con SOLO CV también aparecerá en la tabla "Funcionarios con QR".

## PASOS PARA APLICAR:

1. Abre `backend/routes/qr_routes.py`
2. Busca la función `listar_funcionarios()` (línea ~30)
3. Encuentra la línea 47: `cursor.execute("SELECT contact_id FROM qr_codes")`
4. Reemplaza las líneas 46-49 con el código nuevo
5. Guarda el archivo
6. Reinicia el servidor backend

## RESULTADO ESPERADO:

Después del cambio:
- ✅ Crear QR Normal → Funcionario en tabla
- ✅ Crear CV → Funcionario en tabla
- ✅ Ambos son independientes
- ✅ Funcionarios con solo QR Normal aparecen
- ✅ Funcionarios con solo CV aparecen
- ✅ Funcionarios con ambos aparecen

_Ing. Maikel Cuao • 2025-12-03_
