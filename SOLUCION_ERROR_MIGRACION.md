# 🔧 SOLUCIÓN - ERROR DE MIGRACIÓN "Can't locate revision"

## ❌ ERROR ENCONTRADO:
```
ERROR [flask_migrate] Error: Can't locate revision identified by '12b248eebe64'
```

También hay un error de relaciones que ya fue corregido en los modelos.

---

## ✅ SOLUCIÓN PASO A PASO

### **OPCIÓN 1: Sincronizar la base de datos con las migraciones actuales (RECOMENDADO)**

Esta es la solución más segura que mantiene tus datos existentes.

```bash
# 1. Conectarse a PostgreSQL
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb

# 2. Verificar la revisión actual en la base de datos
SELECT * FROM alembic_version;

# 3. Si la revisión no existe, actualizarla manualmente a la última válida
DELETE FROM alembic_version;
INSERT INTO alembic_version (version_num) VALUES ('4063c09db320');

# 4. Salir de psql
\q
```

Ahora intenta crear la migración nuevamente:

```bash
cd C:\Users\administrator.GTS\Develop\dinqr\backend
flask db migrate -m "Agregar tablas de control de prestadores"
flask db upgrade
```

---

### **OPCIÓN 2: Resetear completamente las migraciones (SI NO TIENES DATOS IMPORTANTES)**

⚠️ **ADVERTENCIA:** Esto eliminará TODAS las tablas y datos existentes.

```bash
# 1. Eliminar todas las tablas de la base de datos
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
"

# 2. Eliminar todos los archivos de migración
cd C:\Users\administrator.GTS\Develop\dinqr\backend\migrations\versions
del /Q *.py
# Mantener solo __pycache__ vacío o eliminarlo también

# 3. Crear una migración inicial desde cero
cd C:\Users\administrator.GTS\Develop\dinqr\backend
flask db init
flask db migrate -m "Migracion inicial con todas las tablas"
flask db upgrade
```

---

### **OPCIÓN 3: Crear las tablas manualmente sin migración**

Si solo quieres crear las nuevas tablas de prestadores sin tocar las existentes:

```bash
# 1. Conectarse a PostgreSQL
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb

# 2. Ejecutar el siguiente script SQL
```

```sql
-- Crear tabla LOCALES
CREATE TABLE IF NOT EXISTS locales (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Crear tabla EMPRESAS
CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefono VARCHAR(30),
    email VARCHAR(50),
    obs TEXT
);

-- Crear tabla CENTRONEG
CREATE TABLE IF NOT EXISTS centroneg (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Crear tabla FUNCTIONS
CREATE TABLE IF NOT EXISTS functions (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

-- Crear tabla TIPOSERVICE
CREATE TABLE IF NOT EXISTS tiposervice (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

-- Crear tabla LOCALSERVICE
CREATE TABLE IF NOT EXISTS localservice (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

-- Crear tabla AREASERVICE
CREATE TABLE IF NOT EXISTS areaservice (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

-- Crear tabla PRESTADORES
CREATE TABLE IF NOT EXISTS prestadores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    filiacao VARCHAR(100),
    data_nas DATE,
    local_id INTEGER REFERENCES locales(id),
    nacionalidade VARCHAR(25),
    bi_pass VARCHAR(20),
    emissao DATE,
    validade DATE,
    local_resid VARCHAR(50),
    telefono VARCHAR(30),
    email VARCHAR(50),
    lock BOOLEAN DEFAULT FALSE,
    obs TEXT,
    empresa_id INTEGER REFERENCES empresas(id)
);

-- Crear tabla HISTORIAL
CREATE TABLE IF NOT EXISTS historial (
    id_hist SERIAL PRIMARY KEY,
    id_prest INTEGER NOT NULL REFERENCES prestadores(id) ON DELETE CASCADE,
    id_empresa INTEGER NOT NULL REFERENCES empresas(id),
    id_centro_neg INTEGER NOT NULL REFERENCES centroneg(id),
    id_funcao INTEGER NOT NULL REFERENCES functions(id),
    data_ini_prest DATE NOT NULL,
    horario VARCHAR(20),
    data_fim_prest DATE,
    motivo VARCHAR(100),
    id_tipo_servico INTEGER NOT NULL REFERENCES tiposervice(id),
    id_local_serv INTEGER NOT NULL REFERENCES localservice(id),
    andar VARCHAR(10),
    conflito BOOLEAN DEFAULT FALSE,
    quando DATE,
    motivo_conflito VARCHAR(100),
    id_areas INTEGER NOT NULL REFERENCES areaservice(id),
    tempo VARCHAR(20)
);

-- Crear índices para mejorar rendimiento
CREATE INDEX idx_prestadores_local ON prestadores(local_id);
CREATE INDEX idx_prestadores_empresa ON prestadores(empresa_id);
CREATE INDEX idx_historial_prestador ON historial(id_prest);
CREATE INDEX idx_historial_empresa ON historial(id_empresa);
CREATE INDEX idx_historial_centro ON historial(id_centro_neg);

-- Verificar que las tablas fueron creadas
\dt
```

