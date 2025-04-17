import * as React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Grid,
  Stack,
  Stepper,
  Step,
  StepLabel,
  Typography,
  Snackbar,
  Alert
} from '@mui/material';
import {
  ChevronLeftRounded as BackIcon,
  ChevronRightRounded as NextIcon,
  CheckCircleOutline as SuccessIcon
} from '@mui/icons-material';
import ProductBasicForm from '../components/ProductBasicForm';
import ProductInventoryForm from '../components/ProductInventoryForm';
import ProductPricingForm from '../components/ProductPricingForm';
import { productService } from '../api/apiService';
import AppTheme from '../shared-theme/AppTheme';
import CssBaseline from '@mui/material/CssBaseline';

const steps = ['Información Básica', 'Inventario', 'Precio y Categoría'];

export default function NovoProducto() {
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState({
    sku: '',
    name: '',
    description: '',
    price: 0,
    unit: 'unidades',
    category: '',
    expiration_date: '',
    image_url: '',
    attributes: {},
    stock: 0,
    location: ''
  });
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    try {
      await productService.createProduct(formData);
      setActiveStep(steps.length);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al crear el producto');
    }
  };

  const handleStepNavigation = (direction: 'next' | 'back') => {
    if (direction === 'next' && !validateStep(activeStep)) return;
    
    direction === 'next' 
      ? activeStep === steps.length - 1 ? handleSubmit() : setActiveStep(prev => prev + 1)
      : setActiveStep(prev => prev - 1);
  };

  const validateStep = (step: number): boolean => {
    const validations = [
      () => !!formData.sku && !!formData.name,
      () => formData.stock >= 0,
      () => !!formData.price && !!formData.category
    ];
    
    if (!validations[step]?.()) {
      setError('Complete los campos requeridos');
      return false;
    }
    setError(null);
    return true;
  };

  return (
    <AppTheme>
      <CssBaseline enableColorScheme />
      
      <Container maxWidth="xl" sx={{ pt: 8, pb: 4 }}>
        <Grid container spacing={3} sx={{ minHeight: 'calc(100vh - 64px)' }}>
          <Grid item xs={12} md={10} lg={8} sx={{ mx: 'auto' }}>
            <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 4 }}>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>

            <Box sx={{ bgcolor: 'background.paper', borderRadius: 2, boxShadow: 1, p: { xs: 2, sm: 4 } }}>
              {activeStep === steps.length ? (
                <Stack spacing={3} alignItems="center" sx={{ py: 4 }}>
                  <SuccessIcon sx={{ fontSize: 80, color: 'success.main' }} />
                  <Typography variant="h5">¡Producto creado exitosamente!</Typography>
                  <Button variant="contained" onClick={() => navigate('/productos')}>
                    Ver listado de productos
                  </Button>
                </Stack>
              ) : (
                <>
                  {activeStep === 0 && <ProductBasicForm formData={formData} handleChange={handleChange} />}
                  {activeStep === 1 && <ProductInventoryForm formData={formData} handleChange={handleChange} />}
                  {activeStep === 2 && <ProductPricingForm formData={formData} handleChange={handleChange} />}
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4, pt: 3, borderTop: 1, borderColor: 'divider' }}>
                    {activeStep > 0 && (
                      <Button onClick={() => handleStepNavigation('back')} startIcon={<BackIcon />}>
                        Anterior
                      </Button>
                    )}
                    <Button 
                      onClick={() => handleStepNavigation('next')} 
                      endIcon={<NextIcon />}
                      variant="contained"
                      sx={{ ml: 'auto' }}
                    >
                      {activeStep === steps.length - 1 ? 'Guardar Producto' : 'Siguiente'}
                    </Button>
                  </Box>
                </>
              )}
            </Box>
          </Grid>
        </Grid>
      </Container>

      <Snackbar open={!!error} autoHideDuration={6000} onClose={() => setError(null)}>
        <Alert severity="error">{error}</Alert>
      </Snackbar>
    </AppTheme>
  );
}