import React from 'react';
import { Container, Typography, TextField, Button, Box } from '@mui/material';

const SignIn: React.FC = () => {
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Handle sign in logic
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Typography variant="h4" gutterBottom>
          Sign In
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField label="Email" fullWidth margin="normal" required />
          <TextField label="Password" type="password" fullWidth margin="normal" required />
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Sign In
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default SignIn;