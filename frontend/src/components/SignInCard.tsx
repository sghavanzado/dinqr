import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import MuiCard from '@mui/material/Card';
import Checkbox from '@mui/material/Checkbox';
import Divider from '@mui/material/Divider';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import Link from '@mui/material/Link';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/AuthContext';
import { GoogleIcon, FacebookIcon, SitemarkIcon } from './CustomIcons';
import LoadingBackdrop from './LoadingBackdrop';

const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignSelf: 'center',
  width: '100%',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  boxShadow:
    'hsla(220, 30%, 5%, 0.05) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.05) 0px 15px 35px -5px',
  [theme.breakpoints.up('sm')]: {
    width: '450px',
  },
  ...theme.applyStyles('dark', {
    boxShadow:
      'hsla(220, 30%, 5%, 0.5) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.08) 0px 15px 35px -5px',
  }),
}));

export default function SignInCard() {
  const { login, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    remember: false
  });
  const [errors, setErrors] = useState({
    email: '',
    password: '',
    general: ''
  });

  const validateForm = (): boolean => {
    let isValid = true;
    const newErrors = {
      email: '',
      password: '',
      general: ''
    };

    // Validación de email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Ingrese un correo electrónico válido';
      isValid = false;
    }

    // Validación de contraseña
    if (formData.password.length < 6) {
      newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      await login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (error: any) {
      setErrors(prev => ({
        ...prev,
        general: error.message || 'Error al iniciar sesión. Verifique sus credenciales.'
      }));
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'remember' ? checked : value
    }));

    // Limpiar errores al escribir
    if (errors[name as keyof typeof errors]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    if (errors.general) {
      setErrors(prev => ({ ...prev, general: '' }));
    }
  };

  return (
    <Card variant="outlined">
      <LoadingBackdrop open={authLoading} />
      
      <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
        <SitemarkIcon />
      </Box>

      <Typography
        component="h1"
        variant="h4"
        sx={{ 
          width: '100%', 
          fontSize: 'clamp(2rem, 10vw, 2.15rem)',
          textAlign: 'center',
          mb: 3
        }}
      >
        Iniciar Sesión
      </Typography>

      {errors.general && (
        <Typography 
          color="error" 
          variant="body2"
          sx={{ 
            textAlign: 'center',
            bgcolor: 'error.light',
            py: 1,
            borderRadius: 1
          }}
        >
          {errors.general}
        </Typography>
      )}

      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          width: '100%', 
          gap: 2 
        }}
      >
        <FormControl fullWidth>
          <FormLabel htmlFor="email">Correo Electrónico</FormLabel>
          <TextField
            id="email"
            name="email"
            type="email"
            placeholder="tucorreo@ejemplo.com"
            autoComplete="email"
            value={formData.email}
            onChange={handleInputChange}
            error={!!errors.email}
            helperText={errors.email}
            required
            variant="outlined"
            disabled={authLoading}
          />
        </FormControl>

        <FormControl fullWidth>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between',
            mb: 1
          }}>
            <FormLabel htmlFor="password">Contraseña</FormLabel>
            <Link 
              href="/forgot-password" 
              variant="body2" 
              sx={{ alignSelf: 'baseline' }}
            >
              ¿Olvidaste tu contraseña?
            </Link>
          </Box>
          <TextField
            id="password"
            name="password"
            type="password"
            placeholder="••••••"
            autoComplete="current-password"
            value={formData.password}
            onChange={handleInputChange}
            error={!!errors.password}
            helperText={errors.password}
            required
            variant="outlined"
            disabled={authLoading}
          />
        </FormControl>

        <FormControlLabel
          control={
            <Checkbox 
              name="remember" 
              checked={formData.remember} 
              onChange={handleInputChange} 
              color="primary" 
              disabled={authLoading}
            />
          }
          label="Recordar sesión"
        />

        <Button 
          type="submit" 
          fullWidth 
          variant="contained"
          disabled={authLoading}
          sx={{ py: 1.5, mt: 2 }}
        >
          {authLoading ? 'Cargando...' : 'Iniciar Sesión'}
        </Button>

        <Typography sx={{ textAlign: 'center', mt: 2 }}>
          ¿No tienes cuenta?{' '}
          <Link
            href="/registro"
            variant="body2"
            sx={{ fontWeight: 600 }}
          >
            Regístrate
          </Link>
        </Typography>
      </Box>

      <Divider sx={{ my: 3 }}>o</Divider>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Button
          fullWidth
          variant="outlined"
          onClick={() => window.location.href = '/api/auth/google'} // Usar ruta proxy
          startIcon={<GoogleIcon />}
        >
          Continuar con Google
        </Button>

        <Button
          fullWidth
          variant="outlined"
          onClick={() => window.location.href = '/api/auth/facebook'}
          startIcon={<FacebookIcon />}
          disabled={authLoading}
        >
          Continuar con Facebook
        </Button>
      </Box>
    </Card>
  );
}