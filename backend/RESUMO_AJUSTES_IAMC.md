# 🔄 Resumo dos Ajustes para Base de Dados IAMC Existente

## ✅ Alterações Realizadas

### 1. **Configuração de Base de Dados**
- **Nome da BD corrigido**: `IAMC_DB` → `IAMC`
- **Arquivos atualizados**:
  - `config.py` - Linha com `IAMC_DB_NAME`
  - `.env` - Variável `IAMC_DB_NAME=IAMC`

### 2. **Modelos SQLAlchemy Atualizados**
Todos os modelos foram ajustados para coincidir com a estrutura real da BD:

#### **Nomes de Tabelas**:
- `funcionarios` → `Funcionarios`
- `departamentos` → `Departamentos`
- `cargos` → `Cargos`
- `presencas` → `Presencas`
- `licencas` → `Licencas`
- E assim por diante...

#### **Nomes de Campos** (CamelCase):
- `funcionario_id` → `FuncionarioID`
- `nome` → `Nome`
- `data_nascimento` → `DataNascimento`
- `estado_funcionario` → `EstadoFuncionario`
- etc.

### 3. **Coleção Postman Atualizada**
- **Arquivo**: `IAMC_Postman_Collection_Melhorada.json`
- **Melhorias**:
  - Nomes de campos corretos nos JSONs de exemplo
  - Testes automáticos para validação
  - Variáveis de ambiente para IDs
  - Scripts pre-request e post-request
  - Documentação inline

### 4. **Novos Arquivos Criados**
- `testar_iamc_bd.py` - Script para testar conectividade
- `IAMC_Postman_Environment.json` - Configuração de ambiente
- `GUIA_TESTE_POSTMAN.md` - Guia passo a passo

## 🚀 Como Testar Agora

### Passo 1: Validar Conectividade
```bash
cd "c:\Users\administrator.GTS\Develop\dinqr\backend"
python testar_iamc_bd.py
```

### Passo 2: Iniciar Servidor Flask
```bash
python app.py
```

### Passo 3: Importar no Postman
1. Importar coleção: `IAMC_Postman_Collection_Melhorada.json`
2. Importar environment: `IAMC_Postman_Environment.json`
3. Ativar o environment "IAMC - Ambiente de Desenvolvimento"

### Passo 4: Executar Testes
1. **Status IAMC** - Verificar se sistema está funcionando
2. **Criar Departamento** - Exemplo:
   ```json
   {
     "Nome": "Tecnologia da Informação",
     "Descricao": "Departamento de TI"
   }
   ```
3. **Criar Funcionário** - Exemplo:
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

## 🔍 Principais Diferenças

### Antes (Snake Case):
```json
{
  "funcionario_id": 1,
  "nome": "João",
  "data_nascimento": "1990-05-15"
}
```

### Agora (Pascal Case - SQL Server):
```json
{
  "FuncionarioID": 1,
  "Nome": "João",
  "DataNascimento": "1990-05-15"
}
```

## 🛠️ Estrutura da BD Esperada
- **Base de Dados**: `IAMC`
- **Servidor**: SQL Server com autenticação SQL
- **Tabelas**: 12 tabelas principais (Funcionarios, Departamentos, etc.)
- **Campos**: Seguem convenção PascalCase do SQL Server

## ⚠️ Notas Importantes
1. A base de dados `IAMC` deve existir e estar acessível
2. As credenciais no `.env` devem estar corretas
3. O SQL Server deve permitir conexões TCP/IP
4. Certifique-se que não há firewall bloqueando a porta 1433

## 🔧 Resolução de Problemas

### Erro de Conexão:
- Verificar credenciais no `.env`
- Testar conectividade com `testar_iamc_bd.py`
- Verificar se SQL Server está rodando

### Erro 404 nos Endpoints:
- Verificar se app Flask está rodando na porta 5000
- Confirmar que blueprints IAMC estão registrados

### Erro de Campos:
- Os nomes dos campos agora seguem PascalCase
- Usar `FuncionarioID` em vez de `funcionario_id`

## 📞 Próximos Passos
1. Executar testes básicos no Postman
2. Verificar logs em `backend/logs/app.log`
3. Implementar funcionalidades adicionais conforme necessário
4. Configurar autenticação se necessário
