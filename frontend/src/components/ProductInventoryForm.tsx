import * as React from 'react';
import { 
  Grid, 
  OutlinedInput, 
  Typography,
  InputAdornment
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { FormGroup, Label, ErrorText } from './FormComponents';
import { Inventory, LocationOn, Event, Tune } from '@mui/icons-material';
import { ProductFormType } from '../components/internals/types';

interface ProductInventoryFormProps {
  formData: ProductFormType;
  handleChange: (event: React.ChangeEvent<HTMLInputElement> | { target: { name: string; value: any } }) => void;
  errors?: {
    stock?: string;
    location?: string;
    expiration_date?: string;
    attributes?: string;
  };
}

export default function ProductInventoryForm({ 
  formData, 
  handleChange,
  errors 
}: ProductInventoryFormProps) {
  const [jsonError, setJsonError] = React.useState<string | null>(null);

  const handleAttributesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    try {
      const value = JSON.parse(e.target.value);
      setJsonError(null);
      handleChange({
        target: {
          name: 'attributes',
          value: value
        }
      });
    } catch (error) {
      setJsonError('Formato JSON inválido');
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
            Gestión de Inventario
          </Typography>
        </Grid>

        {/* Stock */}
        <Grid item xs={12} md={6}>
          <FormGroup>
            <Label required>Stock Disponible</Label>
            <OutlinedInput
              name="stock"
              type="number"
              value={formData.stock}
              onChange={handleChange}
              fullWidth
              error={!!errors?.stock}
              startAdornment={
                <InputAdornment position="start">
                  <Inventory fontSize="small" color="action" />
                </InputAdornment>
              }
              inputProps={{
                'aria-label': 'Cantidad en stock',
                min: 0,
                step: 1
              }}
            />
            {errors?.stock && <ErrorText>{errors.stock}</ErrorText>}
          </FormGroup>
        </Grid>

        {/* Ubicación */}
        <Grid item xs={12} md={6}>
          <FormGroup>
            <Label>Ubicación en Almacén</Label>
            <OutlinedInput
              name="location"
              value={formData.location || ''}
              onChange={handleChange}
              fullWidth
              error={!!errors?.location}
              startAdornment={
                <InputAdornment position="start">
                  <LocationOn fontSize="small" color="action" />
                </InputAdornment>
              }
              inputProps={{
                'aria-label': 'Ubicación física en almacén',
                maxLength: 255
              }}
            />
            {errors?.location && <ErrorText>{errors.location}</ErrorText>}
          </FormGroup>
        </Grid>

        {/* Fecha de Expiración */}
        <Grid item xs={12} md={6}>
          <FormGroup>
            <Label>Fecha de Caducidad</Label>
            <DatePicker
              value={formData.expiration_date ? new Date(formData.expiration_date) : null}
              onChange={(date) => handleChange({
                target: {
                  name: 'expiration_date',
                  value: date?.toISOString()
                }
              })}
              disablePast
              slotProps={{
                textField: {
                  fullWidth: true,
                  error: !!errors?.expiration_date,
                  InputProps: {
                    startAdornment: (
                      <InputAdornment position="start">
                        <Event fontSize="small" color="action" />
                      </InputAdornment>
                    )
                  }
                }
              }}
            />
            {errors?.expiration_date && <ErrorText>{errors.expiration_date}</ErrorText>}
          </FormGroup>
        </Grid>

        {/* Atributos Personalizados */}
        <Grid item xs={12} md={6}>
          <FormGroup>
            <Label>Atributos Adicionales</Label>
            <OutlinedInput
              name="attributes"
              value={JSON.stringify(formData.attributes || {}, null, 2)}
              onChange={handleAttributesChange}
              fullWidth
              multiline
              rows={3}
              error={!!errors?.attributes || !!jsonError}
              startAdornment={
                <InputAdornment position="start">
                  <Tune fontSize="small" color="action" />
                </InputAdornment>
              }
              inputProps={{
                'aria-label': 'Atributos adicionales en formato JSON',
                style: { fontFamily: 'monospace' }
              }}
              placeholder={'{\n  "color": "rojo",\n  "tamaño": "XL"\n}'}
            />
            {(errors?.attributes || jsonError) && (
              <ErrorText>{errors?.attributes || jsonError}</ErrorText>
            )}
          </FormGroup>
        </Grid>
      </Grid>
    </LocalizationProvider>
  );
}