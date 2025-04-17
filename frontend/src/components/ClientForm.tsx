import * as React from 'react';
import { FormLabel, Grid, OutlinedInput, Typography } from '@mui/material';
import { Client } from '../api/apiService';

interface ClientFormProps {
  formData: Client;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function ClientForm({ formData, handleChange }: ClientFormProps) {
  return (
    <Grid container spacing={3}>
      {/* Encabezado de sección */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Información Legal de la Empresa
        </Typography>
      </Grid>

      {/* Fila 1 - Datos básicos */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>NIF/NIE</Label>
          <OutlinedInput
            name="nif"
            value={formData.nif}
            onChange={handleChange}
            inputProps={{ 
              pattern: '^[0-9XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$',
              title: 'Formato de NIF español válido'
            }}
            fullWidth
          />
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Nombre Legal</Label>
          <OutlinedInput
            name="name"
            value={formData.name}
            onChange={handleChange}
            fullWidth
          />
        </FormGroup>
      </Grid>

      {/* Fila 2 - Dirección completa */}
      <Grid item xs={12}>
        <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
          Dirección Fiscal
        </Typography>
      </Grid>

      <Grid item xs={12}>
        <FormGroup>
          <Label required>Dirección Completa</Label>
          <OutlinedInput
            name="address"
            value={formData.address}
            onChange={handleChange}
            fullWidth
            placeholder="Calle, número, piso, puerta"
          />
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={4}>
        <FormGroup>
          <Label required>Ciudad</Label>
          <OutlinedInput
            name="city"
            value={formData.city}
            onChange={handleChange}
            fullWidth
          />
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={4}>
        <FormGroup>
          <Label required>Provincia</Label>
          <OutlinedInput
            name="state"
            value={formData.state}
            onChange={handleChange}
            fullWidth
          />
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={4}>
        <FormGroup>
          <Label required>País</Label>
          <OutlinedInput
            name="country"
            value={formData.country}
            onChange={handleChange}
            fullWidth
          />
        </FormGroup>
      </Grid>

      {/* Fila 3 - Contacto corporativo */}
      <Grid item xs={12}>
        <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
          Contacto Corporativo
        </Typography>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Teléfono Oficial</Label>
          <OutlinedInput
            name="phone.phone"
            value={formData.phone.phone}
            onChange={handleChange}
            inputProps={{
              pattern: '^[+][0-9]{1,3}[0-9]{4,14}$',
              title: 'Formato internacional: +[código país][número]'
            }}
            fullWidth
          />
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Email Corporativo</Label>
          <OutlinedInput
            name="phone.email"
            type="email"
            value={formData.phone.email}
            onChange={handleChange}
            inputProps={{
              pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$'
            }}
            fullWidth
          />
        </FormGroup>
      </Grid>
    </Grid>
  );
}

// Componente auxiliar para agrupar elementos del formulario
const FormGroup = ({ children }: { children: React.ReactNode }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>{children}</div>
);

// Componente auxiliar para labels estilizados
const Label = ({ required, children }: { required?: boolean; children: React.ReactNode }) => (
  <FormLabel required={required} sx={{ 
    fontWeight: 500,
    color: 'text.primary',
    fontSize: '0.875rem'
  }}>
    {children}
  </FormLabel>
);