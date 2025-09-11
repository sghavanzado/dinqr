import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
  IconButton,
  Avatar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Snackbar,
  Tooltip,
  Chip,
  Divider,
  InputAdornment,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  GetApp as ExportIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
  Person as PersonIcon,
  Close as CloseIcon,
  Calculate as CalculateIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { 
  FolhaSalarial, 
  FolhaSalarialFormData,
  Funcionario
} from '../../types/rrhh';
import { 
  getFolhasSalariais, 
  createFolhaSalarial, 
  updateFolhaSalarial,
  getFuncionarios
} from '../../services/api/rrhh';

// Schema de validação
const folhaSalarialSchema = z.object({
  funcionarioID: z.number().min(1, 'Funcionário é obrigatório'),
  periodoInicio: z.string().min(1, 'Período de início é obrigatório'),
  periodoFim: z.string().min(1, 'Período de fim é obrigatório'),
  salarioBase: z.number().min(0, 'Salário base deve ser positivo'),
  bonificacoes: z.number().min(0, 'Bonificações devem ser positivas'),
  descontos: z.number().min(0, 'Descontos devem ser positivos'),
  dataPagamento: z.string().optional(),
}).refine((data) => {
  return new Date(data.periodoInicio) <= new Date(data.periodoFim);
}, {
  message: 'Período de fim deve ser posterior ao período de início',
  path: ['periodoFim'],
});

