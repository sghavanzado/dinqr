import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Paper,
  Alert,
} from '@mui/material';
import {
  PeopleAlt as PeopleIcon,
  PersonAdd as PersonAddIcon,
  EventAvailable as EventIcon,
  Assessment as AssessmentIcon,
  AttachMoney as MoneyIcon,
  CardGiftcard as BenefitsIcon,
  Dashboard as DashboardIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import type { DashboardMetrics, ChartData } from '../../types/rrhh';
import { getDashboardMetrics } from '../../services/api/rrhh.js';
import StatsCard from '../../components/funcionarios/StatsCard';

const RRHHDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      setLoading(true);
      const data = await getDashboardMetrics();
      setMetrics(data);
    } catch (error) {
      console.error('Erro ao carregar métricas:', error);
      // Fallback para dados mock quando a API não estiver disponível
      const mockMetrics: DashboardMetrics = {
        funcionariosAtivos: 125,
        funcionariosInativos: 8,
        ultimasContratacoes: 5,
        licencasAtivas: 12,
        proximasAvaliacoes: 18,
        totalFuncionarios: 133
      };
      setMetrics(mockMetrics);
    } finally {
      setLoading(false);
    }
  };

  const funcionariosData: ChartData[] = [
    { name: 'Ativos', value: metrics?.funcionariosAtivos || 0, color: '#00C49F' },
    { name: 'Inativos', value: metrics?.funcionariosInativos || 0, color: '#FF8042' },
  ];

  const activityData: ChartData[] = [
    { name: 'Jan', value: 12 },
    { name: 'Fev', value: 19 },
    { name: 'Mar', value: 15 },
    { name: 'Abr', value: 22 },
    { name: 'Mai', value: 18 },
    { name: 'Jun', value: 25 },
  ];

  const QuickActionCard: React.FC<{
    title: string;
    description: string;
    icon: React.ReactNode;
    color: string;
    onClick: () => void;
  }> = ({ title, description, icon, color, onClick }) => (
    <Card sx={{ cursor: 'pointer' }} onClick={onClick}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box sx={{ color, mr: 2 }}>
            {icon}
          </Box>
          <Typography variant="h6">{title}</Typography>
        </Box>
        <Typography variant="body2" color="textSecondary">
          {description}
        </Typography>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Carregando dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard RRHH
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Visão geral dos recursos humanos da empresa
        </Typography>
      </Box>

      {/* Development Notice */}
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>Modo de Demonstração:</strong> O sistema RRHH está atualmente exibindo dados simulados. 
          A integração com o backend está em desenvolvimento.
        </Typography>
      </Alert>

      {/* Métricas Principais */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
          <StatsCard
            title="Funcionários Ativos"
            value={metrics?.funcionariosAtivos || 0}
            icon={<PeopleIcon sx={{ fontSize: 40 }} />}
            color="success"
            trend="up"
            trendValue="+12% este mês"
          />
        </Box>
        <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
          <StatsCard
            title="Novas Contratações"
            value={metrics?.ultimasContratacoes || 0}
            icon={<PersonAddIcon sx={{ fontSize: 40 }} />}
            color="primary"
            trend="up"
            trendValue="+5 este mês"
          />
        </Box>
        <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
          <StatsCard
            title="Licenças Ativas"
            value={metrics?.licencasAtivas || 0}
            icon={<EventIcon sx={{ fontSize: 40 }} />}
            color="warning"
          />
        </Box>
        <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
          <StatsCard
            title="Próximas Avaliações"
            value={metrics?.proximasAvaliacoes || 0}
            icon={<AssessmentIcon sx={{ fontSize: 40 }} />}
            color="info"
          />
        </Box>
      </Box>

      {/* Gráficos */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        <Box sx={{ flex: '1 1 400px', minWidth: '300px' }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" mb={2}>
              Distribuição de Funcionários
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={funcionariosData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {funcionariosData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Box>
        <Box sx={{ flex: '1 1 400px', minWidth: '300px' }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" mb={2}>
              Atividade de Contratações (Últimos 6 meses)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#0088FE" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Box>
      </Box>

      {/* Ações Rápidas */}
      <Box mb={4}>
        <Typography variant="h6" mb={2}>
          Ações Rápidas
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <QuickActionCard
              title="Adicionar Funcionário"
              description="Registrar novo funcionário no sistema"
              icon={<PersonAddIcon sx={{ fontSize: 32 }} />}
              color="#00C49F"
              onClick={() => navigate('/rrhh/funcionarios?action=new')}
            />
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <QuickActionCard
              title="Registrar Presença"
              description="Lançamento manual de presença"
              icon={<EventIcon sx={{ fontSize: 32 }} />}
              color="#0088FE"
              onClick={() => navigate('/rrhh/presencas?action=new')}
            />
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <QuickActionCard
              title="Nova Avaliação"
              description="Agendar avaliação de desempenho"
              icon={<AssessmentIcon sx={{ fontSize: 32 }} />}
              color="#FFBB28"
              onClick={() => navigate('/rrhh/avaliacoes?action=new')}
            />
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <QuickActionCard
              title="Gerar Folha"
              description="Processar folha salarial do mês"
              icon={<MoneyIcon sx={{ fontSize: 32 }} />}
              color="#FF8042"
              onClick={() => navigate('/rrhh/folha-salarial?action=new')}
            />
          </Box>
        </Box>
      </Box>

      {/* Resumo por Módulos */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" mb={3}>
          Acesso aos Módulos
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<PeopleIcon />}
              onClick={() => navigate('/rrhh/funcionarios')}
              sx={{ py: 2 }}
            >
              Gestão de Funcionários
            </Button>
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<DashboardIcon />}
              onClick={() => navigate('/rrhh/departamentos')}
              sx={{ py: 2 }}
            >
              Departamentos & Cargos
            </Button>
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<EventIcon />}
              onClick={() => navigate('/rrhh/presencas')}
              sx={{ py: 2 }}
            >
              Controle de Presenças
            </Button>
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<EventIcon />}
              onClick={() => navigate('/rrhh/licencas')}
              sx={{ py: 2 }}
            >
              Gestão de Licenças
            </Button>
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<AssessmentIcon />}
              onClick={() => navigate('/rrhh/avaliacoes')}
              sx={{ py: 2 }}
            >
              Avaliações de Desempenho
            </Button>
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<MoneyIcon />}
              onClick={() => navigate('/rrhh/folha-salarial')}
              sx={{ py: 2 }}
            >
              Folha Salarial
            </Button>
          </Box>
          <Box sx={{ flex: '1 1 300px', minWidth: '250px' }}>
            <Button
              variant="outlined"
              fullWidth
              startIcon={<BenefitsIcon />}
              onClick={() => navigate('/rrhh/beneficios')}
              sx={{ py: 2 }}
            >
              Benefícios
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default RRHHDashboard;
