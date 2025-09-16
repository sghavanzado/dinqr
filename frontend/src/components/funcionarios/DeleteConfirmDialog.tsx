import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Alert,
  Avatar,
  CircularProgress,
} from '@mui/material';
import {
  Warning as WarningIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import type { Funcionario } from '../../types/rrhh';

interface DeleteConfirmDialogProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  funcionario: Funcionario | null;
  loading?: boolean;
}

const DeleteConfirmDialog: React.FC<DeleteConfirmDialogProps> = ({
  open,
  onClose,
  onConfirm,
  funcionario,
  loading = false,
}) => {
  if (!funcionario) {
    return null;
  }

  return (
    <Dialog 
      open={open} 
      onClose={!loading ? onClose : undefined}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <WarningIcon color="error" />
          Confirmar Exclusão
        </Box>
      </DialogTitle>

      <DialogContent>
        <Alert severity="error" sx={{ mb: 3 }}>
          <strong>Atenção!</strong> Esta ação não pode ser desfeita.
        </Alert>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
          <Avatar sx={{ bgcolor: 'error.light' }}>
            <PersonIcon />
          </Avatar>
          <Box>
            <Typography variant="h6">
              {funcionario.nome}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {funcionario.apelido} • BI: {funcionario.bi}
            </Typography>
          </Box>
        </Box>

        <Typography variant="body1" paragraph>
          Tem certeza de que deseja excluir este funcionário?
        </Typography>

        <Typography variant="body2" color="text.secondary">
          Todos os dados relacionados a este funcionário serão removidos permanentemente, 
          incluindo:
        </Typography>

        <Box component="ul" sx={{ mt: 1, mb: 2 }}>
          <Typography component="li" variant="body2" color="text.secondary">
            Dados pessoais e profissionais
          </Typography>
          <Typography component="li" variant="body2" color="text.secondary">
            Histórico de presenças
          </Typography>
          <Typography component="li" variant="body2" color="text.secondary">
            Licenças e benefícios
          </Typography>
          <Typography component="li" variant="body2" color="text.secondary">
            Avaliações de desempenho
          </Typography>
          <Typography component="li" variant="body2" color="text.secondary">
            Foto e documentos anexados
          </Typography>
        </Box>
      </DialogContent>

      <DialogActions>
        <Button 
          onClick={onClose} 
          disabled={loading}
          variant="outlined"
        >
          Cancelar
        </Button>
        <Button 
          onClick={onConfirm}
          disabled={loading}
          variant="contained"
          color="error"
          startIcon={loading ? <CircularProgress size={16} /> : <WarningIcon />}
        >
          {loading ? 'Excluindo...' : 'Confirmar Exclusão'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DeleteConfirmDialog;
