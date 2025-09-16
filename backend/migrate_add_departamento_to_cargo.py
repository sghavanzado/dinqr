#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Migration script to add DepartamentoID to Cargos table
"""

import logging
from extensions import IAMCSession
from sqlalchemy import text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

def migrate_add_departamento_to_cargo():
    """Add DepartamentoID column to Cargos table"""
    
    logger.info("🔄 Starting migration: Add DepartamentoID to Cargos table")
    
    try:
        # Get database session
        session = IAMCSession()
        
        try:
            # Check if column already exists
            check_column_sql = """
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'Cargos' 
            AND COLUMN_NAME = 'DepartamentoID'
            """
            
            result = session.execute(text(check_column_sql))
            column_exists = result.fetchone()[0] > 0
            
            if column_exists:
                logger.info("✅ Column DepartamentoID already exists in Cargos table")
                return True
            
            # Add the column
            logger.info("📝 Adding DepartamentoID column to Cargos table...")
            add_column_sql = """
            ALTER TABLE Cargos 
            ADD DepartamentoID INT NULL
            """
            session.execute(text(add_column_sql))
            
            # Add foreign key constraint
            logger.info("🔗 Adding foreign key constraint...")
            add_fk_sql = """
            ALTER TABLE Cargos 
            ADD CONSTRAINT FK_Cargos_Departamentos 
            FOREIGN KEY (DepartamentoID) REFERENCES Departamentos(DepartamentoID)
            """
            session.execute(text(add_fk_sql))
            
            # Commit transaction
            session.commit()
            logger.info("✅ Migration completed successfully!")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"❌ Error during migration: {str(e)}")
            return False
        finally:
            session.close()
                
    except Exception as e:
        logger.error(f"❌ Error connecting to database: {str(e)}")
        return False

def verify_migration():
    """Verify that the migration was successful"""
    
    logger.info("🔍 Verifying migration...")
    
    try:
        session = IAMCSession()
        
        try:
            # Check table structure
            check_sql = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'Cargos'
            ORDER BY ORDINAL_POSITION
            """
            
            result = session.execute(text(check_sql))
            columns = result.fetchall()
            
            logger.info("📋 Current Cargos table structure:")
            for col in columns:
                logger.info(f"   • {col[0]} ({col[1]}) - Nullable: {col[2]}")
            
            # Check if DepartamentoID exists
            departamento_id_exists = any(col[0] == 'DepartamentoID' for col in columns)
            
            if departamento_id_exists:
                logger.info("✅ DepartamentoID column found in Cargos table")
                return True
            else:
                logger.error("❌ DepartamentoID column not found in Cargos table")
                return False
        finally:
            session.close()
                
    except Exception as e:
        logger.error(f"❌ Error verifying migration: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔄 IAMC Database Migration: Add DepartamentoID to Cargos")
    print("=" * 60)
    
    # Run migration
    if migrate_add_departamento_to_cargo():
        print("\n✅ Migration completed successfully!")
        
        # Verify migration
        if verify_migration():
            print("✅ Migration verification successful!")
        else:
            print("⚠️  Migration verification failed!")
    else:
        print("\n❌ Migration failed!")
        
    print("\n" + "=" * 60)
    print("Migration script completed.")
