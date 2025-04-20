import * as React from 'react';
import { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid2';
import Box from '@mui/material/Box';

import Typography from '@mui/material/Typography';

import CustomizedDataGrid from './CustomizedDataGrid';
import ServerStatus from './ServerStatus';
import StatCard, { StatCardProps } from './StatCard';
import axiosInstance from '../api/axiosInstance';

export default function MainGrid() {
  const [totalFuncionarios, setTotalFuncionarios] = useState<number | null>(null);
  const [funcionariosComQR, setFuncionariosComQR] = useState<number | null>(null);
  const [funcionariosSemQR, setFuncionariosSemQR] = useState<number | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const totalResponse = await axiosInstance.get('/qr/funcionarios/total'); // Endpoint para obtener el total
        const total = totalResponse.data.total;
        setTotalFuncionarios(total);

        const qrResponse = await axiosInstance.get('/qr/funcionarios/total-con-qr'); // Endpoint para obtener los funcionarios con QR
        const totalConQR = qrResponse.data.total;
        setFuncionariosComQR(totalConQR);

        // Calcular funcionarios sin QR
        setFuncionariosSemQR(total - totalConQR);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const data: StatCardProps[] = [
    {
      title: 'Total Funcionarios',
      value: totalFuncionarios !== null ? totalFuncionarios.toString() : 'Cargando...',
      trend: 'up',
    },
    {
      title: 'Funcionários sem QR',
      value: funcionariosSemQR !== null ? funcionariosSemQR.toString() : 'Cargando...',
      trend: 'down',
    },
    {
      title: 'Funcionários com QR',
      value: funcionariosComQR !== null ? funcionariosComQR.toString() : 'Cargando...',
      trend: 'neutral',
    },
  ];

  return (
    <Box sx={{ width: '100%', maxWidth: { sm: '100%', md: '1700px' } }}>
      {/* cards */}
      <Typography component="h2" variant="h6" sx={{ mb: 2 }}>
        Dashboard
      </Typography>
      <Grid
        container
        spacing={1}
        columns={12}
        sx={{ mb: (theme) => theme.spacing(2) }}
      >
        {data.map((card, index) => (
          <Grid key={index} size={{ xs: 12, sm: 6, lg: 3 }}>
            <StatCard {...card} />
          </Grid>
        ))}
        <Grid size={{ xs: 12, sm: 6, lg: 3 }}>
          <ServerStatus />
        </Grid>
    
        <Grid size={{ xs: 12, md: 6, lg: 3  }}>

        </Grid>
      </Grid>

        <Grid size={{ xs: 12, lg: 12 }}>
        <CustomizedDataGrid />
        </Grid>
       

    </Box>
  );
}
