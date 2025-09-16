import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Typography,
  Box,
  Card,
  CardContent,
  Avatar,
  Chip,
  Divider,
  IconButton,
  Alert,
} from '@mui/material';
import {
  Person as PersonIcon,
  Edit as EditIcon,
  Close as CloseIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  Home as HomeIcon,
  Work as WorkIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import type { Funcionario, Departamento, Cargo } from '../../types/rrhh';
import { getFotoInfo } from '../../services/api/funcionarios';

interface FuncionarioViewDialogProps {
  open: boolean;
  onClose: () => void;
  onEdit?: () => void;
  funcionario: Funcionario | null;
  departamentos: Departamento[];
  cargos: Cargo[];
}

const FuncionarioViewDialog: React.FC<FuncionarioViewDialogProps> = ({
  open,
  onClose,
  onEdit,
  funcionario,
  departamentos,
  cargos,
}) => {
  const [fotoUrl, setFotoUrl] = useState<string>('');

  useEffect(() => {
    if (funcionario?.foto) {
      loadFoto(funcionario.funcionarioID);
    } else {
      setFotoUrl('');
    }
  }, [funcionario]);

  const loadFoto = async (funcionarioID: number) => {
    try {
      const response = await getFotoInfo(funcionarioID);
      if (response.success && response.data) {
        setFotoUrl(response.data.foto_url);
      }
    } catch (error) {
      console.error('Erro ao carregar foto:', error);
    }
  };

  if (!funcionario) {
    return null;
  }

  const departamento = departamentos.find(d => d.departamentoID === funcionario.departamentoID);
  const cargo = cargos.find(c => c.cargoID === funcionario.cargoID);

  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'Activo':
        return 'success';
      case 'Inactivo':
        return 'error';
      case 'Suspenso':
        return 'warning';
      default:
        return 'default';
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '-';
    try {
      return new Date(dateStr).toLocaleDateString('pt-BR');
    } catch {
      return dateStr;
    }
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <PersonIcon />
            Detalhes do Funcionário
          </Box>
          <Box>
            {onEdit && (
              <IconButton onClick={onEdit} color="primary">
                <EditIcon />
              </IconButton>
            )}
            <IconButton onClick={onClose}>
              <CloseIcon />
            </IconButton>
          </Box>
        </Box>
      </DialogTitle>

      <DialogContent dividers>
        <Grid container spacing={3}>
          {/* Header com foto e informações básicas */}
          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                  <Avatar
                    src={fotoUrl}
                    sx={{ width: 120, height: 120 }}
                  >
                    <PersonIcon sx={{ fontSize: 60 }} />
                  </Avatar>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="h4" gutterBottom>
                      {funcionario.nome}
                    </Typography>
                    <Typography variant="h6" color="text.secondary" gutterBottom>
                      {funcionario.apelido}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                      <Chip 
                        label={funcionario.estadoFuncionario}
                        color={getEstadoColor(funcionario.estadoFuncionario) as any}
                        size="small"
                      />
                      {cargo && (
                        <Chip 
                          label={cargo.nome}
                          variant="outlined"
                          size="small"
                          icon={<WorkIcon />}
                        />
                      )}
                      {departamento && (
                        <Chip 
                          label={departamento.nome}
                          variant="outlined"
                          size="small"
                        />
                      )}
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      <strong>BI:</strong> {funcionario.bi}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      <strong>Data de Admissão:</strong> {formatDate(funcionario.dataAdmissao)}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Dados Pessoais */}
          <Grid item xs={12} md={6}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <PersonIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Dados Pessoais
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Data de Nascimento
                  </Typography>
                  <Typography variant="body1">
                    {formatDate(funcionario.dataNascimento || '')}
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Sexo
                  </Typography>
                  <Typography variant="body1">
                    {funcionario.sexo === 'M' ? 'Masculino' : 
                     funcionario.sexo === 'F' ? 'Feminino' : 
                     funcionario.sexo === 'O' ? 'Outro' : '-'}
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    Estado Civil
                  </Typography>
                  <Typography variant="body1">
                    {funcionario.estadoCivil || '-'}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Informações de Contato */}
          <Grid item xs={12} md={6}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <EmailIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Contato
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    <EmailIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                    Email
                  </Typography>
                  <Typography variant="body1">
                    {funcionario.email || '-'}
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    <PhoneIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                    Telefone
                  </Typography>
                  <Typography variant="body1">
                    {funcionario.telefone || '-'}
                  </Typography>
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    <HomeIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                    Endereço
                  </Typography>
                  <Typography variant="body1">
                    {funcionario.endereco || '-'}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Informações Profissionais */}
          <Grid item xs={12}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <WorkIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Informações Profissionais
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        <CalendarIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'middle' }} />
                        Data de Admissão
                      </Typography>
                      <Typography variant="body1">
                        {formatDate(funcionario.dataAdmissao)}
                      </Typography>
                    </Box>
                  </Grid>

                  <Grid item xs={12} sm={4}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Departamento
                      </Typography>
                      <Typography variant="body1">
                        {departamento?.nome || '-'}
                      </Typography>
                      {departamento?.descricao && (
                        <Typography variant="caption" color="text.secondary">
                          {departamento.descricao}
                        </Typography>
                      )}
                    </Box>
                  </Grid>

                  <Grid item xs={12} sm={4}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">
                        Cargo
                      </Typography>
                      <Typography variant="body1">
                        {cargo?.nome || '-'}
                      </Typography>
                      {cargo?.descricao && (
                        <Typography variant="caption" color="text.secondary">
                          {cargo.descricao}
                        </Typography>
                      )}
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>

          {/* Informações do Sistema */}
          <Grid item xs={12}>
            <Alert severity="info" sx={{ mt: 1 }}>
              <Typography variant="body2">
                <strong>ID do Sistema:</strong> {funcionario.funcionarioID} | 
                <strong> ID da Tabela:</strong> {funcionario.id}
                {funcionario.createdAt && (
                  <> | <strong> Criado em:</strong> {formatDate(funcionario.createdAt)}</>
                )}
                {funcionario.updatedAt && (
                  <> | <strong> Atualizado em:</strong> {formatDate(funcionario.updatedAt)}</>
                )}
              </Typography>
            </Alert>
          </Grid>
        </Grid>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>
          Fechar
        </Button>
        {onEdit && (
          <Button 
            variant="contained" 
            startIcon={<EditIcon />}
            onClick={onEdit}
          >
            Editar
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default FuncionarioViewDialog;
