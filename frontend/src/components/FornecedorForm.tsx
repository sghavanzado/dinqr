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
import { Business, LocationCity, Public, Phone, Email } from '@mui/icons-material';

interface FornecedorFormProps {
  formData: Supplier;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  errors?: {
    nif?: string;
    name?: string;
    address?: string;
    city?: string;
    state?: string;
    country?: string;
    phone?: {
      phone?: string;
      email?: string;
    };
  };
}

export default function FornecedorForm({ 
  formData, 
  handleChange,
  errors 
}: FornecedorFormProps) {
  return (
    <Grid container spacing={3}>
      {/* Encabezado */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
          Información Legal de la Empresa
        </Typography>
      </Grid>

      {/* NIF */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>NIF/NIE</Label>
          <OutlinedInput
            name="nif"
            value={formData.nif}
            onChange={handleChange}
            fullWidth
            error={!!errors?.nif}
            startAdornment={
              <InputAdornment position="start">
                <Business fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Número de identificación fiscal',
              pattern: '^[0-9XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$',
              title: 'Formato de NIF español válido'
            }}
          />
          {errors?.nif && <ErrorText>{errors.nif}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Nombre Legal */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Nombre Legal</Label>
          <OutlinedInput
            name="name"
            value={formData.name}
            onChange={handleChange}
            fullWidth
            error={!!errors?.name}
            inputProps={{
              'aria-label': 'Nombre legal del proveedor'
            }}
          />
          {errors?.name && <ErrorText>{errors.name}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Dirección Completa */}
      <Grid item xs={12}>
        <FormGroup>
          <Label required>Dirección Fiscal</Label>
          <OutlinedInput
            name="address"
            value={formData.address}
            onChange={handleChange}
            fullWidth
            error={!!errors?.address}
            placeholder="Calle, número, piso, puerta"
            inputProps={{
              'aria-label': 'Dirección completa'
            }}
          />
          {errors?.address && <ErrorText>{errors.address}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Ciudad */}
      <Grid item xs={12} md={4}>
        <FormGroup>
          <Label required>Ciudad</Label>
          <OutlinedInput
            name="city"
            value={formData.city}
            onChange={handleChange}
            fullWidth
            error={!!errors?.city}
            startAdornment={
              <InputAdornment position="start">
                <LocationCity fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Ciudad'
            }}
          />
          {errors?.city && <ErrorText>{errors.city}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Provincia */}
      <Grid item xs={12} md={4}>
        <FormGroup>
          <Label required>Provincia</Label>
          <OutlinedInput
            name="state"
            value={formData.state}
            onChange={handleChange}
            fullWidth
            error={!!errors?.state}
            inputProps={{
              'aria-label': 'Provincia'
            }}
          />
          {errors?.state && <ErrorText>{errors.state}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* País */}
      <Grid item xs={12} md={4}>
        <FormGroup>
          <Label required>País</Label>
          <OutlinedInput
            name="country"
            value={formData.country}
            onChange={handleChange}
            fullWidth
            error={!!errors?.country}
            startAdornment={
              <InputAdornment position="start">
                <Public fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'País'
            }}
          />
          {errors?.country && <ErrorText>{errors.country}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Contacto Corporativo */}
      <Grid item xs={12}>
        <Typography variant="subtitle1" gutterBottom sx={{ mt: 2, color: 'text.primary' }}>
          Contacto Corporativo
        </Typography>
      </Grid>

      {/* Teléfono Oficial */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Teléfono Oficial</Label>
          <OutlinedInput
            name="phone.phone"
            value={formData.phone.phone}
            onChange={handleChange}
            fullWidth
            error={!!errors?.phone?.phone}
            startAdornment={
              <InputAdornment position="start">
                <Phone fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Número de teléfono corporativo',
              pattern: '^[+][0-9]{1,3}[0-9]{4,14}$',
              title: 'Formato internacional: +[código país][número]'
            }}
          />
          {errors?.phone?.phone && <ErrorText>{errors.phone.phone}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Email Corporativo */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Email Corporativo</Label>
          <OutlinedInput
            name="phone.email"
            type="email"
            value={formData.phone.email}
            onChange={handleChange}
            fullWidth
            error={!!errors?.phone?.email}
            startAdornment={
              <InputAdornment position="start">
                <Email fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Dirección de email corporativo',
              pattern: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,4}$'
            }}
          />
          {errors?.phone?.email && <ErrorText>{errors.phone.email}</ErrorText>}
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