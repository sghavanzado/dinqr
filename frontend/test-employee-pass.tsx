import React from 'react';
import { createRoot } from 'react-dom/client';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box, Typography } from '@mui/material';
import EmployeePass from './src/components/funcionarios/EmployeePass';

// Mock employee data
const mockEmployee = {
  id: 1,
  funcionarioID: 1,
  FuncionarioID: 1,
  nome: 'João',
  apelido: 'Silva',
  bi: '123456789LA041',
  dataAdmissao: '2023-01-01',
  estadoFuncionario: 'Activo' as const,
  Nome: 'João',
  Apelido: 'Silva',
  CargoNome: 'Desenvolvedor',
  DepartamentoNome: 'TI'
};

const theme = createTheme();

const TestApp = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ p: 2 }}>
        <Typography variant="h4" gutterBottom>
          Teste de Correções - Passe de Funcionário
        </Typography>
        <EmployeePass 
          funcionario={mockEmployee}
          showDialog={false}
        />
      </Box>
    </ThemeProvider>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<TestApp />);
}
