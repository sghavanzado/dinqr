import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid
} from '@mui/material';
import {
  People as PeopleIcon,
  Dashboard as DashboardIcon
} from '@mui/icons-material';

const RRHHSimple: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        RRHH - Sistema Simples
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <PeopleIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  Funcionários
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Gerir informações dos funcionários da empresa.
              </Typography>
              <Button variant="contained" color="primary">
                Ver Funcionários
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <DashboardIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">
                  Dashboard
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Visão geral dos dados de recursos humanos.
              </Typography>
              <Button variant="contained" color="primary">
                Ver Dashboard
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          Status da Implementação RRHH
        </Typography>
        <Typography variant="body1">
          ✅ Componentes modulares criados<br/>
          ✅ Navegação configurada<br/>
          ✅ Proteção de rotas implementada<br/>
          ✅ Dependências instaladas<br/>
          🔧 Testando servidor de desenvolvimento...
        </Typography>
      </Box>
    </Box>
  );
};

export default RRHHSimple;
