import { Card, CardContent, Typography } from '@mui/material';
import { LineChart } from '@mui/x-charts';

interface AnalyticsProps {
  data?: number[];
  labels?: string[];
}

export default function Analytics({ 
  data = [35, 44, 24, 53, 12, 45, 60],
  labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul']
}: AnalyticsProps) {
  return (
    <div>
      <Typography variant="h4" gutterBottom component="h2">
        Analíticas
      </Typography>
      
      <Card sx={{ mb: 3 }}>
        <CardContent sx={{ width: '100%', overflow: 'auto' }}>
          <div style={{ width: '100%', minWidth: 500 }}>
            <LineChart
              series={[{ 
                data,
                label: 'Ventas',
                color: '#1976d2' 
              }]}
              xAxis={[{ 
                data: labels, 
                scaleType: 'band' 
              }]}
              height={300}
              margin={{ left: 70 }}
              slotProps={{
                chart: {
                  description: 'Gráfico de ventas mensuales'
                }
              }}
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}