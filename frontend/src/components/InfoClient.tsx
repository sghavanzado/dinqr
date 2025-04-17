import * as React from 'react';
import Typography from '@mui/material/Typography';

export default function InfoClient() {
  return (
    <React.Fragment>
      <Typography variant="h6" sx={{ fontWeight: "bold" }}>
      Adicionar novo cliente
      </Typography>
      <Typography variant="subtitle2" sx={{ color: "text.secondary" }}>
      Preencher o formulário
      </Typography>
      <Typography variant="body2" sx={{ mt: 1, color: "text.secondary" }}>
        Preencha corretamente o formulário com nome, NIF, endereço, contato e dados bancários.
        Verifique antes de enviar para evitar erros.
      </Typography>
    </React.Fragment>
  );
}
