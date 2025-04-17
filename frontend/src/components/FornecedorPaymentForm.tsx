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
import { AccountBalance, Payment, Description } from '@mui/icons-material';

interface FornecedorPaymentFormProps {
  formData: Supplier;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  errors?: {
    bank_name?: string;
    iban_number?: string;
    payment_terms?: string;
  };
}

export default function FornecedorPaymentForm({ 
  formData, 
  handleChange,
  errors 
}: FornecedorPaymentFormProps) {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
          Información Bancaria y Términos de Pago
        </Typography>
      </Grid>

      {/* Nombre del Banco */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Nombre del Banco</Label>
          <OutlinedInput
            name="bank_name"
            value={formData.bank_name || ''}
            onChange={handleChange}
            fullWidth
            error={!!errors?.bank_name}
            startAdornment={
              <InputAdornment position="start">
                <AccountBalance fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Nombre de la entidad bancaria',
              maxLength: 50
            }}
          />
          {errors?.bank_name && <ErrorText>{errors.bank_name}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Número IBAN */}
      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Número IBAN</Label>
          <OutlinedInput
            name="iban_number"
            value={formData.iban_number || ''}
            onChange={handleChange}
            fullWidth
            error={!!errors?.iban_number}
            startAdornment={
              <InputAdornment position="start">
                <Payment fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Número de cuenta internacional',
              pattern: '^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$',
              title: 'Formato IBAN válido (Ej: ES9121000418450200051332)',
              placeholder: 'ES00 0000 0000 00 0000000000'
            }}
          />
          {errors?.iban_number && <ErrorText>{errors.iban_number}</ErrorText>}
        </FormGroup>
      </Grid>

      {/* Términos de Pago */}
      <Grid item xs={12}>
        <FormGroup>
          <Label>Términos de Pago</Label>
          <OutlinedInput
            name="payment_terms"
            value={formData.payment_terms || ''}
            onChange={handleChange}
            fullWidth
            multiline
            rows={4}
            error={!!errors?.payment_terms}
            startAdornment={
              <InputAdornment position="start" sx={{ alignSelf: 'flex-start' }}>
                <Description fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Condiciones de pago',
              maxLength: 500
            }}
          />
          {errors?.payment_terms && <ErrorText>{errors.payment_terms}</ErrorText>}
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