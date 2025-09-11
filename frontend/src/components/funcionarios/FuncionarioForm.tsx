import React, { useState, useRef } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Avatar,
  Typography,
  IconButton,
  Divider,
  Alert,
} from '@mui/material';
import {
  PhotoCamera as PhotoCameraIcon,
  Person as PersonIcon,
  Close as CloseIcon,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import type { 
  Funcionario, 
  FuncionarioFormData,
  Departamento,
  Cargo
} from '../../types/rrhh';
import { 
  createFuncionario, 
  updateFuncionario,
  uploadFoto
} from '../../services/api/rrhh';

// Schema de validação
const funcionarioSchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório').max(100, 'Nome muito longo'),
  apelido: z.string().min(1, 'Apelido é obrigatório').max(100, 'Apelido muito longo'),
  bi: z.string().min(1, 'BI é obrigatório').max(20, 'BI muito longo'),
  dataNascimento: z.string().optional(),
  sexo: z.enum(['M', 'F', 'O']).optional(),
  estadoCivil: z.string().optional(),
  email: z.string().email('Email inválido').optional().or(z.literal('')),
  telefone: z.string().optional(),
  endereco: z.string().optional(),
  dataAdmissao: z.string().min(1, 'Data de admissão é obrigatória'),
  estadoFuncionario: z.enum(['Activo', 'Inactivo', 'Suspenso']),
  cargoID: z.number().optional(),
  departamentoID: z.number().optional(),
});

interface FuncionarioFormProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  funcionario: Funcionario | null;
  departamentos: Departamento[];
  cargos: Cargo[];
}

