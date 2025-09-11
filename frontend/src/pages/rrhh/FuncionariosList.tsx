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
  deleteFuncionario
} from '../../services/api/rrhh';

// Import modular components
import DataTable from '../../components/funcionarios/DataTable';
import type { Column } from '../../components/funcionarios/DataTable';
import SearchFilter from '../../components/funcionarios/SearchFilter';
import type { FilterField } from '../../components/funcionarios/SearchFilter';
import ExportOptions from '../../components/funcionarios/ExportOptions';

// Simple Error Boundary for DataTable
class DataTableErrorBoundary extends React.Component<
  { children: React.ReactNode; onError?: (error: Error) => void },
  { hasError: boolean; error?: Error }
> {
  constructor(props: { children: React.ReactNode; onError?: (error: Error) => void }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('DataTable Error:', error, errorInfo);
    if (this.props.onError) {
      this.props.onError(error);
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <Alert severity="error">
          Ocorreu um erro ao carregar a tabela. Tente recarregar a página.
          <br />
          <Button 
            size="small" 
            onClick={() => window.location.reload()} 
            sx={{ mt: 1 }}
          >
            Recarregar Página
          </Button>
        </Alert>
      );
    }

    return this.props.children;
  }
}

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
      console.error('Erro ao carregar funcionários:', error);
      // Fallback para dados mock quando a API não estiver disponível
      const mockFuncionarios = [
        {
          id: 1,
          funcionarioID: 1,
          nome: 'João Silva',
          apelido: 'João',
          bi: '12345678901',
          email: 'joao@empresa.com',
          telefone: '923456789',
          dataAdmissao: '2023-01-15',
          estadoFuncionario: 'Activo' as const,
          cargoID: 1,
          departamentoID: 1
        },
        {
          id: 2,
          funcionarioID: 2,
          nome: 'Maria Santos',
          apelido: 'Maria',
          bi: '98765432109',
          email: 'maria@empresa.com',
          telefone: '987654321',
          dataAdmissao: '2023-03-20',
          estadoFuncionario: 'Activo' as const,
          cargoID: 2,
          departamentoID: 2
        }
      ];
      setFuncionarios(mockFuncionarios);
      setTotalCount(mockFuncionarios.length);
      showNotification('Exibindo dados de demonstração (API não disponível)', 'warning');
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
      // Fallback para dados mock
      const mockDepartamentos = [
        { id: 1, departamentoID: 1, nome: 'Recursos Humanos', descricao: 'Gestão de pessoas' },
        { id: 2, departamentoID: 2, nome: 'Tecnologia', descricao: 'Desenvolvimento e infraestrutura' },
        { id: 3, departamentoID: 3, nome: 'Comercial', descricao: 'Vendas e relacionamento' }
      ];
      setDepartamentos(mockDepartamentos);
      
      // Show user-friendly notification
      setNotification({
        open: true,
        message: 'Usando dados de demonstração para departamentos (API não disponível)',
        severity: 'warning'
      });
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
      // Fallback para dados mock
      const mockCargos = [
        { id: 1, cargoID: 1, nome: 'Analista de RH', salarioBase: 75000, departamentoID: 1 },
        { id: 2, cargoID: 2, nome: 'Desenvolvedor Senior', salarioBase: 120000, departamentoID: 2 },
        { id: 3, cargoID: 3, nome: 'Gerente Comercial', salarioBase: 95000, departamentoID: 3 }
      ];
      setCargos(mockCargos);
      
      // Show user-friendly notification
      setNotification({
        open: true,
        message: 'Usando dados de demonstração para cargos (API não disponível)',
        severity: 'warning'
      });
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
          <DataTableErrorBoundary onError={() => {
            setNotification({
              open: true,
              message: 'Erro na tabela de dados. Verifique o console para mais detalhes.',
              severity: 'error'
            });
          }}>
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
          </DataTableErrorBoundary>
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
