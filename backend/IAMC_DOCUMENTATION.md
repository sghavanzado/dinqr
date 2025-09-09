# 📊 Sistema IAMC - Gestão de Funcionários

## 🎯 Visão Geral

O Sistema IAMC (Integrated Asset Management Control) é um módulo completo de gestão de funcionários integrado ao backend DINQR. Fornece funcionalidades completas para gestão de recursos humanos, incluindo funcionários, contratos, presenças, licenças, folha salarial e benefícios.

## 🏗️ Arquitetura

### Estrutura de Pastas
```
backend/
├── models/
│   ├── iamc_funcionarios.py     # Modelos: Funcionario, Departamento, Cargo, etc.
│   └── iamc_presencas.py        # Modelos: Presenca, Licenca, Beneficio, etc.
├── controllers/
│   ├── iamc_funcionarios_controller.py
│   └── iamc_presencas_controller.py
├── routes/
│   ├── iamc_funcionarios_routes.py
│   ├── iamc_presencas_routes.py
│   └── iamc_routes.py          # Blueprint principal
└── criar_tabelas_iamc.py       # Script de inicialização
```

## 📊 Modelos de Dados

### 1. **Funcionario**
- `FuncionarioID` (PK)
- `Nome`, `Apelido`, `BI` (único)
- `DataNascimento`, `Sexo`, `EstadoCivil`
- `Email`, `Telefone`, `Endereco`
- `DataAdmissao`, `EstadoFuncionario`

### 2. **Departamento**
- `DepartamentoID` (PK)
- `Nome`, `Descricao`

### 3. **Cargo**
- `CargoID` (PK)
- `Nome`, `Descricao`, `Nivel`

### 4. **HistoricoCargoFuncionario**
- `HistoricoID` (PK)
- `FuncionarioID` (FK), `CargoID` (FK), `DepartamentoID` (FK)
- `DataInicio`, `DataFim`

### 5. **Contrato**
- `ContratoID` (PK)
- `FuncionarioID` (FK)
- `TipoContrato`, `DataInicio`, `DataFim`
- `Salario`, `Moeda`, `Estado`
- `salario`, `moeda`, `estado`

### 6. **Presenca**
- `presenca_id` (PK)
- `funcionario_id` (FK)
- `data`, `hora_entrada`, `hora_saida`, `observacao`

### 7. **Licenca**
- `licenca_id` (PK)
- `funcionario_id` (FK)
- `tipo_licenca`, `data_inicio`, `data_fim`, `estado`

### 8. **Formacao**
- `formacao_id` (PK)
- `funcionario_id` (FK)
- `nome_curso`, `instituicao`, `data_inicio`, `data_fim`, `certificado`

### 9. **AvaliacaoDesempenho**
- `avaliacao_id` (PK)
- `funcionario_id` (FK)
- `data_avaliacao`, `avaliador`, `pontuacao`, `comentarios`

### 10. **FolhaSalarial**
- `folha_id` (PK)
- `funcionario_id` (FK)
- `periodo_inicio`, `periodo_fim`
- `salario_base`, `bonificacoes`, `descontos`, `valor_liquido`
- `data_pagamento`

### 11. **Beneficio**
- `beneficio_id` (PK)
- `nome` (único), `descricao`, `tipo`

### 12. **FuncionarioBeneficio**
- `funcionario_beneficio_id` (PK)
- `funcionario_id` (FK), `beneficio_id` (FK)
- `data_inicio`, `data_fim`, `estado`

## 🚀 Endpoints da API

### Base URL: `/api/iamc`

#### **Funcionários**
- `GET /funcionarios` - Listar funcionários (paginado)
- `GET /funcionarios/{id}` - Obter funcionário específico
- `POST /funcionarios` - Criar novo funcionário
- `PUT /funcionarios/{id}` - Atualizar funcionário
- `DELETE /funcionarios/{id}` - Eliminar funcionário

#### **Departamentos**
- `GET /departamentos` - Listar departamentos
- `GET /departamentos/{id}` - Obter departamento específico
- `POST /departamentos` - Criar novo departamento
- `PUT /departamentos/{id}` - Atualizar departamento
- `DELETE /departamentos/{id}` - Eliminar departamento

