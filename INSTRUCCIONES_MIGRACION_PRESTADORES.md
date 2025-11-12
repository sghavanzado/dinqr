# 📋 INSTRUCCIONES PARA MIGRACIÓN DE TABLAS DE PRESTADORES

## ✅ Estado Actual
- ✅ Modelos SQLAlchemy creados en `/backend/models/prestadores.py`
- ✅ Modelos importados en `/backend/models/__init__.py`

## 🚀 PASOS PARA EJECUTAR LA MIGRACIÓN

### **Paso 1: Activar el entorno virtual de Python**

```bash
cd /Users/mcc/shared/dinqr/backend

# Si usas el entorno apiqr:
source ../apiqr/bin/activate

# O si tienes otro entorno virtual:
# source venv/bin/activate
```

### **Paso 2: Verificar que Flask-Migrate está instalado**

```bash
pip list | grep Flask-Migrate
```

Si no está instalado:
```bash
pip install Flask-Migrate
```

### **Paso 3: Verificar la configuración de la base de datos**

Asegúrate que el archivo `.env` en `/backend/.env` tenga la configuración correcta:

```bash
cat .env | grep DATABASE_URL
```

Debe mostrar algo como:
```
DATABASE_URL=postgresql://postgres:postgr3s@192.168.253.133:5432/localdb
```

### **Paso 4: Generar la migración automáticamente**

```bash
# Asegúrate de estar en la carpeta backend
cd /Users/mcc/shared/dinqr/backend

# Genera la migración automática
flask db migrate -m "Agregar tablas de control de prestadores"
```

Este comando:
- Detectará los nuevos modelos (Prestadores, Locales, Empresas, etc.)
- Creará un archivo de migración en `migrations/versions/`
- El archivo contendrá las instrucciones SQL para crear todas las tablas

### **Paso 5: Revisar el archivo de migración (OPCIONAL pero recomendado)**

```bash
# Listar los archivos de migración
ls -ltr migrations/versions/

# Ver el contenido del último archivo generado
cat migrations/versions/XXXXX_agregar_tablas_de_control_de_prestadores.py
```

### **Paso 6: Aplicar la migración a la base de datos**

```bash
flask db upgrade
```

Este comando:
- Ejecutará el script de migración
- Creará todas las tablas en la base de datos `localdb`
- Establecerá todas las relaciones y foreign keys

### **Paso 7: Verificar que las tablas fueron creadas**

```bash
# Conectar a PostgreSQL y verificar
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "\dt"
```

Deberías ver las nuevas tablas:
- `locales`
- `empresas`
- `centroneg`
- `functions`
- `tiposervice`
- `localservice`
- `areaservice`
- `prestadores`
- `historial`

## 📊 TABLAS CREADAS Y SUS RELACIONES

### 1. **LOCALES** (Tabla de ubicaciones)
- `id` (PK)
- `nome`

### 2. **EMPRESAS** (Tabla de empresas)
- `id` (PK)
- `nome`
- `telefono`
- `email`
- `obs`

### 3. **CENTRONEG** (Centros de negocio)
- `id` (PK)
- `nome`

### 4. **FUNCTIONS** (Funciones/Cargos)
- `id` (PK)
- `nome`

### 5. **TIPOSERVICE** (Tipos de servicio)
- `id` (PK)
- `nome`

### 6. **LOCALSERVICE** (Locales de servicio)
- `id` (PK)
- `nome`

### 7. **AREASERVICE** (Áreas de servicio)
- `id` (PK)
- `nome`

### 8. **PRESTADORES** (Tabla principal)
- `id` (PK)
- `nome`
- `filiacao`
- `data_nas` (Date)
- `local` (FK → locales.id)
- `nacionalidade`
- `bi_pass`
- `emissao` (Date)
- `validade` (Date)
- `local_resid`
- `telefono`
- `email`
- `lock` (Boolean)
- `obs`

**Relaciones:**
- Muchos prestadores → Un local
- Muchos prestadores → Una empresa (a través de historial)

