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
  Tabs,
  Tab,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PersonAdd as PersonAddIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
  Person as PersonIcon,
  Close as CloseIcon,
  CardGiftcard as BenefitIcon,
  Assignment as AssignIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { 
  Beneficio, 
  BeneficioFormData,
  FuncionarioBeneficio,
  FuncionarioBeneficioFormData,
  Funcionario
} from '../../types/rrhh';
import { 
  getBeneficios, 
  createBeneficio, 
  updateBeneficio,
  deleteBeneficio,
  getFuncionarioBeneficios,
  createFuncionarioBeneficio,
  updateFuncionarioBeneficio,
  deleteFuncionarioBeneficio,
  getFuncionarios
} from '../../services/api/rrhh';
import ConfirmDialog from '../../components/funcionarios/ConfirmDialog';

// Schemas de validação
const beneficioSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório').max(100, 'Nome muito longo'),
  descricao: z.string().optional(),
  tipo: z.enum(['Saude', 'Transporte', 'Alimentacao', 'Seguro', 'Outros']),
});

const funcionarioBeneficioSchema = z.object({
  funcionarioID: z.number().min(1, 'Funcionário é obrigatório'),
  beneficioID: z.number().min(1, 'Benefício é obrigatório'),
  dataInicio: z.string().min(1, 'Data de início é obrigatória'),
  dataFim: z.string().optional(),
  estado: z.enum(['Activo', 'Inactivo']),
}).refine((data) => {
  if (data.dataFim) {
    return new Date(data.dataInicio) <= new Date(data.dataFim);
  }
  return true;
}, {
  message: 'Data de fim deve ser posterior à data de início',
  path: ['dataFim'],
});

