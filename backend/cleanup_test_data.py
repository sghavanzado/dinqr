#!/usr/bin/env python3
"""
Cleanup Test Data - Passes Configuration
Script to clean up test themes and formats created during development/testing
"""

import sys
import os
sys.path.append('.')

from utils.db_utils import obtener_conexion_local
import requests

def cleanup_test_themes():
    """Remove themes that contain 'test', 'demo', or 'example' in the name"""
    try:
        conn = obtener_conexion_local()
        cursor = conn.cursor()
        
        # Find test themes
        cursor.execute("""
            SELECT id, nome FROM pass_temas_avancado 
            WHERE LOWER(nome) LIKE '%test%' 
               OR LOWER(nome) LIKE '%demo%' 
               OR LOWER(nome) LIKE '%example%'
               OR LOWER(nome) LIKE '%api%'
        """)
        
        test_themes = cursor.fetchall()
        
        if test_themes:
            print(f"🧹 Found {len(test_themes)} test themes to clean:")
            for theme_id, theme_name in test_themes:
                print(f"   - ID {theme_id}: {theme_name}")
            
            confirm = input("\nDelete these test themes? (y/N): ").lower().strip()
            if confirm == 'y':
                for theme_id, theme_name in test_themes:
                    cursor.execute("DELETE FROM pass_temas_avancado WHERE id = ?", (theme_id,))
                    print(f"   ✅ Deleted theme: {theme_name}")
                
                conn.commit()
                print(f"✅ Successfully cleaned {len(test_themes)} test themes")
            else:
                print("❌ Cleanup cancelled")
        else:
            print("✅ No test themes found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error cleaning test themes: {e}")

def cleanup_test_formats():
    """Remove formats that contain 'test', 'demo', or 'example' in the name"""
    try:
        conn = obtener_conexion_local()
        cursor = conn.cursor()
        
        # Find test formats
        cursor.execute("""
            SELECT id, nome FROM pass_formatos_avancado 
            WHERE LOWER(nome) LIKE '%test%' 
               OR LOWER(nome) LIKE '%demo%' 
               OR LOWER(nome) LIKE '%example%'
               OR LOWER(nome) LIKE '%api%'
        """)
        
        test_formats = cursor.fetchall()
        
        if test_formats:
            print(f"🧹 Found {len(test_formats)} test formats to clean:")
            for format_id, format_name in test_formats:
                print(f"   - ID {format_id}: {format_name}")
            
            confirm = input("\nDelete these test formats? (y/N): ").lower().strip()
            if confirm == 'y':
                for format_id, format_name in test_formats:
                    cursor.execute("DELETE FROM pass_formatos_avancado WHERE id = ?", (format_id,))
                    print(f"   ✅ Deleted format: {format_name}")
                
                conn.commit()
                print(f"✅ Successfully cleaned {len(test_formats)} test formats")
            else:
                print("❌ Cleanup cancelled")
        else:
            print("✅ No test formats found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error cleaning test formats: {e}")

def show_current_data():
    """Show current themes and formats in database"""
    try:
        conn = obtener_conexion_local()
        cursor = conn.cursor()
        
        print("📊 CURRENT DATABASE STATE:")
        
        # Show themes
        cursor.execute("SELECT id, nome, cor_primaria, ativo FROM pass_temas_avancado ORDER BY id")
        themes = cursor.fetchall()
        print(f"   🎨 Themes ({len(themes)}):")
        for theme_id, name, color, active in themes:
            status = "✅" if active else "❌"
            print(f"      {status} ID {theme_id}: {name} ({color})")
        
        # Show formats
        cursor.execute("SELECT id, nome, extensao, ativo FROM pass_formatos_avancado ORDER BY id")
        formats = cursor.fetchall()
        print(f"   📄 Formats ({len(formats)}):")
        for format_id, name, extension, active in formats:
            status = "✅" if active else "❌"
            print(f"      {status} ID {format_id}: {name} (.{extension})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error showing current data: {e}")

def reset_to_defaults():
    """Reset database to default themes and formats only"""
    try:
        print("⚠️  WARNING: This will delete ALL custom themes and formats!")
        print("Only the original 4 default themes and 5 default formats will remain.")
        
        confirm = input("\nAre you sure you want to reset to defaults? (type 'RESET' to confirm): ").strip()
        if confirm != 'RESET':
            print("❌ Reset cancelled")
            return
        
        conn = obtener_conexion_local()
        cursor = conn.cursor()
        
        # Count current data
        cursor.execute("SELECT COUNT(*) FROM pass_temas_avancado")
        theme_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pass_formatos_avancado")
        format_count = cursor.fetchone()[0]
        
        # Delete all non-default themes (keep first 4)
        cursor.execute("DELETE FROM pass_temas_avancado WHERE id > 4")
        deleted_themes = cursor.rowcount
        
        # Delete all non-default formats (keep first 5)
        cursor.execute("DELETE FROM pass_formatos_avancado WHERE id > 5")
        deleted_formats = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Reset completed:")
        print(f"   - Deleted {deleted_themes} custom themes")
        print(f"   - Deleted {deleted_formats} custom formats")
        print(f"   - Kept 4 default themes and 5 default formats")
        
    except Exception as e:
        print(f"❌ Error resetting to defaults: {e}")

def main():
    print("🧹 === CLEANUP TOOL: PASSES CONFIGURATION ===\n")
    
    show_current_data()
    
    print("\nSelect an option:")
    print("1. Clean test themes only")
    print("2. Clean test formats only")
    print("3. Clean both test themes and formats")
    print("4. Reset to default data only (DANGEROUS)")
    print("5. Show current data")
    print("0. Exit")
    
    try:
        choice = int(input("\nEnter your choice (0-5): ").strip())
        
        if choice == 1:
            cleanup_test_themes()
        elif choice == 2:
            cleanup_test_formats()
        elif choice == 3:
            cleanup_test_themes()
            cleanup_test_formats()
        elif choice == 4:
            reset_to_defaults()
        elif choice == 5:
            show_current_data()
        elif choice == 0:
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")
            
    except ValueError:
        print("❌ Please enter a valid number")
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")

if __name__ == "__main__":
    main()
