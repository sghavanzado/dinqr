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
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  GetApp as ExportIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
  AccessTime as TimeIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { 
  Presenca, 
  PresencaFormData,
  PresencaFilter,
  Funcionario,
  Departamento,
} from '../../types/rrhh';
import { 
  getPresencas, 
  createPresenca, 
  updatePresenca,
  getFuncionarios,
  getDepartamentos,
} from '../../services/api/rrhh';

// Validation schema
const presencaSchema = z.object({
  funcionarioID: z.number().min(1, 'Funcionário é obrigatório'),
  data: z.string().min(1, 'Data é obrigatória'),
  horaEntrada: z.string().optional(),
  horaSaida: z.string().optional(),
  observacao: z.string().optional(),
});

const PresencasList: React.FC = () => {
  const [presencas, setPresencas] = useState<Presenca[]>([]);
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [loading, setLoading] = useState(false);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [editingPresenca, setEditingPresenca] = useState<Presenca | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [notification, setNotification] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'warning' | 'info';
  }>({
    open: false,
    message: '',
    severity: 'info'
  });

  const [filters, setFilters] = useState<PresencaFilter>({
    funcionarioID: undefined,
    departamentoID: undefined,
    dataInicio: '',
    dataFim: '',
    search: '',
  });

  const { control, handleSubmit, reset, formState: { errors } } = useForm<PresencaFormData>({
    resolver: zodResolver(presencaSchema),
  });

  useEffect(() => {
    loadPresencas();
    loadFuncionarios();
    loadDepartamentos();
  }, [currentPage, rowsPerPage, filters]);

  const showNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setNotification({ open: true, message, severity });
  };

  const loadPresencas = async () => {
    try {
      setLoading(true);
      const response = await getPresencas({
        ...filters,
        page: currentPage + 1,
        per_page: rowsPerPage,
      });
      
      if (response.success && response.data) {
        setPresencas(response.data);
        setTotalCount(response.total || 0);
      }
    } catch (error: any) {
      console.error('Erro ao carregar presenças:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockPresencas: Presenca[] = [
          {
            id: 1,
            presencaID: 1,
            funcionarioID: 1,
            data: '2024-12-09',
            horaEntrada: '08:00',
            horaSaida: '17:00',
            observacao: 'Presente',
            funcionario: { id: 1, funcionarioID: 1, nome: 'João', apelido: 'Silva', bi: '123456789', dataAdmissao: '2024-01-15', estadoFuncionario: 'Activo' }
          },
          {
            id: 2,
            presencaID: 2,
            funcionarioID: 2,
            data: '2024-12-09',
            horaEntrada: '08:30',
            horaSaida: '17:30',
            observacao: 'Presente - Atraso',
            funcionario: { id: 2, funcionarioID: 2, nome: 'Maria', apelido: 'Santos', bi: '987654321', dataAdmissao: '2024-02-01', estadoFuncionario: 'Activo' }
          },
          {
            id: 3,
            presencaID: 3,
            funcionarioID: 3,
            data: '2024-12-08',
            horaEntrada: '08:00',
            observacao: 'Falta',
            funcionario: { id: 3, funcionarioID: 3, nome: 'Pedro', apelido: 'Costa', bi: '456789123', dataAdmissao: '2024-03-01', estadoFuncionario: 'Activo' }
          }
        ];
        
        setPresencas(mockPresencas);
        setTotalCount(mockPresencas.length);
        showNotification('Usando dados de demonstração - API não disponível', 'warning');
      } else {
        showNotification('Erro ao carregar presenças', 'error');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadFuncionarios = async () => {
    try {
      const response = await getFuncionarios();
      if (response.success && response.data) {
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

  const loadDepartamentos = async () => {
    try {
      const response = await getDepartamentos();
      if (response.success && response.data) {
        setDepartamentos(response.data);
      }
    } catch (error: any) {
      console.error('Erro ao carregar departamentos:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockDepartamentos: Departamento[] = [
          { id: 1, departamentoID: 1, nome: 'Recursos Humanos', descricao: 'Gestão de pessoal' },
          { id: 2, departamentoID: 2, nome: 'Tecnologia', descricao: 'Desenvolvimento e TI' },
          { id: 3, departamentoID: 3, nome: 'Financeiro', descricao: 'Gestão financeira' }
        ];
        setDepartamentos(mockDepartamentos);
      }
    }
  };

  const handleSubmitPresenca = async (data: PresencaFormData) => {
    try {
      if (editingPresenca) {
        const response = await updatePresenca(editingPresenca.presencaID, data);
        if (response.success) {
          showNotification('Presença atualizada com sucesso!', 'success');
          loadPresencas();
          handleCloseDialog();
        }
      } else {
        const response = await createPresenca(data);
        if (response.success) {
          showNotification('Presença registrada com sucesso!', 'success');
          loadPresencas();
          handleCloseDialog();
        }
      }
    } catch (error: any) {
      console.error('Erro ao salvar presença:', error);
      
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        showNotification('Funcionalidade não disponível - API não conectada', 'warning');
      } else {
        showNotification('Erro ao salvar presença', 'error');
      }
    }
  };

  const handleEdit = (presenca: Presenca) => {
    setEditingPresenca(presenca);
    reset({
      funcionarioID: presenca.funcionarioID,
      data: presenca.data,
      horaEntrada: presenca.horaEntrada || '',
      horaSaida: presenca.horaSaida || '',
      observacao: presenca.observacao || '',
    });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingPresenca(null);
    reset({
      funcionarioID: 0,
      data: '',
      horaEntrada: '',
      horaSaida: '',
      observacao: '',
    });
  };

  const handlePageChange = (_: unknown, newPage: number) => {
    setCurrentPage(newPage);
  };

  const handleRowsPerPageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setCurrentPage(0);
  };

  const getStatusChip = (presenca: Presenca) => {
    if (!presenca.horaEntrada) {
      return <Chip label="Falta" color="error" size="small" />;
    }
    if (presenca.horaEntrada > '08:00') {
      return <Chip label="Atraso" color="warning" size="small" />;
    }
    return <Chip label="Presente" color="success" size="small" />;
  };

  const formatTime = (time?: string) => {
    return time ? time.substring(0, 5) : '-';
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Gestão de Presenças
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setDialogOpen(true)}
        >
          Nova Presença
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Filtros
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <TextField
              label="Pesquisar"
              variant="outlined"
              size="small"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              InputProps={{
                startAdornment: <SearchIcon sx={{ color: 'action.active', mr: 1 }} />,
              }}
              sx={{ minWidth: 200 }}
            />
            <FormControl size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Funcionário</InputLabel>
              <Select
                value={filters.funcionarioID || ''}
                label="Funcionário"
                onChange={(e) => setFilters({ ...filters, funcionarioID: Number(e.target.value) || undefined })}
              >
                <MenuItem value="">Todos</MenuItem>
                {funcionarios?.map((funcionario) => (
                  <MenuItem key={funcionario.funcionarioID} value={funcionario.funcionarioID}>
                    {funcionario.nome} {funcionario.apelido}
                  </MenuItem>
                )) || []}
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Departamento</InputLabel>
              <Select
                value={filters.departamentoID || ''}
                label="Departamento"
                onChange={(e) => setFilters({ ...filters, departamentoID: Number(e.target.value) || undefined })}
              >
                <MenuItem value="">Todos</MenuItem>
                {departamentos?.map((departamento) => (
                  <MenuItem key={departamento.departamentoID} value={departamento.departamentoID}>
                    {departamento.nome}
                  </MenuItem>
                )) || []}
              </Select>
            </FormControl>
            <TextField
              label="Data Início"
              type="date"
              size="small"
              value={filters.dataInicio}
              onChange={(e) => setFilters({ ...filters, dataInicio: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
            <TextField
              label="Data Fim"
              type="date"
              size="small"
              value={filters.dataFim}
              onChange={(e) => setFilters({ ...filters, dataFim: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={loadPresencas}
            >
              Atualizar
            </Button>
            <Button
              variant="outlined"
              startIcon={<ExportIcon />}
              onClick={() => showNotification('Funcionalidade de exportação em desenvolvimento', 'info')}
            >
              Exportar
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* Table */}
      <Card>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Funcionário</TableCell>
                <TableCell>Data</TableCell>
                <TableCell>Entrada</TableCell>
                <TableCell>Saída</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Observação</TableCell>
                <TableCell align="center">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    Carregando...
                  </TableCell>
                </TableRow>
              ) : !presencas || presencas?.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    Nenhuma presença encontrada
                  </TableCell>
                </TableRow>
              ) : (
                presencas?.map((presenca) => (
                  <TableRow key={presenca.presencaID}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Avatar sx={{ width: 32, height: 32 }}>
                          <PersonIcon />
                        </Avatar>
                        <Box>
                          <Typography variant="body2" fontWeight="medium">
                            {presenca.funcionario?.nome} {presenca.funcionario?.apelido}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            ID: {presenca.funcionarioID}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      {new Date(presenca.data).toLocaleDateString('pt-AO')}
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <TimeIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                        {formatTime(presenca.horaEntrada)}
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <TimeIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
                        {formatTime(presenca.horaSaida)}
                      </Box>
                    </TableCell>
                    <TableCell>
                      {getStatusChip(presenca)}
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {presenca.observacao || '-'}
                      </Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="Editar">
                        <IconButton
                          size="small"
                          onClick={() => handleEdit(presenca)}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          component="div"
          count={totalCount}
          page={currentPage}
          onPageChange={handlePageChange}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleRowsPerPageChange}
          rowsPerPageOptions={[5, 10, 25, 50]}
        />
      </Card>

      {/* Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingPresenca ? 'Editar Presença' : 'Nova Presença'}
        </DialogTitle>
        <form onSubmit={handleSubmit(handleSubmitPresenca)}>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
              <Controller
                name="funcionarioID"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth error={!!errors.funcionarioID}>
                    <InputLabel>Funcionário *</InputLabel>
                    <Select
                      {...field}
                      label="Funcionário *"
                    >
                      {funcionarios?.map((funcionario) => (
                        <MenuItem key={funcionario.funcionarioID} value={funcionario.funcionarioID}>
                          {funcionario.nome} {funcionario.apelido}
                        </MenuItem>
                      )) || []}
                    </Select>
                  </FormControl>
                )}
              />

              <Controller
                name="data"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Data *"
                    type="date"
                    fullWidth
                    error={!!errors.data}
                    helperText={errors.data?.message}
                    InputLabelProps={{ shrink: true }}
                  />
                )}
              />

              <Controller
                name="horaEntrada"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Hora de Entrada"
                    type="time"
                    fullWidth
                    InputLabelProps={{ shrink: true }}
                  />
                )}
              />

              <Controller
                name="horaSaida"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Hora de Saída"
                    type="time"
                    fullWidth
                    InputLabelProps={{ shrink: true }}
                  />
                )}
              />

              <Controller
                name="observacao"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Observação"
                    multiline
                    rows={3}
                    fullWidth
                  />
                )}
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained">
              {editingPresenca ? 'Atualizar' : 'Criar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Notification */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={() => setNotification({ ...notification, open: false })}
      >
        <Alert
          onClose={() => setNotification({ ...notification, open: false })}
          severity={notification.severity}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default PresencasList;
