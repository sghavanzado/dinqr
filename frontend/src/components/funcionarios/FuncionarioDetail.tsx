import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Box,
  Avatar,
  Typography,
  IconButton,
  Card,
  CardContent,
  Chip,
  Divider,
} from '@mui/material';
import {
  Close as CloseIcon,
  Person as PersonIcon,
  Edit as EditIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  LocationOn as LocationIcon,
  Business as BusinessIcon,
  Work as WorkIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import type { 
  Funcionario,
  Departamento,
  Cargo
} from '../../types/rrhh';

interface FuncionarioDetailProps {
  open: boolean;
  onClose: () => void;
  funcionario: Funcionario | null;
  departamentos: Departamento[];
  cargos: Cargo[];
  onEdit?: (funcionario: Funcionario) => void;
}

const FuncionarioDetail: React.FC<FuncionarioDetailProps> = ({
  open,
  onClose,
  funcionario,
  departamentos,
  cargos,
  onEdit,
}) => {
  if (!funcionario) return null;

  const getDepartamentoNome = (departamentoID?: number) => {
    const dept = departamentos.find(d => d.departamentoID === departamentoID);
    return dept?.nome || 'Não definido';
  };

  const getCargoNome = (cargoID?: number) => {
    const cargo = cargos.find(c => c.cargoID === cargoID);
    return cargo?.nome || 'Não definido';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Activo': return 'success';
      case 'Inactivo': return 'error';
      case 'Suspenso': return 'warning';
      default: return 'default';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Não informado';
    return new Date(dateString).toLocaleDateString('pt-AO');
  };

  const getSexoLabel = (sexo?: string) => {
    switch (sexo) {
      case 'M': return 'Masculino';
      case 'F': return 'Feminino';
      case 'O': return 'Outro';
      default: return 'Não informado';
    }
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: { minHeight: '70vh' }
      }}
    >
      <DialogTitle sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">
            Detalhes do Funcionário
          </Typography>
          <Box sx={{ display: 'flex', gap: 1 }}>
            {onEdit && (
              <IconButton onClick={() => onEdit(funcionario)} size="small">
                <EditIcon />
              </IconButton>
            )}
            <IconButton onClick={onClose} size="small">
              <CloseIcon />
            </IconButton>
          </Box>
        </Box>
      </DialogTitle>

      <DialogContent dividers>
        {/* Header com foto e dados principais */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Grid container spacing={3} alignItems="center">
              <Grid item>
                <Avatar
                  src={funcionario.foto}
                  sx={{ 
                    width: 120, 
                    height: 150, 
                    borderRadius: 2,
                    border: '1px solid',
                    borderColor: 'grey.300',
                  }}
                >
                  <PersonIcon sx={{ fontSize: 48 }} />
                </Avatar>
              </Grid>
              <Grid item xs>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="h4" component="h2" gutterBottom>
                    {funcionario.nome} {funcionario.apelido}
                  </Typography>
                  <Chip
                    label={funcionario.estadoFuncionario}
                    color={getStatusColor(funcionario.estadoFuncionario) as any}
                    sx={{ mb: 1 }}
                  />
                </Box>
                
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <BusinessIcon sx={{ mr: 1, color: 'text.secondary' }} />
                      <Typography>
                        <strong>Departamento:</strong> {getDepartamentoNome(funcionario.departamentoID)}
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <WorkIcon sx={{ mr: 1, color: 'text.secondary' }} />
                      <Typography>
                        <strong>Cargo:</strong> {getCargoNome(funcionario.cargoID)}
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <CalendarIcon sx={{ mr: 1, color: 'text.secondary' }} />
                      <Typography>
                        <strong>Admissão:</strong> {formatDate(funcionario.dataAdmissao)}
                      </Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Typography>
                      <strong>BI/NIF:</strong> {funcionario.bi}
                    </Typography>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Dados Pessoais */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Dados Pessoais
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">Data de Nascimento</Typography>
                <Typography variant="body1">{formatDate(funcionario.dataNascimento)}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">Sexo</Typography>
                <Typography variant="body1">{getSexoLabel(funcionario.sexo)}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">Estado Civil</Typography>
                <Typography variant="body1">{funcionario.estadoCivil || 'Não informado'}</Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Contacto */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Contacto
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <PhoneIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Box>
                    <Typography variant="body2" color="text.secondary">Telefone</Typography>
                    <Typography variant="body1">{funcionario.telefone || 'Não informado'}</Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <EmailIcon sx={{ mr: 1, color: 'text.secondary' }} />
                  <Box>
                    <Typography variant="body2" color="text.secondary">Email</Typography>
                    <Typography variant="body1">{funcionario.email || 'Não informado'}</Typography>
                  </Box>
                </Box>
              </Grid>
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
                  <LocationIcon sx={{ mr: 1, color: 'text.secondary', mt: 0.5 }} />
                  <Box>
                    <Typography variant="body2" color="text.secondary">Endereço</Typography>
                    <Typography variant="body1">
                      {funcionario.endereco || 'Não informado'}
                    </Typography>
                  </Box>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Dados Profissionais */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Dados Profissionais
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">Departamento</Typography>
                <Typography variant="body1">{getDepartamentoNome(funcionario.departamentoID)}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">Cargo</Typography>
                <Typography variant="body1">{getCargoNome(funcionario.cargoID)}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">Data de Admissão</Typography>
                <Typography variant="body1">{formatDate(funcionario.dataAdmissao)}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">Estado</Typography>
                <Chip
                  label={funcionario.estadoFuncionario}
                  color={getStatusColor(funcionario.estadoFuncionario) as any}
                  size="small"
                />
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Informações do Sistema */}
        {(funcionario.createdAt || funcionario.updatedAt) && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Informações do Sistema
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Grid container spacing={2}>
                {funcionario.createdAt && (
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary">Criado em</Typography>
                    <Typography variant="body1">{formatDate(funcionario.createdAt)}</Typography>
                  </Grid>
                )}
                {funcionario.updatedAt && (
                  <Grid item xs={12} sm={6}>
                    <Typography variant="body2" color="text.secondary">Última atualização</Typography>
                    <Typography variant="body1">{formatDate(funcionario.updatedAt)}</Typography>
                  </Grid>
                )}
              </Grid>
            </CardContent>
          </Card>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 2 }}>
        {onEdit && (
          <Button 
            variant="outlined"
            startIcon={<EditIcon />}
            onClick={() => onEdit(funcionario)}
          >
            Editar
          </Button>
        )}
        <Button onClick={onClose}>
          Fechar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default FuncionarioDetail;