### 9. **HISTORIAL** (Tabla de historial de servicios)
- `id_hist` (PK)
- `id_prest` (FK → prestadores.id) ⚠️ NOT NULL
- `id_empresa` (FK → empresas.id) ⚠️ NOT NULL
- `id_centro_neg` (FK → centroneg.id) ⚠️ NOT NULL
- `id_funcao` (FK → functions.id) ⚠️ NOT NULL
- `data_ini_prest` (Date) ⚠️ NOT NULL
- `horario`
- `data_fim_prest` (Date)
- `motivo`
- `id_tipo_servico` (FK → tiposervice.id) ⚠️ NOT NULL
- `id_local_serv` (FK → localservice.id) ⚠️ NOT NULL
- `andar`
- `conflito` (Boolean)
- `quando` (Date)
- `motivo_conflito`
- `id_areas` (FK → areaservice.id) ⚠️ NOT NULL
- `tempo`

**Relaciones:**
- Muchos historiales → Un prestador
- Muchos historiales → Una empresa
- Muchos historiales → Un centro de negocio
- Muchos historiales → Una función
- Muchos historiales → Un tipo de servicio
- Muchos historiales → Un local de servicio
- Muchos historiales → Un área de servicio

## 🔧 COMANDOS RESUMIDOS (COPIAR Y PEGAR)

```bash
# 1. Ir a la carpeta backend
cd /Users/mcc/shared/dinqr/backend

# 2. Activar entorno virtual (ajusta según tu entorno)
source ../apiqr/bin/activate

# 3. Verificar Flask-Migrate
pip list | grep Flask-Migrate

# 4. Generar migración
flask db migrate -m "Agregar tablas de control de prestadores"

# 5. Aplicar migración
flask db upgrade

# 6. Verificar tablas creadas
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "\dt"
```

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Error: "No changes in schema detected"
Si Flask no detecta cambios, verifica:
```bash
# Ver si los modelos están importados correctamente
python -c "from models import Prestador, Local, Empresa; print('OK')"
```

### Error: "Could not locate a Flask application"
```bash
# Asegúrate de tener las variables de entorno
export FLASK_APP=app.py
flask db migrate -m "Agregar tablas de control de prestadores"
```

### Error de conexión a la base de datos
```bash
# Verificar que PostgreSQL esté accesible
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "SELECT version();"
```

## 📝 INSERTAR DATOS DE PRUEBA (OPCIONAL)

Después de crear las tablas, puedes insertar datos de prueba:

```sql
-- Conectar a la base de datos
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb

-- Insertar locales
INSERT INTO locales (nome) VALUES 
    ('Luanda'),
    ('Benguela'),
    ('Huambo');

-- Insertar empresas
INSERT INTO empresas (nome, telefono, email) VALUES 
    ('Empresa A', '+244 923 456 789', 'contacto@empresaa.ao'),
    ('Empresa B', '+244 923 456 790', 'contacto@empresab.ao');

-- Insertar centros de negocio
INSERT INTO centroneg (nome) VALUES 
    ('Centro Norte'),
    ('Centro Sul');

-- Insertar funciones
INSERT INTO functions (nome) VALUES 
    ('Técnico'),
    ('Supervisor'),
    ('Gerente');

-- Insertar tipos de servicio
INSERT INTO tiposervice (nome) VALUES 
    ('Manutenção'),
    ('Instalação'),
    ('Consultoria');

-- Insertar locales de servicio
INSERT INTO localservice (nome) VALUES 
    ('Escritório Central'),
    ('Armazém'),
    ('Oficina');

-- Insertar áreas de servicio
INSERT INTO areaservice (nome) VALUES 
    ('Área Técnica'),
    ('Área Administrativa'),
    ('Área Comercial');
```

## ✅ VERIFICACIÓN FINAL

Para verificar que todo está funcionando correctamente:

```bash
# Ver las tablas y sus columnas
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "\d+ prestadores"
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "\d+ historial"

# Ver las relaciones (foreign keys)
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "
SELECT
    tc.table_name, 
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND tc.table_name IN ('prestadores', 'historial')
ORDER BY tc.table_name;
"
```

## 📞 SOPORTE

Si encuentras algún error durante la migración:
1. Verifica los logs en `backend/logs/`
2. Revisa el archivo `.env` para las credenciales de BD
3. Asegúrate de que el servidor PostgreSQL esté corriendo
4. Verifica que el usuario tenga permisos para crear tablas

---

**Fecha de creación:** 12 de noviembre de 2025
**Sistema:** DINQR - Control de Prestadores
