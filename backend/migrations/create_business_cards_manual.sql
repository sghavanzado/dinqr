-- =====================================================
-- SIGA - Migración Manual: Tabla business_cards
-- =====================================================
-- Archivo: create_business_cards_table.sql
-- Descripción: Crea la tabla para almacenar cartones de visita
-- Autor: Ing. Maikel Cuao
-- Fecha: 2025
-- =====================================================

-- Crear tabla business_cards
CREATE TABLE IF NOT EXISTS business_cards (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(20) NOT NULL UNIQUE,
    firma VARCHAR(256) NOT NULL,
    qr_code_path VARCHAR(512) NOT NULL,
    qr_code_data TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_business_cards_contact_id ON business_cards(contact_id);
CREATE INDEX IF NOT EXISTS idx_business_cards_active ON business_cards(is_active);

-- Comentarios descriptivos
COMMENT ON TABLE business_cards IS 'Almacena información de cartones de visita digitales generados';
COMMENT ON COLUMN business_cards.id IS 'ID único autoincremental';
COMMENT ON COLUMN business_cards.contact_id IS 'ID del funcionario (SAP) - debe ser único';
COMMENT ON COLUMN business_cards.firma IS 'Firma HMAC-SHA256 para seguridad';
COMMENT ON COLUMN business_cards.qr_code_path IS 'Ruta del archivo QR en el servidor';
COMMENT ON COLUMN business_cards.qr_code_data IS 'URL completa del cartón de visita';
COMMENT ON COLUMN business_cards.created_at IS 'Fecha y hora de creación del cartón';
COMMENT ON COLUMN business_cards.updated_at IS 'Fecha y hora de última actualización';
COMMENT ON COLUMN business_cards.is_active IS 'Indica si el cartón está activo';

-- =====================================================
-- VERIFICACIÓN
-- =====================================================
-- Verificar que la tabla fue creada correctamente:
-- SELECT table_name, column_name, data_type, is_nullable 
-- FROM information_schema.columns 
-- WHERE table_name = 'business_cards' 
-- ORDER BY ordinal_position;

-- Verificar índices:
-- SELECT indexname, indexdef 
-- FROM pg_indexes 
-- WHERE tablename = 'business_cards';

-- =====================================================
-- ROLLBACK (si es necesario)
-- =====================================================
-- Para eliminar la tabla y sus índices:
-- DROP INDEX IF EXISTS idx_business_cards_active;
-- DROP INDEX IF EXISTS idx_business_cards_contact_id;
-- DROP TABLE IF EXISTS business_cards;

-- =====================================================
-- FIN DE SCRIPT
-- =====================================================
