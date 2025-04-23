// QRManagement.tsx
import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Snackbar,
  Alert,
  CircularProgress,
} from '@mui/material';
import QRTable from '../components/QRTable';
import { fetchFuncionarios } from '../api/apiService';

interface Funcionario {
  id: string;
  nome: string;
  funcao: string;
  area: string;
  nif: string;
  telefone: string;
}

const QRManagement = () => {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');
  // Removed unused state 'totalRows'

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await fetchFuncionarios(1, 10, '');
      console.log('API Response (Funcionários):', data);
      setFuncionarios(data);
      // Removed unused state update for 'totalRows'
    } catch (error) {
      console.error('Erro ao carregar os funcionários:', error);
      setSnackbarMessage('Erro ao carregar os funcionários.');
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
        Gestão de Códigos QR
      </Typography>
      <Grid container spacing={3}>
        
          <QRTable funcionarios={funcionarios} />
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