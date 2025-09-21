#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.db_utils import obtener_conexion_local
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_qr_codes_table():
    """Check the structure of qr_codes table and create it if needed."""
    
    print("Checking qr_codes table structure...")
    
    try:
        with obtener_conexion_local() as conn:
            cursor = conn.cursor()
            
            # Check if table exists
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'qr_codes'
            """)
            table_exists = cursor.fetchone()[0] > 0
            
            if not table_exists:
                print("❌ Table qr_codes does not exist. Creating it...")
                
                # Create table
                cursor.execute("""
                    CREATE TABLE qr_codes (
                        id INTEGER IDENTITY(1,1) PRIMARY KEY,
                        contact_id INTEGER NOT NULL,
                        qr_path NVARCHAR(500),
                        hash_value NVARCHAR(255),
                        generated_at DATETIME DEFAULT GETDATE(),
                        INDEX IX_qr_codes_contact_id (contact_id)
                    )
                """)
                conn.commit()
                print("✅ Table qr_codes created successfully")
            else:
                print("✅ Table qr_codes exists")
                
                # Check table structure
                cursor.execute("""
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'qr_codes'
                    ORDER BY ORDINAL_POSITION
                """)
                columns = cursor.fetchall()
                
                print("Current table structure:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]} (Nullable: {col[2]})")
                
                # Check for required columns
                column_names = [col[0].lower() for col in columns]
                required_columns = ['contact_id', 'qr_path', 'hash_value']
                
                missing_columns = []
                for req_col in required_columns:
                    if req_col not in column_names:
                        missing_columns.append(req_col)
                
                if missing_columns:
                    print(f"❌ Missing columns: {missing_columns}")
                    
                    # Add missing columns
                    for col in missing_columns:
                        if col == 'contact_id':
                            cursor.execute("ALTER TABLE qr_codes ADD contact_id INTEGER")
                        elif col == 'qr_path':
                            cursor.execute("ALTER TABLE qr_codes ADD qr_path NVARCHAR(500)")
                        elif col == 'hash_value':
                            cursor.execute("ALTER TABLE qr_codes ADD hash_value NVARCHAR(255)")
                    
                    conn.commit()
                    print("✅ Missing columns added")
                else:
                    print("✅ All required columns present")
            
            # Check current data
            cursor.execute("SELECT COUNT(*) FROM qr_codes")
            count = cursor.fetchone()[0]
            print(f"Current records in qr_codes: {count}")
            
            if count > 0:
                cursor.execute("SELECT TOP 5 contact_id, qr_path FROM qr_codes")
                sample_data = cursor.fetchall()
                print("Sample data:")
                for row in sample_data:
                    print(f"  - Contact ID: {row[0]}, QR Path: {row[1]}")
            
    except Exception as e:
        print(f"❌ Error checking qr_codes table: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_qr_codes_table()
