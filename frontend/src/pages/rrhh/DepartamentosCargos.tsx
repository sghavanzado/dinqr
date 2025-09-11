import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Snackbar,
  IconButton,
  Tooltip,
  Paper,
} from '@mui/material';
import { SimpleTreeView } from '@mui/x-tree-view/SimpleTreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Business as BusinessIcon,
  Work as WorkIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { 
  Departamento, 
  DepartamentoFormData,
  Cargo,
  CargoFormData,
  ApiResponse
} from '../../types/rrhh';
import { 
  getDepartamentos, 
  createDepartamento, 
  updateDepartamento, 
  deleteDepartamento,
  getCargos,
  createCargo,
  updateCargo,
  deleteCargo
} from '../../services/api/rrhh';

// Simple inline ConfirmDialog component
interface ConfirmDialogProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
}

const ConfirmDialog: React.FC<ConfirmDialogProps> = ({
  open,
  onClose,
  onConfirm,
  title,
  message,
}) => (
  <Dialog open={open} onClose={onClose}>
    <DialogTitle>{title}</DialogTitle>
    <DialogContent>
      <Typography>{message}</Typography>
    </DialogContent>
    <DialogActions>
      <Button onClick={onClose}>Cancelar</Button>
      <Button onClick={onConfirm} variant="contained" color="error">
        Confirmar
      </Button>
    </DialogActions>
  </Dialog>
);

// Schemas de validação
const departamentoSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório').max(100, 'Nome muito longo'),
  descricao: z.string().optional(),
});

const cargoSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório').max(100, 'Nome muito longo'),
  descricao: z.string().optional(),
  nivel: z.string().optional(),
  departamentoID: z.number().optional(),
});

interface TreeNodeData {
  id: string;
  type: 'departamento' | 'cargo';
  data: Departamento | Cargo;
}

