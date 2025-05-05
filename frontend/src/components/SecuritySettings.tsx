import { TextField, Button, Typography, Stack, Alert } from '@mui/material';
import React from 'react';

export const SecuritySettings: React.FC = () => {
  return (
    <Stack spacing={3} sx={{ maxWidth: 600 }}>
      <Typography variant="h4" gutterBottom component="h1">
        Seguridad
      </Typography>
      
      <Alert severity="info" sx={{ mb: 2 }}>
        Actualiza tu contraseña periódicamente para mayor seguridad
      </Alert>
      
      <TextField
        label="Contraseña actual"
        type="password"
        fullWidth
        variant="outlined"
        margin="normal"
      />
      
      <TextField
        label="Nueva contraseña"
        type="password"
        fullWidth
        variant="outlined"
        margin="normal"
      />
      
      <TextField
        label="Confirmar nueva contraseña"
        type="password"
        fullWidth
        variant="outlined"
        margin="normal"
      />
      
      <Button
        variant="contained"
        color="warning"
        sx={{ 
          width: 250, 
          mt: 3,
          alignSelf: 'flex-start'
        }}
      >
        Cambiar Contraseña
      </Button>
    </Stack>
  );
};