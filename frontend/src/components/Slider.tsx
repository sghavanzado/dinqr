import React from 'react';
import { Box, Typography, Container } from '@mui/material';
import Carousel from 'react-material-ui-carousel';

const Slider: React.FC = () => {
  const items = [
    {
      image: '/path/to/image1.jpg',
      text: 'Slide 1',
    },
    {
      image: '/path/to/image2.jpg',
      text: 'Slide 2',
    },
    {
      image: '/path/to/image3.jpg',
      text: 'Slide 3',
    },
  ];

  return (
    <Carousel>
      {items.map((item, index) => (
        <Box key={index} sx={{ position: 'relative', height: '60vh', backgroundImage: `url(${item.image})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
          <Container sx={{ position: 'absolute', bottom: 20, left: 20, color: 'white' }}>
            <Typography variant="h4">{item.text}</Typography>
          </Container>
        </Box>
      ))}
    </Carousel>
  );
};

export default Slider;