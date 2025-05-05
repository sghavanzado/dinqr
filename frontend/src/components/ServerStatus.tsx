import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const ServerStatus: React.FC = () => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography component="h2" variant="subtitle2" gutterBottom>
          Server Status
        </Typography>
        <Typography
          sx={{
            color: 'success.main',
            fontWeight: 'bold',
            fontSize: '1.2rem',
          }}
        >
          Online
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ServerStatus;
