
import type {} from '@mui/x-date-pickers/themeAugmentation';
import type {} from '@mui/x-charts/themeAugmentation';
import type {} from '@mui/x-tree-view/themeAugmentation';
import Stack from '@mui/material/Stack';
import MainGrid from '../components/MainGrid';


export default function Dashboard() {
  return (
<Stack
    spacing={2}
    sx={{
      alignItems: 'center',
      mx: 3,
      pb: 5,
      mt: { xs: 8, md: 0 },
    }}
  >

      <MainGrid />
   
     
 </Stack>   
   
  );
}