Después, actualiza la tabla de versiones de Alembic:

```sql
-- Marcar como aplicada la última migración conocida
DELETE FROM alembic_version WHERE version_num = '12b248eebe64';
INSERT INTO alembic_version (version_num) VALUES ('4063c09db320')
ON CONFLICT DO NOTHING;

\q
```

---

## 🔍 VERIFICAR QUE TODO FUNCIONÓ

```bash
# Verificar las tablas creadas
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb -c "\dt"

# Verificar las relaciones (foreign keys)
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

---

## 📝 INSERTAR DATOS DE PRUEBA

```sql
PGPASSWORD=postgr3s psql -h 192.168.253.133 -U postgres -d localdb

-- Insertar datos de prueba
INSERT INTO locales (nome) VALUES 
    ('Luanda'), ('Benguela'), ('Huambo');

INSERT INTO empresas (nome, telefono, email) VALUES 
    ('Empresa A', '+244 923 456 789', 'info@empresaa.ao'),
    ('Empresa B', '+244 923 456 790', 'info@empresab.ao');

INSERT INTO centroneg (nome) VALUES 
    ('Centro Norte'), ('Centro Sul');

INSERT INTO functions (nome) VALUES 
    ('Técnico'), ('Supervisor'), ('Gerente');

INSERT INTO tiposervice (nome) VALUES 
    ('Manutenção'), ('Instalação'), ('Consultoria');

INSERT INTO localservice (nome) VALUES 
    ('Escritório Central'), ('Armazém'), ('Oficina');

INSERT INTO areaservice (nome) VALUES 
    ('Área Técnica'), ('Área Administrativa'), ('Área Comercial');

-- Verificar
SELECT * FROM locales;
SELECT * FROM empresas;

\q
```

---

## ✅ RESUMEN DE CAMBIOS REALIZADOS EN LOS MODELOS

Se corrigieron los siguientes errores en `/backend/models/prestadores.py`:

1. ✅ Cambio de `local` a `local_id` (columna FK)
2. ✅ Cambio de `local_rel` a `local` (relación)
3. ✅ Cambio de `empresa_rel` a `empresa` (relación)
4. ✅ Se agregó `empresa_id` como foreign key en Prestador
5. ✅ Actualizado el método `to_dict()` para usar los nuevos nombres

**Ahora los modelos son consistentes y funcionarán correctamente.**

---

## 🎯 RECOMENDACIÓN FINAL

**Usa la OPCIÓN 1** si ya tienes datos en la base de datos (usuarios, qr_codes, etc.).

**Usa la OPCIÓN 3** si solo quieres agregar las nuevas tablas sin afectar las existentes y sin lidiar con migraciones.

**Usa la OPCIÓN 2** solo si estás en desarrollo y no te importa perder los datos actuales.
