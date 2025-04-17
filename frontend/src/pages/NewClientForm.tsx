import React, { useState } from 'react';
import { TextField, Button, Grid, Container, Typography } from '@mui/material';
import axios from 'axios';

const NewClientForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    nif: '',
    address: '',
    city: '',
    state: '',
    country: '',
    phone: '',
    contact_first_name: '',
    contact_last_name: '',
    contact_email: '',
    contact_phone_number: '',
    payment_terms: '',
    bank_name: '',
    iban_number: ''
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
      const response = await axios.post('/api/clients', formData);
      console.log(response.data);
      // Handle success (e.g., show a success message, clear the form, etc.)
    } catch (error) {
      console.error(error);
      // Handle error (e.g., show an error message)
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Nuevo Cliente
      </Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="name"
              label="Nombre"
              fullWidth
              value={formData.name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="nif"
              label="NIF"
              fullWidth
              value={formData.nif}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="address"
              label="Dirección"
              fullWidth
              value={formData.address}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="city"
              label="Ciudad"
              fullWidth
              value={formData.city}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="state"
              label="Estado"
              fullWidth
              value={formData.state}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="country"
              label="País"
              fullWidth
              value={formData.country}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="phone"
              label="Teléfono"
              fullWidth
              value={formData.phone}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="contact_first_name"
              label="Nombre del Contacto"
              fullWidth
              value={formData.contact_first_name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="contact_last_name"
              label="Apellido del Contacto"
              fullWidth
              value={formData.contact_last_name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="contact_email"
              label="Email del Contacto"
              fullWidth
              value={formData.contact_email}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              name="contact_phone_number"
              label="Teléfono del Contacto"
              fullWidth
              value={formData.contact_phone_number}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="payment_terms"
              label="Términos de Pago"
              fullWidth
              value={formData.payment_terms}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="bank_name"
              label="Nombre del Banco"
              fullWidth
              value={formData.bank_name}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              name="iban_number"
              label="Número IBAN"
              fullWidth
              value={formData.iban_number}
              onChange={handleChange}
            />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" color="primary">
              Guardar
            </Button>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
};

export default NewClientForm;
