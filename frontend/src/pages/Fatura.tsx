import React, { useState } from 'react';
import { TextField, Button, Grid, Container, Typography } from '@mui/material';
import axios from 'axios';
import Divider from '@mui/material/Divider';
import InvoiceDataGrid from '../components/InvoiceDataGrid';
import Stack from '@mui/material/Stack';

const Fatura = () => {
  const [formData, setFormData] = useState({
    invoice_number: '',
    issue_date: '',
    operation_date: '',
    seller_name: '',
    seller_nif: '',
    seller_address: '',
    client_name: '',
    client_nif: '',
    description: '',
    quantity: '',
    unit_of_measure: '',
    unit_price: '',
    taxable_amount: '',
    vat_rate: '14.0',
    vat_amount: '',
    total_amount: '',
    payment_due_date: '',
    payment_method: '',
    authorization_number: '',
    legal_reference: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/invoices', formData);
      console.log(response.data);
      // Handle success (e.g., show a success message, clear the form, etc.)
    } catch (error) {
      console.error(error);
      // Handle error (e.g., show an error message)
    }
  };

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
    <Container>
    <InvoiceDataGrid/>
    </Container>
    </Stack>
  );
};

export default Fatura;
