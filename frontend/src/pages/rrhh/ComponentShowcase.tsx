import React, { useState } from 'react';
import { Box, Typography, Paper, Grid, Button } from '@mui/material';
import { 
  People as PeopleIcon,
  Assessment as AssessmentIcon,
  AccessTime as TimeIcon,
  Business as BusinessIcon,
  MonetizationOn as SalaryIcon
} from '@mui/icons-material';

// Import our modular components
import StatsCard from '../../components/funcionarios/StatsCard';
import SearchFilter from '../../components/funcionarios/SearchFilter';
import type { FilterField } from '../../components/funcionarios/SearchFilter';
import DataTable from '../../components/funcionarios/DataTable';
import type { Column } from '../../components/funcionarios/DataTable';
import StatusBadge from '../../components/funcionarios/StatusBadge';
import ExportOptions from '../../components/funcionarios/ExportOptions';
import ConfirmDialog from '../../components/funcionarios/ConfirmDialog';

const ComponentShowcase: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // Sample data for the table
  const sampleData = [
    {
      id: 1,
      nome: 'João Silva',
      email: 'joao@empresa.com',
      departamento: 'Tecnologia',
      cargo: 'Desenvolvedor',
      status: 'ATIVO',
      data_admissao: '2023-01-15'
    },
    {
      id: 2,
      nome: 'Maria Santos',
      email: 'maria@empresa.com',
      departamento: 'RRHH',
      cargo: 'Analista',
      status: 'ATIVO',
      data_admissao: '2023-02-20'
    },
    {
      id: 3,
      nome: 'Pedro Costa',
      email: 'pedro@empresa.com',
      departamento: 'Vendas',
      cargo: 'Vendedor',
      status: 'LICENCA',
      data_admissao: '2022-11-10'
    }
  ];

  // Define table columns
  const columns: Column[] = [
    { id: 'id', label: 'ID', align: 'center', minWidth: 80 },
    { id: 'nome', label: 'Nome', minWidth: 200 },
    { id: 'email', label: 'Email', minWidth: 200 },
    { id: 'departamento', label: 'Departamento', minWidth: 150 },
    { id: 'cargo', label: 'Cargo', minWidth: 150 },
    {
      id: 'status',
      label: 'Status',
      align: 'center',
      minWidth: 120,
      format: (value: string) => <StatusBadge status={value} type="employee" />
    },
    {
      id: 'data_admissao',
      label: 'Data Admissão',
      align: 'center',
      minWidth: 120,
      format: (value: string) => value ? new Date(value).toLocaleDateString('pt-BR') : '-'
    }
  ];

  // Define filter fields
  const filterFields: FilterField[] = [
    {
      key: 'departamento',
      label: 'Departamento',
      type: 'select',
      options: [
        { value: 'tecnologia', label: 'Tecnologia' },
        { value: 'rrhh', label: 'RRHH' },
        { value: 'vendas', label: 'Vendas' }
      ]
    },
    {
      key: 'status',
      label: 'Status',
      type: 'select',
      options: [
        { value: 'ATIVO', label: 'Ativo' },
        { value: 'INATIVO', label: 'Inativo' },
        { value: 'LICENCA', label: 'Em Licença' }
      ]
    },
    {
      key: 'data_inicio',
      label: 'Data Início',
      type: 'date'
    }
  ];

  const handleExport = async (format: 'pdf' | 'excel' | 'csv') => {
    console.log(`Exporting data in ${format} format`);
    // Simulate export delay
    await new Promise(resolve => setTimeout(resolve, 2000));
  };

  const handleClearAll = () => {
    setSearchTerm('');
    setFilters({});
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        RRHH - Componentes Modulares
      </Typography>
      <Typography variant="body1" sx={{ mb: 4 }}>
        Esta página demonstra todos os componentes modulares criados para o sistema RRHH.
      </Typography>

      {/* Stats Cards Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          1. Cards de Estatísticas
        </Typography>
        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Total Funcionários"
              value={247}
              subtitle="Colaboradores ativos"
              icon={<PeopleIcon />}
              color="primary"
              trend="up"
              trendValue="+5.2%"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Presenças Hoje"
              value={198}
              subtitle="80% dos funcionários"
              icon={<TimeIcon />}
              color="success"
              trend="neutral"
              trendValue="0%"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Avaliações Pendentes"
              value={15}
              subtitle="Para este mês"
              icon={<AssessmentIcon />}
              color="warning"
              trend="down"
              trendValue="-2.1%"
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <StatsCard
              title="Folha Salarial"
              value="R$ 1.2M"
              subtitle="Valor mensal"
              icon={<SalaryIcon />}
              color="info"
            />
          </Grid>
        </Grid>
      </Paper>

      {/* Status Badges Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          2. Status Badges
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
          <StatusBadge status="ATIVO" type="employee" />
          <StatusBadge status="INATIVO" type="employee" />
          <StatusBadge status="SUSPENSO" type="employee" />
          <StatusBadge status="LICENCA" type="employee" />
          <StatusBadge status="PRESENTE" type="attendance" />
          <StatusBadge status="AUSENTE" type="attendance" />
          <StatusBadge status="ATRASO" type="attendance" />
          <StatusBadge status="APROVADO" type="leave" />
          <StatusBadge status="PENDENTE" type="leave" />
          <StatusBadge status="REJEITADO" type="leave" />
        </Box>
      </Paper>

      {/* Search and Filter Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          3. Busca e Filtros
        </Typography>
        <SearchFilter
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          filters={filters}
          onFiltersChange={setFilters}
          filterFields={filterFields}
          onClearAll={handleClearAll}
          placeholder="Pesquisar funcionários..."
        />
      </Paper>

      {/* Export Options Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          4. Opções de Exportação
        </Typography>
        <Box sx={{ mt: 2 }}>
          <ExportOptions
            data={sampleData}
            filename="funcionarios_demo"
            onExport={handleExport}
          />
        </Box>
      </Paper>

      {/* Data Table Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          5. Tabela de Dados
        </Typography>
        <DataTable
          columns={columns}
          data={sampleData}
          loading={false}
          page={page}
          rowsPerPage={rowsPerPage}
          totalCount={sampleData.length}
          onPageChange={(_, newPage) => setPage(newPage)}
          onRowsPerPageChange={(e) => setRowsPerPage(parseInt(e.target.value, 10))}
          onEdit={(item) => console.log('Edit:', item)}
          onDelete={(item) => console.log('Delete:', item)}
          onView={(item) => console.log('View:', item)}
          title="Lista de Funcionários Demo"
        />
      </Paper>

      {/* Confirm Dialog Section */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          6. Diálogo de Confirmação
        </Typography>
        <Button
          variant="outlined"
          color="error"
          onClick={() => setConfirmOpen(true)}
          sx={{ mt: 2 }}
        >
          Testar Diálogo de Confirmação
        </Button>
        <ConfirmDialog
          open={confirmOpen}
          title="Confirmar Ação"
          message="Esta é uma demonstração do diálogo de confirmação. Tem certeza que deseja continuar?"
          onConfirm={() => {
            setConfirmOpen(false);
            console.log('Action confirmed!');
          }}
          onCancel={() => setConfirmOpen(false)}
          confirmColor="error"
          confirmText="Confirmar"
        />
      </Paper>
    </Box>
  );
};

export default ComponentShowcase;
