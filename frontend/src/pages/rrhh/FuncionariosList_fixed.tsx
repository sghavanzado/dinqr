import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  Add as AddIcon,
  Person as PersonIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import type { 
  Funcionario, 
  FuncionarioFilter,
  Departamento,
  Cargo,
} from '../../types/rrhh';
import { 
  getFuncionarios, 
  getDepartamentos, 
  getCargos,
  updateFuncionario,
  deleteFuncionario
} from '../../services/api/rrhh.js';

// Import modular components
import DataTable from '../../components/funcionarios/DataTable';
import type { Column } from '../../components/funcionarios/DataTable';
import SearchFilter from '../../components/funcionarios/SearchFilter';
import type { FilterField } from '../../components/funcionarios/SearchFilter';
import ExportOptions from '../../components/funcionarios/ExportOptions';

const FuncionariosList: React.FC = () => {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [cargos, setCargos] = useState<Cargo[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  // Search and filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState<Record<string, any>>({});

  // Notification states
  const [notification, setNotification] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'warning' | 'info';
  }>({
    open: false,
    message: '',
    severity: 'success',
  });

  // Define table columns
  const columns: Column[] = [
    {
      id: 'id',
      label: 'ID',
      align: 'center',
      minWidth: 80
    },
    {
      id: 'nome',
      label: 'Nome',
      minWidth: 200
    },
    {
      id: 'email',
      label: 'Email',
      minWidth: 200
    },
    {
      id: 'departamento',
      label: 'Departamento',
      minWidth: 150,
      format: (value: Departamento) => value?.nome || '-'
    },
    {
      id: 'cargo',
      label: 'Cargo',
      minWidth: 150,
      format: (value: Cargo) => value?.nome || '-'
    },
    {
      id: 'estado',
      label: 'Estado',
      align: 'center',
      minWidth: 120
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
      options: departamentos.map((dep: any) => ({ value: dep.id, label: dep.nome }))
    },
    {
      key: 'cargo',
      label: 'Cargo',
      type: 'select',
      options: cargos.map((cargo: any) => ({ value: cargo.id, label: cargo.nome }))
    },
    {
      key: 'estado',
      label: 'Estado',
      type: 'select',
      options: [
        { value: 'ATIVO', label: 'Ativo' },
        { value: 'INATIVO', label: 'Inativo' },
        { value: 'SUSPENSO', label: 'Suspenso' },
        { value: 'LICENCA', label: 'Em Licença' },
        { value: 'FERIAS', label: 'Em Férias' }
      ]
    }
  ];

  useEffect(() => {
    loadData();
  }, [currentPage, rowsPerPage, searchTerm, filters]);

  useEffect(() => {
    loadDepartamentos();
    loadCargos();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const queryFilters: FuncionarioFilter = {
        nome: searchTerm,
        page: currentPage + 1,
        per_page: rowsPerPage,
        ...filters
      };

      const response = await getFuncionarios(queryFilters);
      
      if (response.success) {
        setFuncionarios(response.data);
        setTotalCount(response.total);
      }
    } catch (error) {
      showNotification('Erro ao carregar funcionários', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadDepartamentos = async () => {
    try {
      const response = await getDepartamentos();
      if (response.success && response.data) {
        setDepartamentos(response.data);
      }
    } catch (error) {
      console.error('Erro ao carregar departamentos:', error);
    }
  };

  const loadCargos = async () => {
    try {
      const response = await getCargos();
      if (response.success && response.data) {
        setCargos(response.data);
      }
    } catch (error) {
      console.error('Erro ao carregar cargos:', error);
    }
  };

  const showNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setNotification({ open: true, message, severity });
  };

  const handleRefresh = () => {
    loadData();
  };

  const handleCreate = () => {
    // TODO: Implement create functionality
    showNotification('Função criar funcionário será implementada', 'info');
  };

  const handleEdit = (funcionario: Funcionario) => {
    // TODO: Implement edit functionality
    showNotification(`Editar funcionário: ${funcionario.nome}`, 'info');
  };

  const handleView = (funcionario: Funcionario) => {
    // TODO: Implement view functionality
    showNotification(`Visualizar funcionário: ${funcionario.nome}`, 'info');
  };

  const handleDelete = async (funcionario: Funcionario) => {
    try {
      await deleteFuncionario(funcionario.id);
      showNotification('Funcionário excluído com sucesso!', 'success');
      loadData();
    } catch (error) {
      showNotification('Erro ao excluir funcionário', 'error');
    }
  };

  const handlePageChange = (_event: unknown, newPage: number) => {
    setCurrentPage(newPage);
  };

  const handleRowsPerPageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setCurrentPage(0);
  };

  const handleSearchChange = (value: string) => {
    setSearchTerm(value);
    setCurrentPage(0);
  };

  const handleFiltersChange = (newFilters: Record<string, any>) => {
    setFilters(newFilters);
    setCurrentPage(0);
  };

  const handleClearAll = () => {
    setSearchTerm('');
    setFilters({});
    setCurrentPage(0);
  };

  const handleExport = async (format: 'pdf' | 'excel' | 'csv', _selectedColumns?: string[]) => {
    try {
      showNotification(`Exportando dados em formato ${format.toUpperCase()}...`, 'info');
      
      // This is where you'd call your export API
      // await exportFuncionarios({ format, columns: selectedColumns, filters: { ...filters, nome: searchTerm } });
      
      showNotification('Dados exportados com sucesso!', 'success');
    } catch (error) {
      showNotification('Erro ao exportar dados', 'error');
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          {/* Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <PersonIcon color="primary" />
              <Typography variant="h5" component="h1">
                Funcionários
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <ExportOptions
                data={funcionarios}
                filename={`funcionarios_${new Date().toISOString().split('T')[0]}`}
                onExport={handleExport}
                loading={loading}
              />
              <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={handleRefresh}
                disabled={loading}
              >
                Atualizar
              </Button>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleCreate}
              >
                Novo Funcionário
              </Button>
            </Box>
          </Box>

          {/* Search and Filters */}
          <SearchFilter
            searchTerm={searchTerm}
            onSearchChange={handleSearchChange}
            filters={filters}
            onFiltersChange={handleFiltersChange}
            filterFields={filterFields}
            onClearAll={handleClearAll}
            loading={loading}
            placeholder="Pesquisar funcionários por nome, email..."
          />

          {/* Data Table */}
          <DataTable
            columns={columns}
            data={funcionarios}
            loading={loading}
            page={currentPage}
            rowsPerPage={rowsPerPage}
            totalCount={totalCount}
            onPageChange={handlePageChange}
            onRowsPerPageChange={handleRowsPerPageChange}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onView={handleView}
            emptyMessage="Nenhum funcionário encontrado"
            title="Lista de Funcionários"
          />
        </CardContent>
      </Card>

      {/* Notification Snackbar */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={() => setNotification({ ...notification, open: false })}
      >
        <Alert
          severity={notification.severity}
          onClose={() => setNotification({ ...notification, open: false })}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default FuncionariosList;
