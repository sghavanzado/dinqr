
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';

import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';


export type StatCardProps = {
  title: string;
  value: string;
  trend: 'up' | 'down' | 'neutral';
};



export default function StatCard({
  title,
  value,
  trend,
}: StatCardProps) {

  const labelColors = {
    up: 'success' as const,
    down: 'error' as const,
    neutral: 'default' as const,
  };

  const color = labelColors[trend];

  return (
    <Card variant="outlined" sx={{ height: '100%', flexGrow: 1 }}>
      <CardContent>
        <Typography component="h2" variant="subtitle2" gutterBottom >
          {title}
        </Typography>
        <Stack
          direction="column"
          sx={{ justifyContent: 'space-between', flexGrow: '1', gap: 1 }}
        >
          <Stack sx={{ justifyContent: 'space-between' }}>
            <Stack
              direction="row"
              sx={{ justifyContent: 'space-between', alignItems: 'center' }}
            >
              <Typography variant="h4" component="p" color={color} >
                {value}
              </Typography>
            </Stack>
          </Stack>
          
        </Stack>
      </CardContent>
    </Card>
  );
}
