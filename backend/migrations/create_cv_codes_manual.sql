-- ================================================
-- MIGRACIÓN: Crear tabla cv_codes
-- Estructura idéntica a qr_codes
-- ================================================

-- Crear tabla cv_codes
CREATE TABLE IF NOT EXISTS cv_codes (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    firma VARCHAR(64) NOT NULL,
    archivo_qr VARCHAR(255) NOT NULL
);

-- Crear índice en contact_id para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_cv_codes_contact_id ON cv_codes(contact_id);

-- Comentarios
COMMENT ON TABLE cv_codes IS 'Almacena información de cartones de visita generados';
COMMENT ON COLUMN cv_codes.contact_id IS 'SAP del funcionario (único)';
COMMENT ON COLUMN cv_codes.nombre IS 'Nombre completo del funcionario';
COMMENT ON COLUMN cv_codes.firma IS 'Firma HMAC-SHA256 para seguridad';
COMMENT ON COLUMN cv_codes.archivo_qr IS 'Ruta del archivo QR generado';
