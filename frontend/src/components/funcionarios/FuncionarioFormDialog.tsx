import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Typography,
  Box,
  Alert,
  Divider,
  Avatar,
  IconButton,
  CircularProgress,
} from '@mui/material';
import {
  PhotoCamera as PhotoCameraIcon,
  Delete as DeleteIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import type { 
  Funcionario, 
  FuncionarioFormData, 
  Departamento, 
  Cargo 
} from '../../types/rrhh';
import { 
  createFuncionario, 
  updateFuncionario, 
  uploadFoto, 
  deleteFoto,
  getFotoInfo 
} from '../../services/api/funcionarios';

interface FuncionarioFormDialogProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
  funcionario?: Funcionario | null;
  departamentos: Departamento[];
  cargos: Cargo[];
}

const FuncionarioFormDialog: React.FC<FuncionarioFormDialogProps> = ({
  open,
  onClose,
  onSuccess,
  funcionario,
  departamentos,
  cargos,
}) => {
  const [formData, setFormData] = useState<FuncionarioFormData>({
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

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [fotoUrl, setFotoUrl] = useState<string>('');
  const [fotoFile, setFotoFile] = useState<File | null>(null);
  const [uploadingFoto, setUploadingFoto] = useState(false);

  const isEdit = !!funcionario;

  useEffect(() => {
    if (funcionario) {
      // Mapear dados do backend (PascalCase) para frontend (camelCase)
      setFormData({
        nome: funcionario.Nome || funcionario.nome || '',
        apelido: funcionario.Apelido || funcionario.apelido || '',
        bi: funcionario.BI || funcionario.bi || '',
        dataNascimento: funcionario.DataNascimento || funcionario.dataNascimento || '',
        sexo: funcionario.Sexo || funcionario.sexo,
        estadoCivil: funcionario.EstadoCivil || funcionario.estadoCivil || '',
        email: funcionario.Email || funcionario.email || '',
        telefone: funcionario.Telefone || funcionario.telefone || '',
        endereco: funcionario.Endereco || funcionario.endereco || '',
        dataAdmissao: funcionario.DataAdmissao || funcionario.dataAdmissao || '',
        estadoFuncionario: funcionario.EstadoFuncionario || funcionario.estadoFuncionario || 'Activo',
        cargoID: funcionario.CargoID || funcionario.cargoID,
        departamentoID: funcionario.DepartamentoID || funcionario.departamentoID,
      });

      // Carregar foto se existir
      const funcionarioId = funcionario.FuncionarioID || funcionario.funcionarioID;
      const fotoPath = funcionario.Foto || funcionario.foto;
      if (fotoPath && funcionarioId) {
        loadFoto(funcionarioId);
      }
    } else {
      // Reset form for new funcionario
      setFormData({
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
      setFotoUrl('');
      setFotoFile(null);
    }
    setErrors({});
  }, [funcionario, open]);

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

  const handleInputChange = (field: keyof FuncionarioFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handleFotoChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFotoFile(file);
      // Preview da imagem
      const reader = new FileReader();
      reader.onload = (e) => {
        setFotoUrl(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUploadFoto = async () => {
    if (!fotoFile || !funcionario) return;

    try {
      setUploadingFoto(true);
      const funcionarioId = funcionario.funcionarioID || funcionario.FuncionarioID || funcionario.id;
      const response = await uploadFoto(funcionarioId, fotoFile);
      if (response.success) {
        setFotoFile(null);
        await loadFoto(funcionarioId);
      }
    } catch (error) {
      console.error('Erro ao fazer upload da foto:', error);
    } finally {
      setUploadingFoto(false);
    }
  };

  const handleDeleteFoto = async () => {
    if (!funcionario) return;

    try {
      const funcionarioId = funcionario.funcionarioID || funcionario.FuncionarioID || funcionario.id;
      const response = await deleteFoto(funcionarioId);
      if (response.success) {
        setFotoUrl('');
        setFotoFile(null);
      }
    } catch (error) {
      console.error('Erro ao deletar foto:', error);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.nome) newErrors.nome = 'Nome é obrigatório';
    if (!formData.apelido) newErrors.apelido = 'Apelido é obrigatório';
    if (!formData.bi) newErrors.bi = 'BI é obrigatório';
    if (!formData.dataAdmissao) newErrors.dataAdmissao = 'Data de admissão é obrigatória';

    // Validar email se fornecido
    if (formData.email && !/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    if (!validateForm()) return;

    try {
      setLoading(true);
      
      let response;
      if (isEdit && funcionario) {
        // Para edición, usar el ID correcto (puede ser FuncionarioID o funcionarioID)
        const funcionarioId = funcionario.funcionarioID || funcionario.FuncionarioID || funcionario.id;
        response = await updateFuncionario(funcionarioId, formData as any);
      } else {
        // Para creación, usar los campos tal como están en formData
        response = await createFuncionario(formData as any);
      }

      if (response.success) {
        // Se há foto para upload e é um novo funcionário ou edição bem-sucedida
        if (fotoFile && response.data) {
          const funcionarioId = response.data.funcionarioID || response.data.FuncionarioID || response.data.id;
          await uploadFoto(funcionarioId, fotoFile);
        }

        onSuccess();
        onClose();
      }
    } catch (error) {
      console.error('Erro ao salvar funcionário:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      onClose();
    }
  };

  return (
    <Dialog 
      open={open} 
      onClose={handleClose}
      maxWidth="md"
        fullWidth
        disableEscapeKeyDown={loading}
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <PersonIcon />
            {isEdit ? 'Editar Funcionário' : 'Novo Funcionário'}
          </Box>
        </DialogTitle>

        <form onSubmit={handleSubmit}>
          <DialogContent dividers>
            <Grid container spacing={3}>
              {/* Foto Section */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Foto do Funcionário
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Avatar
                    src={fotoUrl}
                    sx={{ width: 100, height: 100 }}
                  >
                    <PersonIcon sx={{ fontSize: 40 }} />
                  </Avatar>
                  <Box>
                    <input
                      accept="image/*"
                      style={{ display: 'none' }}
                      id="foto-upload"
                      type="file"
                      onChange={handleFotoChange}
                    />
                    <label htmlFor="foto-upload">
                      <IconButton color="primary" component="span">
                        <PhotoCameraIcon />
                      </IconButton>
                    </label>
                    {fotoUrl && (
                      <IconButton color="error" onClick={handleDeleteFoto}>
                        <DeleteIcon />
                      </IconButton>
                    )}
                    {fotoFile && isEdit && (
                      <Button
                        size="small"
                        onClick={handleUploadFoto}
                        disabled={uploadingFoto}
                      >
                        {uploadingFoto ? <CircularProgress size={20} /> : 'Upload'}
                      </Button>
                    )}
                  </Box>
                </Box>
                <Divider sx={{ my: 2 }} />
              </Grid>

              {/* Dados Pessoais */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                  Dados Pessoais
                </Typography>
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Nome *"
                  value={formData.nome}
                  onChange={(e) => handleInputChange('nome', e.target.value)}
                  error={!!errors.nome}
                  helperText={errors.nome}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Apelido *"
                  value={formData.apelido}
                  onChange={(e) => handleInputChange('apelido', e.target.value)}
                  error={!!errors.apelido}
                  helperText={errors.apelido}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="BI *"
                  value={formData.bi}
                  onChange={(e) => handleInputChange('bi', e.target.value)}
                  error={!!errors.bi}
                  helperText={errors.bi}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Data de Nascimento"
                  type="date"
                  value={formData.dataNascimento || ''}
                  onChange={(e) => handleInputChange('dataNascimento', e.target.value)}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Sexo</InputLabel>
                  <Select
                    value={formData.sexo || ''}
                    label="Sexo"
                    onChange={(e) => handleInputChange('sexo', e.target.value || undefined)}
                  >
                    <MenuItem value="">
                      <em>Selecionar</em>
                    </MenuItem>
                    <MenuItem value="M">Masculino</MenuItem>
                    <MenuItem value="F">Feminino</MenuItem>
                    <MenuItem value="O">Outro</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={8}>
                <TextField
                  fullWidth
                  label="Estado Civil"
                  value={formData.estadoCivil}
                  onChange={(e) => handleInputChange('estadoCivil', e.target.value)}
                />
              </Grid>

              {/* Contato */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                  Informações de Contato
                </Typography>
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  error={!!errors.email}
                  helperText={errors.email}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Telefone"
                  value={formData.telefone}
                  onChange={(e) => handleInputChange('telefone', e.target.value)}
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Endereço"
                  multiline
                  rows={2}
                  value={formData.endereco}
                  onChange={(e) => handleInputChange('endereco', e.target.value)}
                />
              </Grid>

              {/* Dados Profissionais */}
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                  Dados Profissionais
                </Typography>
              </Grid>

              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label="Data de Admissão *"
                  type="date"
                  value={formData.dataAdmissao || ''}
                  onChange={(e) => handleInputChange('dataAdmissao', e.target.value)}
                  error={!!errors.dataAdmissao}
                  helperText={errors.dataAdmissao}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Departamento</InputLabel>
                  <Select
                    value={formData.departamentoID || ''}
                    label="Departamento"
                    onChange={(e) => handleInputChange('departamentoID', e.target.value ? Number(e.target.value) : undefined)}
                  >
                    <MenuItem value="">
                      <em>Selecionar</em>
                    </MenuItem>
                    {departamentos.map((dept) => (
                      <MenuItem key={dept.departamentoID} value={dept.departamentoID}>
                        {dept.nome}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Cargo</InputLabel>
                  <Select
                    value={formData.cargoID || ''}
                    label="Cargo"
                    onChange={(e) => handleInputChange('cargoID', e.target.value ? Number(e.target.value) : undefined)}
                  >
                    <MenuItem value="">
                      <em>Selecionar</em>
                    </MenuItem>
                    {cargos.map((cargo) => (
                      <MenuItem key={cargo.cargoID} value={cargo.cargoID}>
                        {cargo.nome}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel>Estado do Funcionário</InputLabel>
                  <Select
                    value={formData.estadoFuncionario}
                    label="Estado do Funcionário"
                    onChange={(e) => handleInputChange('estadoFuncionario', e.target.value)}
                  >
                    <MenuItem value="Activo">Activo</MenuItem>
                    <MenuItem value="Inactivo">Inactivo</MenuItem>
                    <MenuItem value="Suspenso">Suspenso</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            {Object.keys(errors).length > 0 && (
              <Alert severity="error" sx={{ mt: 2 }}>
                Por favor, corrija os erros no formulário.
              </Alert>
            )}
          </DialogContent>

          <DialogActions>
            <Button onClick={handleClose} disabled={loading}>
              Cancelar
            </Button>
            <Button 
              type="submit" 
              variant="contained" 
              disabled={loading}
            >
              {loading ? <CircularProgress size={20} /> : (isEdit ? 'Atualizar' : 'Criar')}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
  );
};

export default FuncionarioFormDialog;
