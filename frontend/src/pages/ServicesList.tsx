import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Fab,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Snackbar,
  CircularProgress,
  Box,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import { Add, Edit, Delete, ErrorOutline } from '@mui/icons-material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';
import { Service, serviceService } from '../api/apiService';

const ServicesList: React.FC = () => {
  const [services, setServices] = useState<Service[]>([]);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [view, setView] = useState<'list' | 'table'>('list'); // State for view selection
  const navigate = useNavigate();

  useEffect(() => {
    const loadServices = async () => {
      try {
        const data = await serviceService.getServices();
        if (Array.isArray(data)) {
          setServices(data);
        } else {
          setError('Formato de datos inválido recibido del servidor');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error al cargar los servicios');
      } finally {
        setLoading(false);
      }
    };

    loadServices();
  }, []);

  const handleDeleteConfirm = async () => {
    if (!selectedService?.id) {
      setError('Servicio no válido para eliminar');
      setDeleteDialogOpen(false);
      return;
    }

    try {
      await serviceService.deleteService(selectedService.id);
      setServices((prev) => prev.filter((s) => s.id !== selectedService.id));
      setDeleteDialogOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al eliminar el servicio');
      setDeleteDialogOpen(false);
    }
  };

  // Columns for the DataGrid
  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Nombre', width: 200 },
    { field: 'category', headerName: 'Categoría', width: 150 },
    { field: 'price', headerName: 'Precio', width: 100 },
    { field: 'duration', headerName: 'Duración', width: 150 },
    {
      field: 'actions',
      headerName: 'Acciones',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<Edit />}
            onClick={() => navigate(`/edit-service/${params.row.id}`)}
            color="primary"
          >
            Editar
          </Button>
          <Button
            variant="outlined"
            startIcon={<Delete />}
            onClick={() => {
              setSelectedService(params.row);
              setDeleteDialogOpen(true);
            }}
            color="error"
          >
            Eliminar
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <Box sx={{ p: { xs: 2, sm: 4 } }}>
      {/* View Selector */}
      <FormControl fullWidth margin="normal">
        <InputLabel id="view-selector-label">Vista</InputLabel>
        <Select
          labelId="view-selector-label"
          value={view}
          onChange={(e) => setView(e.target.value as 'list' | 'table')}
        >
          <MenuItem value="list">Listado</MenuItem>
          <MenuItem value="table">Tabla</MenuItem>
        </Select>
      </FormControl>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress size={60} />
        </Box>
      ) : error ? (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <ErrorOutline color="error" sx={{ fontSize: 60 }} />
          <Typography variant="h6" color="error" sx={{ mt: 2 }}>
            {error}
          </Typography>
        </Box>
      ) : view === 'list' ? (
        <Grid container spacing={3}>
          {services.map((service) => (
            <Grid item xs={12} sm={6} md={4} key={service.id}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  boxShadow: 3,
                  borderRadius: 2,
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 6,
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                    {service.name}
                  </Typography>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Categoría: <strong>{service.category}</strong>
                    </Typography>
                    <Typography variant="body2">
                      Precio: <strong>{service.price}</strong>
                    </Typography>
                    <Typography variant="body2">
                      Duración: <strong>{service.duration}</strong>
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', gap: 1, justifyContent: 'flex-end' }}>
                    <Button
                      variant="outlined"
                      startIcon={<Edit />}
                      onClick={() => navigate(`/edit-service/${service.id}`)}
                      color="primary"
                    >
                      Editar
                    </Button>
                    <Button
                      variant="outlined"
                      startIcon={<Delete />}
                      onClick={() => {
                        setSelectedService(service);
                        setDeleteDialogOpen(true);
                      }}
                      color="error"
                    >
                      Eliminar
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : (
        <Box sx={{ height: 600, width: '100%' }}>
          <DataGrid rows={services} columns={columns} pageSize={10} rowsPerPageOptions={[10, 20, 50]} />
        </Box>
      )}

      <Fab
        color="primary"
        sx={{
          position: 'fixed',
          bottom: 32,
          right: 32,
          transition: 'transform 0.2s',
          '&:hover': {
            transform: 'scale(1.1)',
          },
        }}
        onClick={() => navigate('/new-service')}
        aria-label="Añadir servicio"
      >
        <Add />
      </Fab>

      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle variant="h6" sx={{ fontWeight: 'bold' }}>
          Confirmar eliminación
        </DialogTitle>
        <DialogContent>
          <Typography>
            ¿Estás seguro de eliminar el servicio <strong>"{selectedService?.name}"</strong> (ID: {selectedService?.id})?
          </Typography>
        </DialogContent>
        <DialogActions sx={{ p: 3 }}>
          <Button onClick={() => setDeleteDialogOpen(false)} variant="outlined" sx={{ mr: 2 }}>
            Cancelar
          </Button>
          <Button
            onClick={handleDeleteConfirm}
            variant="contained"
            color="error"
            startIcon={<Delete />}
          >
            Confirmar eliminación
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError('')}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert severity="error" variant="filled" sx={{ width: '100%' }} onClose={() => setError('')}>
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ServicesList;
