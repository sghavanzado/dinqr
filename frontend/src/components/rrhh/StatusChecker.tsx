import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  Chip,
  Grid,
  CircularProgress,
  Divider
} from '@mui/material';
import {
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
  Api as ApiIcon,
  Storage as DatabaseIcon,
  Speed as MetricsIcon
} from '@mui/icons-material';

interface StatusCheck {
  name: string;
  endpoint: string;
  status: 'loading' | 'success' | 'error';
  message?: string;
  data?: any;
}

const StatusChecker: React.FC = () => {
  const [checks, setChecks] = useState<StatusCheck[]>([
    { name: 'Status IAMC', endpoint: '/api/iamc/status', status: 'loading' },
    { name: 'Funcionários', endpoint: '/api/iamc/funcionarios', status: 'loading' },
    { name: 'Dashboard Metrics', endpoint: '/api/iamc/dashboard/metrics', status: 'loading' },
    { name: 'Departamentos', endpoint: '/api/iamc/departamentos', status: 'loading' },
    { name: 'Presenças', endpoint: '/api/iamc/presencas', status: 'loading' },
    { name: 'Licenças', endpoint: '/api/iamc/licencas', status: 'loading' }
  ]);

  const [isRunning, setIsRunning] = useState(false);

  const runChecks = async () => {
    setIsRunning(true);
    const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
    
    const newChecks = [...checks];
    
    for (let i = 0; i < newChecks.length; i++) {
      newChecks[i].status = 'loading';
      setChecks([...newChecks]);
      
      try {
        const response = await fetch(`${baseUrl}${newChecks[i].endpoint}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          timeout: 10000
        });
        
        if (response.ok) {
          const data = await response.json();
          newChecks[i].status = 'success';
          newChecks[i].message = 'OK';
          newChecks[i].data = data;
        } else {
          newChecks[i].status = 'error';
          newChecks[i].message = `HTTP ${response.status}`;
        }
      } catch (error) {
        newChecks[i].status = 'error';
        newChecks[i].message = error instanceof Error ? error.message : 'Erro desconhecido';
      }
      
      setChecks([...newChecks]);
      
      // Pequeno delay para melhor UX
      await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    setIsRunning(false);
  };

  useEffect(() => {
    runChecks();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'loading':
        return <CircularProgress size={20} />;
      case 'success':
        return <CheckIcon color="success" />;
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'success';
      case 'error':
        return 'error';
      case 'loading':
        return 'info';
      default:
        return 'default';
    }
  };

  const successCount = checks.filter(check => check.status === 'success').length;
  const totalChecks = checks.length;

  return (
    <Box sx={{ p: 3 }}>
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
            <Typography variant="h5" component="h1">
              🔍 Verificação de Integração RRHH
            </Typography>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={runChecks}
              disabled={isRunning}
            >
              {isRunning ? 'Verificando...' : 'Atualizar'}
            </Button>
          </Box>

          <Alert
            severity={successCount === totalChecks ? 'success' : 'warning'}
            sx={{ mb: 3 }}
          >
            <strong>Status Geral:</strong> {successCount}/{totalChecks} serviços funcionando
            {successCount === totalChecks && ' 🎉 Todos os sistemas operacionais!'}
          </Alert>

          <Grid container spacing={2}>
            {checks.map((check, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card variant="outlined" sx={{ p: 2 }}>
                  <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Box display="flex" alignItems="center" gap={1}>
                      {check.name.includes('IAMC') && <ApiIcon color="primary" />}
                      {check.name.includes('Funcionários') && <DatabaseIcon color="primary" />}
                      {check.name.includes('Metrics') && <MetricsIcon color="primary" />}
                      <Typography variant="subtitle1" fontWeight="medium">
                        {check.name}
                      </Typography>
                    </Box>
                    <Box display="flex" alignItems="center" gap={1}>
                      {getStatusIcon(check.status)}
                      <Chip
                        label={check.status === 'loading' ? 'Verificando...' : 
                               check.status === 'success' ? 'OK' : 'Erro'}
                        color={getStatusColor(check.status) as any}
                        size="small"
                      />
                    </Box>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {check.endpoint}
                  </Typography>
                  
                  {check.message && (
                    <Typography 
                      variant="body2" 
                      color={check.status === 'error' ? 'error' : 'text.secondary'}
                      sx={{ mt: 1 }}
                    >
                      {check.message}
                    </Typography>
                  )}
                  
                  {check.status === 'success' && check.data && (
                    <Box sx={{ mt: 2 }}>
                      <Divider sx={{ mb: 1 }} />
                      <Typography variant="caption" color="text.secondary">
                        {check.name.includes('Funcionários') && check.data.total && 
                          `${check.data.total} funcionários encontrados`}
                        {check.name.includes('Metrics') && check.data.metrics && 
                          `${check.data.metrics.totalFuncionarios || 0} funcionários total`}
                        {check.name.includes('Departamentos') && check.data.departamentos && 
                          `${check.data.departamentos.length} departamentos`}
                        {check.name.includes('Presenças') && check.data.data && 
                          `${check.data.data.length} registros de presença`}
                        {check.name.includes('Licenças') && check.data.data && 
                          `${check.data.data.length} licenças`}
                        {check.name.includes('IAMC') && check.data.status && 
                          `Status: ${check.data.status}`}
                      </Typography>
                    </Box>
                  )}
                </Card>
              </Grid>
            ))}
          </Grid>

          <Box sx={{ mt: 3 }}>
            <Alert severity="info">
              <Typography variant="body2">
                <strong>Como usar:</strong> Esta página verifica se todos os endpoints da API RRHH estão funcionando corretamente.
                Se algum serviço estiver com erro, verifique se o backend está rodando e se a base de dados IAMC está acessível.
              </Typography>
            </Alert>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default StatusChecker;
