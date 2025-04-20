import { Card, CardContent, Typography, Stack } from '@mui/material';
import { BarChart } from '@mui/x-charts';
import React from 'react';

export const Summary: React.FC = () => {
  return (
    <Stack spacing={3}>
      <Typography variant="h4" gutterBottom component="h1">
        Resumo do Sistema
      </Typography>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={3} sx={{ mb: 4 }}>
        <Card sx={{ minWidth: 275, flex: 1 }}>
          <CardContent>
            <Typography variant="h6" component="h2" gutterBottom>
              Utilizadores Ativos
            </Typography>
            <Typography variant="h3" color="primary.main">
              1,234
            </Typography>
          </CardContent>
        </Card>
        <Card sx={{ minWidth: 275, flex: 1 }}>
          <CardContent>
            <Typography variant="h6" component="h2" gutterBottom>
              Receitas Mensais
            </Typography>
            <Typography variant="h3" color="success.main">
              €45,678
            </Typography>
          </CardContent>
        </Card>
      </Stack>
      <BarChart
        series={[
          {
            data: [35, 44, 24, 53],
            label: 'Desempenho Trimestral',
            color: '#1976d2',
          },
        ]}
        xAxis={[
          {
            data: ['T1', 'T2', 'T3', 'T4'],
            scaleType: 'band',
            label: 'Trimestres',
          },
        ]}
        yAxis={[{ label: 'Vendas (milhares)' }]}
        height={400}
        margin={{ left: 80, right: 30, top: 30, bottom: 50 }}
      />
    </Stack>
  );
};