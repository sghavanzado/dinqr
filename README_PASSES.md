# 🆔 DINQR - Sistema de Passes de Funcionários

## 📋 Visão Geral

Este módulo implementa um sistema completo de geração de passes de identificação para funcionários no formato CR80 (cartão de crédito). Integrado ao sistema RRHH do DINQR, permite gerar passes personalizados com foto, dados do funcionário, código QR e logótipo da empresa.

## 🎯 Funcionalidades

### ✅ Geração de Passes
- **Formato CR80**: Dimensões padrão de cartão de crédito (85.6mm × 53.98mm)
- **Alta Resolução**: Otimizado para impressão em 300 DPI
- **Múltiplos Formatos**: PDF (para impressão) e HTML (para pré-visualização)
- **Responsivo**: Layout adaptado para diferentes tamanhos

### ✅ Elementos do Passe
- **Foto do Funcionário**: Integração com sistema de fotos existente
- **Dados Pessoais**: Nome completo e ID do funcionário
- **Dados Profissionais**: Cargo e departamento
- **Código QR**: Gerado dinamicamente com informações do funcionário
- **Logótipo da Empresa**: Personalizável por tema
- **Fundo Estilizado**: Múltiplos temas disponíveis

### ✅ Temas Disponíveis
- **Default**: Tema corporativo padrão (azul)
- **Corporate**: Estilo empresarial elegante (cinza)
- **Modern**: Design moderno (gradiente)
- **Professional**: Visual profissional (verde)

## 🏗️ Arquitetura

### Backend (Flask)
```
backend/
├── routes/
│   ├── passes_routes.py      # Endpoints da API
│   └── example_input.json    # Exemplo de payload
├── templates/
│   └── employee_pass_template.html  # Template HTML do passe
└── static/css/
    └── employee_pass.css     # Estilos CSS com temas
```

### Frontend (React/TypeScript)
```
frontend/src/
├── pages/rrhh/
│   └── PassesList.tsx        # Lista de funcionários para passes
└── components/funcionarios/
    └── EmployeePass.tsx      # Componente de geração de passes
```

### Integração
- **Rotas**: Registradas no blueprint `iamc_bp` com prefixo `/passes`
- **Navegação**: Menu "Impressão" > "Passes de Funcionários"
- **API**: Endpoints RESTful integrados com sistema IAMC

## 🌐 Endpoints da API

### Base URL: `/api/iamc/passes`

#### **Gerar Passe Individual**
```http
POST /api/iamc/passes/gerar
Content-Type: application/json

{
  "funcionario_id": 1,
  "incluir_qr": true,
  "tema": "default",
  "formato_saida": "pdf"
}
```

**Resposta (PDF):**
- Content-Type: `application/pdf`
- Arquivo PDF pronto para impressão

**Resposta (HTML):**
- Content-Type: `text/html`
- HTML renderizado para pré-visualização

#### **Gerar Passes em Lote**
```http
POST /api/iamc/passes/lote
Content-Type: application/json

{
  "funcionarios_ids": [1, 2, 3, 4, 5],
  "incluir_qr": true,
  "tema": "corporate",
  "formato_saida": "pdf"
}
```

#### **Pré-visualização HTML**
```http
GET /api/iamc/passes/preview/{funcionario_id}
```

#### **Configuração Disponível**
```http
GET /api/iamc/passes/configuracao
```

**Resposta:**
```json
{
  "data": {
    "temas_disponiveis": [
      {
        "id": "default",
        "nome": "Corporativo",
        "cor_primaria": "#1976d2"
      }
    ],
    "formatos_saida": [
      {
        "id": "pdf",
        "nome": "PDF",
        "descricao": "Para impressão"
      }
    ],
    "dimensoes": {
      "formato": "CR80",
      "largura_mm": 85.6,
      "altura_mm": 53.98,
      "dpi_recomendado": 300
    },
    "validade_padrao_dias": 365
  }
}
```

## 🎨 Frontend - Interface de Utilizador

### Página de Passes (`/rrhh/passes`)
- **Lista de Funcionários**: Grid responsivo com cards
- **Filtros Avançados**: Por departamento, cargo, estado e pesquisa
- **Ações Rápidas**: Botão "Gerar Passe" em cada card
- **Estados Visuais**: Loading, vazio, erro

### Componente EmployeePass
- **Configuração**: Seleção de tema, formato e opções
- **Pré-visualização**: Modal com iframe para HTML
- **Download**: Geração e download automático de PDF
- **Feedback**: Notificações de sucesso/erro

## 📏 Especificações Técnicas

