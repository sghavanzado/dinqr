-- Script SQL para crear base de datos DINQR
-- Ejecutar este script después de instalar PostgreSQL

-- Conectar como superusuario (postgres)
\c postgres

-- Eliminar base de datos si existe (CUIDADO: elimina todos los datos)
DROP DATABASE IF EXISTS localdb;

-- Crear base de datos principal
CREATE DATABASE localdb
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252'
    LC_CTYPE = 'Spanish_Spain.1252'
    TEMPLATE = template0;

-- Comentario de la base de datos
COMMENT ON DATABASE localdb IS 'Base de datos principal para DINQR - Sistema de Códigos QR';

-- Crear usuario de aplicación
DROP USER IF EXISTS dinqr_user;
CREATE USER dinqr_user WITH
    PASSWORD 'dinqr_password'
    CREATEDB
    NOSUPERUSER
    NOCREATEROLE;

-- Comentario del usuario
COMMENT ON ROLE dinqr_user IS 'Usuario de aplicación para DINQR';

-- Conectar a la nueva base de datos
\c localdb

-- Asignar permisos al usuario de aplicación
GRANT ALL PRIVILEGES ON DATABASE localdb TO dinqr_user;
GRANT ALL ON SCHEMA public TO dinqr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dinqr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dinqr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO dinqr_user;

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Comentarios para las extensiones
COMMENT ON EXTENSION "uuid-ossp" IS 'Generación de UUIDs para DINQR';
COMMENT ON EXTENSION "pgcrypto" IS 'Funciones criptográficas para DINQR';

-- Configurar zona horaria por defecto
ALTER DATABASE localdb SET timezone TO 'Europe/Madrid';

-- Crear esquemas adicionales si son necesarios
CREATE SCHEMA IF NOT EXISTS audit;
CREATE SCHEMA IF NOT EXISTS logs;

-- Asignar permisos a los esquemas adicionales
GRANT ALL ON SCHEMA audit TO dinqr_user;
GRANT ALL ON SCHEMA logs TO dinqr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA audit GRANT ALL ON TABLES TO dinqr_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA logs GRANT ALL ON TABLES TO dinqr_user;

-- Comentarios para los esquemas
COMMENT ON SCHEMA audit IS 'Esquema para tablas de auditoría';
COMMENT ON SCHEMA logs IS 'Esquema para tablas de logging';

-- Crear tabla de configuración inicial (será recreada por Alembic)
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Comentario para la tabla settings
COMMENT ON TABLE settings IS 'Configuración del sistema DINQR';
COMMENT ON COLUMN settings.key IS 'Clave de configuración única';
COMMENT ON COLUMN settings.value IS 'Valor de configuración en formato texto';

-- Insertar configuraciones iniciales básicas
INSERT INTO settings (key, value) VALUES 
    ('serverDomain', '127.0.0.1'),
    ('serverPort', '5000'),
    ('outputFolder', 'C:\inetpub\wwwroot\dinqr\uploads\qr_codes'),
    ('appName', 'DINQR'),
    ('appVersion', '1.0.0'),
    ('maxQRPerBatch', '100'),
    ('qrCodeSize', '200'),
    ('qrCodeMargin', '4')
ON CONFLICT (key) DO NOTHING;

-- Crear función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger para updated_at en la tabla settings
CREATE TRIGGER update_settings_updated_at 
    BEFORE UPDATE ON settings 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Crear tabla temporal para información de instalación
CREATE TABLE IF NOT EXISTS installation_info (
    id SERIAL PRIMARY KEY,
    installation_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    database_version TEXT,
    script_version TEXT DEFAULT '1.0.0',
    notes TEXT
);

-- Insertar información de esta instalación
INSERT INTO installation_info (database_version, notes) 
VALUES (version(), 'Base de datos creada por script automatizado para DINQR');

-- Mostrar información de la instalación
SELECT 
    'Base de datos creada exitosamente' as status,
    current_database() as database_name,
    current_user as connected_as,
    version() as postgresql_version,
    now() as installation_time;

-- Mostrar configuraciones insertadas
SELECT 'Configuraciones iniciales:' as info;
SELECT key, value FROM settings ORDER BY key;

-- Mostrar permisos del usuario dinqr_user
SELECT 'Permisos asignados a dinqr_user:' as info;
\du dinqr_user

-- Mostrar esquemas creados
SELECT 'Esquemas disponibles:' as info;
\dn

-- Mostrar extensiones instaladas
SELECT 'Extensiones instaladas:' as info;
\dx

-- Instrucciones finales
SELECT 'INSTALACION COMPLETADA' as status;
SELECT 'Ejecuta el siguiente comando para continuar:' as next_step;
SELECT 'migrar_base_datos.bat' as command;
