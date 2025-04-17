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
import AppTheme from '../shared-theme/AppTheme';
import CssBaseline from '@mui/material/CssBaseline';
import ColorModeIconDropdown from '../shared-theme/ColorModeIconDropdown';
import { Supplier } from '../api/apiService';
import FornecedorForm from '../components/FornecedorForm';
import FornecedorContactForm from '../components/FornecedorContactForm';
import FornecedorPaymentForm from '../components/FornecedorPaymentForm';
import { supplierService } from '../api/apiService';

const steps = ['Información Legal', 'Contacto', 'Información Bancaria'];

export default function NovoFornecedor() {
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState<Supplier>({
    name: '',
    nif: '',
    address: '',
    city: '',
    state: '',
    country: '',
    phone: { phone: '', email: '' },
    contact_first_name: '',
    contact_last_name: '',
    contact_email: '',
    contact_phone_number: '',
    bank_name: '',
    iban_number: '',
    payment_terms: ''
  });
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    if (name.startsWith('phone.')) {
      const [, field] = name.split('.') as [string, keyof Supplier['phone']];
      setFormData(prev => ({
        ...prev,
        phone: { ...prev.phone, [field]: value }
      }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async () => {
    try {
      await supplierService.createSupplier(formData);
      setActiveStep(steps.length);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al crear el proveedor');
    }
  };

  const handleStepNavigation = (direction: 'next' | 'back') => {
    direction === 'next' 
      ? activeStep === steps.length - 1 ? handleSubmit() : setActiveStep(prev => prev + 1)
      : setActiveStep(prev => prev - 1);
  };

  const getStepContent = (step: number) => {
    switch (step) {
      case 0: return <FornecedorForm formData={formData} handleChange={handleChange} />;
      case 1: return <FornecedorContactForm formData={formData} handleChange={handleChange} />;
      case 2: return <FornecedorPaymentForm formData={formData} handleChange={handleChange} />;
      default: return null;
    }
  };

  return (
    <AppTheme>
      <CssBaseline enableColorScheme />
      
      <Box sx={{ position: 'fixed', top: '1rem', right: '1rem', zIndex: 1 }}>
        <ColorModeIconDropdown />
      </Box>

      <Container maxWidth="xl" sx={{ pt: 8, pb: 4 }}>
        <Grid container spacing={3} sx={{ minHeight: 'calc(100vh - 64px)' }}>
          <Grid item xs={12} md={10} lg={8} sx={{ mx: 'auto' }}>
            <Stepper
              activeStep={activeStep}
              alternativeLabel
              sx={{ 
                mb: 4, 
                '& .MuiStepLabel-label': { 
                  fontSize: { xs: '0.75rem', sm: '0.875rem' },
                  fontWeight: 500
                } 
              }}
            >
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>

            <Box sx={{ 
              bgcolor: 'background.paper',
              borderRadius: 2,
              boxShadow: 1,
              p: { xs: 2, sm: 4 },
              position: 'relative'
            }}>
              {activeStep === steps.length ? (
                <Stack spacing={3} alignItems="center" sx={{ py: 4 }}>
                  <SuccessIcon sx={{ fontSize: 80, color: 'success.main' }} />
                  <Typography variant="h5" textAlign="center">
                    ¡Proveedor registrado exitosamente!
                  </Typography>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={() => navigate('/fornecedores')}
                    sx={{ width: { xs: '100%', sm: 'auto' } }}
                  >
                    Volver al listado
                  </Button>
                </Stack>
              ) : (
                <>
                  {getStepContent(activeStep)}
                  
                  <Box sx={{
                    display: 'flex',
                    justifyContent: activeStep === 0 ? 'flex-end' : 'space-between',
                    gap: 2,
                    mt: 4,
                    pt: 3,
                    borderTop: '1px solid',
                    borderColor: 'divider'
                  }}>
                    {activeStep > 0 && (
                      <Button
                        onClick={() => handleStepNavigation('back')}
                        startIcon={<BackIcon />}
                        variant="outlined"
                        size="large"
                        sx={{ minWidth: 120 }}
                      >
                        Anterior
                      </Button>
                    )}
                    
                    <Button
                      onClick={() => handleStepNavigation('next')}
                      endIcon={<NextIcon />}
                      variant="contained"
                      size="large"
                      sx={{ minWidth: 180, ml: 'auto' }}
                    >
                      {activeStep === steps.length - 1 ? 'Guardar proveedor' : 'Siguiente'}
                    </Button>
                  </Box>
                </>
              )}
            </Box>
          </Grid>
        </Grid>
      </Container>

      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity="error" variant="filled" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>
    </AppTheme>
  );
}