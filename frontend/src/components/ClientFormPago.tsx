import * as React from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Grid from '@mui/material/Grid2';
import OutlinedInput from '@mui/material/OutlinedInput';
import { styled } from '@mui/material/styles';

const FormGrid = styled(Grid)(() => ({
  display: 'flex',
  flexDirection: 'column',
}));


export default function ClientFormPago() {

    return (
        <Grid container spacing={3}>
          <FormGrid size={{ xs: 12, md: 3 }}>
            <FormLabel htmlFor="contact_first_name" required>
             Bank Name
            </FormLabel>
            <OutlinedInput
              id="contact_first_name"
              name="contact_first_name"
              type="contact_first_name"
              placeholder="Jose"
              autoComplete="Name"
              required
              size="small"
            />
          </FormGrid>
          <FormGrid size={{ xs: 12, md: 9 }}>
            <FormLabel htmlFor="contact_last_name" required>
             IBAN
            </FormLabel>
            <OutlinedInput
              id="contact_last_name"
              name="contact_last_name"
              type="contact_last_name"
              placeholder="Pedro"
              autoComplete="Las Name"
              required
              size="small"
            />
          </FormGrid>
          
          <FormGrid size={{ xs: 12 }}>
            <FormControlLabel
              control={<Checkbox name="saveAddress" value="yes" />}
              label="details"
            />
          </FormGrid>
        </Grid>
      );
}
