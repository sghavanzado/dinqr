import React, { useEffect, useState } from 'react';
import { Box, Grid, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

const Stats: React.FC = () => {
  const [stats, setStats] = useState({ clients: 0, projects: 0, partners: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/stats')
      .then(response => {
        setStats(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching stats:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} sm={4}>
        <Box textAlign="center">
          <Typography variant="h4">{stats.clients}</Typography>
          <Typography variant="body1">Clients</Typography>
        </Box>
      </Grid>
      <Grid item xs={12} sm={4}>
        <Box textAlign="center">
          <Typography variant="h4">{stats.projects}</Typography>
          <Typography variant="body1">Projects</Typography>
        </Box>
      </Grid>
      <Grid item xs={12} sm={4}>
        <Box textAlign="center">
          <Typography variant="h4">{stats.partners}</Typography>
          <Typography variant="body1">Partners</Typography>
        </Box>
      </Grid>
    </Grid>
  );
};

export default Stats;