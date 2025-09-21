#!/usr/bin/env python3
"""Script para verificar funcionarios con y sin QR."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Checking funcionarios with and without QR codes...")

try:
    # 1. Verificar QR codes en base local
    from utils.db_utils import obtener_conexion_local
    
    conn = obtener_conexion_local()
    cursor = conn.cursor()
    cursor.execute("SELECT contact_id FROM qr_codes")
    qr_ids = [str(row[0]) for row in cursor.fetchall()]
    conn.close()
    
    print(f"QR codes found for IDs: {qr_ids}")
    
    # 2. Verificar total de funcionarios en IAMC
    from extensions import IAMCSession
    from models.iamc_funcionarios_new import Funcionario
    
    session = IAMCSession()
    
    # Total de funcionarios
    total_funcionarios = session.query(Funcionario).count()
    print(f"Total funcionarios in IAMC: {total_funcionarios}")
    
    # Funcionarios con QR (que están en qr_codes)
    funcionarios_con_qr = session.query(Funcionario).filter(Funcionario.FuncionarioID.in_(qr_ids)).count()
    print(f"Funcionarios with QR codes: {funcionarios_con_qr}")
    
    # Funcionarios sin QR (que NO están en qr_codes)
    funcionarios_sin_qr = session.query(Funcionario).filter(~Funcionario.FuncionarioID.in_(qr_ids)).count()
    print(f"Funcionarios without QR codes: {funcionarios_sin_qr}")
    
    # Mostrar algunos ejemplos de funcionarios sin QR
    ejemplos_sin_qr = session.query(Funcionario).filter(~Funcionario.FuncionarioID.in_(qr_ids)).limit(5).all()
    
    if ejemplos_sin_qr:
        print("\nExamples of funcionarios WITHOUT QR codes:")
        for func in ejemplos_sin_qr:
            print(f"  - ID: {func.FuncionarioID}, Nome: {func.Nome}, Apelido: {func.Apelido}")
    else:
        print("\nNo funcionarios without QR codes found")
    
    session.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
