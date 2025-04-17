import { FormLabel, Stack, Typography } from '@mui/material';
import { ReactNode } from 'react';

export const FormGroup = ({ children }: { children: ReactNode }) => (
  <Stack spacing={1} sx={{ width: '100%' }}>{children}</Stack>
);

export const Label = ({ required, children }: { required?: boolean; children: ReactNode }) => (
  <FormLabel required={required} sx={{ fontWeight: 500, fontSize: '0.875rem' }}>
    {children}
  </FormLabel>
);

export const ErrorText = ({ children }: { children: ReactNode }) => (
  <Typography variant="caption" color="error" sx={{ mt: 0.5 }}>
    {children}
  </Typography>
);