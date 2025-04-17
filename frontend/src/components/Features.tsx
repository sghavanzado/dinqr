import React from 'react';
import { Box, Grid, Typography } from '@mui/material';
import ViewQuiltRoundedIcon from '@mui/icons-material/ViewQuiltRounded';
import EdgesensorHighRoundedIcon from '@mui/icons-material/EdgesensorHighRounded';
import DevicesRoundedIcon from '@mui/icons-material/DevicesRounded';

const templateImageUrl = import.meta.env.VITE_TEMPLATE_IMAGE_URL || 'https://mui.com';

const items = [
  {
    icon: <ViewQuiltRoundedIcon />,
    title: 'Dashboard',
    description:
      'This item could provide a snapshot of the most important metrics or data points related to the product.',
    imageLight: `url("${templateImageUrl}/static/images/templates/templates-images/dash-light.png")`,
    imageDark: `url("${templateImageUrl}/static/images/templates/templates-images/dash-dark.png")`,
  },
  {
    icon: <EdgesensorHighRoundedIcon />,
    title: 'Mobile integration',
    description:
      'This item could provide information about the mobile app version of the product.',
    imageLight: `url("${templateImageUrl}/static/images/templates/templates-images/mobile-light.png")`,
    imageDark: `url("${templateImageUrl}/static/images/templates/templates-images/mobile-dark.png")`,
  },
  {
    icon: <DevicesRoundedIcon />,
    title: 'Available on all platforms',
    description:
      'This item could let users know the product is available on all platforms, such as web, mobile, and desktop.',
    imageLight: `url("${templateImageUrl}/static/images/templates/templates-images/devices-light.png")`,
    imageDark: `url("${templateImageUrl}/static/images/templates/templates-images/devices-dark.png")`,
  },
];

const Features: React.FC = () => {
  return (
    <Grid container spacing={2}>
      {items.map((item, index) => (
        <Grid item xs={12} sm={6} md={4} key={index}>
          <Box textAlign="center">
            {item.icon}
            <Typography variant="h6">{item.title}</Typography>
            <Typography variant="body1">{item.description}</Typography>
            <Box
              sx={{
                backgroundImage: item.imageLight,
                height: 200,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                mt: 2,
              }}
            />
          </Box>
        </Grid>
      ))}
    </Grid>
  );
};

export default Features;
