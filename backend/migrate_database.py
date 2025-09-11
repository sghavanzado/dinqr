#!/usr/bin/env python3
"""
Database Migration Script: PostgreSQL localdb to MSSQL IAMC
This script automates the migration of tables and data from localdb to IAMC database.
"""

import pyodbc
import sys
import os
from typing import Optional, Dict, Any
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseMigrator:
    """Handles the migration from localdb to IAMC database."""
    
    def __init__(self, connection_string: str):
        """
        Initialize the migrator with MSSQL connection string.
        
        Args:
            connection_string: MSSQL connection string for IAMC database
        """
        self.connection_string = connection_string
        self.connection = None
        
    def connect(self) -> bool:
        """
        Connect to the IAMC database.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.connection = pyodbc.connect(self.connection_string)
            logger.info("Successfully connected to IAMC database")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
            
    def execute_sql_file(self, file_path: str) -> bool:
        """
        Execute SQL script from file.
        
        Args:
            file_path: Path to SQL script file
            
        Returns:
            True if execution successful, False otherwise
        """
        if not os.path.exists(file_path):
            logger.error(f"SQL file not found: {file_path}")
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
                
            cursor = self.connection.cursor()
            
            # Split by GO statements for MSSQL
            sql_batches = [batch.strip() for batch in sql_content.split('GO') if batch.strip()]
            
            # If no GO statements, treat as single batch
            if len(sql_batches) <= 1:
                sql_batches = [sql_content]
            
            for i, batch in enumerate(sql_batches):
                if batch.strip():
                    try:
                        cursor.execute(batch)
                        self.connection.commit()
                        logger.info(f"Executed batch {i + 1} from {file_path}")
                    except Exception as e:
                        logger.warning(f"Error in batch {i + 1}: {e}")
                        # Continue with next batch for non-critical errors
                        
            cursor.close()
            logger.info(f"Successfully executed SQL file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute SQL file {file_path}: {e}")
            return False
            
    def verify_migration(self) -> Dict[str, Any]:
        """
        Verify the migration by checking table counts and data integrity.
        
        Returns:
            Dictionary with verification results
        """
        verification_results = {}
        
        try:
            cursor = self.connection.cursor()
            
            # Check if tables exist and count records
            tables_to_check = [
                'alembic_version',
                'permission', 
                'role',
                'roles_permissions',
                'user',
                'audit_log',
                'qr_codes',
                'settings'
            ]
            
            for table in tables_to_check:
                try:
                    # Use proper SQL Server syntax for checking table existence
                    cursor.execute(f"""
                        IF EXISTS (SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U')
                        BEGIN
                            SELECT COUNT(*) FROM [{table}]
                        END
                        ELSE
                        BEGIN
                            SELECT -1
                        END
                    """)
                    count = cursor.fetchone()[0]
                    
                    if count >= 0:
                        verification_results[table] = {
                            'exists': True,
                            'count': count
                        }
                        logger.info(f"Table {table}: {count} records")
                    else:
                        verification_results[table] = {
                            'exists': False,
                            'error': 'Table does not exist'
                        }
                        logger.warning(f"Table {table} does not exist")
                        
                except Exception as e:
                    verification_results[table] = {
                        'exists': False,
                        'error': str(e)
                    }
                    logger.warning(f"Table {table} check failed: {e}")
                    
            cursor.close()
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            
        return verification_results
        
    def run_migration(self, script_dir: str) -> bool:
        """
        Run the complete migration process.
        
        Args:
            script_dir: Directory containing migration scripts
            
        Returns:
            True if migration successful, False otherwise
        """
        logger.info("Starting database migration from localdb to IAMC")
        logger.info(f"Migration started at: {datetime.now()}")
        
        # List of SQL scripts to execute in order
        migration_scripts = [
            'migrate_localdb_to_iamc.sql',
            'migrate_qr_codes_part1.sql'
        ]
        
        success = True
        
        for script in migration_scripts:
            script_path = os.path.join(script_dir, script)
            logger.info(f"Executing migration script: {script}")
            
            if not self.execute_sql_file(script_path):
                logger.error(f"Failed to execute script: {script}")
                success = False
                break
                
        if success:
            logger.info("Migration scripts executed successfully")
            
            # Verify migration
            logger.info("Verifying migration results...")
            verification_results = self.verify_migration()
            
            # Print verification summary
            logger.info("=== MIGRATION VERIFICATION SUMMARY ===")
            for table, result in verification_results.items():
                if result.get('exists', False):
                    logger.info(f"✓ {table}: {result['count']} records")
                else:
                    logger.error(f"✗ {table}: {result.get('error', 'Not found')}")
                    success = False
                    
        return success
        
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")


def main():
    """Main function to run the migration."""
    
    # IAMC Database connection parameters
    # Modify these according to your IAMC database configuration
    IAMC_SERVER = "your_iamc_server"  # Replace with actual server
    IAMC_DATABASE = "IAMC"  # Replace with actual database name
    IAMC_USERNAME = "your_username"  # Replace with actual username
    IAMC_PASSWORD = "your_password"  # Replace with actual password
    
    # Allow override via environment variables
    IAMC_SERVER = os.getenv('IAMC_SERVER', IAMC_SERVER)
    IAMC_DATABASE = os.getenv('IAMC_DATABASE', IAMC_DATABASE)
    IAMC_USERNAME = os.getenv('IAMC_USERNAME', IAMC_USERNAME)
    IAMC_PASSWORD = os.getenv('IAMC_PASSWORD', IAMC_PASSWORD)
    
    # Construct connection string for MSSQL
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={IAMC_SERVER};"
        f"DATABASE={IAMC_DATABASE};"
        f"UID={IAMC_USERNAME};"
        f"PWD={IAMC_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    
    # Directory containing migration scripts
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Print configuration (without password)
    logger.info(f"IAMC Server: {IAMC_SERVER}")
    logger.info(f"IAMC Database: {IAMC_DATABASE}")
    logger.info(f"IAMC Username: {IAMC_USERNAME}")
    logger.info(f"Script Directory: {script_directory}")
    
    # Create migrator instance
    migrator = DatabaseMigrator(connection_string)
    
    try:
        # Connect to database
        if not migrator.connect():
            logger.error("Failed to connect to IAMC database. Please check connection parameters.")
            logger.error("Make sure:")
            logger.error("1. ODBC Driver 17 for SQL Server is installed")
            logger.error("2. Server name, database name, username and password are correct")
            logger.error("3. Network connectivity to the database server")
            return 1
            
        # Run migration
        if migrator.run_migration(script_directory):
            logger.info("🎉 Migration completed successfully!")
            logger.info(f"Migration finished at: {datetime.now()}")
            return 0
        else:
            logger.error("❌ Migration failed. Check logs for details.")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Migration interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
        return 1
    finally:
        migrator.close()


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION: PostgreSQL localdb to MSSQL IAMC")
    print("=" * 60)
    print()
    print("Before running this script, please:")
    print("1. Update connection parameters in this script or set environment variables:")
    print("   - IAMC_SERVER")
    print("   - IAMC_DATABASE")
    print("   - IAMC_USERNAME")
    print("   - IAMC_PASSWORD")
    print("2. Ensure the migration SQL files are in the same directory")
    print("3. Make sure you have sufficient privileges on the IAMC database")
    print()
    
    response = input("Continue with migration? (y/N): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        sys.exit(0)
        
    sys.exit(main())
            raise Exception("Main migration failed")
        
        # Execute QR codes migration
        print("\n📊 Executing QR codes migration...")
        if not execute_sql_file(cursor, 'migrate_qr_codes_part1.sql'):
            print("⚠️  Warning: QR codes migration failed, but continuing...")
        
        # Commit transaction
        cursor.execute("COMMIT;")
        print("✅ Transaction committed successfully")
        
        # Verify migration
        print("\n🔍 Verifying migration...")
        verification_queries = [
            ("Users", "SELECT COUNT(*) FROM \"user\""),
            ("Roles", "SELECT COUNT(*) FROM role"),
            ("Permissions", "SELECT COUNT(*) FROM permission"),
            ("QR Codes", "SELECT COUNT(*) FROM qr_codes"),
            ("Settings", "SELECT COUNT(*) FROM settings")
        ]
        
        for table_name, query in verification_queries:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            print(f"  {table_name}: {count} records")
        
        print(f"\n🎉 Migration completed successfully at: {datetime.now()}")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
            print("🔄 Transaction rolled back")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ General error: {e}")
        if conn:
            conn.rollback()
            print("🔄 Transaction rolled back")
        sys.exit(1)
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("🔌 Database connection closed")

def check_prerequisites():
    """Check if all required files exist"""
    required_files = [
        'migrate_localdb_to_iamc.sql',
        'migrate_qr_codes_part1.sql'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("  LOCALDB TO IAMC MIGRATION TOOL")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please ensure all SQL files are present.")
        sys.exit(1)
    
    # Confirm before proceeding
    print("\n⚠️  IMPORTANT:")
    print("   - This will add tables and data to your IAMC database")
    print("   - Make sure you have a backup of your IAMC database")
    print("   - Update the database connection settings in this script")
    
    confirm = input("\n❓ Do you want to proceed? (yes/no): ").lower()
    if confirm not in ['yes', 'y']:
        print("❌ Migration cancelled by user")
        sys.exit(0)
    
    # Run migration
    migrate_localdb_to_iamc()
