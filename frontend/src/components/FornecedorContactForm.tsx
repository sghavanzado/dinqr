import * as React from 'react';
import { 
  FormLabel, 
  Grid, 
  OutlinedInput, 
  Typography, 
  Stack,
  InputAdornment
} from '@mui/material';
import { Supplier } from '../api/apiService';
import { Phone, Email } from '@mui/icons-material';

interface FornecedorContactFormProps {
  formData: Supplier;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  errors?: {
    contact_first_name?: string;
    contact_last_name?: string;
    contact_phone_number?: string;
    contact_email?: string;
  };
}

export default function FornecedorContactForm({ 
  formData, 
  handleChange,
  errors 
}: FornecedorContactFormProps) {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
          Información del Contacto Principal
        </Typography>
      </Grid>

      {/* Nombre */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Nombre</Label>
          <OutlinedInput
            name="contact_first_name"
            value={formData.contact_first_name}
            onChange={handleChange}
            fullWidth
            error={!!errors?.contact_first_name}
            inputProps={{
              'aria-label': 'Nombre del contacto',
              pattern: '^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
              title: 'Solo letras y espacios'
            }}
          />
          {errors?.contact_first_name && <ErrorText>{errors.contact_first_name}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Apellidos */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Apellidos</Label>
          <OutlinedInput
            name="contact_last_name"
            value={formData.contact_last_name}
            onChange={handleChange}
            fullWidth
            error={!!errors?.contact_last_name}
            inputProps={{
              'aria-label': 'Apellidos del contacto',
              pattern: '^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$',
              title: 'Solo letras y espacios'
            }}
          />
          {errors?.contact_last_name && <ErrorText>{errors.contact_last_name}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Teléfono */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Teléfono Directo</Label>
          <OutlinedInput
            name="contact_phone_number"
            value={formData.contact_phone_number}
            onChange={handleChange}
            fullWidth
            error={!!errors?.contact_phone_number}
            startAdornment={
              <InputAdornment position="start">
                <Phone fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Número de teléfono',
              pattern: '^[+][0-9]{1,3}[0-9]{4,14}$',
              title: 'Formato internacional: +[código país][número]',
              placeholder: '+34123456789'
            }}
          />
          {errors?.contact_phone_number && <ErrorText>{errors.contact_phone_number}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Email */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Correo Electrónico</Label>
          <OutlinedInput
            name="contact_email"
            type="email"
            value={formData.contact_email}
            onChange={handleChange}
            fullWidth
            error={!!errors?.contact_email}
            startAdornment={
              <InputAdornment position="start">
                <Email fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Dirección de email',
              pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$',
              autoComplete: 'email'
            }}
          />
          {errors?.contact_email && <ErrorText>{errors.contact_email}</ErrorText>}
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

const Label = ({ required, children }: { required?: boolean; children: React.ReactNode }) => (
  <FormLabel required={required} sx={{
    fontWeight: 500,
    fontSize: '0.875rem',
    color: 'text.primary',
    display: 'block',
    mb: 0.5
  }}>
    {children}
  </FormLabel>
);

const ErrorText = ({ children }: { children: React.ReactNode }) => (
  <Typography variant="caption" color="error" sx={{ mt: 0.5, display: 'block' }}>
    {children}
  </Typography>
);