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
  deleteFuncionario
} from '../../services/api/funcionarios';
import { 
  getDepartamentos, 
  getCargos
} from '../../services/api/rrhh';

// Import modular components
import DataTable from '../../components/funcionarios/DataTable';
import type { Column } from '../../components/funcionarios/DataTable';
import SearchFilter from '../../components/funcionarios/SearchFilter';
import type { FilterField } from '../../components/funcionarios/SearchFilter';
import ExportOptions from '../../components/funcionarios/ExportOptions';

// Import CRUD dialog components
import FuncionarioFormDialog from '../../components/funcionarios/FuncionarioFormDialog';
import FuncionarioViewDialog from '../../components/funcionarios/FuncionarioViewDialog';
import DeleteConfirmDialog from '../../components/funcionarios/DeleteConfirmDialog';

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

  // Dialog states
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [viewDialogOpen, setViewDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedFuncionario, setSelectedFuncionario] = useState<Funcionario | null>(null);
  const [deletingFuncionario, setDeletingFuncionario] = useState(false);

  // Define table columns (usando campos do backend)
  const columns: Column[] = [
    {
      id: 'FuncionarioID',
      label: 'ID',
      align: 'center',
      minWidth: 80
    },
    {
      id: 'nomeCompleto',
      label: 'Nome Completo',
      minWidth: 200
    },
    {
      id: 'Email',
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
      id: 'EstadoFuncionario',
      label: 'Estado',
      align: 'center',
      minWidth: 120
    },
    {
      id: 'DataAdmissao',
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
    const initializeData = async () => {
      // Cargar departamentos y cargos PRIMERO y esperar
      await Promise.all([loadDepartamentos(), loadCargos()]);
      // Solo después cargar funcionários
      await loadData();
    };
    
    initializeData();
  }, []);

  useEffect(() => {
    // Solo recargar funcionários si ya tenemos departamentos y cargos cargados
    if (departamentos.length > 0 && cargos.length > 0) {
      loadData();
    }
  }, [currentPage, rowsPerPage, searchTerm, filters]);

  const loadData = async () => {
    try {
      setLoading(true);
      const queryFilters: FuncionarioFilter = {
        nome: searchTerm,
        page: currentPage + 1,
        per_page: rowsPerPage,
        ...filters
      };

      console.log('🔍 Carregando funcionários com filtros:', queryFilters);
      
      // Verificar se o backend está acessível primeiro
      try {
        const statusResponse = await fetch('http://localhost:5000/api/iamc/status');
        if (!statusResponse.ok) {
          throw new Error(`Backend não acessível: ${statusResponse.status}`);
        }
        console.log('✅ Backend está acessível');
      } catch (statusError) {
        console.error('❌ Backend não está acessível:', statusError);
        showNotification('Servidor backend não está rodando. Verifique se está executando na porta 5000.', 'error');
        return;
      }

      const response = await getFuncionarios(queryFilters);
      
      // Verificar se a resposta tem a estrutura esperada
      if (typeof response !== 'object' || response === null) {
        console.error('❌ Resposta inválida:', response);
        showNotification('Resposta inválida do servidor', 'error');
        return;
      }
      
      if (response.success) {
        const funcionariosData = response.data || [];
        const totalData = response.total || 0;
        
        // Processar dados para adicionar campos calculados
        const funcionariosProcessados = funcionariosData.map((f: any) => {
          return {
            ...f,
            nomeCompleto: `${f.Nome || ''} ${f.Apelido || ''}`.trim(),
            // Garantir que existe um campo de ID para a tabela
            id: f.FuncionarioID || f.funcionarioID || f.id,
            // Usar los nomes de cargo e departamento que já vêm do backend
            departamento: { nome: f.DepartamentoNome || 'Não especificado' },
            cargo: { nome: f.CargoNome || 'Não especificado' }
          };
        });
        
        setFuncionarios(funcionariosProcessados);
        setTotalCount(totalData);
        
        if (funcionariosData.length === 0 && totalData === 0) {
          showNotification('Nenhum funcionário encontrado na base de dados', 'info');
        } else if (funcionariosData.length === 0) {
          showNotification('Nenhum funcionário encontrado com os filtros aplicados', 'info');
        } else {
          console.log(`✅ Carregados ${funcionariosData.length} funcionários de ${totalData} total`);
        }
      } else {
        console.error('❌ Resposta de erro:', response);
        const errorMessage = (response as any).message || (response as any).error || 'Erro desconhecido';
        showNotification(`Erro do servidor: ${errorMessage}`, 'error');
      }
    } catch (error) {
      console.error('❌ Erro ao carregar funcionários:', error);
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        showNotification('Erro de conexão com o servidor. Verifique se o backend está rodando.', 'error');
      } else {
        showNotification('Erro ao carregar funcionários. Verifique sua conexão.', 'error');
      }
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
      showNotification('Erro ao carregar departamentos', 'error');
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
      showNotification('Cargos não disponíveis (backend precisa ser reiniciado)', 'warning');
    }
  };

  const showNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setNotification({ open: true, message, severity });
  };

  const handleRefresh = () => {
    loadData();
  };

  const handleCreate = () => {
    setSelectedFuncionario(null);
    setFormDialogOpen(true);
  };

  const handleEdit = (funcionario: Funcionario) => {
    setSelectedFuncionario(funcionario);
    setFormDialogOpen(true);
  };

  const handleView = (funcionario: Funcionario) => {
    setSelectedFuncionario(funcionario);
    setViewDialogOpen(true);
  };

  const handleDelete = (funcionario: Funcionario) => {
    setSelectedFuncionario(funcionario);
    setDeleteDialogOpen(true);
  };

  const handleFormDialogClose = () => {
    setFormDialogOpen(false);
    setSelectedFuncionario(null);
  };

  const handleFormSuccess = () => {
    loadData();
    showNotification('Funcionário salvo com sucesso!', 'success');
  };

  const handleViewDialogClose = () => {
    setViewDialogOpen(false);
    setSelectedFuncionario(null);
  };

  const handleViewEditClick = () => {
    setViewDialogOpen(false);
    setFormDialogOpen(true);
    // selectedFuncionario já está definido
  };

  const handleDeleteDialogClose = () => {
    setDeleteDialogOpen(false);
    setSelectedFuncionario(null);
  };

  const handleDeleteConfirm = async () => {
    if (!selectedFuncionario) return;

    try {
      setDeletingFuncionario(true);
      const response = await deleteFuncionario(selectedFuncionario.funcionarioID);
      
      if (response.success) {
        showNotification('Funcionário excluído com sucesso!', 'success');
        loadData();
        handleDeleteDialogClose();
      } else {
        showNotification('Erro ao excluir funcionário', 'error');
      }
    } catch (error) {
      console.error('Erro ao excluir funcionário:', error);
      showNotification('Erro ao excluir funcionário', 'error');
    } finally {
      setDeletingFuncionario(false);
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

  // Test function to verify backend connectivity
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

      {/* CRUD Dialogs */}
      <FuncionarioFormDialog
        open={formDialogOpen}
        onClose={handleFormDialogClose}
        onSuccess={handleFormSuccess}
        funcionario={selectedFuncionario}
        departamentos={departamentos}
        cargos={cargos}
      />

      <FuncionarioViewDialog
        open={viewDialogOpen}
        onClose={handleViewDialogClose}
        onEdit={handleViewEditClick}
        funcionario={selectedFuncionario}
        departamentos={departamentos}
        cargos={cargos}
      />

      <DeleteConfirmDialog
        open={deleteDialogOpen}
        onClose={handleDeleteDialogClose}
        onConfirm={handleDeleteConfirm}
        funcionario={selectedFuncionario}
        loading={deletingFuncionario}
      />
    </Box>
  );
};

export default FuncionariosList;
