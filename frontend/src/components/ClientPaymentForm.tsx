import * as React from 'react';
import { FormLabel, Grid, OutlinedInput, Stack, Typography } from '@mui/material';
import { Client } from '../api/apiService';

interface ClientPaymentFormProps {
  formData: Client;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function ClientPaymentForm({ formData, handleChange }: ClientPaymentFormProps) {
  return (
    <Stack spacing={3}>
      <Typography variant="h6" component="h2">
        Información Bancaria
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <FormLabel htmlFor="bank_name">
            Nombre del Banco
          </FormLabel>
          <OutlinedInput
            id="bank_name"
            name="bank_name"
            value={formData.bank_name}
            onChange={handleChange}
            size="small"
            fullWidth
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <FormLabel htmlFor="iban_number">
            Número IBAN
          </FormLabel>
          <OutlinedInput
            id="iban_number"
            name="iban_number"
            value={formData.iban_number}
            onChange={handleChange}
            size="small"
            fullWidth
            inputProps={{
              pattern: '^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$',
              title: 'Formato IBAN válido (Ej: ES9121000418450200051332)'
            }}
          />
        </Grid>

        <Grid item xs={12}>
          <FormLabel htmlFor="payment_terms">
            Términos de Pago
          </FormLabel>
          <OutlinedInput
            id="payment_terms"
            name="payment_terms"
            value={formData.payment_terms || ''}
            onChange={handleChange}
            size="small"
            fullWidth
            multiline
            rows={3}
          />
        </Grid>
      </Grid>
    </Stack>
  );
}