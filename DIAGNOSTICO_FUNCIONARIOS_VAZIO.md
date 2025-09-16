# 🔍 DIAGNÓSTICO: Lista de Funcionários Vazia

## 🎯 Problema
A lista de funcionários está aparecendo vazia mesmo tendo dados na base de dados.

## 📋 Passos de Diagnóstico

### 1. ✅ Verificar se o Backend está Rodando

**Abrir terminal e executar:**
```bash
cd backend
python app.py
```

**Verificar se aparece:**
- ✅ "DINQR Backend Application Starting"
- ✅ Lista de rotas registradas incluindo `/api/iamc/funcionarios`
- ✅ Servidor rodando na porta 5000

### 2. 🌐 Testar Endpoints Manualmente

**Abrir navegador e testar:**

1. **Status:** http://localhost:5000/api/iamc/status
   - Deve retornar: `{"success": true, "module": "IAMC - Gestão de Funcionários"...}`

2. **Funcionários:** http://localhost:5000/api/iamc/funcionarios
   - Deve retornar: `{"success": true, "data": [...], "total": X}`

### 3. 🔧 Verificar Console do Navegador

**No frontend (http://localhost:3000/rrhh/funcionarios):**

1. Abrir DevTools (F12)
2. Ir para aba **Console**
3. Recarregar a página
4. Procurar por mensagens que começam com:
   - 🧪 "Testando conexão com backend..."
   - 🔍 "Carregando funcionários com filtros..."
   - 📊 "Resposta do backend:"
   - ✅ ou ❌ para sucesso/erro

### 4. 📡 Verificar Network Tab

**No DevTools:**
1. Ir para aba **Network**
2. Recarregar página
3. Procurar por requisição para `/api/iamc/funcionarios`
4. Verificar:
   - Status Code (deve ser 200)
   - Response (deve ter `success: true`)

## 🐛 Problemas Comuns e Soluções

### ❌ Backend não está rodando
**Sintomas:** Erro de conexão no console
**Solução:** 
```bash
cd backend
python app.py
```

### ❌ CORS Error
**Sintomas:** "Access to fetch blocked by CORS policy"
**Solução:** Verificar configuração CORS no backend

### ❌ Status 404
**Sintomas:** "404 Not Found" na requisição
**Solução:** Verificar se as rotas estão registradas corretamente

### ❌ Status 500
**Sintomas:** "500 Internal Server Error"
**Solução:** Verificar logs do backend para erro de SQL

### ❌ Base de dados vazia
**Sintomas:** Resposta success=true mas data=[]
**Solução:** Verificar se há funcionários na tabela `funcionarios`

## 🔧 Scripts de Diagnóstico

### Script Python (Diagnóstico Completo)
```bash
python diagnosticar_funcionarios_vazio.py
```

### Script Frontend (Logs Detalhados)
- Os logs já estão habilitados no código
- Verifique o console do navegador

## 📊 Estrutura de Dados Esperada

### Backend Response
```json
{
  "success": true,
  "data": [
    {
      "funcionarioID": 1,
      "nome": "João Silva",
      "email": "joao@empresa.com",
      "estadoFuncionario": "Activo",
      "dataAdmissao": "2023-01-15",
      "departamentoID": 1,
      "cargoID": 1
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 10,
  "pages": 1
}
```

### Frontend State
```javascript
funcionarios: Array[Funcionario]
totalCount: number
loading: boolean
```

## 🚨 Checklist de Verificação

- [ ] Backend está rodando na porta 5000
- [ ] Endpoint `/api/iamc/status` retorna success=true
- [ ] Endpoint `/api/iamc/funcionarios` retorna dados
- [ ] Console do frontend não mostra erros de rede
- [ ] Network tab mostra status 200 nas requisições
- [ ] Base de dados tem funcionários na tabela
- [ ] CORS está configurado corretamente

## 💡 Próximos Passos

1. **Se backend não roda:** Verificar dependências Python
2. **Se endpoint não responde:** Verificar rotas e conexão DB
3. **Se dados não aparecem:** Verificar mapeamento frontend-backend
4. **Se ainda não funciona:** Verificar logs detalhados

## 🆘 Suporte

Se o problema persistir, verifique:
- Logs do backend (`backend/logs/app.log`)
- Console do navegador (mensagens de erro)
- Network tab (requisições e respostas)
- Base de dados (conectividade e dados)

---
**📝 Nota:** O código já foi atualizado com logs detalhados para facilitar o diagnóstico.