### Dimensões do Passe (CR80)
- **Largura**: 85.6mm (1011px a 300 DPI)
- **Altura**: 53.98mm (637px a 300 DPI)
- **Proporção**: 1.586:1 (padrão internacional)
- **Margens**: 3mm mínimo para impressão

### Qualidade de Impressão
- **Resolução**: 300 DPI mínimo
- **Formato**: PDF vectorial para melhor qualidade
- **Cores**: CMYK compatível
- **Fontes**: Web fonts incluídas no CSS

### Código QR
- **Dados**: JSON com informações do funcionário
- **Formato**: Base64 incorporado no HTML
- **Tamanho**: 80x80px (dimensão fixa)
- **Correção de Erro**: Nível M (15%)

## 🚀 Como Utilizar

### 1. Aceder à Interface
```
http://localhost:3000/rrhh/passes
```

### 2. Filtrar Funcionários
- Use os filtros para encontrar funcionários específicos
- Pesquise por nome ou apelido
- Filtre por departamento, cargo ou estado

### 3. Gerar Passe
1. Clique no ícone de "Gerar Passe" no card do funcionário
2. Selecione o tema desejado
3. Escolha o formato (PDF para impressão, HTML para visualização)
4. Marque/desmarque "Incluir Código QR"
5. Clique "Gerar Passe" ou "Pré-visualizar"

### 4. Impressão
- **PDF**: Faça download e imprima em impressora com qualidade fotográfica
- **Papel**: Use papel cartão ou PVC branco
- **Configurações**: 300 DPI, sem redimensionamento
- **Margem**: Configure para "sem margens" ou "margem mínima"

## 🔧 Configuração e Personalização

### Adicionar Novo Tema
1. **CSS**: Adicione variáveis no arquivo `employee_pass.css`
```css
/* Novo tema */
.employee-pass[data-theme="novo-tema"] {
  --primary-color: #your-color;
  --secondary-color: #your-secondary;
  --background-gradient: linear-gradient(...);
}
```

2. **Backend**: Adicione à lista de temas em `passes_routes.py`
```python
temas_disponiveis = [
    # ... temas existentes
    {
        "id": "novo-tema",
        "nome": "Novo Tema",
        "cor_primaria": "#your-color"
    }
]
```

### Personalizar Logótipo
1. Substitua o arquivo `logosonangol.jpg` na pasta `backend/uploads/logos/`
2. Ou adicione lógica para múltiplas empresas no template

### Modificar Template
- **HTML**: Edite `employee_pass_template.html`
- **CSS**: Modifique estilos em `employee_pass.css`
- **Variáveis**: Use placeholders `{{ variavel }}` no template

## 🧪 Testes e Desenvolvimento

### Testar API com cURL
```bash
# Gerar passe individual
curl -X POST http://localhost:5000/api/iamc/passes/gerar \
  -H "Content-Type: application/json" \
  -d '{"funcionario_id": 1, "incluir_qr": true, "tema": "default", "formato_saida": "pdf"}' \
  --output passe.pdf

# Obter configuração
curl http://localhost:5000/api/iamc/passes/configuracao

# Pré-visualização
curl http://localhost:5000/api/iamc/passes/preview/1 > preview.html
```

### Desenvolvimento Local
1. **Backend**: Execute `python app.py` na pasta backend
2. **Frontend**: Execute `npm start` na pasta frontend
3. **Navegue**: Para `http://localhost:3000/rrhh/passes`

## 🔍 Resolução de Problemas

### Problemas Comuns
1. **Foto não aparece**: Verifique se o funcionário tem foto cadastrada
2. **QR não gera**: Verifique conexão com API e dados do funcionário
3. **PDF em branco**: Problema de renderização, teste HTML primeiro
4. **Estilos não aplicados**: Verifique caminho do CSS no template

### Logs e Debugging
- **Backend**: Logs em `backend/logs/app.log`
- **Frontend**: Console do navegador
- **API**: Use ferramentas como Postman para testar endpoints

### Melhorias Futuras
- [ ] Múltiplos logótipos por empresa
- [ ] Editor visual de temas
- [ ] Templates personalizáveis
- [ ] Impressão direta (sem download)
- [ ] Gestão de validade de passes
- [ ] Histórico de passes gerados
- [ ] Assinatura digital nos passes

## 📞 Suporte

Para suporte técnico ou dúvidas sobre implementação:
- Consulte logs do sistema
- Verifique configuração de base de dados IAMC
- Teste endpoints individualmente
- Valide permissões de ficheiros e pastas

---

**Sistema de Passes DINQR v1.0**
*Implementação completa em Português (Portugal)*