const FuncionarioForm: React.FC<FuncionarioFormProps> = ({
  open,
  onClose,
  onSuccess,
  funcionario,
  departamentos,
  cargos,
}) => {
  const [loading, setLoading] = useState(false);
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [photoPreview, setPhotoPreview] = useState<string>('');
  const [error, setError] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const isEdit = !!funcionario;

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
    watch,
  } = useForm<FuncionarioFormData>({
    resolver: zodResolver(funcionarioSchema),
    defaultValues: {
      nome: '',
      apelido: '',
      bi: '',
      dataNascimento: '',
      sexo: undefined,
      estadoCivil: '',
      email: '',
      telefone: '',
      endereco: '',
      dataAdmissao: new Date().toISOString().split('T')[0],
      estadoFuncionario: 'Activo',
      cargoID: undefined,
      departamentoID: undefined,
    },
  });

  const selectedDepartamentoID = watch('departamentoID');

  React.useEffect(() => {
    if (open) {
      if (funcionario) {
        reset({
          nome: funcionario.nome,
          apelido: funcionario.apelido,
          bi: funcionario.bi,
          dataNascimento: funcionario.dataNascimento || '',
          sexo: funcionario.sexo,
          estadoCivil: funcionario.estadoCivil || '',
          email: funcionario.email || '',
          telefone: funcionario.telefone || '',
          endereco: funcionario.endereco || '',
          dataAdmissao: funcionario.dataAdmissao,
          estadoFuncionario: funcionario.estadoFuncionario,
          cargoID: funcionario.cargoID,
          departamentoID: funcionario.departamentoID,
        });
        setPhotoPreview(funcionario.foto || '');
      } else {
        reset({
          nome: '',
          apelido: '',
          bi: '',
          dataNascimento: '',
          sexo: undefined,
          estadoCivil: '',
          email: '',
          telefone: '',
          endereco: '',
          dataAdmissao: new Date().toISOString().split('T')[0],
          estadoFuncionario: 'Activo',
          cargoID: undefined,
          departamentoID: undefined,
        });
        setPhotoPreview('');
      }
      setPhotoFile(null);
      setError('');
    }
  }, [open, funcionario, reset]);

  const handlePhotoChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validar tipo e tamanho do arquivo
      if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
        setError('Apenas arquivos JPG e PNG são permitidos');
        return;
      }

      if (file.size > 2 * 1024 * 1024) { // 2MB
        setError('O arquivo deve ter no máximo 2MB');
        return;
      }

      setPhotoFile(file);
      
      // Criar preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPhotoPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
      setError('');
    }
  };

  const handleRemovePhoto = () => {
    setPhotoFile(null);
    setPhotoPreview('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const onSubmit = async (data: FuncionarioFormData) => {
    try {
      setLoading(true);
      setError('');

      let response;
      if (isEdit && funcionario) {
        response = await updateFuncionario(funcionario.funcionarioID, data);
      } else {
        response = await createFuncionario(data);
      }

      if (response.success && response.data) {
        // Upload da foto se foi selecionada
        if (photoFile) {
          try {
            await uploadFoto(response.data.funcionarioID, photoFile);
          } catch (photoError) {
            console.error('Erro ao fazer upload da foto:', photoError);
            // Não bloqueamos a operação por erro na foto
          }
        }

        onSuccess();
      } else {
        setError(response.message || 'Erro ao salvar funcionário');
      }
    } catch (error: any) {
      setError(error.response?.data?.message || 'Erro ao salvar funcionário');
    } finally {
      setLoading(false);
    }
  };

  const filteredCargos = selectedDepartamentoID 
    ? cargos.filter(cargo => cargo.departamentoID === selectedDepartamentoID)
    : cargos;

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
            {isEdit ? 'Editar Funcionário' : 'Adicionar Funcionário'}
          </Typography>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent dividers>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* Foto */}
          <Box sx={{ mb: 3, textAlign: 'center' }}>
            <Typography variant="subtitle1" gutterBottom>
              Foto Tipo Visa *
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <Avatar
                src={photoPreview}
                sx={{ 
                  width: 120, 
                  height: 150, 
                  borderRadius: 2,
                  mb: 2,
                  border: '2px dashed',
                  borderColor: 'grey.300',
                }}
              >
                <PersonIcon sx={{ fontSize: 48 }} />
              </Avatar>
              
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="outlined"
                  startIcon={<PhotoCameraIcon />}
                  onClick={() => fileInputRef.current?.click()}
                  size="small"
                >
                  Selecionar Foto
                </Button>
                {photoPreview && (
                  <Button
                    variant="outlined"
                    color="error"
                    onClick={handleRemovePhoto}
                    size="small"
                  >
                    Remover
                  </Button>
                )}
              </Box>
              
              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept="image/jpeg,image/png,image/jpg"
                onChange={handlePhotoChange}
              />
              
              <Typography variant="caption" color="textSecondary" sx={{ mt: 1 }}>
                Formatos: JPG, PNG | Tamanho máximo: 2MB
              </Typography>
            </Box>
          </Box>

          <Divider sx={{ mb: 3 }} />

          {/* Dados Pessoais */}
          <Typography variant="h6" gutterBottom>
            Dados Pessoais
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6}>
              <Controller
                name="nome"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Nome *"
                    error={!!errors.nome}
                    helperText={errors.nome?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="apelido"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Apelido *"
                    error={!!errors.apelido}
                    helperText={errors.apelido?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="bi"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="BI/NIF *"
                    error={!!errors.bi}
                    helperText={errors.bi?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="dataNascimento"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Data de Nascimento"
                    type="date"
                    InputLabelProps={{ shrink: true }}
                    error={!!errors.dataNascimento}
                    helperText={errors.dataNascimento?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="sexo"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Sexo</InputLabel>
                    <Select
                      {...field}
                      label="Sexo"
                      value={field.value || ''}
                    >
                      <MenuItem value="">Não especificar</MenuItem>
                      <MenuItem value="M">Masculino</MenuItem>
                      <MenuItem value="F">Feminino</MenuItem>
                      <MenuItem value="O">Outro</MenuItem>
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="estadoCivil"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Estado Civil</InputLabel>
                    <Select
                      {...field}
                      label="Estado Civil"
                      value={field.value || ''}
                    >
                      <MenuItem value="">Não especificar</MenuItem>
                      <MenuItem value="Solteiro">Solteiro</MenuItem>
                      <MenuItem value="Casado">Casado</MenuItem>
                      <MenuItem value="Divorciado">Divorciado</MenuItem>
                      <MenuItem value="Viúvo">Viúvo</MenuItem>
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
          </Grid>

          <Divider sx={{ mb: 3 }} />

          {/* Contacto */}
          <Typography variant="h6" gutterBottom>
            Contacto
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6}>
              <Controller
                name="telefone"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Telefone"
                    error={!!errors.telefone}
                    helperText={errors.telefone?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="email"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Email"
                    type="email"
                    error={!!errors.email}
                    helperText={errors.email?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12}>
              <Controller
                name="endereco"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Endereço"
                    multiline
                    rows={2}
                    error={!!errors.endereco}
                    helperText={errors.endereco?.message}
                  />
                )}
              />
            </Grid>
          </Grid>

          <Divider sx={{ mb: 3 }} />

          {/* Dados Profissionais */}
          <Typography variant="h6" gutterBottom>
            Dados Profissionais
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Controller
                name="departamentoID"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Departamento</InputLabel>
                    <Select
                      {...field}
                      label="Departamento"
                      value={field.value || ''}
                      onChange={(e) => {
                        field.onChange(e.target.value ? Number(e.target.value) : undefined);
                        // Reset cargo when department changes
                        // setValue('cargoID', undefined);
                      }}
                    >
                      <MenuItem value="">Nenhum</MenuItem>
                      {departamentos.map((dept) => (
                        <MenuItem key={dept.departamentoID} value={dept.departamentoID}>
                          {dept.nome}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="cargoID"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Cargo</InputLabel>
                    <Select
                      {...field}
                      label="Cargo"
                      value={field.value || ''}
                      onChange={(e) => field.onChange(e.target.value ? Number(e.target.value) : undefined)}
                    >
                      <MenuItem value="">Nenhum</MenuItem>
                      {filteredCargos.map((cargo) => (
                        <MenuItem key={cargo.cargoID} value={cargo.cargoID}>
                          {cargo.nome}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="dataAdmissao"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Data de Admissão *"
                    type="date"
                    InputLabelProps={{ shrink: true }}
                    error={!!errors.dataAdmissao}
                    helperText={errors.dataAdmissao?.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Controller
                name="estadoFuncionario"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth>
                    <InputLabel>Estado</InputLabel>
                    <Select
                      {...field}
                      label="Estado"
                      error={!!errors.estadoFuncionario}
                    >
                      <MenuItem value="Activo">Activo</MenuItem>
                      <MenuItem value="Inactivo">Inactivo</MenuItem>
                      <MenuItem value="Suspenso">Suspenso</MenuItem>
                    </Select>
                  </FormControl>
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>

        <DialogActions sx={{ p: 2 }}>
          <Button onClick={onClose} disabled={loading}>
            Cancelar
          </Button>
          <Button 
            type="submit" 
            variant="contained"
            disabled={loading}
          >
            {loading ? 'Salvando...' : (isEdit ? 'Salvar' : 'Criar')}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default FuncionarioForm;