const BeneficiosList: React.FC = () => {
  const [beneficios, setBeneficios] = useState<Beneficio[]>([]);
  const [funcionariosBeneficios, setFuncionariosBeneficios] = useState<FuncionarioBeneficio[]>([]);
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [currentTab, setCurrentTab] = useState(0);
  
  // Dialog states
  const [isBeneficioFormOpen, setIsBeneficioFormOpen] = useState(false);
  const [isAssignFormOpen, setIsAssignFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedBeneficio, setSelectedBeneficio] = useState<Beneficio | null>(null);
  const [selectedFuncBeneficio, setSelectedFuncBeneficio] = useState<FuncionarioBeneficio | null>(null);
  const [actionType, setActionType] = useState<'create' | 'edit' | 'delete' | 'assign'>('create');

  // Filter states
  const [filters, setFilters] = useState({
    nome: '',
    tipo: '',
    funcionarioID: undefined as number | undefined,
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

  // Forms
  const beneficioForm = useForm<BeneficioFormData>({
    resolver: zodResolver(beneficioSchema),
    defaultValues: {
      nome: '',
      descricao: '',
      tipo: 'Outros',
    },
  });

  const assignForm = useForm<FuncionarioBeneficioFormData>({
    resolver: zodResolver(funcionarioBeneficioSchema),
    defaultValues: {
      funcionarioID: 0,
      beneficioID: 0,
      dataInicio: new Date().toISOString().split('T')[0],
      dataFim: '',
      estado: 'Activo',
    },
  });

  useEffect(() => {
    loadData();
  }, [currentPage, rowsPerPage, filters, currentTab]);

  const loadData = async () => {
    try {
      setLoading(true);
      if (currentTab === 0) {
        await loadBeneficios();
      } else {
        await loadFuncionariosBeneficios();
      }
      await loadFuncionarios();
    } catch (error) {
      showNotification('Erro ao carregar dados', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadBeneficios = async () => {
    try {
      const response = await getBeneficios();
      
      if (response.success && response.data) {
        setBeneficios(response.data || []);
        setTotalCount(response.data?.length || 0);
      }
    } catch (error: any) {
      console.error('Erro ao carregar benefícios:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockBeneficios: Beneficio[] = [
          {
            id: 1,
            beneficioID: 1,
            nome: 'Seguro de Saúde',
            descricao: 'Cobertura médica completa',
            tipo: 'Saude'
          },
          {
            id: 2,
            beneficioID: 2,
            nome: 'Vale Transporte',
            descricao: 'Subsídio para transporte público',
            tipo: 'Transporte'
          },
          {
            id: 3,
            beneficioID: 3,
            nome: 'Vale Alimentação',
            descricao: 'Subsídio para alimentação',
            tipo: 'Alimentacao'
          }
        ];
        
        setBeneficios(mockBeneficios);
        setTotalCount(mockBeneficios.length);
        showNotification('Usando dados de demonstração - API não disponível', 'warning');
      }
    }
  };

  const loadFuncionariosBeneficios = async () => {
    try {
      const response = await getFuncionarioBeneficios();
      
      if (response.success) {
        setFuncionariosBeneficios(response.data || []);
        setTotalCount(response.data?.length || 0);
      }
    } catch (error: any) {
      console.error('Erro ao carregar funcionários-benefícios:', error);
      
      // Mock data fallback for 404 or network errors
      if (error?.status === 404 || error?.code === 'NETWORK_ERROR' || error?.message?.includes('fetch')) {
        const mockFuncionariosBeneficios: FuncionarioBeneficio[] = [
          {
            id: 1,
            funcionarioBeneficioID: 1,
            funcionarioID: 1,
            beneficioID: 1,
            dataInicio: '2024-01-15',
            estado: 'Activo',
            funcionario: { id: 1, funcionarioID: 1, nome: 'João', apelido: 'Silva', bi: '123456789', dataAdmissao: '2024-01-15', estadoFuncionario: 'Activo' },
            beneficio: { id: 1, beneficioID: 1, nome: 'Seguro de Saúde', tipo: 'Saude' }
          },
          {
            id: 2,
            funcionarioBeneficioID: 2,
            funcionarioID: 2,
            beneficioID: 2,
            dataInicio: '2024-02-01',
            estado: 'Activo',
            funcionario: { id: 2, funcionarioID: 2, nome: 'Maria', apelido: 'Santos', bi: '987654321', dataAdmissao: '2024-02-01', estadoFuncionario: 'Activo' },
            beneficio: { id: 2, beneficioID: 2, nome: 'Vale Transporte', tipo: 'Transporte' }
          }
        ];
        
        setFuncionariosBeneficios(mockFuncionariosBeneficios);
        setTotalCount(mockFuncionariosBeneficios.length);
        showNotification('Usando dados de demonstração - API não disponível', 'warning');
      }
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
    loadData();
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

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
    setCurrentPage(0);
  };

  // Beneficio handlers
  const handleAddBeneficio = () => {
    beneficioForm.reset({ nome: '', descricao: '', tipo: 'Outros' });
    setSelectedBeneficio(null);
    setActionType('create');
    setIsBeneficioFormOpen(true);
  };

  const handleEditBeneficio = (beneficio: Beneficio) => {
    beneficioForm.reset({
      nome: beneficio.nome,
      descricao: beneficio.descricao || '',
      tipo: beneficio.tipo,
    });
    setSelectedBeneficio(beneficio);
    setActionType('edit');
    setIsBeneficioFormOpen(true);
  };

  const handleDeleteBeneficio = (beneficio: Beneficio) => {
    setSelectedBeneficio(beneficio);
    setActionType('delete');
    setIsConfirmOpen(true);
  };

  const handleBeneficioSubmit = async (data: BeneficioFormData) => {
    try {
      let response;
      if (actionType === 'create') {
        response = await createBeneficio(data);
      } else if (selectedBeneficio) {
        response = await updateBeneficio(selectedBeneficio.beneficioID, data);
      }

      if (response?.success) {
        setIsBeneficioFormOpen(false);
        loadData();
        showNotification(
          actionType === 'create' ? 'Benefício criado com sucesso!' : 'Benefício atualizado com sucesso!',
          'success'
        );
      } else {
        showNotification(response?.message || 'Erro ao salvar benefício', 'error');
      }
    } catch (error: any) {
      showNotification(error.response?.data?.message || 'Erro ao salvar benefício', 'error');
    }
  };

  // Assign handlers
  const handleAssignBeneficio = (beneficio?: Beneficio) => {
    assignForm.reset({
      funcionarioID: 0,
      beneficioID: beneficio?.beneficioID || 0,
      dataInicio: new Date().toISOString().split('T')[0],
      dataFim: '',
      estado: 'Activo',
    });
    setSelectedFuncBeneficio(null);
    setActionType('assign');
    setIsAssignFormOpen(true);
  };

  const handleEditAssignment = (funcBeneficio: FuncionarioBeneficio) => {
    assignForm.reset({
      funcionarioID: funcBeneficio.funcionarioID,
      beneficioID: funcBeneficio.beneficioID,
      dataInicio: funcBeneficio.dataInicio,
      dataFim: funcBeneficio.dataFim || '',
      estado: funcBeneficio.estado,
    });
    setSelectedFuncBeneficio(funcBeneficio);
    setActionType('edit');
    setIsAssignFormOpen(true);
  };

  const handleDeleteAssignment = (funcBeneficio: FuncionarioBeneficio) => {
    setSelectedFuncBeneficio(funcBeneficio);
    setActionType('delete');
    setIsConfirmOpen(true);
  };

  const handleAssignSubmit = async (data: FuncionarioBeneficioFormData) => {
    try {
      let response;
      if (actionType === 'assign') {
        response = await createFuncionarioBeneficio(data);
      } else if (selectedFuncBeneficio) {
        response = await updateFuncionarioBeneficio(selectedFuncBeneficio.funcionarioBeneficioID, data);
      }

      if (response?.success) {
        setIsAssignFormOpen(false);
        loadData();
        showNotification(
          actionType === 'assign' ? 'Benefício associado com sucesso!' : 'Associação atualizada com sucesso!',
          'success'
        );
      } else {
        showNotification(response?.message || 'Erro ao associar benefício', 'error');
      }
    } catch (error: any) {
      showNotification(error.response?.data?.message || 'Erro ao associar benefício', 'error');
    }
  };

  const handleConfirm = async () => {
    try {
      let response;
      if (actionType === 'delete') {
        if (selectedBeneficio) {
          response = await deleteBeneficio(selectedBeneficio.beneficioID);
        } else if (selectedFuncBeneficio) {
          response = await deleteFuncionarioBeneficio(selectedFuncBeneficio.funcionarioBeneficioID);
        }
      }

      if (response?.success) {
        setIsConfirmOpen(false);
        loadData();
        showNotification('Item removido com sucesso!', 'success');
      } else {
        showNotification(response?.message || 'Erro ao remover item', 'error');
      }
    } catch (error) {
      showNotification('Erro ao remover item', 'error');
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

  const getBeneficioNome = (beneficioID: number) => {
    const beneficio = (beneficios || []).find(b => b.beneficioID === beneficioID);
    return beneficio?.nome || 'N/A';
  };

  const getTipoLabel = (tipo: string) => {
    switch (tipo) {
      case 'Saude': return 'Saúde';
      case 'Transporte': return 'Transporte';
      case 'Alimentacao': return 'Alimentação';
      case 'Seguro': return 'Seguro';
      case 'Outros': return 'Outros';
      default: return tipo;
    }
  };

  const getTipoColor = (tipo: string) => {
    switch (tipo) {
      case 'Saude': return 'error';
      case 'Transporte': return 'info';
      case 'Alimentacao': return 'warning';
      case 'Seguro': return 'success';
      default: return 'default';
    }
  };

  const getStatusColor = (estado: string) => {
    return estado === 'Activo' ? 'success' : 'error';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4" component="h1">
              Gestão de Benefícios
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                variant="outlined"
                startIcon={<AssignIcon />}
                onClick={() => handleAssignBeneficio()}
              >
                Associar Benefício
              </Button>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddBeneficio}
              >
                Novo Benefício
              </Button>
            </Box>
          </Box>

          {/* Tabs */}
          <Tabs value={currentTab} onChange={handleTabChange} sx={{ mb: 3 }}>
            <Tab label="Benefícios" />
            <Tab label="Funcionários & Benefícios" />
          </Tabs>

          {/* Filters */}
          <Card sx={{ mb: 3, bgcolor: 'grey.50' }}>
            <CardContent>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
                {currentTab === 0 ? (
                  <>
                    <Box sx={{ minWidth: 200, flex: '1 1 200px' }}>
                      <TextField
                        fullWidth
                        label="Buscar por nome"
                        size="small"
                        value={filters.nome}
                        onChange={(e) => handleFilterChange('nome', e.target.value)}
                      />
                    </Box>
                    <Box sx={{ minWidth: 140, flex: '1 1 140px' }}>
                      <FormControl fullWidth size="small">
                        <InputLabel>Tipo</InputLabel>
                        <Select
                          value={filters.tipo || ''}
                          label="Tipo"
                          onChange={(e) => handleFilterChange('tipo', e.target.value)}
                        >
                          <MenuItem value="">Todos</MenuItem>
                          <MenuItem value="Saude">Saúde</MenuItem>
                          <MenuItem value="Transporte">Transporte</MenuItem>
                          <MenuItem value="Alimentacao">Alimentação</MenuItem>
                          <MenuItem value="Seguro">Seguro</MenuItem>
                          <MenuItem value="Outros">Outros</MenuItem>
                        </Select>
                      </FormControl>
                    </Box>
                  </>
                ) : (
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
                )}
                
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
                    <IconButton onClick={loadData}>
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Content based on tab */}
          {currentTab === 0 ? (
            // Benefícios Table
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Nome</TableCell>
                    <TableCell>Tipo</TableCell>
                    <TableCell>Descrição</TableCell>
                    <TableCell align="center">Funcionários Associados</TableCell>
                    <TableCell align="center">Ações</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {loading ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        Carregando...
                      </TableCell>
                    </TableRow>
                  ) : beneficios.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center">
                        Nenhum benefício encontrado
                      </TableCell>
                    </TableRow>
                  ) : (
                    beneficios.map((beneficio) => {
                      const funcionariosCount = funcionariosBeneficios.filter(
                        fb => fb.beneficioID === beneficio.beneficioID && fb.estado === 'Activo'
                      ).length;
                      
                      return (
                        <TableRow key={beneficio.beneficioID}>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <BenefitIcon color="primary" />
                              <Typography variant="body2" fontWeight="medium">
                                {beneficio.nome}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={getTipoLabel(beneficio.tipo)}
                              color={getTipoColor(beneficio.tipo) as any}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" noWrap>
                              {beneficio.descricao || '-'}
                            </Typography>
                          </TableCell>
                          <TableCell align="center">
                            <Chip
                              label={funcionariosCount}
                              color="primary"
                              size="small"
                            />
                          </TableCell>
                          <TableCell align="center">
                            <Box sx={{ display: 'flex', gap: 0.5 }}>
                              <Tooltip title="Associar a funcionário">
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleAssignBeneficio(beneficio)}
                                  color="primary"
                                >
                                  <PersonAddIcon />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Editar">
                                <IconButton size="small" onClick={() => handleEditBeneficio(beneficio)}>
                                  <EditIcon />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Remover">
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleDeleteBeneficio(beneficio)}
                                  color="error"
                                >
                                  <DeleteIcon />
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
          ) : (
            // Funcionários-Benefícios Table
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Funcionário</TableCell>
                    <TableCell>Benefício</TableCell>
                    <TableCell>Tipo</TableCell>
                    <TableCell>Data Início</TableCell>
                    <TableCell>Data Fim</TableCell>
                    <TableCell>Estado</TableCell>
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
                  ) : funcionariosBeneficios.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={7} align="center">
                        Nenhuma associação encontrada
                      </TableCell>
                    </TableRow>
                  ) : (
                    funcionariosBeneficios.map((funcBeneficio) => {
                      const beneficio = (beneficios || []).find(b => b.beneficioID === funcBeneficio.beneficioID);
                      return (
                        <TableRow key={funcBeneficio.funcionarioBeneficioID}>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <Avatar
                                src={getFuncionarioFoto(funcBeneficio.funcionarioID)}
                                sx={{ width: 32, height: 32 }}
                              >
                                <PersonIcon />
                              </Avatar>
                              <Typography variant="body2">
                                {getFuncionarioNome(funcBeneficio.funcionarioID)}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>{getBeneficioNome(funcBeneficio.beneficioID)}</TableCell>
                          <TableCell>
                            <Chip
                              label={getTipoLabel(beneficio?.tipo || '')}
                              color={getTipoColor(beneficio?.tipo || '') as any}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            {new Date(funcBeneficio.dataInicio).toLocaleDateString('pt-AO')}
                          </TableCell>
                          <TableCell>
                            {funcBeneficio.dataFim ? 
                              new Date(funcBeneficio.dataFim).toLocaleDateString('pt-AO') : 
                              '-'
                            }
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={funcBeneficio.estado}
                              color={getStatusColor(funcBeneficio.estado) as any}
                              size="small"
                            />
                          </TableCell>
                          <TableCell align="center">
                            <Box sx={{ display: 'flex', gap: 0.5 }}>
                              <Tooltip title="Editar">
                                <IconButton size="small" onClick={() => handleEditAssignment(funcBeneficio)}>
                                  <EditIcon />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Remover">
                                <IconButton 
                                  size="small" 
                                  onClick={() => handleDeleteAssignment(funcBeneficio)}
                                  color="error"
                                >
                                  <DeleteIcon />
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
          )}

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

      {/* Beneficio Form Dialog */}
      <Dialog 
        open={isBeneficioFormOpen} 
        onClose={() => setIsBeneficioFormOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={beneficioForm.handleSubmit(handleBeneficioSubmit)}>
          <DialogTitle sx={{ pb: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                {actionType === 'create' ? 'Novo Benefício' : 'Editar Benefício'}
              </Typography>
              <IconButton onClick={() => setIsBeneficioFormOpen(false)} size="small">
                <CloseIcon />
              </IconButton>
            </Box>
          </DialogTitle>
          
          <DialogContent dividers>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <Box>
                <Controller
                  name="nome"
                  control={beneficioForm.control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label="Nome *"
                      error={!!beneficioForm.formState.errors.nome}
                      helperText={beneficioForm.formState.errors.nome?.message}
                    />
                  )}
                />
              </Box>
              
              <Box>
                <Controller
                  name="tipo"
                  control={beneficioForm.control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Tipo *</InputLabel>
                      <Select
                        {...field}
                        label="Tipo *"
                      >
                        <MenuItem value="Saude">Saúde</MenuItem>
                        <MenuItem value="Transporte">Transporte</MenuItem>
                        <MenuItem value="Alimentacao">Alimentação</MenuItem>
                        <MenuItem value="Seguro">Seguro</MenuItem>
                        <MenuItem value="Outros">Outros</MenuItem>
                      </Select>
                    </FormControl>
                  )}
                />
              </Box>
              
              <Box>
                <Controller
                  name="descricao"
                  control={beneficioForm.control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      fullWidth
                      label="Descrição"
                      multiline
                      rows={3}
                      error={!!beneficioForm.formState.errors.descricao}
                      helperText={beneficioForm.formState.errors.descricao?.message}
                    />
                  )}
                />
              </Box>
            </Box>
          </DialogContent>
          
          <DialogActions sx={{ p: 2 }}>
            <Button onClick={() => setIsBeneficioFormOpen(false)}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained">
              {actionType === 'create' ? 'Criar' : 'Salvar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Assign Form Dialog */}
      <Dialog 
        open={isAssignFormOpen} 
        onClose={() => setIsAssignFormOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={assignForm.handleSubmit(handleAssignSubmit)}>
          <DialogTitle sx={{ pb: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Typography variant="h6">
                {actionType === 'assign' ? 'Associar Benefício' : 'Editar Associação'}
              </Typography>
              <IconButton onClick={() => setIsAssignFormOpen(false)} size="small">
                <CloseIcon />
              </IconButton>
            </Box>
          </DialogTitle>
          
          <DialogContent dividers>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <Box>
                <Controller
                  name="funcionarioID"
                  control={assignForm.control}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!assignForm.formState.errors.funcionarioID}>
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
                      {assignForm.formState.errors.funcionarioID && (
                        <Typography variant="caption" color="error">
                          {assignForm.formState.errors.funcionarioID.message}
                        </Typography>
                      )}
                    </FormControl>
                  )}
                />
              </Box>
              
              <Box>
                <Controller
                  name="beneficioID"
                  control={assignForm.control}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!assignForm.formState.errors.beneficioID}>
                      <InputLabel>Benefício *</InputLabel>
                      <Select
                        {...field}
                        label="Benefício *"
                        value={field.value || ''}
                        onChange={(e) => field.onChange(Number(e.target.value))}
                      >
                        <MenuItem value="">Selecione um benefício</MenuItem>
                        {(beneficios || []).map((beneficio) => (
                          <MenuItem key={beneficio.beneficioID} value={beneficio.beneficioID}>
                            {beneficio.nome} ({getTipoLabel(beneficio.tipo)})
                          </MenuItem>
                        ))}
                      </Select>
                      {assignForm.formState.errors.beneficioID && (
                        <Typography variant="caption" color="error">
                          {assignForm.formState.errors.beneficioID.message}
                        </Typography>
                      )}
                    </FormControl>
                  )}
                />
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
                  <Controller
                    name="dataInicio"
                    control={assignForm.control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Data de Início *"
                        type="date"
                        InputLabelProps={{ shrink: true }}
                        error={!!assignForm.formState.errors.dataInicio}
                        helperText={assignForm.formState.errors.dataInicio?.message}
                      />
                    )}
                  />
                </Box>
                
                <Box sx={{ flex: '1 1 200px', minWidth: 200 }}>
                  <Controller
                    name="dataFim"
                    control={assignForm.control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        fullWidth
                        label="Data de Fim"
                        type="date"
                        InputLabelProps={{ shrink: true }}
                        error={!!assignForm.formState.errors.dataFim}
                        helperText={assignForm.formState.errors.dataFim?.message || 'Deixe em branco se não tem fim'}
                      />
                    )}
                  />
                </Box>
              </Box>
              
              <Box>
                <Controller
                  name="estado"
                  control={assignForm.control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Estado</InputLabel>
                      <Select
                        {...field}
                        label="Estado"
                      >
                        <MenuItem value="Activo">Activo</MenuItem>
                        <MenuItem value="Inactivo">Inactivo</MenuItem>
                      </Select>
                    </FormControl>
                  )}
                />
              </Box>
            </Box>
          </DialogContent>
          
          <DialogActions sx={{ p: 2 }}>
            <Button onClick={() => setIsAssignFormOpen(false)}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained">
              {actionType === 'assign' ? 'Associar' : 'Salvar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Confirm Dialog */}
      <ConfirmDialog
        open={isConfirmOpen}
        onClose={() => setIsConfirmOpen(false)}
        onConfirm={handleConfirm}
        title="Remover Item"
        message={
          selectedBeneficio
            ? `Tem certeza que deseja remover o benefício "${selectedBeneficio.nome}"?`
            : selectedFuncBeneficio
            ? `Tem certeza que deseja remover a associação do benefício?`
            : 'Tem certeza que deseja remover este item?'
        }
        severity="warning"
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

export default BeneficiosList;
