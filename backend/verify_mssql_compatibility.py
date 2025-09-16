#!/usr/bin/env python3
"""
Script de verificación y corrección de compatibilidad MSSQL
Identifica problemas específicos y sugiere correcciones
"""

import sys
import os
import re
from pathlib import Path

def check_file_for_mysql_functions(file_path):
    """Verifica archivo para funciones específicas de MySQL"""
    mysql_functions = [
        'DATE_FORMAT', 'date_format',
        'CONCAT_WS', 'concat_ws',
        'IFNULL', 'ifnull',
        'SUBSTRING_INDEX', 'substring_index',
        'UNIX_TIMESTAMP', 'unix_timestamp',
        'FROM_UNIXTIME', 'from_unixtime',
        'NOW()', 'CURDATE()', 'CURTIME()',
        'YEAR()', 'MONTH()', 'DAY()'  # En context de func.
    ]
    
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                for func in mysql_functions:
                    if func.lower() in line.lower():
                        # Verificar si no es parte de un comentario
                        if not line.strip().startswith('#') and not line.strip().startswith('//'):
                            issues.append({
                                'file': file_path,
                                'line': i,
                                'function': func,
                                'content': line.strip()
                            })
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
    
    return issues

def check_sql_server_compatibility():
    """Verifica compatibilidad general con SQL Server"""
    print("VERIFICACIÓN DE COMPATIBILIDAD SQL SERVER")
    print("=" * 50)
    
    backend_path = Path('.')
    py_files = list(backend_path.rglob('*.py'))
    
    all_issues = []
    
    for py_file in py_files:
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        issues = check_file_for_mysql_functions(py_file)
        all_issues.extend(issues)
    
    if all_issues:
        print("⚠️  PROBLEMAS ENCONTRADOS:")
        print("-" * 30)
        
        for issue in all_issues:
            print(f"Archivo: {issue['file']}")
            print(f"Linha: {issue['line']}")
            print(f"Função: {issue['function']}")
            print(f"Código: {issue['content']}")
            print("-" * 30)
    else:
        print("✅ Nenhum problema de compatibilidade encontrado!")

def check_string_sizes():
    """Verifica se há strings muito grandes que possam causar problemas"""
    print("\n=== VERIFICAÇÃO DE TAMANHOS DE STRING ===")
    
    backend_path = Path('.')
    py_files = list(backend_path.rglob('models/*.py'))
    
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Procurar por String() sem tamanho especificado
                string_patterns = re.findall(r'String\(\)', content)
                if string_patterns:
                    print(f"⚠️  {py_file}: String() sem tamanho especificado (pode usar NVARCHAR(MAX))")
                
                # Procurar por String com tamanhos muito grandes
                string_sizes = re.findall(r'String\((\d+)\)', content)
                for size in string_sizes:
                    if int(size) > 4000:
                        print(f"⚠️  {py_file}: String({size}) muito grande para SQL Server (max recomendado: 4000)")
        except Exception as e:
            print(f"Erro verificando {py_file}: {e}")

def check_pagination_patterns():
    """Verifica padrões de paginação"""
    print("\n=== VERIFICAÇÃO DE PAGINAÇÃO ===")
    
    backend_path = Path('.')
    py_files = list(backend_path.rglob('controllers/*.py'))
    
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Verificar se usa LIMIT sem ORDER BY
                if '.limit(' in content and '.order_by(' not in content:
                    print(f"⚠️  {py_file}: Uso de limit() sem order_by() - obrigatório no SQL Server")
                
                # Verificar se usa offset() corretamente
                if '.offset(' in content:
                    if '.order_by(' in content:
                        print(f"✅ {py_file}: Paginação correta com ORDER BY")
                    else:
                        print(f"❌ {py_file}: offset() sem ORDER BY - causará erro no SQL Server")
        except Exception as e:
            print(f"Erro verificando {py_file}: {e}")

def suggest_improvements():
    """Sugere melhorias específicas para SQL Server"""
    print("\n=== SUGESTÕES DE MELHORIAS ===")
    
    suggestions = [
        "✅ Usar SQLAlchemy ORM evita a maioria dos problemas de compatibilidade",
        "✅ Usar func.year(), func.month() em vez de DATE_FORMAT()",
        "✅ Usar func.concat() em vez de CONCAT_WS() ou operador ||",
        "✅ Usar func.coalesce() em vez de IFNULL()",
        "✅ Sempre usar ORDER BY com LIMIT/OFFSET",
        "✅ Usar String(4000) em vez de String() ou Text para campos grandes",
        "✅ Usar Boolean em vez de TINYINT para campos booleanos",
        "✅ Configurar pool_pre_ping=True para conexões persistentes",
        "✅ Usar TrustServerCertificate=yes para conexões SSL"
    ]
    
    for suggestion in suggestions:
        print(suggestion)

def main():
    """Execução principal"""
    check_sql_server_compatibility()
    check_string_sizes()
    check_pagination_patterns()
    suggest_improvements()
    
    print("\n" + "=" * 50)
    print("VERIFICAÇÃO COMPLETA")
    print("=" * 50)
    print("Para garantir total compatibilidade com SQL Server:")
    print("1. ✅ Use sempre SQLAlchemy ORM")
    print("2. ✅ Evite SQL raw quando possível")
    print("3. ✅ Use func.* para funções de banco")
    print("4. ✅ Sempre use ORDER BY com paginação")
    print("5. ✅ Teste em ambiente SQL Server real")

if __name__ == '__main__':
    main()