const DepartamentosCargos: React.FC = () => {
  const [departamentos, setDepartamentos] = useState<Departamento[]>([]);
  const [cargos, setCargos] = useState<Cargo[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string[]>([]);
  
  // Dialog states
  const [isDepartamentoFormOpen, setIsDepartamentoFormOpen] = useState(false);
  const [isCargoFormOpen, setIsCargoFormOpen] = useState(false);
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<TreeNodeData | null>(null);
  const [actionType, setActionType] = useState<'create' | 'edit' | 'delete'>('create');

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
  const departamentoForm = useForm<DepartamentoFormData>({
    resolver: zodResolver(departamentoSchema),
    defaultValues: { nome: '', descricao: '' },
  });

  const cargoForm = useForm<CargoFormData>({
    resolver: zodResolver(cargoSchema),
    defaultValues: { nome: '', descricao: '', nivel: '', departamentoID: undefined },
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [deptsResponse, cargosResponse] = await Promise.all([
        getDepartamentos(),
        getCargos()
      ]);

      if (deptsResponse.success && deptsResponse.data) {
        setDepartamentos(deptsResponse.data);
      }

      if (cargosResponse.success && cargosResponse.data) {
        setCargos(cargosResponse.data);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      // Fallback para dados mock quando a API não estiver disponível
      const mockDepartamentos = [
        { id: 1, departamentoID: 1, nome: 'Recursos Humanos', descricao: 'Gestão de pessoas e talentos' },
        { id: 2, departamentoID: 2, nome: 'Tecnologia', descricao: 'Desenvolvimento e infraestrutura tecnológica' },
        { id: 3, departamentoID: 3, nome: 'Comercial', descricao: 'Vendas e relacionamento com clientes' },
        { id: 4, departamentoID: 4, nome: 'Financeiro', descricao: 'Controle financeiro e contabilidade' }
      ];
      
      const mockCargos = [
        { id: 1, cargoID: 1, nome: 'Analista de RH', salarioBase: 75000, departamentoID: 1, nivel: 'Pleno' },
        { id: 2, cargoID: 2, nome: 'Gerente de RH', salarioBase: 120000, departamentoID: 1, nivel: 'Senior' },
        { id: 3, cargoID: 3, nome: 'Desenvolvedor Frontend', salarioBase: 85000, departamentoID: 2, nivel: 'Pleno' },
        { id: 4, cargoID: 4, nome: 'Desenvolvedor Backend', salarioBase: 90000, departamentoID: 2, nivel: 'Senior' },
        { id: 5, cargoID: 5, nome: 'Vendedor', salarioBase: 60000, departamentoID: 3, nivel: 'Junior' },
        { id: 6, cargoID: 6, nome: 'Contador', salarioBase: 70000, departamentoID: 4, nivel: 'Pleno' }
      ];
      
      setDepartamentos(mockDepartamentos);
      setCargos(mockCargos);
      showNotification('Exibindo dados de demonstração (API não disponível)', 'warning');
    } finally {
      setLoading(false);
    }
  };

  const showNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setNotification({ open: true, message, severity });
  };

  const handleExpandToggle = (nodeIds: string[]) => {
    setExpanded(nodeIds);
  };

  // Departamento handlers
  const handleAddDepartamento = () => {
    departamentoForm.reset({ nome: '', descricao: '' });
    setSelectedItem(null);
    setActionType('create');
    setIsDepartamentoFormOpen(true);
  };

  const handleEditDepartamento = (departamento: Departamento) => {
    departamentoForm.reset({
      nome: departamento.nome,
      descricao: departamento.descricao || '',
    });
    setSelectedItem({
      id: departamento.departamentoID.toString(),
      type: 'departamento',
      data: departamento,
    });
    setActionType('edit');
    setIsDepartamentoFormOpen(true);
  };

  const handleDeleteDepartamento = (departamento: Departamento) => {
    setSelectedItem({
      id: departamento.departamentoID.toString(),
      type: 'departamento',
      data: departamento,
    });
    setActionType('delete');
    setIsConfirmOpen(true);
  };

  const handleDepartamentoSubmit = async (data: DepartamentoFormData) => {
    try {
      let response: ApiResponse<Departamento>;

      if (actionType === 'create') {
        response = await createDepartamento(data);
      } else {
        const dept = selectedItem?.data as Departamento;
        response = await updateDepartamento(dept.departamentoID, data);
      }

      if (response.success) {
        setIsDepartamentoFormOpen(false);
        loadData();
        showNotification(
          actionType === 'create' ? 'Departamento criado com sucesso!' : 'Departamento atualizado com sucesso!',
          'success'
        );
      } else {
        showNotification(response.message || 'Erro ao salvar departamento', 'error');
      }
    } catch (error) {
      showNotification('Erro ao salvar departamento', 'error');
    }
  };

  // Cargo handlers
  const handleAddCargo = (departamentoID?: number) => {
    cargoForm.reset({ 
      nome: '', 
      descricao: '', 
      nivel: '', 
      departamentoID: departamentoID 
    });
    setSelectedItem(null);
    setActionType('create');
    setIsCargoFormOpen(true);
  };

  const handleEditCargo = (cargo: Cargo) => {
    cargoForm.reset({
      nome: cargo.nome,
      descricao: cargo.descricao || '',
      nivel: cargo.nivel || '',
      departamentoID: cargo.departamentoID,
    });
    setSelectedItem({
      id: cargo.cargoID.toString(),
      type: 'cargo',
      data: cargo,
    });
    setActionType('edit');
    setIsCargoFormOpen(true);
  };

  const handleDeleteCargo = (cargo: Cargo) => {
    setSelectedItem({
      id: cargo.cargoID.toString(),
      type: 'cargo',
      data: cargo,
    });
    setActionType('delete');
    setIsConfirmOpen(true);
  };

  const handleCargoSubmit = async (data: CargoFormData) => {
    try {
      let response: ApiResponse<Cargo>;

      if (actionType === 'create') {
        response = await createCargo(data);
      } else {
        const cargo = selectedItem?.data as Cargo;
        response = await updateCargo(cargo.cargoID, data);
      }

      if (response.success) {
        setIsCargoFormOpen(false);
        loadData();
        showNotification(
          actionType === 'create' ? 'Cargo criado com sucesso!' : 'Cargo atualizado com sucesso!',
          'success'
        );
      } else {
        showNotification(response.message || 'Erro ao salvar cargo', 'error');
      }
    } catch (error) {
      showNotification('Erro ao salvar cargo', 'error');
    }
  };

  const handleConfirmDelete = async () => {
    if (!selectedItem) return;

    try {
      let response: ApiResponse<void>;

      if (selectedItem.type === 'departamento') {
        const dept = selectedItem.data as Departamento;
        response = await deleteDepartamento(dept.departamentoID);
      } else {
        const cargo = selectedItem.data as Cargo;
        response = await deleteCargo(cargo.cargoID);
      }

      if (response.success) {
        setIsConfirmOpen(false);
        loadData();
        showNotification(
          `${selectedItem.type === 'departamento' ? 'Departamento' : 'Cargo'} removido com sucesso!`,
          'success'
        );
      } else {
        showNotification(response.message || 'Erro ao remover item', 'error');
      }
    } catch (error) {
      showNotification('Erro ao remover item', 'error');
    }
  };

  const getCargosByDepartamento = (departamentoID: number) => {
    return cargos.filter(cargo => cargo.departamentoID === departamentoID);
  };

  const renderDepartamentoTree = (departamento: Departamento) => {
    const departamentoCargos = getCargosByDepartamento(departamento.departamentoID);
    
    return (
      <TreeItem 
        key={departamento.departamentoID}
        itemId={`dept-${departamento.departamentoID}`}
        label={
          <Box sx={{ display: 'flex', alignItems: 'center', py: 1 }}>
            <BusinessIcon sx={{ mr: 1, color: 'primary.main' }} />
            <Typography variant="body1" sx={{ fontWeight: 'medium', flexGrow: 1 }}>
              {departamento.nome}
            </Typography>
            <Box sx={{ display: 'flex', gap: 0.5 }}>
              <Tooltip title="Adicionar Cargo">
                <IconButton 
                  size="small" 
                  onClick={(e) => {
                    e.stopPropagation();
                    handleAddCargo(departamento.departamentoID);
                  }}
                >
                  <AddIcon fontSize="small" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Editar Departamento">
                <IconButton 
                  size="small" 
                  onClick={(e) => {
                    e.stopPropagation();
                    handleEditDepartamento(departamento);
                  }}
                >
                  <EditIcon fontSize="small" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Remover Departamento">
                <IconButton 
                  size="small" 
                  color="error"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteDepartamento(departamento);
                  }}
                >
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>
        }
      >
        {departamentoCargos.map((cargo) => (
          <TreeItem
            key={cargo.cargoID}
            itemId={`cargo-${cargo.cargoID}`}
            label={
              <Box sx={{ display: 'flex', alignItems: 'center', py: 0.5 }}>
                <WorkIcon sx={{ mr: 1, color: 'secondary.main', fontSize: 20 }} />
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="body2">
                    {cargo.nome}
                  </Typography>
                  {cargo.nivel && (
                    <Typography variant="caption" color="textSecondary">
                      Nível: {cargo.nivel}
                    </Typography>
                  )}
                </Box>
                <Box sx={{ display: 'flex', gap: 0.5 }}>
                  <Tooltip title="Editar Cargo">
                    <IconButton 
                      size="small" 
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditCargo(cargo);
                      }}
                    >
                      <EditIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Remover Cargo">
                    <IconButton 
                      size="small" 
                      color="error"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteCargo(cargo);
                      }}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>
            }
          />
        ))}
      </TreeItem>
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h4" component="h1">
              Departamentos e Cargos
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={() => handleAddCargo()}
              >
                Adicionar Cargo
              </Button>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={handleAddDepartamento}
              >
                Adicionar Departamento
              </Button>
              <Tooltip title="Atualizar">
                <IconButton onClick={loadData}>
                  <RefreshIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>

          <Paper sx={{ p: 2, minHeight: 400 }}>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
                <Typography>Carregando...</Typography>
              </Box>
            ) : departamentos.length === 0 ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
                <Typography color="textSecondary">
                  Nenhum departamento encontrado. Clique em "Adicionar Departamento" para começar.
                </Typography>
              </Box>
            ) : (
              <SimpleTreeView
                expandedItems={expanded}
                onExpandedItemsChange={(_, nodeIds) => handleExpandToggle(nodeIds)}
                sx={{ flexGrow: 1, overflowY: 'auto' }}
              >
                {departamentos.map(renderDepartamentoTree)}
              </SimpleTreeView>
            )}
          </Paper>
        </CardContent>
      </Card>

      {/* Departamento Form Dialog */}
      <Dialog 
        open={isDepartamentoFormOpen} 
        onClose={() => setIsDepartamentoFormOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={departamentoForm.handleSubmit(handleDepartamentoSubmit)}>
          <DialogTitle>
            {actionType === 'create' ? 'Adicionar Departamento' : 'Editar Departamento'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <TextField
                fullWidth
                label="Nome *"
                error={!!departamentoForm.formState.errors.nome}
                helperText={departamentoForm.formState.errors.nome?.message}
                {...departamentoForm.register('nome')}
              />
              <TextField
                fullWidth
                label="Descrição"
                multiline
                rows={3}
                error={!!departamentoForm.formState.errors.descricao}
                helperText={departamentoForm.formState.errors.descricao?.message}
                {...departamentoForm.register('descricao')}
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setIsDepartamentoFormOpen(false)}>
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="contained"
              disabled={departamentoForm.formState.isSubmitting}
            >
              {actionType === 'create' ? 'Criar' : 'Salvar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Cargo Form Dialog */}
      <Dialog 
        open={isCargoFormOpen} 
        onClose={() => setIsCargoFormOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <form onSubmit={cargoForm.handleSubmit(handleCargoSubmit)}>
          <DialogTitle>
            {actionType === 'create' ? 'Adicionar Cargo' : 'Editar Cargo'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
              <TextField
                fullWidth
                label="Nome *"
                error={!!cargoForm.formState.errors.nome}
                helperText={cargoForm.formState.errors.nome?.message}
                {...cargoForm.register('nome')}
              />
              <Box sx={{ display: 'flex', gap: 2 }}>
                <FormControl fullWidth>
                  <InputLabel>Departamento</InputLabel>
                  <Select
                    value={cargoForm.watch('departamentoID') || ''}
                    label="Departamento"
                    onChange={(e) => cargoForm.setValue('departamentoID', Number(e.target.value) || undefined)}
                  >
                    <MenuItem value="">Nenhum</MenuItem>
                    {departamentos.map((dept) => (
                      <MenuItem key={dept.departamentoID} value={dept.departamentoID}>
                        {dept.nome}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <TextField
                  fullWidth
                  label="Nível"
                  error={!!cargoForm.formState.errors.nivel}
                  helperText={cargoForm.formState.errors.nivel?.message}
                  {...cargoForm.register('nivel')}
                />
              </Box>
              <TextField
                fullWidth
                label="Descrição"
                multiline
                rows={3}
                error={!!cargoForm.formState.errors.descricao}
                helperText={cargoForm.formState.errors.descricao?.message}
                {...cargoForm.register('descricao')}
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setIsCargoFormOpen(false)}>
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="contained"
              disabled={cargoForm.formState.isSubmitting}
            >
              {actionType === 'create' ? 'Criar' : 'Salvar'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>

      {/* Confirm Dialog */}
      <ConfirmDialog
        open={isConfirmOpen}
        onClose={() => setIsConfirmOpen(false)}
        onConfirm={handleConfirmDelete}
        title={`Remover ${selectedItem?.type === 'departamento' ? 'Departamento' : 'Cargo'}`}
        message={`Tem certeza que deseja remover ${selectedItem?.type === 'departamento' ? 'o departamento' : 'o cargo'} "${(selectedItem?.data as any)?.nome}"?`}
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

export default DepartamentosCargos;
