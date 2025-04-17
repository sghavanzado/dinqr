import * as React from 'react';
import { 
  Grid, 
  OutlinedInput, 
  Typography,
  InputAdornment
} from '@mui/material';
import { FormGroup, Label, ErrorText } from './FormComponents';
import { Numbers, Description } from '@mui/icons-material';
import { ProductFormType } from '../components/internals/types';

interface ProductBasicFormProps {
  formData: ProductFormType;
  handleChange: (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
  errors?: {
    sku?: string;
    name?: string;
    description?: string;
  };
}

export default function ProductBasicForm({
  formData,
  handleChange,
  errors
}: ProductBasicFormProps) {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
          Información Básica del Producto
        </Typography>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>SKU</Label>
          <OutlinedInput
            name="sku"
            value={formData.sku}
            onChange={handleChange}
            fullWidth
            error={!!errors?.sku}
            startAdornment={
              <InputAdornment position="start">
                <Numbers fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{ 
              pattern: '^[A-Z0-9\\-]+$', // Regex corregido
              'aria-label': 'Código SKU',
              maxLength: 50
            }}
          />
          {errors?.sku && <ErrorText>{errors.sku}</ErrorText>}
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Nombre</Label>
          <OutlinedInput
            name="name"
            value={formData.name}
            onChange={handleChange}
            fullWidth
            error={!!errors?.name}
            inputProps={{ 
              'aria-label': 'Nombre del producto',
              maxLength: 100
            }}
          />
          {errors?.name && <ErrorText>{errors.name}</ErrorText>}
        </FormGroup>
      </Grid>

      <Grid item xs={12}>
        <FormGroup>
          <Label>Descripción</Label>
          <OutlinedInput
            name="description"
            value={formData.description}
            onChange={handleChange}
            multiline
            rows={3}
            error={!!errors?.description}
            startAdornment={
              <InputAdornment position="start">
                <Description fontSize="small" color="action" />
              </InputAdornment>
            }
            inputProps={{
              'aria-label': 'Descripción del producto',
              maxLength: 500
            }}
          />
          {errors?.description && <ErrorText>{errors.description}</ErrorText>}
        </FormGroup>
      </Grid>
    </Grid>
  );
}