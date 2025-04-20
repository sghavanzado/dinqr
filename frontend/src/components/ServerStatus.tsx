import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

const ServerStatus: React.FC = () => {
  const [serverStatus, setServerStatus] = useState<string | null>(null);
  const [serverPid, setServerPid] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchServerStatus = async () => {
      try {
        const response = await axios.get('/settings/server/status'); // Endpoint para consultar el estado del servidor
        const { status, pid } = response.data;
        setServerStatus(status !== 'running' ? 'Online' : 'Offline');
        setServerPid(pid || null);
      } catch (error) {
        console.error('Error al obtener el estado del servidor:', error);
        setServerStatus('Error');
      } finally {
        setLoading(false);
      }
    };

    fetchServerStatus();
  }, []);

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography component="h2" variant="subtitle2" gutterBottom>
          Estado del Servidor
        </Typography>
        {loading ? (
          <CircularProgress size={24} />
        ) : (
          <>
            <Typography
              sx={{
                color: serverStatus === 'Online' ? 'success.main' : 'error.main',
                fontWeight: 'bold',
                fontSize: '1.2rem',
              }}
            >
              {serverStatus}
            </Typography>
            {serverStatus === 'Online' && serverPid && (
              <Typography variant="body2" color="textSecondary">
                PID: {serverPid}
              </Typography>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default ServerStatus;
