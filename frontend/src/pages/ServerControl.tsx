import React from 'react';
import { Box, Button, Stack, Typography } from '@mui/material';
import axios from 'axios';

const ServerControl: React.FC = () => {
  const handleAction = async (action: string) => {
    try {
      const response = await axios.post(`/server/${action}`);
      alert(response.data.message);
    } catch (error: any) {
      console.error(error);
      const errorMessage =
        error.response?.data?.error || error.response?.data?.message || 'Erro ao realizar a ação.';
      alert(`Erro: ${errorMessage}`);
    }
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Controlo do Servidor
      </Typography>
      <Stack spacing={2} direction="row">
        <Button variant="contained" color="primary" onClick={() => handleAction('start')}>
          Iniciar Servidor
        </Button>
        <Button variant="contained" color="warning" onClick={() => handleAction('pause')}>
          Pausar Servidor
        </Button>
        <Button variant="contained" color="error" onClick={() => handleAction('stop')}>
          Parar Servidor
        </Button>
        <Button variant="contained" color="secondary" onClick={() => handleAction('exit')}>
          Sair
        </Button>
      </Stack>
    </Box>
  );
};

export default ServerControl;