const FolhaSalarialList: React.FC = () => {
  const [folhasSalariais, setFolhasSalariais] = useState<FolhaSalarial[]>([]);
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  // Dialog states
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedFolha, setSelectedFolha] = useState<FolhaSalarial | null>(null);
  const [actionType, setActionType] = useState<'create' | 'edit'>('create');

  // Filter states
  const [filters, setFilters] = useState({
    funcionarioID: undefined as number | undefined,
    periodoInicio: '',
    periodoFim: '',
    page: 1,
    per_page: 10,
  });

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

  // Form
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
    watch,
  } = useForm<FolhaSalarialFormData>({
    resolver: zodResolver(folhaSalarialSchema),
    defaultValues: {
      funcionarioID: 0,
      periodoInicio: '',
      periodoFim: '',
      salarioBase: 0,
      bonificacoes: 0,
      descontos: 0,
      dataPagamento: '',
    },
  });

  const watchedValues = watch(['salarioBase', 'bonificacoes', 'descontos']);

  useEffect(() => {
    loadFolhasSalariais();
    loadFuncionarios();
  }, [currentPage, rowsPerPage, filters]);

  const loadFolhasSalariais = async () => {
    try {
      setLoading(true);
      const response = await getFolhasSalariais();
      
      if (response.success) {
        setFolhasSalariais(response.data || []);
        setTotalCount(response.data?.length || 0);
      }
    } catch (error: any) {
      console.error('Erro ao carregar folhas salariais:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockFolhasSalariais: FolhaSalarial[] = [
          {
            id: 1,
            folhaID: 1,
            funcionarioID: 1,
            periodoInicio: '2024-11-01',
            periodoFim: '2024-11-30',
            salarioBase: 150000,
            bonificacoes: 25000,
            descontos: 15000,
            valorLiquido: 160000,
            dataPagamento: '2024-12-01',
            funcionario: { id: 1, funcionarioID: 1, nome: 'João', apelido: 'Silva', bi: '123456789', dataAdmissao: '2024-01-15', estadoFuncionario: 'Activo' }
          },
          {
            id: 2,
            folhaID: 2,
            funcionarioID: 2,
            periodoInicio: '2024-11-01',
            periodoFim: '2024-11-30',
            salarioBase: 120000,
            bonificacoes: 20000,
            descontos: 12000,
            valorLiquido: 128000,
            dataPagamento: '2024-12-01',
            funcionario: { id: 2, funcionarioID: 2, nome: 'Maria', apelido: 'Santos', bi: '987654321', dataAdmissao: '2024-02-01', estadoFuncionario: 'Activo' }
          }
        ];
        
        setFolhasSalariais(mockFolhasSalariais);
        setTotalCount(mockFolhasSalariais.length);
        showNotification('Usando dados de demonstração - API não disponível', 'warning');
      } else {
        showNotification('Erro ao carregar folhas salariais', 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadFuncionarios = async () => {
    try {
      const response = await getFuncionarios();
      if (response.success) {
        setFuncionarios(response.data || []);
      }
    } catch (error: any) {
      console.error('Erro ao carregar funcionários:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockFuncionarios: Funcionario[] = [
          { id: 1, funcionarioID: 1, nome: 'João', apelido: 'Silva', bi: '123456789', dataAdmissao: '2024-01-15', estadoFuncionario: 'Activo' },
          { id: 2, funcionarioID: 2, nome: 'Maria', apelido: 'Santos', bi: '987654321', dataAdmissao: '2024-02-01', estadoFuncionario: 'Activo' },
          { id: 3, funcionarioID: 3, nome: 'Pedro', apelido: 'Costa', bi: '456789123', dataAdmissao: '2024-03-01', estadoFuncionario: 'Activo' }
        ];
        setFuncionarios(mockFuncionarios);
      }
    }
  };

  const showNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setNotification({ open: true, message, severity });
  };

  const handleSearch = () => {
    setCurrentPage(0);
    loadFolhasSalariais();
  };

  const handleFilterChange = (field: string, value: string | number | undefined) => {
    setFilters(prev => ({ 
      ...prev, 
      [field]: value === '' ? undefined : value 
    }));
  };

  const handlePageChange = (_: unknown, newPage: number) => {
    setCurrentPage(newPage);
  };

  const handleRowsPerPageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setCurrentPage(0);
  };

  const handleAdd = () => {
    const currentDate = new Date();
    const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    
    reset({
      funcionarioID: 0,
      periodoInicio: firstDay.toISOString().split('T')[0],
      periodoFim: lastDay.toISOString().split('T')[0],
      salarioBase: 0,
      bonificacoes: 0,
      descontos: 0,
      dataPagamento: '',
    });
    setSelectedFolha(null);
    setActionType('create');
    setIsFormOpen(true);
  };

  const handleEdit = (folha: FolhaSalarial) => {
    reset({
      funcionarioID: folha.funcionarioID,
      periodoInicio: folha.periodoInicio,
      periodoFim: folha.periodoFim,
      salarioBase: folha.salarioBase,
      bonificacoes: folha.bonificacoes,
      descontos: folha.descontos,
      dataPagamento: folha.dataPagamento || '',
    });
    setSelectedFolha(folha);
    setActionType('edit');
    setIsFormOpen(true);
  };

  const handleCalculate = () => {
    // Auto-calcular valores líquidos - função demonstrativa
    showNotification('Cálculos atualizados automaticamente', 'info');
  };

  const onSubmit = async (data: FolhaSalarialFormData) => {
    try {
      let response;
      if (actionType === 'create') {
        response = await createFolhaSalarial(data);
      } else if (selectedFolha) {
        response = await updateFolhaSalarial(selectedFolha.folhaID, data);
      }

      if (response?.success) {
        setIsFormOpen(false);
        loadFolhasSalariais();
        showNotification(
          actionType === 'create' ? 'Folha salarial criada com sucesso!' : 'Folha salarial atualizada com sucesso!',
          'success'
        );
      } else {
        showNotification(response?.message || 'Erro ao salvar folha salarial', 'error');
      }
    } catch (error: any) {
      showNotification(error.response?.data?.message || 'Erro ao salvar folha salarial', 'error');
    }
  };

  const getFuncionarioNome = (funcionarioID: number) => {
    const funcionario = (funcionarios || []).find(f => f.funcionarioID === funcionarioID);
    return funcionario ? `${funcionario.nome} ${funcionario.apelido}` : 'N/A';
  };

  const getFuncionarioFoto = (funcionarioID: number) => {
    const funcionario = (funcionarios || []).find(f => f.funcionarioID === funcionarioID);
    return funcionario?.foto;
  };

  const calculateSalarioLiquido = (salarioBase: number, bonificacoes: number, descontos: number) => {
    return salarioBase + bonificacoes - descontos;
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-AO', {
      style: 'currency',
      currency: 'AOA',
    }).format(value);
  };

  const formatPeriod = (inicio: string, fim: string) => {
    const startDate = new Date(inicio);
    const endDate = new Date(fim);
    return `${startDate.toLocaleDateString('pt-AO')} - ${endDate.toLocaleDateString('pt-AO')}`;
  };

  const handleExport = () => {
    // Implementar exportação PDF/Excel
    showNotification('Funcionalidade de exportação será implementada', 'info');
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4" component="h1">
              Folha Salarial
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                variant="outlined"
                startIcon={<ExportIcon />}
                onClick={handleExport}
              >
                Exportar
              </Button>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAdd}
              >
                Nova Folha
              </Button>
            </Box>
          </Box>

          {/* Filters */}
          <Card sx={{ mb: 3, bgcolor: 'grey.50' }}>
            <CardContent>
              <Box sx={{ 
                display: 'flex', 
                flexWrap: 'wrap', 
                gap: 2, 
                alignItems: 'center' 
              }}>
                <Box sx={{ minWidth: 200, flex: '1 1 200px' }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Funcionário</InputLabel>
                    <Select
                      value={filters.funcionarioID || ''}
                      label="Funcionário"
                      onChange={(e) => handleFilterChange('funcionarioID', Number(e.target.value) || undefined)}
                    >
                      <MenuItem value="">Todos</MenuItem>
                      {(funcionarios || []).map((func) => (
                        <MenuItem key={func.funcionarioID} value={func.funcionarioID}>
                          {func.nome} {func.apelido}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Box>
                <Box sx={{ minWidth: 160, flex: '1 1 160px' }}>
                  <TextField
                    fullWidth
                    label="Período Início"
                    type="date"
                    size="small"
                    value={filters.periodoInicio || ''}
                    onChange={(e) => handleFilterChange('periodoInicio', e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                </Box>
                <Box sx={{ minWidth: 160, flex: '1 1 160px' }}>
                  <TextField
                    fullWidth
                    label="Período Fim"
                    type="date"
                    size="small"
                    value={filters.periodoFim || ''}
                    onChange={(e) => handleFilterChange('periodoFim', e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                </Box>
                <Box sx={{ minWidth: 120, display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    startIcon={<SearchIcon />}
                    onClick={handleSearch}
                    fullWidth
                  >
                    Buscar
                  </Button>
                  <Tooltip title="Atualizar">
                    <IconButton onClick={loadFolhasSalariais}>
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Table */}
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Funcionário</TableCell>
                  <TableCell>Período</TableCell>
                  <TableCell align="right">Salário Base</TableCell>
                  <TableCell align="right">Bonificações</TableCell>
                  <TableCell align="right">Descontos</TableCell>
                  <TableCell align="right">Salário Líquido</TableCell>
                  <TableCell>Data Pagamento</TableCell>
                  <TableCell align="center">Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={8} align="center">
                      Carregando...
                    </TableCell>
                  </TableRow>
                ) : folhasSalariais.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} align="center">
                      Nenhuma folha salarial encontrada
                    </TableCell>
                  </TableRow>
                ) : (
                  (folhasSalariais || []).map((folha) => {
                    const salarioLiquido = calculateSalarioLiquido(
                      folha.salarioBase,
                      folha.bonificacoes,
                      folha.descontos
                    );
                    return (
                      <TableRow key={folha.folhaID || folha.id}>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Avatar
                              src={getFuncionarioFoto(folha.funcionarioID)}
                              sx={{ width: 32, height: 32 }}
                            >
                              <PersonIcon />
                            </Avatar>
                            <Typography variant="body2">
                              {getFuncionarioNome(folha.funcionarioID)}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {formatPeriod(folha.periodoInicio, folha.periodoFim)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2" fontWeight="medium">
                            {formatCurrency(folha.salarioBase)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2" color="success.main">
                            {formatCurrency(folha.bonificacoes)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2" color="error.main">
                            {formatCurrency(folha.descontos)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2" fontWeight="bold" color="primary.main">
                            {formatCurrency(salarioLiquido)}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          {folha.dataPagamento ? 
                            new Date(folha.dataPagamento).toLocaleDateString('pt-AO') : 
                            <Chip label="Pendente" size="small" color="warning" />
                          }
                        </TableCell>
                        <TableCell align="center">
                          <Tooltip title="Editar">
                            <IconButton size="small" onClick={() => handleEdit(folha)}>
                              <EditIcon />
                            </IconButton>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    );
                  })
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {/* Pagination */}
          <TablePagination
            component="div"
            count={totalCount}
            page={currentPage}
            onPageChange={handlePageChange}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={handleRowsPerPageChange}
            labelRowsPerPage="Registros por página:"
            labelDisplayedRows={({ from, to, count }) =>
              `${from}-${to} de ${count}`
            }
          />
        </CardContent>
      </Card>

      {/* Form Dialog */}
      <Dialog 
        open={isFormOpen} 
        onClose={() => setIsFormOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogTitle sx={{ pb: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                {actionType === 'create' ? 'Nova Folha Salarial' : 'Editar Folha Salarial'}
              </Typography>
              <IconButton onClick={() => setIsFormOpen(false)} size="small">
                <CloseIcon />
              </IconButton>
            </Box>
          </DialogTitle>
          
          <DialogContent dividers>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              <Box>
                <Controller
                  name="funcionarioID"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!errors.funcionarioID}>
                      <InputLabel>Funcionário *</InputLabel>
                      <Select
                        {...field}
                        label="Funcionário *"
                        value={field.value || ''}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                      >
                        <MenuItem value="">Selecione um funcionário</MenuItem>
                        {(funcionarios || []).map((func) => (
                          <MenuItem key={func.funcionarioID} value={func.funcionarioID}>
                            {func.nome} {func.apelido}
                          </MenuItem>
                        ))}
                      </Select>
                      {errors.funcionarioID && (
                        <Typography variant="caption" color="error">
                          {errors.funcionarioID.message}
                        </Typography>
                      )}
                    </FormControl>
                  )}
                />
              </Box>

              <Box>
                <Divider sx={{ my: 1 }} />
                <Typography variant="h6" gutterBottom>
                  Período de Trabalho
                </Typography>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
                  <Controller
                    name="periodoInicio"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Período Início *"
                        type="date"
                        InputLabelProps={{ shrink: true }}
                        error={!!errors.periodoInicio}
                        helperText={errors.periodoInicio?.message}
                      />
                    )}
                  />
                </Box>
                
                <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
                  <Controller
                    name="periodoFim"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Período Fim *"
                        type="date"
                        InputLabelProps={{ shrink: true }}
                        error={!!errors.periodoFim}
                        helperText={errors.periodoFim?.message}
                      />
                    )}
                  />
                </Box>
              </Box>

              <Box>
                <Divider sx={{ my: 1 }} />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="h6">
                    Valores Salariais
                  </Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<CalculateIcon />}
                    onClick={handleCalculate}
                  >
                    Calcular
                  </Button>
                </Box>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
                  <Controller
                    name="salarioBase"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Salário Base *"
                        type="number"
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <MoneyIcon />
                            </InputAdornment>
                          ),
                        }}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                        error={!!errors.salarioBase}
                        helperText={errors.salarioBase?.message}
                      />
                    )}
                  />
                </Box>
                
                <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
                  <Controller
                    name="bonificacoes"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Bonificações"
                        type="number"
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <MoneyIcon />
                            </InputAdornment>
                          ),
                        }}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                        error={!!errors.bonificacoes}
                        helperText={errors.bonificacoes?.message}
                      />
                    )}
                  />
                </Box>
                
                <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
                  <Controller
                    name="descontos"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Descontos"
                        type="number"
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <MoneyIcon />
                            </InputAdornment>
                          ),
                        }}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                        error={!!errors.descontos}
                        helperText={errors.descontos?.message}
                      />
                    )}
                  />
                </Box>
              </Box>

              {/* Preview do cálculo */}
              <Box>
                <Card sx={{ bgcolor: 'primary.main', color: 'primary.contrastText', p: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    Salário Líquido: {formatCurrency(calculateSalarioLiquido(
                      watchedValues[0] || 0,
                      watchedValues[1] || 0,
                      watchedValues[2] || 0
                    ))}
                  </Typography>
                  <Typography variant="body2">
                    Base: {formatCurrency(watchedValues[0] || 0)} + 
                    Bonificações: {formatCurrency(watchedValues[1] || 0)} - 
                    Descontos: {formatCurrency(watchedValues[2] || 0)}
                  </Typography>
                </Card>
              </Box>
              
              <Box>
                <Controller
                  name="dataPagamento"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label="Data de Pagamento"
                      type="date"
                      InputLabelProps={{ shrink: true }}
                      error={!!errors.dataPagamento}
                      helperText={errors.dataPagamento?.message || 'Deixe em branco se ainda não foi pago'}
                    />
                  )}
                />
              </Box>
            </Box>
          </DialogContent>
          
          <DialogActions sx={{ p: 2 }}>
            <Button onClick={() => setIsFormOpen(false)}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained">
              {actionType === 'create' ? 'Criar' : 'Salvar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Notification */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={() => setNotification(prev => ({ ...prev, open: false }))}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Alert 
          onClose={() => setNotification(prev => ({ ...prev, open: false }))} 
          severity={notification.severity}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default FolhaSalarialList;
