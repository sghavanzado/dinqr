import React, { useState } from 'react';
import {
  Container,
  Typography,
  Button,
  Grid,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Snackbar,
  Alert,
  LinearProgress,
} from '@mui/material';
import { clientService, supplierService, productService, invoiceService, serviceService } from '../api/apiService';

const DataImport = () => {
  const [file, setFile] = useState<File | null>(null);
  const [importType, setImportType] = useState('');
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleImport = async () => {
    if (!file || !importType) {
      setSnackbarMessage('Seleccione un archivo y un tipo de importación.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
      return;
    }

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        setLoading(true);
        const jsonData = JSON.parse(e.target?.result as string);

        switch (importType) {
          case 'customers':
            await clientService.createClient(jsonData);
            break;
          case 'suppliers':
            await supplierService.createSupplier(jsonData);
            break;
          case 'products':
            await productService.createProduct(jsonData);
            break;
          case 'invoices':
            await invoiceService.createInvoice(jsonData);
            break;
          case 'services':
            await serviceService.createService(jsonData);
            break;
          default:
            throw new Error('Tipo de importación no válido.');
        }

        setSnackbarMessage('Importación exitosa.');
        setSnackbarSeverity('success');
      } catch (error: any) {
        setSnackbarMessage(error.message || 'Error al importar datos.');
        setSnackbarSeverity('error');
      } finally {
        setLoading(false);
        setSnackbarOpen(true);
      }
    };
    reader.readAsText(file);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Importar Datos
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FormControl fullWidth>
            <InputLabel>Tipo de Importación</InputLabel>
            <Select
              value={importType}
              onChange={(e) => setImportType(e.target.value)}
            >
              <MenuItem value="customers">Clientes</MenuItem>
              <MenuItem value="suppliers">Proveedores</MenuItem>
              <MenuItem value="products">Productos</MenuItem>
              <MenuItem value="invoices">Facturas</MenuItem>
              <MenuItem value="services">Servicios</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" component="label" fullWidth>
            Seleccionar Archivo JSON
            <input type="file" hidden accept=".json" onChange={handleFileChange} />
          </Button>
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={handleImport}
            disabled={loading}
          >
            Importar
          </Button>
        </Grid>
        {loading && (
          <Grid item xs={12}>
            <LinearProgress />
          </Grid>
        )}
      </Grid>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbarSeverity}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default DataImport;
