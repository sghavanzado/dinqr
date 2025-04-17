import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Snackbar,
  Alert,
} from '@mui/material';
import axiosInstance from '../api/axiosInstance';

interface Invoice {
  id?: number;
  invoice_number: string;
  issue_date: string;
  operation_date?: string;
  seller_name: string;
  seller_nif: string;
  seller_address: string;
  client_name: string;
  client_nif?: string;
  description: string;
  quantity: number;
  unit_of_measure: string;
  unit_price: number;
  taxable_amount: number;
  vat_rate: number;
  vat_amount: number;
  total_amount: number;
  payment_due_date?: string;
  payment_method?: string;
  authorization_number?: string;
  legal_reference?: string;
}

const InvoiceManagement = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);
  const [formData, setFormData] = useState<Invoice | null>(null);
  const [loading, setLoading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/invoices');
      setInvoices(response.data);
    } catch (error) {
      console.error('Error fetching invoices:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!formData) return;
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev!,
      [name]: name === 'quantity' || name === 'unit_price' || name === 'vat_rate'
        ? parseFloat(value)
        : value,
    }));
  };

  const handleOpenDialog = (invoice?: Invoice) => {
    setSelectedInvoice(invoice || null);
    setFormData(invoice || {
      invoice_number: '',
      issue_date: '',
      seller_name: '',
      seller_nif: '',
      seller_address: '',
      client_name: '',
      description: '',
      quantity: 1,
      unit_of_measure: '',
      unit_price: 0,
      taxable_amount: 0,
      vat_rate: 14.0,
      vat_amount: 0,
      total_amount: 0,
    });
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setFormData(null);
  };

  const handleSubmit = async () => {
    if (!formData) return;
    setLoading(true);
    try {
      if (selectedInvoice) {
        // Update existing invoice
        await axiosInstance.put(`/invoices/${selectedInvoice.id}`, formData);
        setSnackbarMessage('Factura actualizada con éxito');
      } else {
        // Create new invoice
        await axiosInstance.post('/invoices', formData);
        setSnackbarMessage('Factura creada con éxito');
      }
      fetchInvoices();
      setSnackbarOpen(true);
      handleCloseDialog();
    } catch (error) {
      console.error('Error saving invoice:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    setLoading(true);
    try {
      await axiosInstance.delete(`/invoices/${id}`);
      setSnackbarMessage('Factura eliminada con éxito');
      fetchInvoices();
      setSnackbarOpen(true);
    } catch (error) {
      console.error('Error deleting invoice:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Gestión de Facturas
      </Typography>
      <Button variant="contained" color="primary" onClick={() => handleOpenDialog()}>
        Crear Factura
      </Button>
      {loading && <CircularProgress />}
      <TableContainer component={Paper} sx={{ mt: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Número de Factura</TableCell>
              <TableCell>Fecha de Emisión</TableCell>
              <TableCell>Nombre del Cliente</TableCell>
              <TableCell>Total</TableCell>
              <TableCell>Acciones</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {invoices.map((invoice) => (
              <TableRow key={invoice.id}>
                <TableCell>{invoice.invoice_number}</TableCell>
                <TableCell>{invoice.issue_date}</TableCell>
                <TableCell>{invoice.client_name}</TableCell>
                <TableCell>{invoice.total_amount}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    color="primary"
                    onClick={() => handleOpenDialog(invoice)}
                  >
                    Editar
                  </Button>
                  <Button
                    variant="outlined"
                    color="secondary"
                    onClick={() => handleDelete(invoice.id!)}
                  >
                    Eliminar
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Dialog for creating/editing invoices */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} fullWidth maxWidth="md">
        <DialogTitle>{selectedInvoice ? 'Editar Factura' : 'Crear Factura'}</DialogTitle>
        <DialogContent>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                name="invoice_number"
                label="Número de Factura"
                fullWidth
                value={formData?.invoice_number || ''}
                onChange={handleInputChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="issue_date"
                label="Fecha de Emisión"
                type="date"
                fullWidth
                value={formData?.issue_date || ''}
                onChange={handleInputChange}
                InputLabelProps={{ shrink: true }}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                name="description"
                label="Descripción"
                fullWidth
                multiline
                rows={4}
                value={formData?.description || ''}
                onChange={handleInputChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="quantity"
                label="Cantidad"
                type="number"
                fullWidth
                value={formData?.quantity || ''}
                onChange={handleInputChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                name="unit_price"
                label="Precio Unitario"
                type="number"
                fullWidth
                value={formData?.unit_price || ''}
                onChange={handleInputChange}
                required
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="secondary">
            Cancelar
          </Button>
          <Button onClick={handleSubmit} color="primary" variant="contained">
            Guardar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setSnackbarOpen(false)} severity="success">
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default InvoiceManagement;
