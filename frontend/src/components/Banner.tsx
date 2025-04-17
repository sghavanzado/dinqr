import React from 'react';
import { Box, Typography, Container } from '@mui/material';

const Banner: React.FC = () => {
  return (
    <Box sx={{ position: 'relative', height: '40vh', backgroundImage: 'url(/path/to/banner.jpg)', backgroundSize: 'cover', backgroundPosition: 'center' }}>
      <Container sx={{ position: 'absolute', bottom: 20, left: 20, color: 'white' }}>
        <Typography variant="h4">Featured Banner</Typography>
        <Typography variant="body1">This is a description of the featured banner.</Typography>
      </Container>
    </Box>
  );
};

export default Banner;