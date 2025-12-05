"""
Script de diagnóstico para verificar el problema de CV en Dashboard
"""
import sys
sys.path.append('c:/Users/administrator.GTS/Develop/dinqr/backend')

from utils.db_utils import obtener_conexion_local

print("="*60)
print("DIAGNOSTICO: Tabla cv_codes y qr_codes")
print("="*60)

try:
    with obtener_conexion_local() as conn:
        cursor = conn.cursor()
        
        # Verificar tabla cv_codes
        print("\n1. Verificando tabla cv_codes...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'cv_codes'
        """)
        tabla_cv = cursor.fetchone()
        if tabla_cv:
            print("   [OK] Tabla cv_codes EXISTE")
        else:
            print("   [ERROR] Tabla cv_codes NO EXISTE")
        
        # Verificar tabla qr_codes
        print("\n2. Verificando tabla qr_codes...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'qr_codes'
        """)
        tabla_qr = cursor.fetchone()
        if tabla_qr:
            print("   [OK] Tabla qr_codes EXISTE")
        else:
            print("   [ERROR] Tabla qr_codes NO EXISTE")
        
        # Contar registros en cv_codes
        print("\n3. Contando registros en cv_codes...")
        cursor.execute("SELECT COUNT(*) FROM cv_codes")
        count_cv = cursor.fetchone()[0]
        print(f"   Total de CV generados: {count_cv}")
        
        # Mostrar IDs en cv_codes
        if count_cv > 0:
            cursor.execute("SELECT contact_id, nombre FROM cv_codes LIMIT 10")
            cv_records = cursor.fetchall()
            print("\n   Primeros registros en cv_codes:")
            for record in cv_records:
                print(f"      - SAP: {record[0]}, Nombre: {record[1]}")
        
        # Contar registros en qr_codes
        print("\n4. Contando registros en qr_codes...")
        cursor.execute("SELECT COUNT(*) FROM qr_codes")
        count_qr = cursor.fetchone()[0]
        print(f"   Total de QR generados: {count_qr}")
        
        # Mostrar IDs en qr_codes
        if count_qr > 0:
            cursor.execute("SELECT contact_id, nombre FROM qr_codes LIMIT 10")
            qr_records = cursor.fetchall()
            print("\n   Primeros registros en qr_codes:")
            for record in qr_records:
                print(f"      - SAP: {record[0]}, Nombre: {record[1]}")
        
        # Probar UNION
        print("\n5. Probando consulta UNION...")
        cursor.execute("""
            SELECT contact_id FROM qr_codes
            UNION
            SELECT contact_id FROM cv_codes
        """)
        union_ids = [row[0] for row in cursor.fetchall()]
        print(f"   Total de IDs unicos (UNION): {len(union_ids)}")
        print(f"   IDs: {union_ids}")
        
        print("\n" + "="*60)
        print("RESUMEN:")
        print("="*60)
        print(f"QR normales: {count_qr}")
        print(f"CVs generados: {count_cv}")
        print(f"Total unico (UNION): {len(union_ids)}")
        print("="*60)
        
except Exception as e:
    print(f"\n[ERROR]: {str(e)}")
    import traceback
    traceback.print_exc()
