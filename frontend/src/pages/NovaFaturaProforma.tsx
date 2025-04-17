import React, { useState } from 'react';
import { TextField, Button, Grid, Container, Typography } from '@mui/material';
import axios from 'axios';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';

const NovaFaturaProforma = () => {
  const [formData, setFormData] = useState({
    invoice_number: '',
    issue_date: '',
    operation_date: '',
    seller_name: '',
    seller_nif: '',
    seller_address: '',
    client_name: '',
    client_nif: '',
    description: '',
    quantity: '',
    unit_of_measure: '',
    unit_price: '',
    taxable_amount: '',
    vat_rate: '14.0',
    vat_amount: '',
    total_amount: '',
    payment_due_date: '',
    payment_method: '',
    authorization_number: '',
    legal_reference: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/invoices', formData);
      console.log(response.data);
      // Handle success (e.g., show a success message, clear the form, etc.)
    } catch (error) {
      console.error(error);
      // Handle error (e.g., show an error message)
    }
  };

  return (
           <Stack
                spacing={2}
                sx={{
                  alignItems: 'center',
                  mx: 3,
                  pb: 5,
                  mt: { xs: 8, md: 0 },
                }}
              >
    <Container>
      <Typography variant="h4" gutterBottom>
        Crear Proforma
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="invoice_number"
              label="Número de Factura"
              fullWidth
              value={formData.invoice_number}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="issue_date"
              label="Fecha de Emisión"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={formData.issue_date}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="operation_date"
              label="Fecha de Operación"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={formData.operation_date}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="seller_name"
              label="Nombre del Vendedor"
              fullWidth
              value={formData.seller_name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="seller_nif"
              label="NIF del Vendedor"
              fullWidth
              value={formData.seller_nif}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="seller_address"
              label="Dirección del Vendedor"
              fullWidth
              value={formData.seller_address}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="client_name"
              label="Nombre del Cliente"
              fullWidth
              value={formData.client_name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="client_nif"
              label="NIF del Cliente"
              fullWidth
              value={formData.client_nif}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              required
              name="description"
              label="Descripción"
              fullWidth
              multiline
              rows={4}
              value={formData.description}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="quantity"
              label="Cantidad"
              fullWidth
              value={formData.quantity}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="unit_of_measure"
              label="Unidad de Medida"
              fullWidth
              value={formData.unit_of_measure}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="unit_price"
              label="Precio Unitario"
              fullWidth
              value={formData.unit_price}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="taxable_amount"
              label="Base Imponible"
              fullWidth
              value={formData.taxable_amount}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="vat_rate"
              label="Tipo de IVA"
              fullWidth
              value={formData.vat_rate}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="vat_amount"
              label="Monto del IVA"
              fullWidth
              value={formData.vat_amount}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="total_amount"
              label="Total a Pagar"
              fullWidth
              value={formData.total_amount}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="payment_due_date"
              label="Fecha Límite de Pago"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={formData.payment_due_date}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="payment_method"
              label="Método de Pago"
              fullWidth
              value={formData.payment_method}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="authorization_number"
              label="Número de Autorización"
              fullWidth
              value={formData.authorization_number}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              name="legal_reference"
              label="Referencia Legal"
              fullWidth
              value={formData.legal_reference}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary">
              Crear Factura
            </Button>
          </Grid>
        </Grid>
      </form>
       
    </Container>
    </Stack>
  );
};

export default NovaFaturaProforma;
