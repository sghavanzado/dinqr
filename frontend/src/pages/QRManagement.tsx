// QRManagement.tsx
import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Snackbar,
  Alert,
  CircularProgress,
} from '@mui/material';
import QRTable from '../components/QRTable';
import { fetchFuncionarios } from '../api/apiService'; // Asegúrate de que esta ruta sea correcta

interface Funcionario {
  id: number;
  nombre: string;
  empresa: string;
  telefono: string;
  email: string;
  cargo: string;
}

const QRManagement = () => {
  // Ya no gestionamos selectedIds aquí en esta implementación alternativa
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');
  const [totalRows, setTotalRows] = useState(0);

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await fetchFuncionarios(1, 10, ''); // Ajusta los parámetros según tu API
      console.log('API Response (Funcionarios):', data);
      setFuncionarios(data);
      setTotalRows(data.length);
    } catch (error) {
      console.error('Error fetching funcionarios:', error);
      setSnackbarMessage('Error al cargar los funcionarios.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  console.log('QRManagement rendered');

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Gestión de Códigos QR
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <QRTable
          // No pasamos selectedIds ni setSelectedIds como props ahora
          />
        </Grid>
      </Grid>
      {loading && <CircularProgress />}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity={snackbarSeverity}>{snackbarMessage}</Alert>
      </Snackbar>
    </Container>
  );
};

export default QRManagement;