#### **Presenças**
- `GET /presencas` - Listar presenças (paginado)
- `GET /presencas/{id}` - Obter presença específica
- `POST /presencas` - Registrar nova presença

#### **Licenças**
- `GET /licencas` - Listar licenças (paginado)
- `GET /licencas/{id}` - Obter licença específica
- `POST /licencas` - Criar nova licença

#### **Benefícios**
- `GET /beneficios` - Listar benefícios
- `GET /beneficios/{id}` - Obter benefício específico
- `POST /beneficios` - Criar novo benefício
- `PUT /beneficios/{id}` - Atualizar benefício
- `DELETE /beneficios/{id}` - Eliminar benefício

#### **Folha Salarial**
- `GET /folha-salarial` - Listar folhas salariais (paginado)

#### **Status**
- `GET /status` - Verificar status do módulo IAMC

## 📝 Exemplos de Uso

### Criar Funcionário
```http
POST /api/iamc/funcionarios
Content-Type: application/json

{
    "nome": "João",
    "apelido": "Silva",
    "bi": "123456789",
    "data_nascimento": "1990-05-15",
    "sexo": "M",
    "estado_civil": "Solteiro",
    "email": "joao.silva@empresa.com",
    "telefone": "+244 923 456 789",
    "endereco": "Luanda, Angola",
    "data_admissao": "2024-01-15",
    "estado_funcionario": "Ativo"
}
```

### Registrar Presença
```http
POST /api/iamc/presencas
Content-Type: application/json

{
    "funcionario_id": 1,
    "data": "2024-08-14",
    "hora_entrada": "08:00",
    "hora_saida": "17:00",
    "observacao": "Presente todo o dia"
}
```

### Criar Licença
```http
POST /api/iamc/licencas
Content-Type: application/json

{
    "funcionario_id": 1,
    "tipo_licenca": "Férias",
    "data_inicio": "2024-09-01",
    "data_fim": "2024-09-15",
    "estado": "Pendente"
}
```

## 🔧 Configuração

### 1. **Variáveis de Ambiente (.env)**
```env
# IAMC Database (SQL Server)
IAMC_DB_SERVER=localhost
IAMC_DB_NAME=IAMC
IAMC_DB_USERNAME=sa
IAMC_DB_PASSWORD=Global2020
```

### 2. **Inicialização da Base de Dados**
```bash
python criar_tabelas_iamc.py
```

### 3. **Integração com Flask**
O módulo está automaticamente integrado no `app.py` com o prefixo `/api/iamc`.

## 📋 Respostas da API

### Resposta de Sucesso
```json
{
    "success": true,
    "funcionario": {
        "funcionario_id": 1,
        "nome": "João",
        "apelido": "Silva",
        "bi": "123456789",
        "email": "joao.silva@empresa.com",
        "estado_funcionario": "Ativo"
    },
    "message": "Funcionário criado com sucesso"
}
```

### Resposta de Erro
```json
{
    "success": false,
    "error": "Nome, apelido e BI são obrigatórios"
}
```

### Resposta Paginada
```json
{
    "success": true,
    "funcionarios": [...],
    "total": 50,
    "pages": 3,
    "current_page": 1
}
```

## 🔐 Funcionalidades

### ✅ Implementado
- Modelos SQLAlchemy completos
- Controladores CRUD
- Rotas RESTful
- Validação de dados
- Respostas JSON padronizadas
- Paginação
- Relacionamentos entre tabelas
- Serialização automática (`.to_dict()`)

### 🔄 Para Desenvolver
- Autenticação e autorização
- Relatórios avançados
- Upload de documentos
- Notificações automáticas
- Dashboard analítico
- Exportação para Excel/PDF

## 🚀 Deploy

O sistema IAMC está integrado ao `generadorqr.exe` e será incluído automaticamente na próxima compilação do executável.

## 📞 Suporte

Para questões técnicas ou suporte, consulte a documentação principal do projeto DINQR.
