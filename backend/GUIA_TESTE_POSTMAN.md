# 🚀 Guia de Teste dos Endpoints IAMC com Postman

## 📋 Pré-requisitos

1. **Postman instalado** (versão 9.0+ recomendada)
2. **Servidor Flask rodando** na porta 5000
3. **Base de dados IAMC** configurada no SQL Server

## 📥 Importação dos Arquivos

### 1. Importar a Coleção
1. Abra o Postman
2. Clique em **Import** (canto superior esquerdo)
3. Selecione **Upload Files**
4. Importe o arquivo: `IAMC_Postman_Collection_Melhorada.json`

### 2. Importar o Environment
1. No Postman, clique no ícone de **Environments** (canto superior direito)
2. Clique em **Import**
3. Selecione o arquivo: `IAMC_Postman_Environment.json`
4. Ative o environment "IAMC - Ambiente de Desenvolvimento"

## 🔧 Configuração Inicial

### 1. Verificar Variáveis de Environment
No environment ativo, certifique-se que:
- `base_url` = `http://localhost:5000`
- Outras variáveis podem ficar vazias (preenchidas automaticamente)

### 2. Verificar Servidor Flask
Execute o comando no terminal:
```bash
cd "c:\Users\administrator.GTS\Develop\dinqr\backend"
python app.py
```

## 🧪 Sequência de Testes Recomendada

### ✅ Fase 1: Verificação de Conectividade
1. **Status IAMC** - Verifica se o módulo IAMC está funcionando
2. **Health Check Geral** - Verifica o estado geral do sistema

### ✅ Fase 2: Criação de Dados Base
Execute nesta ordem para criar dados relacionados:

1. **Criar Departamento** 
   - Cria um departamento de TI
   - ID salvo automaticamente na variável `departamento_id`

2. **Criar Cargo**
   - Cria o cargo "Desenvolvedor Senior"
   - ID salvo automaticamente na variável `cargo_id`

3. **Criar Funcionário**
   - Cria um funcionário completo
   - ID salvo automaticamente na variável `funcionario_id`

### ✅ Fase 3: Operações de Leitura
4. **Listar Departamentos** - Visualiza todos os departamentos
5. **Listar Cargos** - Visualiza todos os cargos
6. **Listar Funcionários** - Visualiza todos os funcionários

### ✅ Fase 4: Operações Específicas
7. **Obter Funcionário por ID** - Busca funcionário específico
8. **Obter Departamento por ID** - Busca departamento específico
9. **Obter Cargo por ID** - Busca cargo específico

### ✅ Fase 5: Operações de Atualização
10. **Atualizar Funcionário** - Modifica dados do funcionário
11. **Atualizar Departamento** - Modifica dados do departamento

### ✅ Fase 6: Registros de Atividade
12. **Registrar Presença** - Registra presença do funcionário
13. **Criar Licença** - Cria licença para o funcionário
14. **Criar Registro Salarial** - Cria registro na folha salarial
15. **Criar Benefício** - Cria novo benefício

### ✅ Fase 7: Consultas Avançadas
16. **Obter Presenças por Funcionário** - Lista presenças de um funcionário
17. **Listar Licenças** - Visualiza todas as licenças
18. **Listar Folha Salarial** - Visualiza registros salariais
19. **Listar Benefícios** - Visualiza todos os benefícios

## 🔍 Validação Automática

### Testes Globais (executados automaticamente)
- ✅ Status code válido (200, 201, 204)
- ✅ Tempo de resposta < 5 segundos
- ✅ Content-Type é application/json

### Testes Específicos por Endpoint
- ✅ Estrutura de dados correta
- ✅ Campos obrigatórios presentes
- ✅ Validação de valores esperados
- ✅ IDs salvos automaticamente nas variáveis

## 🚨 Solução de Problemas

### Erro 500 - Internal Server Error
- Verifique se a base de dados IAMC está acessível
- Confirme as credenciais no arquivo `.env`
- Verifique os logs do Flask para detalhes

### Erro 404 - Not Found
- Confirme que o servidor Flask está rodando
- Verifique se a URL base está correta
- Certifique-se que os blueprints IAMC estão registrados

### Erro de Conexão
- Confirme que o servidor está na porta 5000
- Verifique firewall/antivírus
- Teste com `curl http://localhost:5000/health`

### Variáveis Não Preenchidas
- Execute primeiro os endpoints de criação
- Verifique se os testes estão sendo executados
- Confirme que o environment está ativo

## 📊 Interpretação dos Resultados

### Resposta de Sucesso
```json
{
  "funcionario_id": 1,
  "nome": "João Silva",
  "email": "joao.silva@empresa.com",
  "estado_funcionario": "Ativo"
}
```

### Resposta de Erro
```json
{
  "error": "Descrição do erro",
  "request_id": "uuid-da-requisição",
  "timestamp": "2024-12-09T10:00:00Z"
}
```

## 🔄 Limpeza de Dados

⚠️ **CUIDADO**: A pasta "Limpeza (DELETE)" contém operações destrutivas!

- Use apenas em ambiente de desenvolvimento
- Backup sempre antes de executar DELETE
- Operações DELETE são irreversíveis

## 📈 Monitoramento

### Console do Postman
- Verifique o console para logs detalhados
- IDs salvos são exibidos com ✅
- Erros são destacados em vermelho

### Variáveis de Collection
- `funcionario_id`: ID do último funcionário criado
- `departamento_id`: ID do último departamento criado
- `cargo_id`: ID do último cargo criado

## 🎯 Próximos Passos

1. **Automatização**: Configure newman para execução em CI/CD
2. **Dados de Teste**: Crie datasets maiores para testing
3. **Performance**: Execute testes de carga com múltiplas requisições
4. **Segurança**: Adicione testes de autenticação quando implementado

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs do Flask em `backend/logs/app.log`
2. Execute `python criar_tabelas_iamc.py` para recriar as tabelas
3. Consulte a documentação em `IAMC_DOCUMENTATION.md`
