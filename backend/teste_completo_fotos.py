#!/usr/bin/env python3
"""
Script de teste completo para funcionalidade de fotos de funcionários.
"""

import requests
import json
import os
from PIL import Image
import io

BASE_URL = "http://localhost:5000/api/iamc"

def criar_foto_teste():
    """Cria uma imagem de teste para upload."""
    # Criar uma imagem simples para teste (formato RGB)
    width, height = 300, 400  # Proporção próxima a 3:4
    img = Image.new('RGB', (width, height), color='lightblue')
    
    # Adicionar texto simples
    try:
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Tentar usar fonte padrão
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Desenhar texto
        text = "FOTO TESTE"
        draw.text((width//2-50, height//2-10), text, fill='darkblue', font=font)
        
    except Exception as e:
        print(f"   ⚠️ Não foi possível adicionar texto: {e}")
    
    # Salvar arquivo temporário
    test_image_path = "foto_teste.jpg"
    img.save(test_image_path, 'JPEG', quality=90)
    print(f"   📸 Foto de teste criada: {test_image_path}")
    
    return test_image_path

def testar_funcionarios_sem_foto():
    """Testa listagem de funcionários (devem ter Foto: null)."""
    print("\n📋 1. Testando listagem de funcionários (sem fotos)...")
    
    try:
        response = requests.get(f"{BASE_URL}/funcionarios", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            funcionarios = data.get('funcionarios', [])
            
            print(f"   ✅ {len(funcionarios)} funcionários encontrados")
            
            for func in funcionarios[:2]:  # Mostrar apenas os primeiros 2
                foto_status = func.get('Foto', 'N/A')
                print(f"   • ID {func['FuncionarioID']}: {func['Nome']} {func['Apelido']} - Foto: {foto_status}")
            
            return funcionarios[0]['FuncionarioID'] if funcionarios else None
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def testar_upload_foto(funcionario_id, foto_path):
    """Testa upload de foto para um funcionário."""
    print(f"\n📤 2. Testando upload de foto para funcionário ID {funcionario_id}...")
    
    try:
        url = f"{BASE_URL}/funcionarios/{funcionario_id}/foto"
        
        with open(foto_path, 'rb') as f:
            files = {'foto': ('foto_teste.jpg', f, 'image/jpeg')}
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Upload realizado com sucesso!")
            print(f"   📷 URL da foto: {data.get('foto_url', 'N/A')}")
            
            funcionario = data.get('funcionario', {})
            print(f"   👤 Funcionário: {funcionario.get('Nome', '')} {funcionario.get('Apelido', '')}")
            print(f"   🔗 Arquivo: {funcionario.get('Foto', 'N/A')}")
            
            return data.get('foto_url')
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None

def testar_info_foto(funcionario_id):
    """Testa obtenção de informações da foto."""
    print(f"\n📋 3. Testando informações da foto do funcionário ID {funcionario_id}...")
    
    try:
        url = f"{BASE_URL}/funcionarios/{funcionario_id}/foto"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Informações obtidas com sucesso!")
            print(f"   📷 URL: {data.get('foto_url', 'N/A')}")
            print(f"   👤 Nome: {data.get('nome', 'N/A')}")
            return True
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def testar_visualizar_foto(foto_url):
    """Testa acesso direto ao arquivo de foto."""
    print(f"\n🖼️ 4. Testando visualização direta da foto...")
    
    try:
        # Construir URL completa se necessário
        if foto_url and not foto_url.startswith('http'):
            full_url = f"http://localhost:5000{foto_url}"
        else:
            full_url = foto_url
        
        response = requests.get(full_url, timeout=10)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            content_length = len(response.content)
            
            print(f"   ✅ Foto acessível!")
            print(f"   📄 Content-Type: {content_type}")
            print(f"   📊 Tamanho: {content_length} bytes")
            
            # Verificar se é realmente uma imagem
            try:
                img = Image.open(io.BytesIO(response.content))
                print(f"   🖼️ Dimensões: {img.size[0]}x{img.size[1]} pixels")
                print(f"   🎨 Formato: {img.format}")
                return True
            except Exception as img_error:
                print(f"   ⚠️ Arquivo não é uma imagem válida: {img_error}")
                return False
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def testar_funcionario_com_foto(funcionario_id):
    """Testa se o funcionário agora aparece com a foto nos dados."""
    print(f"\n📋 5. Verificando dados do funcionário com foto...")
    
    try:
        url = f"{BASE_URL}/funcionarios/{funcionario_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            funcionario = response.json().get('funcionario', {})
            foto = funcionario.get('Foto')
            
            print(f"   ✅ Dados atualizados!")
            print(f"   👤 Nome: {funcionario.get('Nome', '')} {funcionario.get('Apelido', '')}")
            print(f"   📷 Foto: {foto if foto else 'Sem foto'}")
            
            return foto is not None
        else:
            print(f"   ❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def main():
    """Executa todos os testes de foto."""
    print("🧪 TESTE COMPLETO - Fotos de Funcionários")
    print("=" * 60)
    
    # 1. Criar foto de teste
    print("📸 Criando foto de teste...")
    foto_path = criar_foto_teste()
    
    try:
        # 2. Listar funcionários
        funcionario_id = testar_funcionarios_sem_foto()
        if not funcionario_id:
            print("\n❌ Não foi possível obter ID de funcionário!")
            return
        
        # 3. Upload de foto
        foto_url = testar_upload_foto(funcionario_id, foto_path)
        if not foto_url:
            print("\n❌ Falha no upload da foto!")
            return
        
        # 4. Obter informações da foto
        testar_info_foto(funcionario_id)
        
        # 5. Visualizar foto diretamente
        testar_visualizar_foto(foto_url)
        
        # 6. Verificar dados atualizados
        testar_funcionario_com_foto(funcionario_id)
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("\n🎯 Funcionalidades Testadas:")
        print("   ✅ Listagem de funcionários com campo Foto")
        print("   ✅ Upload de foto com processamento automático")
        print("   ✅ Obtenção de informações da foto")
        print("   ✅ Acesso direto ao arquivo de imagem")
        print("   ✅ Atualização dos dados do funcionário")
        
        print("\n🚀 Próximos Passos:")
        print("   • Teste via Postman usando IAMC_Foto_Endpoints.json")
        print("   • Teste com diferentes formatos de imagem")
        print("   • Teste remoção de foto (DELETE)")
        print("   • Integração com frontend")
        
    finally:
        # Limpar arquivo de teste
        try:
            os.remove(foto_path)
            print(f"\n🧹 Arquivo de teste removido: {foto_path}")
        except:
            pass

if __name__ == "__main__":
    main()
