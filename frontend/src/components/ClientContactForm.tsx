import * as React from 'react';
import { FormLabel, Grid, OutlinedInput, Typography, Stack } from '@mui/material';
import { Client } from '../api/apiService';

interface ClientContactFormProps {
  formData: Client;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function ClientContactForm({ formData, handleChange }: ClientContactFormProps) {
  return (
    <Grid container spacing={3}>
      {/* Encabezado de sección */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Información del Contacto Principal
        </Typography>
      </Grid>

      {/* Fila 1 - Nombre completo */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <StyledLabel required>Nombre</StyledLabel>
          <OutlinedInput
            name="contact_first_name"
            value={formData.contact_first_name}
            onChange={handleChange}
            fullWidth
            inputProps={{
              'aria-label': 'Nombre del contacto',
              pattern: '^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
              title: 'Solo letras y espacios'
            }}
          />
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <StyledLabel required>Apellidos</StyledLabel>
          <OutlinedInput
            name="contact_last_name"
            value={formData.contact_last_name}
            onChange={handleChange}
            fullWidth
            inputProps={{
              'aria-label': 'Apellidos del contacto',
              pattern: '^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
              title: 'Solo letras y espacios'
            }}
          />
        </FormGroup>
      </Grid>

      {/* Fila 2 - Datos de contacto */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <StyledLabel required>Teléfono Directo</StyledLabel>
          <OutlinedInput
            name="contact_phone_number"
            value={formData.contact_phone_number}
            onChange={handleChange}
            fullWidth
            inputProps={{
              'aria-label': 'Número de teléfono',
              pattern: '^[+][0-9]{1,3}[0-9]{4,14}$',
              title: 'Formato internacional: +[código país][número]',
              placeholder: '+34123456789'
            }}
          />
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <StyledLabel required>Correo Electrónico</StyledLabel>
          <OutlinedInput
            name="contact_email"
            type="email"
            value={formData.contact_email}
            onChange={handleChange}
            fullWidth
            inputProps={{
              'aria-label': 'Dirección de email',
              pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$',
              autoComplete: 'email'
            }}
          />
        </FormGroup>
      </Grid>
    </Grid>
  );
}

// Componentes auxiliares reutilizables
const FormGroup = ({ children }: { children: React.ReactNode }) => (
  <Stack spacing={1} sx={{ width: '100%' }}>
    {children}
  </Stack>
);

const StyledLabel = ({ required, children }: { required?: boolean; children: React.ReactNode }) => (
  <FormLabel required={required} sx={{
    fontWeight: 500,
    fontSize: '0.875rem',
    color: 'text.primary'
  }}>
    {children}
  </FormLabel>
);