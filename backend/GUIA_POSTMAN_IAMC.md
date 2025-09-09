# 🧪 Guia de Teste com Postman - IAMC

## 📋 Passo a Passo para Testar com Postman

### 1️⃣ Importar a Collection
1. Abra o Postman
2. Clique em "Import" 
3. Selecione o arquivo: `IAMC_Postman_Collection_Melhorada.json`
4. Importe também o Environment: `IAMC_Postman_Environment.json`

### 2️⃣ Configurar Variáveis
- **base_url**: `http://127.0.0.1:5000` (ou onde seu servidor está rodando)
- Outras variáveis serão preenchidas automaticamente pelos testes

### 3️⃣ Ordem de Teste Recomendada

#### ✅ 1. Verificar Status
```
GET {{base_url}}/api/iamc/status
```
- **Objetivo**: Verificar se o módulo IAMC está funcionando
- **Esperado**: Status 200 com informações do módulo

#### ✅ 2. Testar Departamentos
```
GET {{base_url}}/api/iamc/departamentos
POST {{base_url}}/api/iamc/departamentos
```

#### ✅ 3. Testar Funcionários
```
GET {{base_url}}/api/iamc/funcionarios
POST {{base_url}}/api/iamc/funcionarios
```

**Exemplo de dados para POST funcionário:**
```json
{
    "Nome": "João Silva",
    "Apelido": "Silva", 
    "BI": "123456789LA041",
    "DataNascimento": "1990-05-15",
    "Sexo": "M",
    "EstadoCivil": "Solteiro",
    "Email": "joao.silva@empresa.com",
    "Telefone": "+244 923 456 789",
    "Endereco": "Rua da Paz, 123, Luanda",
    "DataAdmissao": "2024-01-15",
    "EstadoFuncionario": "Activo"
}
```

#### ✅ 4. Testar Presenças
```
GET {{base_url}}/api/iamc/presencas
POST {{base_url}}/api/iamc/presencas
```

### 🔧 Status dos Endpoints

| Endpoint | Método | Status | Observações |
|----------|--------|--------|-------------|
| `/api/iamc/status` | GET | ✅ Funcionando | Status do módulo |
| `/api/iamc/funcionarios` | GET/POST/PUT/DELETE | ✅ Atualizado | Novos controllers |
| `/api/iamc/departamentos` | GET/POST/PUT/DELETE | ✅ Atualizado | Novos controllers |
| `/api/iamc/presencas` | GET/POST/PUT/DELETE | ✅ Atualizado | Novos controllers |
| `/api/iamc/licencas` | GET/POST/PUT/DELETE | ✅ Atualizado | Novos controllers |
| `/api/iamc/beneficios` | GET/POST/PUT/DELETE | ✅ Atualizado | Novos controllers |
| `/api/iamc/folha-salarial` | GET/POST/PUT/DELETE | ✅ Atualizado | Novos controllers |

### 🚨 Soluções para Problemas Comuns

#### ❌ "NoneType object is not callable"
- **Causa**: IAMCSession não inicializado
- **Solução**: Reiniciar o servidor Flask (já corrigido no código)

#### ❌ "Connection refused"
- **Causa**: Servidor Flask não está rodando
- **Solução**: Iniciar o servidor com `python app.py`

#### ❌ "psycopg2.errors.UndefinedTable"
- **Causa**: Usando PostgreSQL em vez de SQL Server
- **Solução**: Já corrigido - agora usa SQL Server

### 📝 Campos Obrigatórios por Entidade

#### Funcionário:
- `Nome` (string)
- `BI` (string, único)
- `Email` (string, único)

#### Departamento:
- `NomeDepartamento` (string)

#### Presença:
- `FuncionarioID` (integer)
- `DataPresenca` (date: YYYY-MM-DD)

### 🎯 Testes Automáticos
A collection inclui testes automáticos que:
- ✅ Verificam status codes
- ✅ Validam estrutura das respostas
- ✅ Extraem IDs automaticamente
- ✅ Verificam campos obrigatórios

### 🔄 Próximos Passos
1. Testar todos os endpoints básicos (GET/POST)
2. Testar endpoints de atualização (PUT)
3. Testar endpoints de eliminação (DELETE)
4. Validar integridade dos dados no SQL Server
5. Testar cenários de erro (dados inválidos)

---
**Nota**: Todos os endpoints agora usam SQL Server em vez de PostgreSQL. O erro original foi resolvido! 🎉
