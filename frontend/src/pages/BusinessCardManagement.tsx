// BusinessCardManagement.tsx
import { useState, useEffect } from 'react';
import {
    Container,
    Typography,
    Grid,
    Snackbar,
    Alert,
    CircularProgress,
} from '@mui/material';
import BusinessCardTable from '../components/BusinessCardTable';
import { fetchFuncionarios } from '../api/apiService';
import type { Funcionario } from '../types/Funcionario';

const BusinessCardManagement = () => {
    const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
    const [loading, setLoading] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');

    const fetchData = async () => {
        setLoading(true);
        try {
            const data = await fetchFuncionarios(1, 10, '');
            console.log('API Response (Funcionários):', data);
            setFuncionarios(data);
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

    console.log('BusinessCardManagement rendered');

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Gestão de Cartões de Visita
            </Typography>

            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <BusinessCardTable />
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

export default BusinessCardManagement;
