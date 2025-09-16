#!/usr/bin/env python3
"""
Script de verificação rápida para verificar se os imports do frontend estão corretos
"""

import os
import re
from pathlib import Path

def verificar_imports_frontend():
    """Verifica se há imports problemáticos no frontend"""
    print("🔍 Verificando Imports do Frontend...")
    
    frontend_dir = Path("frontend/src")
    problemas = []
    
    # Padrões problemáticos
    padroes_problematicos = [
        r"from '[^']*rrhh'(?!\.)",  # Import sem extensão ou com extensão incorreta
        r"from \"[^\"]*rrhh\"(?!\.)",  # Mesmo padrão com aspas duplas
    ]
    
    # Arquivos para verificar
    arquivos_tsx = list(frontend_dir.rglob("*.tsx")) + list(frontend_dir.rglob("*.ts"))
    
    for arquivo in arquivos_tsx:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                
            # Verificar cada padrão problemático
            for i, linha in enumerate(conteudo.split('\n'), 1):
                for padrao in padroes_problematicos:
                    if re.search(padrao, linha):
                        problemas.append(f"{arquivo}:{i} - {linha.strip()}")
        except Exception as e:
            print(f"   ⚠️  Erro ao ler {arquivo}: {e}")
    
    if problemas:
        print(f"   ❌ Encontrados {len(problemas)} imports problemáticos:")
        for problema in problemas[:10]:  # Mostrar apenas os primeiros 10
            print(f"      {problema}")
        if len(problemas) > 10:
            print(f"      ... e mais {len(problemas) - 10} problemas")
        return False
    else:
        print("   ✅ Todos os imports estão corretos!")
        return True

def verificar_arquivos_api():
    """Verifica se os arquivos de API existem"""
    print("\n📁 Verificando Arquivos de API...")
    
    arquivos_api = [
        "frontend/src/services/api/rrhh.ts",
        "frontend/src/services/api/funcionarios.ts",
        "frontend/src/types/rrhh.ts"
    ]
    
    todos_existem = True
    for arquivo in arquivos_api:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - NÃO ENCONTRADO")
            todos_existem = False
    
    return todos_existem

def verificar_exports():
    """Verifica se as funções estão sendo exportadas corretamente"""
    print("\n📤 Verificando Exports...")
    
    arquivo_funcionarios = "frontend/src/services/api/funcionarios.ts"
    funcoes_necessarias = [
        "getFuncionarios",
        "createFuncionario", 
        "updateFuncionario",
        "deleteFuncionario",
        "getFotoInfo",
        "uploadFoto",
        "deleteFoto",
        "getDepartamentos",
        "getCargos"
    ]
    
    if not os.path.exists(arquivo_funcionarios):
        print(f"   ❌ {arquivo_funcionarios} não encontrado")
        return False
    
    try:
        with open(arquivo_funcionarios, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        funcoes_encontradas = []
        funcoes_nao_encontradas = []
        
        for funcao in funcoes_necessarias:
            if f"export const {funcao}" in conteudo:
                funcoes_encontradas.append(funcao)
            else:
                funcoes_nao_encontradas.append(funcao)
        
        print(f"   ✅ Encontradas {len(funcoes_encontradas)} funções:")
        for funcao in funcoes_encontradas:
            print(f"      • {funcao}")
        
        if funcoes_nao_encontradas:
            print(f"   ❌ Faltando {len(funcoes_nao_encontradas)} funções:")
            for funcao in funcoes_nao_encontradas:
                print(f"      • {funcao}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao ler arquivo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Verificação de Imports do Frontend")
    print("=" * 50)
    
    arquivos_ok = verificar_arquivos_api()
    exports_ok = verificar_exports()
    imports_ok = verificar_imports_frontend()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO:")
    print(f"   Arquivos API: {'✅ OK' if arquivos_ok else '❌ PROBLEMA'}")
    print(f"   Exports: {'✅ OK' if exports_ok else '❌ PROBLEMA'}")
    print(f"   Imports: {'✅ OK' if imports_ok else '❌ PROBLEMA'}")
    
    if all([arquivos_ok, exports_ok, imports_ok]):
        print("\n🎉 Todos os imports estão funcionando corretamente!")
        print("   O frontend deveria compilar sem erros agora.")
    else:
        print("\n⚠️  Alguns problemas foram encontrados.")
        print("   Corrija os problemas listados acima.")
    
    print("\n💡 Dica: Se ainda houver erros, tente:")
    print("   1. Parar o servidor (Ctrl+C)")
    print("   2. Limpar cache: npm run build --clean")
    print("   3. Reinstalar: npm install")
    print("   4. Reiniciar: npm start")
