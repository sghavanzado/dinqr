import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  Snackbar,
  Grid,
  Avatar,
  Chip,
  IconButton,
  Tooltip,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  CircularProgress,
} from '@mui/material';
import {
  Badge as BadgeIcon,
  Person as PersonIcon,
  Refresh as RefreshIcon,
  Business as BusinessIcon,
  Work as WorkIcon,
} from '@mui/icons-material';
import type { 
  Funcionario, 
  Departamento,
  Cargo,
} from '../../types/rrhh';
import { 
  getFuncionarios, 
  getDepartamentos, 
  getCargos
} from '../../services/api/rrhh';
import EmployeePass from '../../components/funcionarios/EmployeePass';

const PassesList: React.FC = () => {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [cargos, setCargos] = useState<Cargo[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<{
    departamentoID?: number;
    cargoID?: number;
    estadoFuncionario?: string;
    search?: string;
  }>({});

  // Dialog states
  const [selectedFuncionario, setSelectedFuncionario] = useState<Funcionario | null>(null);
  const [passDialogOpen, setPassDialogOpen] = useState(false);

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

  useEffect(() => {
    loadData();
  }, [filters]);

  useEffect(() => {
    loadDepartamentos();
    loadCargos();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const queryFilters = {
        nome: filters.search,
        departamentoID: filters.departamentoID,
        cargoID: filters.cargoID,
        estadoFuncionario: filters.estadoFuncionario,
        page: 1,
        per_page: 50 // Carregar mais para mostrar todos
      };

      const response = await getFuncionarios(queryFilters);
      
      if (response.success) {
        const funcionariosData = response.data || [];
        
        // Processar dados para incluir nomes de cargo e departamento
        const funcionariosProcessados = funcionariosData.map((f: any) => {
          return {
            ...f,
            nomeCompleto: `${f.Nome || ''} ${f.Apelido || ''}`.trim(),
            id: f.FuncionarioID || f.funcionarioID || f.id,
            // Usar os nomes que já vêm do backend
            departamentoNome: f.DepartamentoNome || 'Não especificado',
            cargoNome: f.CargoNome || 'Não especificado'
          };
        });
        
        setFuncionarios(funcionariosProcessados);
        
        if (funcionariosData.length === 0) {
          showNotification('Nenhum funcionário encontrado com os filtros aplicados', 'info');
        }
      } else {
        showNotification('Erro ao carregar funcionários', 'error');
      }
    } catch (error) {
      console.error('Erro ao carregar funcionários:', error);
      showNotification('Erro de conexão com o servidor', 'error');
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

  const handleGeneratePass = (funcionario: Funcionario) => {
    setSelectedFuncionario(funcionario);
    setPassDialogOpen(true);
  };

  const handleClosePassDialog = () => {
    setPassDialogOpen(false);
    setSelectedFuncionario(null);
  };

  const handleFilterChange = (field: string, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value === '' ? undefined : value
    }));
  };

  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'Activo': return 'success';
      case 'Inactivo': return 'error';
      case 'Suspenso': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          {/* Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              <BadgeIcon color="primary" sx={{ fontSize: 32 }} />
              <Box>
                <Typography variant="h4" component="h1">
                  Passes de Funcionários
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Gerar passes de identificação (CR80) para funcionários
                </Typography>
              </Box>
            </Box>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={handleRefresh}
              disabled={loading}
            >
              Atualizar
            </Button>
          </Box>

          {/* Filtros */}
          <Paper sx={{ p: 2, mb: 3, bgcolor: 'grey.50' }}>
            <Typography variant="h6" gutterBottom>
              Filtros
            </Typography>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} sm={6} md={3}>
                <TextField
                  fullWidth
                  label="Pesquisar funcionário"
                  value={filters.search || ''}
                  onChange={(e) => handleFilterChange('search', e.target.value)}
                  size="small"
                  placeholder="Nome ou apelido"
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel>Departamento</InputLabel>
                  <Select
                    value={filters.departamentoID || ''}
                    label="Departamento"
                    onChange={(e) => handleFilterChange('departamentoID', Number(e.target.value) || undefined)}
                  >
                    <MenuItem value="">Todos</MenuItem>
                    {departamentos.map((dept) => (
                      <MenuItem key={dept.departamentoID} value={dept.departamentoID}>
                        {dept.nome}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel>Cargo</InputLabel>
                  <Select
                    value={filters.cargoID || ''}
                    label="Cargo"
                    onChange={(e) => handleFilterChange('cargoID', Number(e.target.value) || undefined)}
                  >
                    <MenuItem value="">Todos</MenuItem>
                    {cargos.map((cargo) => (
                      <MenuItem key={cargo.cargoID} value={cargo.cargoID}>
                        {cargo.nome}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel>Estado</InputLabel>
                  <Select
                    value={filters.estadoFuncionario || ''}
                    label="Estado"
                    onChange={(e) => handleFilterChange('estadoFuncionario', e.target.value || undefined)}
                  >
                    <MenuItem value="">Todos</MenuItem>
                    <MenuItem value="Activo">Activo</MenuItem>
                    <MenuItem value="Inactivo">Inactivo</MenuItem>
                    <MenuItem value="Suspenso">Suspenso</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Paper>

          {/* Lista de Funcionários */}
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : funcionarios.length === 0 ? (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <PersonIcon sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
              <Typography variant="h6" color="textSecondary">
                Nenhum funcionário encontrado
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Ajuste os filtros ou verifique se existem funcionários cadastrados
              </Typography>
            </Box>
          ) : (
            <Grid container spacing={2}>
              {funcionarios.map((funcionario) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={funcionario.funcionarioID}>
                  <Card 
                    variant="outlined" 
                    sx={{ 
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      '&:hover': {
                        boxShadow: 2,
                        transform: 'translateY(-2px)',
                        transition: 'all 0.2s ease-in-out'
                      }
                    }}
                  >
                    <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                      {/* Foto e informações básicas */}
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Avatar
                          src={funcionario.foto || ''}
                          sx={{ width: 48, height: 48, mr: 2 }}
                        >
                          <PersonIcon />
                        </Avatar>
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="subtitle1" fontWeight="medium" noWrap>
                            {`${funcionario.nome || ''} ${funcionario.apelido || ''}`.trim()}
                          </Typography>
                          <Typography variant="body2" color="textSecondary" noWrap>
                            ID: {funcionario.funcionarioID}
                          </Typography>
                        </Box>
                      </Box>

                      {/* Informações profissionais */}
                      <Box sx={{ flex: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <BusinessIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                          <Typography variant="body2" noWrap>
                            {(funcionario as any).departamentoNome || 'N/A'}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <WorkIcon sx={{ fontSize: 16, mr: 1, color: 'text.secondary' }} />
                          <Typography variant="body2" noWrap>
                            {(funcionario as any).cargoNome || 'N/A'}
                          </Typography>
                        </Box>
                      </Box>

                      {/* Estado e ações */}
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                        <Chip
                          label={funcionario.estadoFuncionario || 'Activo'}
                          color={getEstadoColor(funcionario.estadoFuncionario || 'Activo') as any}
                          size="small"
                        />
                        <Box>
                          <Tooltip title="Gerar Passe">
                            <IconButton
                              size="small"
                              color="primary"
                              onClick={() => handleGeneratePass(funcionario)}
                            >
                              <BadgeIcon />
                            </IconButton>
                          </Tooltip>
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </CardContent>
      </Card>

      {/* Dialog do Passe */}
      {selectedFuncionario && (
        <EmployeePass
          funcionario={selectedFuncionario}
          onClose={handleClosePassDialog}
          showDialog={passDialogOpen}
        />
      )}

      {/* Notification Snackbar */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={() => setNotification({ ...notification, open: false })}
      >
        <Alert
          severity={notification.severity}
          onClose={() => setNotification({ ...notification, open: false })}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default PassesList;
