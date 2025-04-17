import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const SignOut: React.FC = () => {
  // Handle sign out logic

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Typography variant="h4" gutterBottom>
          You have been signed out.
        </Typography>
      </Box>
    </Container>
  );
};

export default SignOut;