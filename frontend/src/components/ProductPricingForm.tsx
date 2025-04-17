import * as React from 'react';
import { 
  Typography, 
  Grid, 
  OutlinedInput, 
  MenuItem, 
  Select,
  SelectChangeEvent
} from '@mui/material';
import { FormGroup, Label, ErrorText } from './FormComponents';
import { AttachMoney, Category } from '@mui/icons-material';
import { ProductFormType } from '../components/internals/types';

interface ProductPricingFormProps {
  formData: ProductFormType;
  handleChange: (event: 
    | React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> 
    | SelectChangeEvent<string>
  ) => void;
  errors?: {
    price?: string;
    unit?: string;
    category?: string;
  };
}

export default function ProductPricingForm({ 
  formData, 
  handleChange,
  errors
}: ProductPricingFormProps) {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom sx={{ color: 'text.primary' }}>
          Precio y Categorización
        </Typography>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Precio</Label>
          <OutlinedInput
            name="price"
            type="number"
            value={formData.price}
            onChange={handleChange}
            fullWidth
            error={!!errors?.price}
            startAdornment={<AttachMoney fontSize="small" />}
            inputProps={{ 
              min: 0, 
              step: 0.01, 
              'aria-label': 'Precio del producto',
              inputMode: 'decimal'
            }}
          />
          {errors?.price && <ErrorText>{errors.price}</ErrorText>}
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Unidad de Medida</Label>
          <Select
            name="unit"
            value={formData.unit}
            onChange={handleChange}
            fullWidth
            error={!!errors?.unit}
            inputProps={{ 'aria-label': 'Unidad de medida' }}
          >
            <MenuItem value="unidades">Unidades</MenuItem>
            <MenuItem value="kg">Kilogramos</MenuItem>
            <MenuItem value="litros">Litros</MenuItem>
          </Select>
          {errors?.unit && <ErrorText>{errors.unit}</ErrorText>}
        </FormGroup>
      </Grid>

      <Grid item xs={12} md={6}>
        <FormGroup>
          <Label required>Categoría</Label>
          <OutlinedInput
            name="category"
            value={formData.category}
            onChange={handleChange}
            fullWidth
            error={!!errors?.category}
            startAdornment={<Category fontSize="small" />}
            inputProps={{
              'aria-label': 'Categoría del producto',
              maxLength: 50
            }}
          />
          {errors?.category && <ErrorText>{errors.category}</ErrorText>}
        </FormGroup>
      </Grid>
    </Grid>
  );
}