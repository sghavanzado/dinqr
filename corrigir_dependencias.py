#!/usr/bin/env python3
"""
Script para corrigir problemas de dependências no frontend
"""

import os
import json
from pathlib import Path

def verificar_package_json():
    """Verifica se todas as dependências necessárias estão instaladas"""
    print("📦 Verificando package.json...")
    
    package_json_path = "frontend/package.json"
    
    if not os.path.exists(package_json_path):
        print("   ❌ package.json não encontrado")
        return False
    
    with open(package_json_path, 'r', encoding='utf-8') as f:
        package_data = json.load(f)
    
    dependencies = package_data.get('dependencies', {})
    
    # Dependências necessárias para MUI DatePickers (se usarmos)
    deps_necessarias = {
        '@mui/x-date-pickers': 'Para date pickers',
        '@mui/material': 'Para componentes Material-UI',
        '@mui/icons-material': 'Para ícones',
        'react': 'Framework React',
        'axios': 'Para chamadas API'
    }
    
    deps_opcionais = {
        'date-fns': 'Para formatação de datas (opcional)'
    }
    
    print("   ✅ Dependências essenciais:")
    for dep, desc in deps_necessarias.items():
        if dep in dependencies:
            print(f"      • {dep}: {dependencies[dep]} - {desc}")
        else:
            print(f"      ❌ {dep}: FALTANDO - {desc}")
    
    print("   🔧 Dependências opcionais:")
    for dep, desc in deps_opcionais.items():
        if dep in dependencies:
            print(f"      • {dep}: {dependencies[dep]} - {desc}")
        else:
            print(f"      ⚪ {dep}: não instalado - {desc}")
    
    return True

def verificar_imports_problematicos():
    """Verifica se há imports problemáticos relacionados a date-fns"""
    print("\n🔍 Verificando imports problemáticos...")
    
    arquivos_tsx = [
        "frontend/src/components/funcionarios/FuncionarioFormDialog.tsx",
        "frontend/src/components/funcionarios/FuncionarioViewDialog.tsx"
    ]
    
    problemas_encontrados = []
    
    for arquivo in arquivos_tsx:
        if not os.path.exists(arquivo):
            print(f"   ⚪ {arquivo} - não encontrado")
            continue
            
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar imports problemáticos
        imports_problematicos = [
            "from 'date-fns/locale'",
            "from \"date-fns/locale\"",
            "import { ptBR }",
            "adapterLocale={ptBR}"
        ]
        
        for i, linha in enumerate(conteudo.split('\n'), 1):
            for import_prob in imports_problematicos:
                if import_prob in linha:
                    problemas_encontrados.append(f"{arquivo}:{i} - {linha.strip()}")
    
    if problemas_encontrados:
        print("   ❌ Problemas encontrados:")
        for problema in problemas_encontrados:
            print(f"      {problema}")
        return False
    else:
        print("   ✅ Nenhum import problemático encontrado")
        return True

def sugerir_solucoes():
    """Sugere soluções para os problemas encontrados"""
    print("\n💡 SOLUÇÕES SUGERIDAS:")
    print("=" * 50)
    
    print("1️⃣ OPÇÃO SIMPLES (Recomendada):")
    print("   • Usar TextField com type='date'")
    print("   • Não requer dependências extras")
    print("   • Funciona perfeitamente para input de datas")
    print("   • Já implementado nos arquivos")
    
    print("\n2️⃣ OPÇÃO AVANÇADA:")
    print("   • Instalar date-fns: npm install date-fns")
    print("   • Usar DatePicker do MUI com localização")
    print("   • Melhor UX mas mais complexo")
    
    print("\n3️⃣ VERIFICAÇÃO:")
    print("   • Reiniciar o servidor de desenvolvimento")
    print("   • Limpar cache: npm run build --clean")
    print("   • Verificar console para outros erros")

def main():
    print("🔧 CORRETOR DE DEPENDÊNCIAS - Frontend")
    print("=" * 60)
    
    package_ok = verificar_package_json()
    imports_ok = verificar_imports_problematicos()
    
    print("\n📋 RESUMO:")
    print(f"   Package.json: {'✅ OK' if package_ok else '❌ PROBLEMA'}")
    print(f"   Imports: {'✅ OK' if imports_ok else '❌ PROBLEMA'}")
    
    if imports_ok:
        print("\n🎉 Todos os imports estão corretos!")
        print("   O frontend deveria compilar sem erros agora.")
    else:
        print("\n⚠️  Alguns imports ainda têm problemas.")
    
    sugerir_solucoes()
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("   1. Verifique se o servidor está rodando: npm start")
    print("   2. Acesse: http://localhost:3000/rrhh/funcionarios")
    print("   3. Teste todas as funcionalidades CRUD")

if __name__ == "__main__":
    main()
