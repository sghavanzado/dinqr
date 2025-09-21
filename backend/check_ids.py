#!/usr/bin/env python3
"""
Script para verificar IDs de funcionarios IAMC vs QR codes
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extensions import IAMCSession
from models.iamc_funcionarios_new import Funcionario
from utils.db_utils import obtener_conexion_local

print("=== VERIFICANDO IDs ===")

# 1. Ver IDs de IAMC Funcionarios
session = IAMCSession()
try:
    funcs = session.query(Funcionario.FuncionarioID, Funcionario.Nome, Funcionario.Apelido).limit(10).all()
    print(f"\n📋 Funcionarios en IAMC (primeros 10):")
    for func in funcs:
        print(f"  ID: {func.FuncionarioID} - {func.Nome} {func.Apelido}")
finally:
    session.close()

# 2. Ver IDs en QR codes
try:
    conn_local = obtener_conexion_local()
    cursor = conn_local.cursor()
    cursor.execute("SELECT DISTINCT contact_id FROM qr_codes LIMIT 10")
    qr_ids = [row[0] for row in cursor.fetchall()]
    print(f"\n🔗 QR Codes existentes (primeros 10):")
    for qr_id in qr_ids:
        print(f"  QR ID: {qr_id}")
    conn_local.close()
except Exception as e:
    print(f"Error al consultar QR codes: {e}")

print(f"\n🔍 DIAGNÓSTICO:")
print(f"- Los IDs de IAMC van del 1-5 aproximadamente") 
print(f"- Los QR codes tienen IDs legacy como 102, 106, etc.")
print(f"- Por eso no hay matches en los JOINs")
print(f"- Necesitamos generar QR codes para los IDs de IAMC (1-5)")
