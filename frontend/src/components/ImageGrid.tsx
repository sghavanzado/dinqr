import React from 'react';
import { Grid, Box, Typography } from '@mui/material';

const ImageGrid: React.FC = () => {
  const images = [
    { src: '/path/to/image1.jpg', description: 'Image 1' },
    { src: '/path/to/image2.jpg', description: 'Image 2' },
    { src: '/path/to/image3.jpg', description: 'Image 3' },
    { src: '/path/to/image4.jpg', description: 'Image 4' },
    { src: '/path/to/image5.jpg', description: 'Image 5' },
    { src: '/path/to/image6.jpg', description: 'Image 6' },
    { src: '/path/to/image7.jpg', description: 'Image 7' },
    { src: '/path/to/image8.jpg', description: 'Image 8' },
  ];

  return (
    <Grid container spacing={2}>
      {images.map((image, index) => (
        <Grid item xs={12} sm={6} md={3} key={index}>
          <Box sx={{ position: 'relative' }}>
            <img src={image.src} alt={image.description} style={{ width: '100%', height: 'auto' }} />
            <Typography variant="body2" sx={{ position: 'absolute', bottom: 8, left: 8, color: 'white', backgroundColor: 'rgba(0, 0, 0, 0.5)', padding: '4px 8px', borderRadius: '4px' }}>
              {image.description}
            </Typography>
          </Box>
        </Grid>
      ))}
    </Grid>
  );
};

export default ImageGrid;