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
  Menu,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Check as ApproveIcon,
  Close as RejectIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
  Person as PersonIcon,
  MoreVert as MoreVertIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { 
  Licenca, 
  LicencaFormData,
  LicencaFilter,
  Funcionario
} from '../../types/rrhh';
import { 
  getLicencas, 
  createLicenca, 
  updateLicenca,
  getFuncionarios
} from '../../services/api/rrhh.js';
import ConfirmDialog from '../../components/funcionarios/ConfirmDialog';

// Schema de validação
const licencaSchema = z.object({
  funcionarioID: z.number().min(1, 'Funcionário é obrigatório'),
  tipo: z.enum(['Ferias', 'Medica', 'Maternidade', 'Paternidade', 'Outras']),
  dataInicio: z.string().min(1, 'Data de início é obrigatória'),
  dataFim: z.string().min(1, 'Data de fim é obrigatória'),
  motivo: z.string().optional(),
  estado: z.enum(['Pendente', 'Aprovada', 'Rejeitada']),
}).refine((data) => {
  return new Date(data.dataInicio) <= new Date(data.dataFim);
}, {
  message: 'Data de fim deve ser posterior à data de início',
  path: ['dataFim'],
});

const LicencasList: React.FC = () => {
  const [licencas, setLicencas] = useState<Licenca[]>([]);
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  // Dialog states
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedLicenca, setSelectedLicenca] = useState<Licenca | null>(null);
  const [actionType, setActionType] = useState<'create' | 'edit' | 'approve' | 'reject'>('create');

  // Menu state
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [menuLicenca, setMenuLicenca] = useState<Licenca | null>(null);

  // Filter states
  const [filters, setFilters] = useState<LicencaFilter>({
    funcionarioID: undefined,
    tipo: '',
    estado: '',
    dataInicio: '',
    dataFim: '',
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
  } = useForm<LicencaFormData>({
    resolver: zodResolver(licencaSchema),
    defaultValues: {
      funcionarioID: 0,
      tipo: 'Ferias',
      dataInicio: '',
      dataFim: '',
      motivo: '',
      estado: 'Pendente',
    },
  });

  useEffect(() => {
    loadLicencas();
    loadFuncionarios();
  }, [currentPage, rowsPerPage, filters]);

  const loadLicencas = async () => {
    try {
      setLoading(true);
      const response = await getLicencas({
        ...filters,
        page: currentPage + 1,
        per_page: rowsPerPage,
      });
      
      if (response.success) {
        setLicencas(response.data);
        setTotalCount(response.total);
      }
    } catch (error: any) {
      console.error('Erro ao carregar licenças:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockLicencas: Licenca[] = [
          {
            id: 1,
            licencaID: 1,
            funcionarioID: 1,
            tipo: 'Ferias',
            dataInicio: '2024-12-10',
            dataFim: '2024-12-20',
            motivo: 'Férias de fim de ano',
            estado: 'Aprovada',
            funcionario: { id: 1, funcionarioID: 1, nome: 'João', apelido: 'Silva', bi: '123456789', dataAdmissao: '2024-01-15', estadoFuncionario: 'Activo' }
          },
          {
            id: 2,
            licencaID: 2,
            funcionarioID: 2,
            tipo: 'Medica',
            dataInicio: '2024-12-05',
            dataFim: '2024-12-08',
            motivo: 'Consulta médica',
            estado: 'Pendente',
            funcionario: { id: 2, funcionarioID: 2, nome: 'Maria', apelido: 'Santos', bi: '987654321', dataAdmissao: '2024-02-01', estadoFuncionario: 'Activo' }
          }
        ];
        
        setLicencas(mockLicencas);
        setTotalCount(mockLicencas.length);
        showNotification('Usando dados de demonstração - API não disponível', 'warning');
      } else {
        showNotification('Erro ao carregar licenças', 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadFuncionarios = async () => {
    try {
      const response = await getFuncionarios();
      if (response.success) {
        setFuncionarios(response.data);
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
    loadLicencas();
  };

  const handleFilterChange = (field: keyof LicencaFilter, value: string | number) => {
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
    reset({
      funcionarioID: 0,
      tipo: 'Ferias',
      dataInicio: '',
      dataFim: '',
      motivo: '',
      estado: 'Pendente',
    });
    setSelectedLicenca(null);
    setActionType('create');
    setIsFormOpen(true);
  };

  const handleEdit = (licenca: Licenca) => {
    reset({
      funcionarioID: licenca.funcionarioID,
      tipo: licenca.tipo,
      dataInicio: licenca.dataInicio,
      dataFim: licenca.dataFim,
      motivo: licenca.motivo || '',
      estado: licenca.estado,
    });
    setSelectedLicenca(licenca);
    setActionType('edit');
    setIsFormOpen(true);
    handleCloseMenu();
  };

  const handleApprove = (licenca: Licenca) => {
    setSelectedLicenca(licenca);
    setActionType('approve');
    setIsConfirmOpen(true);
    handleCloseMenu();
  };

  const handleReject = (licenca: Licenca) => {
    setSelectedLicenca(licenca);
    setActionType('reject');
    setIsConfirmOpen(true);
    handleCloseMenu();
  };

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, licenca: Licenca) => {
    setAnchorEl(event.currentTarget);
    setMenuLicenca(licenca);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
    setMenuLicenca(null);
  };

  const onSubmit = async (data: LicencaFormData) => {
    try {
      let response;
      if (actionType === 'create') {
        response = await createLicenca(data);
      } else if (selectedLicenca) {
        response = await updateLicenca(selectedLicenca.licencaID, data);
      }

      if (response?.success) {
        setIsFormOpen(false);
        loadLicencas();
        showNotification(
          actionType === 'create' ? 'Licença solicitada com sucesso!' : 'Licença atualizada com sucesso!',
          'success'
        );
      } else {
        showNotification(response?.message || 'Erro ao salvar licença', 'error');
      }
    } catch (error: any) {
      showNotification(error.response?.data?.message || 'Erro ao salvar licença', 'error');
    }
  };

  const handleConfirm = async () => {
    if (!selectedLicenca) return;

    try {
      const newEstado = actionType === 'approve' ? 'Aprovada' : 'Rejeitada';
      const response = await updateLicenca(selectedLicenca.licencaID, {
        ...selectedLicenca,
        estado: newEstado,
      });

      if (response.success) {
        setIsConfirmOpen(false);
        loadLicencas();
        showNotification(
          `Licença ${newEstado.toLowerCase()} com sucesso!`,
          'success'
        );
      } else {
        showNotification(response.message || 'Erro ao atualizar licença', 'error');
      }
    } catch (error) {
      showNotification('Erro ao atualizar licença', 'error');
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

  const getStatusColor = (estado: string) => {
    switch (estado) {
      case 'Aprovada': return 'success';
      case 'Rejeitada': return 'error';
      case 'Pendente': return 'warning';
      default: return 'default';
    }
  };

  const getTipoLabel = (tipo: string) => {
    switch (tipo) {
      case 'Ferias': return 'Férias';
      case 'Medica': return 'Médica';
      case 'Maternidade': return 'Maternidade';
      case 'Paternidade': return 'Paternidade';
      case 'Outras': return 'Outras';
      default: return tipo;
    }
  };

  const calculateDays = (dataInicio: string, dataFim: string) => {
    const start = new Date(dataInicio);
    const end = new Date(dataFim);
    const diffTime = Math.abs(end.getTime() - start.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    return diffDays;
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4" component="h1">
              Gestão de Licenças
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleAdd}
            >
              Solicitar Licença
            </Button>
          </Box>

          {/* Filters */}
          <Card sx={{ mb: 3, bgcolor: 'grey.50' }}>
            <CardContent>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
                <Box sx={{ minWidth: 200, flex: '1 1 250px' }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Funcionário</InputLabel>
                    <Select
                      value={filters.funcionarioID || ''}
                      label="Funcionário"
                      onChange={(e) => handleFilterChange('funcionarioID', e.target.value || '')}
                    >
                      <MenuItem value="">Todos</MenuItem>
                      {funcionarios?.map((func) => (
                        <MenuItem key={func.funcionarioID} value={func.funcionarioID}>
                          {func.nome} {func.apelido}
                        </MenuItem>
                      )) || []}
                    </Select>
                  </FormControl>
                </Box>
                <Box sx={{ minWidth: 140, flex: '1 1 150px' }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Tipo</InputLabel>
                    <Select
                      value={filters.tipo || ''}
                      label="Tipo"
                      onChange={(e) => handleFilterChange('tipo', e.target.value)}
                    >
                      <MenuItem value="">Todos</MenuItem>
                      <MenuItem value="Ferias">Férias</MenuItem>
                      <MenuItem value="Medica">Médica</MenuItem>
                      <MenuItem value="Maternidade">Maternidade</MenuItem>
                      <MenuItem value="Paternidade">Paternidade</MenuItem>
                      <MenuItem value="Outras">Outras</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
                <Box sx={{ minWidth: 140, flex: '1 1 150px' }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Estado</InputLabel>
                    <Select
                      value={filters.estado || ''}
                      label="Estado"
                      onChange={(e) => handleFilterChange('estado', e.target.value)}
                    >
                      <MenuItem value="">Todos</MenuItem>
                      <MenuItem value="Pendente">Pendente</MenuItem>
                      <MenuItem value="Aprovada">Aprovada</MenuItem>
                      <MenuItem value="Rejeitada">Rejeitada</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
                <Box sx={{ minWidth: 140, flex: '1 1 150px' }}>
                  <TextField
                    fullWidth
                    label="Data Início"
                    type="date"
                    size="small"
                    value={filters.dataInicio || ''}
                    onChange={(e) => handleFilterChange('dataInicio', e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                </Box>
                <Box sx={{ minWidth: 200, flex: '1 1 220px' }}>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Button
                      variant="contained"
                      startIcon={<SearchIcon />}
                      onClick={handleSearch}
                      fullWidth
                    >
                      Buscar
                    </Button>
                    <Tooltip title="Atualizar">
                      <IconButton onClick={loadLicencas}>
                        <RefreshIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
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
                  <TableCell>Tipo</TableCell>
                  <TableCell>Data Início</TableCell>
                  <TableCell>Data Fim</TableCell>
                  <TableCell>Dias</TableCell>
                  <TableCell>Estado</TableCell>
                  <TableCell>Motivo</TableCell>
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
                ) : (licencas || []).length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} align="center">
                      Nenhuma licença encontrada
                    </TableCell>
                  </TableRow>
                ) : (
                  (licencas || []).map((licenca) => (
                    <TableRow key={licenca.licencaID}>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Avatar
                            src={getFuncionarioFoto(licenca.funcionarioID)}
                            sx={{ width: 32, height: 32 }}
                          >
                            <PersonIcon />
                          </Avatar>
                          <Typography variant="body2">
                            {getFuncionarioNome(licenca.funcionarioID)}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>{getTipoLabel(licenca.tipo)}</TableCell>
                      <TableCell>
                        {new Date(licenca.dataInicio).toLocaleDateString('pt-AO')}
                      </TableCell>
                      <TableCell>
                        {new Date(licenca.dataFim).toLocaleDateString('pt-AO')}
                      </TableCell>
                      <TableCell>
                        {calculateDays(licenca.dataInicio, licenca.dataFim)} dias
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={licenca.estado}
                          color={getStatusColor(licenca.estado) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" noWrap>
                          {licenca.motivo || '-'}
                        </Typography>
                      </TableCell>
                      <TableCell align="center">
                        <IconButton 
                          size="small" 
                          onClick={(e) => handleMenuClick(e, licenca)}
                        >
                          <MoreVertIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>

          {/* Action Menu */}
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleCloseMenu}
          >
            <MenuItem onClick={() => menuLicenca && handleEdit(menuLicenca)}>
              <ListItemIcon>
                <EditIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Editar</ListItemText>
            </MenuItem>
            {menuLicenca?.estado === 'Pendente' && (
              <>
                <MenuItem onClick={() => menuLicenca && handleApprove(menuLicenca)}>
                  <ListItemIcon>
                    <ApproveIcon fontSize="small" color="success" />
                  </ListItemIcon>
                  <ListItemText>Aprovar</ListItemText>
                </MenuItem>
                <MenuItem onClick={() => menuLicenca && handleReject(menuLicenca)}>
                  <ListItemIcon>
                    <RejectIcon fontSize="small" color="error" />
                  </ListItemIcon>
                  <ListItemText>Rejeitar</ListItemText>
                </MenuItem>
              </>
            )}
          </Menu>

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
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogTitle sx={{ pb: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                {actionType === 'create' ? 'Solicitar Licença' : 'Editar Licença'}
              </Typography>
              <IconButton onClick={() => setIsFormOpen(false)} size="small">
                <CloseIcon />
              </IconButton>
            </Box>
          </DialogTitle>
          
          <DialogContent dividers>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
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
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Box sx={{ flex: '1 1 200px' }}>
                  <Controller
                  name="tipo"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Tipo de Licença *</InputLabel>
                      <Select
                        {...field}
                        label="Tipo de Licença *"
                      >
                        <MenuItem value="Ferias">Férias</MenuItem>
                        <MenuItem value="Medica">Médica</MenuItem>
                        <MenuItem value="Maternidade">Maternidade</MenuItem>
                        <MenuItem value="Paternidade">Paternidade</MenuItem>
                        <MenuItem value="Outras">Outras</MenuItem>
                      </Select>
                    </FormControl>
                  )}
                />
                </Box>
                
                <Box sx={{ flex: '1 1 200px' }}>
                  <Controller
                    name="estado"
                    control={control}
                    render={({ field }) => (
                      <FormControl fullWidth>
                        <InputLabel>Estado</InputLabel>
                        <Select
                          {...field}
                          label="Estado"
                        >
                          <MenuItem value="Pendente">Pendente</MenuItem>
                          <MenuItem value="Aprovada">Aprovada</MenuItem>
                          <MenuItem value="Rejeitada">Rejeitada</MenuItem>
                        </Select>
                      </FormControl>
                    )}
                  />
                </Box>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Box sx={{ flex: '1 1 200px' }}>
                  <Controller
                    name="dataInicio"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Data de Início *"
                        type="date"
                        InputLabelProps={{ shrink: true }}
                        error={!!errors.dataInicio}
                        helperText={errors.dataInicio?.message}
                      />
                    )}
                  />
                </Box>
                
                <Box sx={{ flex: '1 1 200px' }}>
                  <Controller
                    name="dataFim"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Data de Fim *"
                        type="date"
                        InputLabelProps={{ shrink: true }}
                        error={!!errors.dataFim}
                        helperText={errors.dataFim?.message}
                      />
                    )}
                  />
                </Box>
              </Box>
              
              <Box>
                <Controller
                  name="motivo"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label="Motivo"
                      multiline
                      rows={3}
                      error={!!errors.motivo}
                      helperText={errors.motivo?.message}
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
              {actionType === 'create' ? 'Solicitar' : 'Salvar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Confirm Dialog */}
      <ConfirmDialog
        open={isConfirmOpen}
        onClose={() => setIsConfirmOpen(false)}
        onConfirm={handleConfirm}
        title={actionType === 'approve' ? 'Aprovar Licença' : 'Rejeitar Licença'}
        message={
          actionType === 'approve'
            ? `Tem certeza que deseja aprovar a licença de ${selectedLicenca ? getFuncionarioNome(selectedLicenca.funcionarioID) : ''}?`
            : `Tem certeza que deseja rejeitar a licença de ${selectedLicenca ? getFuncionarioNome(selectedLicenca.funcionarioID) : ''}?`
        }
        confirmText={actionType === 'approve' ? 'Aprovar' : 'Rejeitar'}
        severity={actionType === 'approve' ? 'info' : 'warning'}
      />

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

export default LicencasList;
