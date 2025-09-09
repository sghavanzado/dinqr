# IAMC - Funcionários com Foto - Guia de Endpoints

## 🖼️ Novos Endpoints de Foto para Funcionários

### Upload de Foto
**POST** `/api/iamc/funcionarios/{id}/foto`

- **Descrição**: Faz upload de uma foto tipo visa para o funcionário
- **Content-Type**: `multipart/form-data`
- **Parâmetros**:
  - `foto` (file): Arquivo de imagem (PNG, JPG, JPEG)
- **Processamento**: A imagem é automaticamente redimensionada para formato tipo visa (3x4 cm, 354x472 pixels)

**Exemplo de Upload (cURL):**
```bash
curl -X POST \
  http://localhost:5000/api/iamc/funcionarios/5/foto \
  -H "Content-Type: multipart/form-data" \
  -F "foto=@caminho/para/foto.jpg"
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "message": "Foto do funcionário atualizada com sucesso",
  "foto_url": "/api/iamc/uploads/fotos_funcionarios/funcionario_5_abc12345.jpg",
  "funcionario": {
    "FuncionarioID": 5,
    "Nome": "Ana",
    "Apelido": "Silva",
    "Foto": "funcionario_5_abc12345.jpg",
    // ... outros campos
  }
}
```

### Obter Foto
**GET** `/api/iamc/funcionarios/{id}/foto`

- **Descrição**: Obtém informações sobre a foto do funcionário
- **Resposta**: JSON com URL da foto

**Exemplo:**
```bash
curl http://localhost:5000/api/iamc/funcionarios/5/foto
```

### Visualizar Foto
**GET** `/api/iamc/uploads/fotos_funcionarios/{filename}`

- **Descrição**: Serve o arquivo de foto diretamente
- **Resposta**: Arquivo de imagem

**Exemplo:**
```bash
curl http://localhost:5000/api/iamc/uploads/fotos_funcionarios/funcionario_5_abc12345.jpg
```

### Remover Foto
**DELETE** `/api/iamc/funcionarios/{id}/foto`

- **Descrição**: Remove a foto do funcionário
- **Efeito**: Remove arquivo físico e referência no banco

## 📋 Formato da Foto Tipo Visa

### Especificações Técnicas:
- **Dimensões**: 354 x 472 pixels (3x4 cm a 300 DPI)
- **Formato**: JPEG
- **Qualidade**: 90%
- **Proporção**: 3:4 (largura:altura)

### Processamento Automático:
1. **Conversão**: RGB se necessário
2. **Recorte**: Mantém proporção 3:4, corta excesso
3. **Redimensionamento**: Para tamanho exato 354x472px
4. **Compressão**: JPEG qualidade 90%

## 🧪 Testando com Postman

### 1. Upload de Foto:
1. Criar novo request POST
2. URL: `{{base_url}}/api/iamc/funcionarios/{{funcionario_id}}/foto`
3. Body → form-data
4. Adicionar key `foto` (tipo File)
5. Selecionar arquivo de imagem
6. Enviar request

### 2. Verificar Foto:
1. Usar URL retornada no upload
2. Acessar via browser ou GET request
3. Verificar se imagem está no formato correto

### 3. Atualizar Funcionário:
- O campo `Foto` agora aparece nos dados do funcionário
- Contém o nome do arquivo (sem caminho completo)
- URL completa é construída dinamicamente

## 📁 Estrutura de Arquivos

```
backend/
├── uploads/
│   └── fotos_funcionarios/
│       ├── funcionario_5_abc12345.jpg
│       ├── funcionario_6_def67890.jpg
│       └── funcionario_7_ghi11121.jpg
├── models/
│   └── iamc_funcionarios_new.py  # Campo Foto adicionado
├── controllers/
│   └── iamc_funcionarios_controller_new.py  # Métodos de foto
└── routes/
    └── iamc_funcionarios_routes.py  # Rotas de foto
```

## ⚠️ Considerações de Segurança

### Validações Implementadas:
- ✅ Tipos de arquivo permitidos (PNG, JPG, JPEG)
- ✅ Nome de arquivo seguro (secure_filename)
- ✅ Verificação de funcionário existente
- ✅ Remoção de foto anterior ao fazer upload

### Recomendações Adicionais:
- Implementar limite de tamanho de arquivo
- Adicionar autenticação/autorização
- Implementar backup de fotos
- Considerar CDN para servir imagens em produção

## 🔄 Fluxo de Uso Típico

1. **Criar Funcionário** → POST `/api/iamc/funcionarios`
2. **Upload Foto** → POST `/api/iamc/funcionarios/{id}/foto`
3. **Visualizar Dados** → GET `/api/iamc/funcionarios/{id}` (inclui campo Foto)
4. **Visualizar Foto** → GET `/api/iamc/uploads/fotos_funcionarios/{filename}`
5. **Atualizar Foto** → POST `/api/iamc/funcionarios/{id}/foto` (substitui anterior)
6. **Remover Foto** → DELETE `/api/iamc/funcionarios/{id}/foto`

---

**Status**: ✅ Implementado e pronto para teste  
**Versão**: 2.1 - Com suporte a fotos tipo visa
