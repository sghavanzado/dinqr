import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Tabs,
  Tab,
  Switch,
  FormControlLabel,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  Alert,
  Snackbar,
  IconButton,
  Tooltip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Palette as PaletteIcon,
  Settings as SettingsIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import type { 
  TemaAvancado, 
  FormatoAvancado, 
  ConfiguracaoAvancada
} from '../../services/api/passesConfigTypes';
import {
  configuracaoAvancadaService,
  temasAvancadosService,
  formatosAvancadosService,
  passesConfigUtils,
  MEDIDAS_PADRAO
} from '../../services/api/passesConfig';
import CardDesigner from '../../components/CardDesigner';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`config-tabpanel-${index}`}
      aria-labelledby={`config-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `config-tab-${index}`,
    'aria-controls': `config-tabpanel-${index}`,
  };
}

const PassesConfigSimple: React.FC = () => {
  // Estados principais
  const [tabAtiva, setTabAtiva] = useState(0);
  const [temas, setTemas] = useState<TemaAvancado[]>([]);
  const [formatos, setFormatos] = useState<FormatoAvancado[]>([]);
  const [configuracao, setConfiguracao] = useState<ConfiguracaoAvancada | null>(null);
  const [loading, setLoading] = useState(true);

  // Estados para dialogs
  const [dialogTemaAberto, setDialogTemaAberto] = useState(false);
  const [dialogFormatoAberto, setDialogFormatoAberto] = useState(false);
  const [temaEditando, setTemaEditando] = useState<TemaAvancado | null>(null);
  const [formatoEditando, setFormatoEditando] = useState<FormatoAvancado | null>(null);
  const [designerAberto, setDesignerAberto] = useState(false);
  const [abaTemaAtiva, setAbaTemaAtiva] = useState(0); // 0 = manual, 1 = designer

  // Estados para notificações
  const [snackbar, setSnackbar] = useState({
    aberto: false,
    mensagem: '',
    tipo: 'success' as 'success' | 'error' | 'warning' | 'info'
  });

  // Formulários
  const [formTema, setFormTema] = useState<Partial<TemaAvancado>>({
    nome: '',
    cor_primaria: '#1976d2',
    cor_secundaria: '#ffffff',
    cor_texto: '#000000',
    cor_borda: '#cccccc',
    layout_tipo: 'horizontal',
    margem_superior: 5.0,
    margem_inferior: 5.0,
    margem_esquerda: 5.0,
    margem_direita: 5.0,
    fonte_titulo: 'Helvetica-Bold',
    tamanho_fonte_titulo: 12,
    fonte_nome: 'Helvetica-Bold',
    tamanho_fonte_nome: 10,
    fonte_cargo: 'Helvetica',
    tamanho_fonte_cargo: 8,
    fonte_info: 'Helvetica',
    tamanho_fonte_info: 7,
    mostrar_logo: true,
    posicao_logo: 'superior_esquerda',
    tamanho_logo: 15.0,
    mostrar_qr_borda: true,
    qr_tamanho: 20.0,
    qr_posicao: 'direita',
    fundo_tipo: 'solido',
    fundo_cor: '#ffffff',
    fundo_cor_gradiente: '#f0f0f0',
    fundo_imagem_url: '',
    fundo_opacidade: 1.0,
    ativo: true
  });

  const [formFormato, setFormFormato] = useState<Partial<FormatoAvancado>>({
    nome: '',
    extensao: 'pdf',
    descricao: '',
    largura: 85.6,
    altura: 53.98,
    dpi: 300,
    orientacao: 'horizontal',
    qualidade: 95,
    compressao: false,
    ativo: true
  });

  // Efeitos
  useEffect(() => {
    carregarDados();
  }, []);

  // Funções de carregamento
  const carregarDados = async () => {
    setLoading(true);
    try {
      console.log('Iniciando carregamento de dados...');
      
      const temasData = await temasAvancadosService.listar();
      const formatosData = await formatosAvancadosService.listar();
      const configData = await configuracaoAvancadaService.obter();

      setTemas(temasData.temas || []);
      setFormatos(formatosData.formatos || []);
      setConfiguracao(configData);
      
      mostrarSnackbar('Configurações carregadas com sucesso!', 'success');
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      
      let mensagemErro = 'Erro ao carregar configurações';
      if (error instanceof Error) {
        if (error.message.includes('<!doctype')) {
          mensagemErro = 'Erro de servidor: a API não está respondendo corretamente. Verifique se o backend está funcionando.';
        } else {
          mensagemErro = `Erro: ${error.message}`;
        }
      }
      
      mostrarSnackbar(mensagemErro, 'error');
    } finally {
      setLoading(false);
    }
  };

  // Funções utilitárias
  const mostrarSnackbar = (mensagem: string, tipo: 'success' | 'error' | 'warning' | 'info') => {
    setSnackbar({ aberto: true, mensagem, tipo });
  };

  const fecharSnackbar = () => {
    setSnackbar({ ...snackbar, aberto: false });
  };

  // Funções para temas
  const abrirDialogTema = (tema?: TemaAvancado) => {
    if (tema) {
      setTemaEditando(tema);
      setFormTema(tema);
    } else {
      setTemaEditando(null);
      setFormTema({
        nome: '',
        cor_primaria: '#1976d2',
        cor_secundaria: '#ffffff',
        cor_texto: '#000000',
        cor_borda: '#cccccc',
        layout_tipo: 'horizontal',
        margem_superior: 5.0,
        margem_inferior: 5.0,
        margem_esquerda: 5.0,
        margem_direita: 5.0,
        fonte_titulo: 'Helvetica-Bold',
        tamanho_fonte_titulo: 12,
        fonte_nome: 'Helvetica-Bold',
        tamanho_fonte_nome: 10,
        fonte_cargo: 'Helvetica',
        tamanho_fonte_cargo: 8,
        fonte_info: 'Helvetica',
        tamanho_fonte_info: 7,
        mostrar_logo: true,
        posicao_logo: 'superior_esquerda',
        tamanho_logo: 15.0,
        mostrar_qr_borda: true,
        qr_tamanho: 20.0,
        qr_posicao: 'direita',
        fundo_tipo: 'solido',
        fundo_cor: '#ffffff',
        fundo_cor_gradiente: '#f0f0f0',
        fundo_imagem_url: '',
        fundo_opacidade: 1.0,
        ativo: true
      });
    }
    setDialogTemaAberto(true);
  };

  const fecharDialogTema = () => {
    setDialogTemaAberto(false);
    setTemaEditando(null);
    setAbaTemaAtiva(0); // Reset para a aba de configuração manual
  };

  const salvarTema = async () => {
    try {
      const resultadoValidacao = await configuracaoAvancadaService.validarTema(formTema as TemaAvancado);
      if (!resultadoValidacao.valido) {
        mostrarSnackbar(`Erros de validação: ${resultadoValidacao.erros.join(', ')}`, 'error');
        return;
      }

      if (temaEditando) {
        await temasAvancadosService.atualizar(temaEditando.id!, formTema as TemaAvancado);
        mostrarSnackbar('Tema atualizado com sucesso!', 'success');
      } else {
        await temasAvancadosService.criar(formTema as TemaAvancado);
        mostrarSnackbar('Tema criado com sucesso!', 'success');
      }

      fecharDialogTema();
      carregarDados();
    } catch (error) {
      console.error('Erro ao salvar tema:', error);
      mostrarSnackbar('Erro ao salvar tema', 'error');
    }
  };

  const excluirTema = async (id: number) => {
    if (!confirm('Tem certeza que deseja excluir este tema?')) {
      return;
    }

    try {
      await temasAvancadosService.deletar(id);
      mostrarSnackbar('Tema excluído com sucesso!', 'success');
      carregarDados();
    } catch (error) {
      console.error('Erro ao excluir tema:', error);
      mostrarSnackbar('Erro ao excluir tema', 'error');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>Carregando configurações...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box mb={3} display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            <SettingsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
            Configurações de Passes
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Gestão avançada de temas e formatos para passes de funcionários
          </Typography>
        </Box>
        <Button
          startIcon={<RefreshIcon />}
          variant="outlined"
          onClick={carregarDados}
          disabled={loading}
        >
          Atualizar
        </Button>
      </Box>

      {/* Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabAtiva} onChange={(_, newValue) => setTabAtiva(newValue)}>
            <Tab label="Temas Visuais" icon={<PaletteIcon />} {...a11yProps(0)} />
            <Tab label="Formatos de Saída" icon={<SettingsIcon />} {...a11yProps(1)} />
          </Tabs>
        </Box>

        {/* Tab Panel - Temas */}
        <TabPanel value={tabAtiva} index={0}>
          <Box mb={2} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">
              Temas Disponíveis ({temas.length})
            </Typography>
            <Button
              startIcon={<AddIcon />}
              variant="contained"
              onClick={() => abrirDialogTema()}
            >
              Novo Tema
            </Button>
          </Box>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Nome</TableCell>
                  <TableCell>Preview</TableCell>
                  <TableCell>Layout</TableCell>
                  <TableCell>Fonte Título</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {temas.map((tema) => (
                  <TableRow key={tema.id}>
                    <TableCell>{tema.nome}</TableCell>
                    <TableCell>
                      <Box display="flex" gap={0.5}>
                        <Box
                          width={16}
                          height={16}
                          bgcolor={tema.cor_primaria}
                          border="1px solid #ccc"
                          borderRadius={0.5}
                        />
                        <Box
                          width={16}
                          height={16}
                          bgcolor={tema.cor_secundaria}
                          border="1px solid #ccc"
                          borderRadius={0.5}
                        />
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={tema.layout_tipo} 
                        size="small" 
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>{tema.fonte_titulo}</TableCell>
                    <TableCell>
                      <Chip 
                        label={tema.ativo ? 'Ativo' : 'Inativo'} 
                        color={tema.ativo ? 'success' : 'default'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Tooltip title="Editar">
                        <IconButton 
                          size="small" 
                          onClick={() => abrirDialogTema(tema)}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Excluir">
                        <IconButton 
                          size="small" 
                          color="error"
                          onClick={() => excluirTema(tema.id!)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Tab Panel - Formatos */}
        <TabPanel value={tabAtiva} index={1}>
          <Box mb={2} display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h6">
              Formatos Disponíveis ({formatos.length})
            </Typography>
            <Button
              startIcon={<AddIcon />}
              variant="contained"
              onClick={() => setDialogFormatoAberto(true)}
            >
              Novo Formato
            </Button>
          </Box>

          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Nome</TableCell>
                  <TableCell>Tipo</TableCell>
                  <TableCell>Dimensões (mm)</TableCell>
                  <TableCell>DPI</TableCell>
                  <TableCell>Orientação</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {formatos.map((formato) => (
                  <TableRow key={formato.id}>
                    <TableCell>{formato.nome}</TableCell>
                    <TableCell>
                      <Chip 
                        label={formato.extensao.toUpperCase()} 
                        size="small" 
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      {formato.largura} × {formato.altura}
                      <br />
                      <Typography variant="caption" color="text.secondary">
                        {passesConfigUtils.getAspectRatio(formato.largura, formato.altura)}
                      </Typography>
                    </TableCell>
                    <TableCell>{formato.dpi}</TableCell>
                    <TableCell>
                      <Chip 
                        label={formato.orientacao} 
                        size="small" 
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={formato.ativo ? 'Ativo' : 'Inativo'} 
                        color={formato.ativo ? 'success' : 'default'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Tooltip title="Editar">
                        <IconButton 
                          size="small" 
                          onClick={() => setDialogFormatoAberto(true)}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Excluir">
                        <IconButton 
                          size="small" 
                          color="error"
                          onClick={() => console.log('Excluir formato', formato.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>
      </Card>

      {/* Dialog - Tema com Designer Visual */}
      <Dialog
        open={dialogTemaAberto}
        onClose={fecharDialogTema}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          {temaEditando ? 'Editar Tema' : 'Novo Tema'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
            <Tabs
              value={abaTemaAtiva}
              onChange={(_, newValue) => setAbaTemaAtiva(newValue)}
              aria-label="tema tabs"
            >
              <Tab label="Configuração Manual" {...a11yProps(0)} />
              <Tab label="Designer Visual" {...a11yProps(1)} />
            </Tabs>
          </Box>

          {/* Aba Configuração Manual */}
          <TabPanel value={abaTemaAtiva} index={0}>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              {/* Informações Básicas */}
              <Typography variant="h6" gutterBottom>
                Informações Básicas
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  label="Nome do Tema"
                  value={formTema.nome || ''}
                  onChange={(e) => setFormTema({ ...formTema, nome: e.target.value })}
                  required
                />
                <FormControl fullWidth>
                  <InputLabel>Layout</InputLabel>
                  <Select
                    value={formTema.layout_tipo || 'horizontal'}
                    onChange={(e) => setFormTema({ ...formTema, layout_tipo: e.target.value as any })}
                  >
                    <MenuItem value="horizontal">Horizontal</MenuItem>
                    <MenuItem value="vertical">Vertical</MenuItem>
                    <MenuItem value="compact">Compacto</MenuItem>
                  </Select>
                </FormControl>
              </Box>

              {/* Cores */}
              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Cores
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <TextField
                  fullWidth
                  type="color"
                  label="Cor Primária"
                  value={formTema.cor_primaria || '#1976d2'}
                  onChange={(e) => setFormTema({ ...formTema, cor_primaria: e.target.value })}
                />
                <TextField
                  fullWidth
                  type="color"
                  label="Cor Secundária"
                  value={formTema.cor_secundaria || '#ffffff'}
                  onChange={(e) => setFormTema({ ...formTema, cor_secundaria: e.target.value })}
                />
                <TextField
                  fullWidth
                  type="color"
                  label="Cor do Texto"
                  value={formTema.cor_texto || '#000000'}
                  onChange={(e) => setFormTema({ ...formTema, cor_texto: e.target.value })}
                />
                <TextField
                  fullWidth
                  type="color"
                  label="Cor da Borda"
                  value={formTema.cor_borda || '#cccccc'}
                  onChange={(e) => setFormTema({ ...formTema, cor_borda: e.target.value })}
                />
              </Box>

              {/* Estado */}
              <Box sx={{ mt: 2 }}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={formTema.ativo !== false}
                      onChange={(e) => setFormTema({ ...formTema, ativo: e.target.checked })}
                    />
                  }
                  label="Tema Ativo"
                />
              </Box>
            </Box>
          </TabPanel>

          {/* Aba Designer Visual */}
          <TabPanel value={abaTemaAtiva} index={1}>
            <Box sx={{ 
              display: 'flex', 
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '60vh',
              gap: 2 
            }}>
              <Typography variant="h6" color="text.secondary">
                Designer Visual de Passes
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2, textAlign: 'center' }}>
                Use o designer visual para criar o layout do seu passe de forma interativa
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={() => {
                  // Abrir o CardDesigner como um dialog separado
                  setDesignerAberto(true);
                }}
                startIcon={<PaletteIcon />}
              >
                Abrir Designer Visual
              </Button>
            </Box>
          </TabPanel>
        </DialogContent>
        <DialogActions>
          <Button onClick={fecharDialogTema} startIcon={<CancelIcon />}>
            Cancelar
          </Button>
          <Button onClick={salvarTema} variant="contained" startIcon={<SaveIcon />}>
            {temaEditando ? 'Atualizar' : 'Criar'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog - CardDesigner */}
      <CardDesigner
        open={designerAberto}
        onClose={() => setDesignerAberto(false)}
        onSave={(design) => {
          console.log('Design do passe salvo:', design);
          // Aqui você pode converter o design para o formato do tema
          // e atualizar o formTema conforme necessário
          setDesignerAberto(false);
          mostrarSnackbar('Design do passe salvo com sucesso!', 'success');
        }}
        initialDesign={undefined} // Pode ser preenchido com dados existentes
      />

      {/* Snackbar */}
      <Snackbar
        open={snackbar.aberto}
        autoHideDuration={6000}
        onClose={fecharSnackbar}
      >
        <Alert 
          onClose={fecharSnackbar} 
          severity={snackbar.tipo}
          sx={{ width: '100%' }}
        >
          {snackbar.mensagem}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default PassesConfigSimple;
