# Alteração do Botão de Ação - Lista de Funcionários para Passes

## Problema:
Na página de Lista de Funcionários para Passes (`/rrhh/passes`), o botão de ação estava mostrando ícone de "Editar" e texto "Editar" em vez de um ícone e texto apropriados para "Gerar Passe".

## Solução Implementada:

### 1. Tornou o DataTable mais flexível
**Arquivo:** `frontend/src/components/funcionarios/DataTable.tsx`

- Adicionadas novas props opcionais para personalizar textos e ícones dos botões:
  - `editButtonText?: string` (padrão: "Editar")
  - `deleteButtonText?: string` (padrão: "Excluir") 
  - `viewButtonText?: string` (padrão: "Ver")
  - `editIcon?: React.ReactNode` (padrão: `<EditIcon />`)

- Atualizados os atributos `title` dos botões para usar os textos personalizados
- Atualizado o ícone do botão de edição para aceitar ícone personalizado

### 2. Personalizado o texto e ícone na Lista de Passes
**Arquivo:** `frontend/src/pages/rrhh/PassesList.tsx`

- Adicionada a prop `editButtonText="Gerar Passe"` no componente DataTable
- Adicionada a prop `editIcon={<BadgeIcon />}` para usar ícone de crachá/passe
- Agora o botão mostra ícone de Badge (passe) e tooltip "Gerar Passe"

## Resultado:
- ✅ **Ícone:** Mudou de ✏️ (Edit) para 🎫 (Badge) - mais apropriado para passes
- ✅ **Texto:** Tooltip mostra "Gerar Passe" em português
- ✅ **Funcionalidade:** Permanece a mesma (chama `handleGerarPasse`)
- ✅ **Compatibilidade:** DataTable continua compatível com outros usos

## Arquivos Modificados:
- `frontend/src/components/funcionarios/DataTable.tsx`
- `frontend/src/pages/rrhh/PassesList.tsx`

## Data da Alteração:
7 de outubro de 2025
