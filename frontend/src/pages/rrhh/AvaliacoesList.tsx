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
  Rating,
  Divider,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Visibility as ViewIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
  Person as PersonIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { 
  Avaliacao, 
  AvaliacaoFormData,
  Funcionario
} from '../../types/rrhh';
import { 
  getAvaliacoes, 
  createAvaliacao, 
  updateAvaliacao,
  getFuncionarios
} from '../../services/api/rrhh.js';

// Schema de validação
const avaliacaoSchema = z.object({
  funcionarioID: z.number().min(1, 'Funcionário é obrigatório'),
  dataAvaliacao: z.string().min(1, 'Data da avaliação é obrigatória'),
  assiduidade: z.number().min(1, 'Assiduidade é obrigatória').max(5, 'Máximo 5'),
  competenciasTecnicas: z.number().min(1, 'Competências técnicas é obrigatória').max(5, 'Máximo 5'),
  softSkills: z.number().min(1, 'Soft Skills é obrigatória').max(5, 'Máximo 5'),
  comentarios: z.string().optional(),
});

const AvaliacoesList: React.FC = () => {
  const [avaliacoes, setAvaliacoes] = useState<Avaliacao[]>([]);
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  
  // Dialog states
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [selectedAvaliacao, setSelectedAvaliacao] = useState<Avaliacao | null>(null);
  const [actionType, setActionType] = useState<'create' | 'edit'>('create');

  // Filter states
  const [filters, setFilters] = useState({
    funcionarioID: undefined as number | undefined,
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
    watch,
  } = useForm<AvaliacaoFormData>({
    resolver: zodResolver(avaliacaoSchema),
    defaultValues: {
      funcionarioID: 0,
      dataAvaliacao: new Date().toISOString().split('T')[0],
      assiduidade: 3,
      competenciasTecnicas: 3,
      softSkills: 3,
      comentarios: '',
    },
  });

  const watchedValues = watch(['assiduidade', 'competenciasTecnicas', 'softSkills']);

  useEffect(() => {
    loadAvaliacoes();
    loadFuncionarios();
  }, [currentPage, rowsPerPage, filters]);

  const loadAvaliacoes = async () => {
    try {
      setLoading(true);
      const response = await getAvaliacoes();
      
      if (response.success && response.data) {
        setAvaliacoes(response.data);
        setTotalCount(response.data.length);
      }
    } catch (error: any) {
      console.error('Erro ao carregar avaliações:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockAvaliacoes: Avaliacao[] = [
          {
            id: 1,
            avaliacaoID: 1,
            funcionarioID: 1,
            dataAvaliacao: '2024-12-01',
            assiduidade: 4,
            competenciasTecnicas: 5,
            softSkills: 4,
            comentarios: 'Excelente desempenho técnico',
            funcionario: { id: 1, funcionarioID: 1, nome: 'João', apelido: 'Silva', bi: '123456789', dataAdmissao: '2024-01-15', estadoFuncionario: 'Activo' }
          },
          {
            id: 2,
            avaliacaoID: 2,
            funcionarioID: 2,
            dataAvaliacao: '2024-11-15',
            assiduidade: 5,
            competenciasTecnicas: 4,
            softSkills: 5,
            comentarios: 'Ótima capacidade de trabalho em equipe',
            funcionario: { id: 2, funcionarioID: 2, nome: 'Maria', apelido: 'Santos', bi: '987654321', dataAdmissao: '2024-02-01', estadoFuncionario: 'Activo' }
          }
        ];
        
        setAvaliacoes(mockAvaliacoes);
        setTotalCount(mockAvaliacoes.length);
        showNotification('Usando dados de demonstração - API não disponível', 'warning');
      } else {
        showNotification('Erro ao carregar avaliações', 'error');
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
    loadAvaliacoes();
  };

  const handleFilterChange = (field: string, value: string | number) => {
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
      dataAvaliacao: new Date().toISOString().split('T')[0],
      assiduidade: 3,
      competenciasTecnicas: 3,
      softSkills: 3,
      comentarios: '',
    });
    setSelectedAvaliacao(null);
    setActionType('create');
    setIsFormOpen(true);
  };

  const handleEdit = (avaliacao: Avaliacao) => {
    reset({
      funcionarioID: avaliacao.funcionarioID,
      dataAvaliacao: avaliacao.dataAvaliacao,
      assiduidade: avaliacao.assiduidade,
      competenciasTecnicas: avaliacao.competenciasTecnicas,
      softSkills: avaliacao.softSkills,
      comentarios: avaliacao.comentarios || '',
    });
    setSelectedAvaliacao(avaliacao);
    setActionType('edit');
    setIsFormOpen(true);
  };

  const handleView = (avaliacao: Avaliacao) => {
    setSelectedAvaliacao(avaliacao);
    setIsDetailOpen(true);
  };

  const onSubmit = async (data: AvaliacaoFormData) => {
    try {
      let response;
      if (actionType === 'create') {
        response = await createAvaliacao(data);
      } else if (selectedAvaliacao) {
        response = await updateAvaliacao(selectedAvaliacao.avaliacaoID, data);
      }

      if (response?.success) {
        setIsFormOpen(false);
        loadAvaliacoes();
        showNotification(
          actionType === 'create' ? 'Avaliação registrada com sucesso!' : 'Avaliação atualizada com sucesso!',
          'success'
        );
      } else {
        showNotification(response?.message || 'Erro ao salvar avaliação', 'error');
      }
    } catch (error: any) {
      showNotification(error.response?.data?.message || 'Erro ao salvar avaliação', 'error');
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

  const calculateMediaGeral = (assiduidade: number, competenciasTecnicas: number, softSkills: number) => {
    return ((assiduidade + competenciasTecnicas + softSkills) / 3);
  };

  const getPerformanceColor = (media: number) => {
    if (media >= 4.5) return 'success';
    if (media >= 3.5) return 'warning';
    return 'error';
  };

  const getPerformanceLabel = (media: number) => {
    if (media >= 4.5) return 'Excelente';
    if (media >= 3.5) return 'Bom';
    if (media >= 2.5) return 'Regular';
    return 'Precisa Melhorar';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4" component="h1">
              Avaliações de Desempenho
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleAdd}
            >
              Nova Avaliação
            </Button>
          </Box>

          {/* Filters */}
          <Card sx={{ mb: 3, bgcolor: 'grey.50' }}>
            <CardContent>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
                <Box sx={{ minWidth: 250, flex: '1 1 300px' }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Funcionário</InputLabel>
                    <Select
                      value={filters.funcionarioID || ''}
                      label="Funcionário"
                      onChange={(e) => handleFilterChange('funcionarioID', e.target.value || '')}
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
                <Box sx={{ minWidth: 160, flex: '1 1 180px' }}>
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
                <Box sx={{ minWidth: 160, flex: '1 1 180px' }}>
                  <TextField
                    fullWidth
                    label="Data Fim"
                    type="date"
                    size="small"
                    value={filters.dataFim || ''}
                    onChange={(e) => handleFilterChange('dataFim', e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                </Box>
                <Box sx={{ minWidth: 140, flex: '1 1 160px' }}>
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
                      <IconButton onClick={loadAvaliacoes}>
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
                  <TableCell>Data Avaliação</TableCell>
                  <TableCell align="center">Assiduidade</TableCell>
                  <TableCell align="center">Competências</TableCell>
                  <TableCell align="center">Soft Skills</TableCell>
                  <TableCell align="center">Média Geral</TableCell>
                  <TableCell>Performance</TableCell>
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
                ) : (avaliacoes || []).length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} align="center">
                      Nenhuma avaliação encontrada
                    </TableCell>
                  </TableRow>
                ) : (
                  (avaliacoes || []).map((avaliacao) => {
                    const media = calculateMediaGeral(
                      avaliacao.assiduidade,
                      avaliacao.competenciasTecnicas,
                      avaliacao.softSkills
                    );
                    return (
                      <TableRow key={avaliacao.avaliacaoID}>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Avatar
                              src={getFuncionarioFoto(avaliacao.funcionarioID)}
                              sx={{ width: 32, height: 32 }}
                            >
                              <PersonIcon />
                            </Avatar>
                            <Typography variant="body2">
                              {getFuncionarioNome(avaliacao.funcionarioID)}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          {new Date(avaliacao.dataAvaliacao).toLocaleDateString('pt-AO')}
                        </TableCell>
                        <TableCell align="center">
                          <Rating value={avaliacao.assiduidade} readOnly size="small" />
                        </TableCell>
                        <TableCell align="center">
                          <Rating value={avaliacao.competenciasTecnicas} readOnly size="small" />
                        </TableCell>
                        <TableCell align="center">
                          <Rating value={avaliacao.softSkills} readOnly size="small" />
                        </TableCell>
                        <TableCell align="center">
                          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                            <Rating value={media} readOnly size="small" precision={0.1} />
                            <Typography variant="body2" fontWeight="medium">
                              {media.toFixed(1)}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={getPerformanceLabel(media)}
                            color={getPerformanceColor(media) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell align="center">
                          <Box sx={{ display: 'flex', gap: 0.5 }}>
                            <Tooltip title="Ver detalhes">
                              <IconButton size="small" onClick={() => handleView(avaliacao)}>
                                <ViewIcon />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Editar">
                              <IconButton size="small" onClick={() => handleEdit(avaliacao)}>
                                <EditIcon />
                              </IconButton>
                            </Tooltip>
                          </Box>
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
                {actionType === 'create' ? 'Nova Avaliação' : 'Editar Avaliação'}
              </Typography>
              <IconButton onClick={() => setIsFormOpen(false)} size="small">
                <CloseIcon />
              </IconButton>
            </Box>
          </DialogTitle>
          
          <DialogContent dividers>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Box sx={{ flex: '1 1 200px' }}>
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
                
                <Box sx={{ flex: '1 1 200px' }}>
                  <Controller
                    name="dataAvaliacao"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Data da Avaliação *"
                        type="date"
                        InputLabelProps={{ shrink: true }}
                        error={!!errors.dataAvaliacao}
                        helperText={errors.dataAvaliacao?.message}
                      />
                    )}
                  />
                </Box>
              </Box>

              <Box>
                <Divider sx={{ my: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Critérios de Avaliação
                </Typography>
              </Box>
              
              <Box>
                <Controller
                  name="assiduidade"
                  control={control}
                  render={({ field }) => (
                    <Box>
                      <Typography component="legend" gutterBottom>
                        Assiduidade *
                      </Typography>
                      <Rating
                        {...field}
                        precision={1}
                        size="large"
                        onChange={(_, value) => field.onChange(value || 1)}
                      />
                      {errors.assiduidade && (
                        <Typography variant="caption" color="error" display="block">
                          {errors.assiduidade.message}
                        </Typography>
                      )}
                    </Box>
                  )}
                />
              </Box>
              
              <Box>
                <Controller
                  name="competenciasTecnicas"
                  control={control}
                  render={({ field }) => (
                    <Box>
                      <Typography component="legend" gutterBottom>
                        Competências Técnicas *
                      </Typography>
                      <Rating
                        {...field}
                        precision={1}
                        size="large"
                        onChange={(_, value) => field.onChange(value || 1)}
                      />
                      {errors.competenciasTecnicas && (
                        <Typography variant="caption" color="error" display="block">
                          {errors.competenciasTecnicas.message}
                        </Typography>
                      )}
                    </Box>
                  )}
                />
              </Box>
              
              <Box>
                <Controller
                  name="softSkills"
                  control={control}
                  render={({ field }) => (
                    <Box>
                      <Typography component="legend" gutterBottom>
                        Soft Skills *
                      </Typography>
                      <Rating
                        {...field}
                        precision={1}
                        size="large"
                        onChange={(_, value) => field.onChange(value || 1)}
                      />
                      {errors.softSkills && (
                        <Typography variant="caption" color="error" display="block">
                          {errors.softSkills.message}
                        </Typography>
                      )}
                    </Box>
                  )}
                />
              </Box>

              {/* Preview da média */}
              <Box>
                <Card sx={{ bgcolor: 'grey.50', p: 2 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Média Geral: {calculateMediaGeral(watchedValues[0], watchedValues[1], watchedValues[2]).toFixed(1)}
                  </Typography>
                  <Rating 
                    value={calculateMediaGeral(watchedValues[0], watchedValues[1], watchedValues[2])} 
                    readOnly 
                    precision={0.1} 
                  />
                  <Chip
                    label={getPerformanceLabel(calculateMediaGeral(watchedValues[0], watchedValues[1], watchedValues[2]))}
                    color={getPerformanceColor(calculateMediaGeral(watchedValues[0], watchedValues[1], watchedValues[2])) as any}
                    size="small"
                    sx={{ ml: 1 }}
                  />
                </Card>
              </Box>
              
              <Box>
                <Controller
                  name="comentarios"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label="Comentários"
                      multiline
                      rows={4}
                      placeholder="Observações adicionais sobre o desempenho do funcionário..."
                      error={!!errors.comentarios}
                      helperText={errors.comentarios?.message}
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
              {actionType === 'create' ? 'Registrar' : 'Salvar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Detail Dialog */}
      {selectedAvaliacao && (
        <Dialog 
          open={isDetailOpen} 
          onClose={() => setIsDetailOpen(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                Detalhes da Avaliação
              </Typography>
              <IconButton onClick={() => setIsDetailOpen(false)} size="small">
                <CloseIcon />
              </IconButton>
            </Box>
          </DialogTitle>
          
          <DialogContent dividers>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                  <Avatar
                    src={getFuncionarioFoto(selectedAvaliacao.funcionarioID)}
                    sx={{ width: 48, height: 48 }}
                  >
                    <PersonIcon />
                  </Avatar>
                  <Box>
                    <Typography variant="h6">
                      {getFuncionarioNome(selectedAvaliacao.funcionarioID)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Avaliação de {new Date(selectedAvaliacao.dataAvaliacao).toLocaleDateString('pt-AO')}
                    </Typography>
                  </Box>
                </Box>
              </Box>
              
              <Box>
                <Typography variant="subtitle2" gutterBottom>Assiduidade</Typography>
                <Rating value={selectedAvaliacao.assiduidade} readOnly />
              </Box>
              
              <Box>
                <Typography variant="subtitle2" gutterBottom>Competências Técnicas</Typography>
                <Rating value={selectedAvaliacao.competenciasTecnicas} readOnly />
              </Box>
              
              <Box>
                <Typography variant="subtitle2" gutterBottom>Soft Skills</Typography>
                <Rating value={selectedAvaliacao.softSkills} readOnly />
              </Box>
              
              <Box>
                <Divider sx={{ my: 1 }} />
                <Typography variant="subtitle2" gutterBottom>Média Geral</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Rating 
                    value={calculateMediaGeral(
                      selectedAvaliacao.assiduidade,
                      selectedAvaliacao.competenciasTecnicas,
                      selectedAvaliacao.softSkills
                    )} 
                    readOnly 
                    precision={0.1}
                  />
                  <Typography variant="h6">
                    {calculateMediaGeral(
                      selectedAvaliacao.assiduidade,
                      selectedAvaliacao.competenciasTecnicas,
                      selectedAvaliacao.softSkills
                    ).toFixed(1)}
                  </Typography>
                  <Chip
                    label={getPerformanceLabel(calculateMediaGeral(
                      selectedAvaliacao.assiduidade,
                      selectedAvaliacao.competenciasTecnicas,
                      selectedAvaliacao.softSkills
                    ))}
                    color={getPerformanceColor(calculateMediaGeral(
                      selectedAvaliacao.assiduidade,
                      selectedAvaliacao.competenciasTecnicas,
                      selectedAvaliacao.softSkills
                    )) as any}
                    size="small"
                  />
                </Box>
              </Box>
              
              {selectedAvaliacao.comentarios && (
                <Box>
                  <Typography variant="subtitle2" gutterBottom>Comentários</Typography>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="body2">
                      {selectedAvaliacao.comentarios}
                    </Typography>
                  </Paper>
                </Box>
              )}
            </Box>
          </DialogContent>
          
          <DialogActions>
            <Button onClick={() => setIsDetailOpen(false)}>
              Fechar
            </Button>
            <Button 
              variant="outlined"
              startIcon={<EditIcon />}
              onClick={() => {
                setIsDetailOpen(false);
                handleEdit(selectedAvaliacao);
              }}
            >
              Editar
            </Button>
          </DialogActions>
        </Dialog>
      )}

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

export default AvaliacoesList;
