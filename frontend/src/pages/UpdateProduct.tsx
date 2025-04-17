// src/pages/UpdateProduct/UpdateProduct.tsx
import React, { useState, useEffect } from 'react';
import {
  Stepper,
  Step,
  StepLabel,
  Button,
  Grid,
  Typography,
  Snackbar,
  MenuItem,
  CircularProgress
} from '@mui/material';
import { ChevronLeft, ChevronRight, CalendarToday, Inventory, AttachMoney, Scale, Category, Place } from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { FormGroup, Label, StyledTextField, ErrorText, IconWrapper } from '../components/Form';
import { Product, productService } from '../api/apiService';

const steps = ['Información Básica', 'Detalles del Producto', 'Inventario'];

const UpdateProduct: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState<Partial<Product>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [globalError, setGlobalError] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadProductData = async () => {
      if (!id) {
        setGlobalError('ID de producto no válido');
        return;
      }

      try {
        const product = await productService.getProduct(parseInt(id));
        setFormData(product);
        setLoading(false);
      } catch (err) {
        setGlobalError('Error al cargar el producto');
        setLoading(false);
      }
    };

    loadProductData();
  }, [id]);

  const validateStep = () => {
    const newErrors: Record<string, string> = {};
    
    if (activeStep === 0) {
      if (!formData.sku?.match(/^[A-Z0-9]{6,12}$/)) {
        newErrors.sku = 'SKU inválido (6-12 caracteres alfanuméricos en mayúsculas)';
      }
      if (!formData.name?.trim()) {
        newErrors.name = 'Nombre requerido';
      }
      if (!formData.price || formData.price <= 0) {
        newErrors.price = 'Precio debe ser mayor a 0';
      }
    }

    if (activeStep === 1 && !formData.category) {
      newErrors.category = 'Categoría requerida';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (!validateStep()) return;
    setActiveStep(prev => Math.min(prev + 1, steps.length - 1));
  };

  const handleBack = () => {
    setActiveStep(prev => Math.max(prev - 1, 0));
  };

  const handleSubmit = async () => {
    if (!id) {
      setGlobalError('ID de producto no válido');
      return;
    }

    try {
      const productData = {
        ...formData,
        price: Number(formData.price),
        stock: Number(formData.stock)
      };

      await productService.updateProduct(parseInt(id), productData);
      navigate('/listagem-produtos');
    } catch (err) {
      setGlobalError('Error al actualizar el producto');
    }
  };

  if (loading) {
    return <CircularProgress sx={{ display: 'block', mx: 'auto', mt: 4 }} />;
  }

  return (
    <Grid container sx={{ p: { xs: 2, sm: 4 }, maxWidth: 800, mx: 'auto' }}>
      <Stepper activeStep={activeStep} sx={{ width: '100%', mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {activeStep === 0 && (
        <Grid item xs={12}>
          <FormGroup>
            <Label>SKU *</Label>
            <StyledTextField
              fullWidth
              value={formData.sku}
              onChange={(e) => setFormData({ ...formData, sku: e.target.value.toUpperCase() })}
              error={!!errors.sku}
              InputProps={{
                startAdornment: (
                  <IconWrapper position="start">
                    <Inventory />
                  </IconWrapper>
                )
              }}
              disabled
            />
            {errors.sku && <ErrorText>{errors.sku}</ErrorText>}
          </FormGroup>

          <FormGroup>
            <Label>Nombre del Producto *</Label>
            <StyledTextField
              fullWidth
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              error={!!errors.name}
            />
            {errors.name && <ErrorText>{errors.name}</ErrorText>}
          </FormGroup>

          <FormGroup>
            <Label>Precio *</Label>
            <StyledTextField
              fullWidth
              type="number"
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
              error={!!errors.price}
              InputProps={{
                startAdornment: (
                  <IconWrapper position="start">
                    <AttachMoney />
                  </IconWrapper>
                )
              }}
            />
            {errors.price && <ErrorText>{errors.price}</ErrorText>}
          </FormGroup>
        </Grid>
      )}

      {activeStep === 1 && (
        <Grid item xs={12}>
          <FormGroup>
            <Label>Categoría *</Label>
            <StyledTextField
              select
              fullWidth
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              error={!!errors.category}
              InputProps={{
                startAdornment: (
                  <IconWrapper position="start">
                    <Category />
                  </IconWrapper>
                )
              }}
            >
              <MenuItem value="alimentos">Alimentos</MenuItem>
              <MenuItem value="bebidas">Bebidas</MenuItem>
              <MenuItem value="limpieza">Limpieza</MenuItem>
              <MenuItem value="electronicos">Electrónicos</MenuItem>
            </StyledTextField>
            {errors.category && <ErrorText>{errors.category}</ErrorText>}
          </FormGroup>

          <FormGroup>
            <Label>Fecha de Vencimiento</Label>
            <StyledTextField
              fullWidth
              type="date"
              value={formData.expiration_date || ''}
              onChange={(e) => setFormData({ ...formData, expiration_date: e.target.value })}
              InputProps={{
                startAdornment: (
                  <IconWrapper position="start">
                    <CalendarToday />
                  </IconWrapper>
                )
              }}
            />
          </FormGroup>

          <FormGroup>
            <Label>Descripción</Label>
            <StyledTextField
              fullWidth
              multiline
              rows={4}
              value={formData.description || ''}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </FormGroup>
        </Grid>
      )}

      {activeStep === 2 && (
        <Grid item xs={12}>
          <FormGroup>
            <Label>Unidad de Medida *</Label>
            <StyledTextField
              select
              fullWidth
              value={formData.unit}
              onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
              InputProps={{
                startAdornment: (
                  <IconWrapper position="start">
                    <Scale />
                  </IconWrapper>
                )
              }}
            >
              <MenuItem value="unidades">Unidades</MenuItem>
              <MenuItem value="litros">Litros</MenuItem>
              <MenuItem value="kilogramos">Kilogramos</MenuItem>
              <MenuItem value="cajas">Cajas</MenuItem>
            </StyledTextField>
          </FormGroup>

          <FormGroup>
            <Label>Stock Disponible *</Label>
            <StyledTextField
              fullWidth
              type="number"
              value={formData.stock}
              onChange={(e) => setFormData({ ...formData, stock: parseInt(e.target.value) || 0 })}
              InputProps={{
                startAdornment: (
                  <IconWrapper position="start">
                    <Inventory />
                  </IconWrapper>
                )
              }}
            />
          </FormGroup>

          <FormGroup>
            <Label>Ubicación en Almacén</Label>
            <StyledTextField
              fullWidth
              value={formData.location || ''}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              InputProps={{
                startAdornment: (
                  <IconWrapper position="start">
                    <Place />
                  </IconWrapper>
                )
              }}
            />
          </FormGroup>
        </Grid>
      )}

      <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          startIcon={<ChevronLeft />}
          disabled={activeStep === 0}
          onClick={handleBack}
        >
          Anterior
        </Button>
        
        {activeStep === steps.length - 1 ? (
          <Button
            variant="contained"
            endIcon={<ChevronRight />}
            onClick={handleSubmit}
          >
            Actualizar Producto
          </Button>
        ) : (
          <Button
            variant="contained"
            endIcon={<ChevronRight />}
            onClick={handleNext}
          >
            Siguiente
          </Button>
        )}
      </Grid>

      <Snackbar
        open={!!globalError}
        autoHideDuration={6000}
        onClose={() => setGlobalError('')}
        message={globalError}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      />
    </Grid>
  );
};

export default UpdateProduct;