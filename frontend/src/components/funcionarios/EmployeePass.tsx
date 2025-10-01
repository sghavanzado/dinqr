import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Alert,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Paper,
  IconButton,
} from '@mui/material';
import {
  Print as PrintIcon,
  Preview as PreviewIcon,
  Download as DownloadIcon,
  Settings as SettingsIcon,
  Close as CloseIcon,
  QrCode as QrCodeIcon,
  Badge as BadgeIcon,
} from '@mui/icons-material';
import type { Funcionario } from '../../types/rrhh';
import { 
  gerarPasse, 
  previewPasse, 
  getPassesConfig,
  type PassConfig,
  type PassRequest 
} from '../../services/api/passes';



interface EmployeePassProps {
  funcionario: Funcionario;
  onClose?: () => void;
  showDialog?: boolean;
}

const EmployeePass: React.FC<EmployeePassProps> = ({
  funcionario,
  onClose,
  showDialog = false
}) => {
  const [config, setConfig] = useState<PassConfig | null>(null);
  const [tema, setTema] = useState('default');
  const [incluirQr, setIncluirQr] = useState(true);
  const [formatoSaida, setFormatoSaida] = useState<'pdf' | 'html'>('pdf');
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'warning' | 'info';
  }>({
    open: false,
    message: '',
    severity: 'info'
  });
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string>('');

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const configData = await getPassesConfig();
      setConfig(configData);
    } catch (error) {
      console.error('Erro ao carregar configuração de passes:', error);
      showNotification('Erro ao carregar configuração de passes', 'error');
    }
  };

  const showNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setNotification({ open: true, message, severity });
  };

  const handleGerarPasse = async () => {
    setLoading(true);
    try {
      const requestData: PassRequest = {
        funcionario_id: funcionario.FuncionarioID || funcionario.funcionarioID || funcionario.id,
        incluir_qr: incluirQr,
        tema: tema as any,
        formato_saida: formatoSaida
      };

      const blob = await gerarPasse(requestData);

      if (formatoSaida === 'pdf') {
        // Download PDF
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `passe_${(funcionario.Nome || funcionario.nome || 'funcionario').replace(/\s+/g, '_')}_${funcionario.FuncionarioID || funcionario.funcionarioID || funcionario.id}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showNotification('Passe gerado e transferido com sucesso!', 'success');
      } else {
        // Mostrar preview HTML (convertir blob a HTML)
        const html = await blob.text();
        const htmlBlob = new Blob([html], { type: 'text/html' });
        const url = window.URL.createObjectURL(htmlBlob);
        setPreviewUrl(url);
        setPreviewOpen(true);
      }
    } catch (error) {
      console.error('Erro:', error);
      showNotification(
        error instanceof Error ? error.message : 'Erro ao gerar passe',
        'error'
      );
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = async () => {
    setLoading(true);
    try {
      const funcionarioId = funcionario.FuncionarioID || funcionario.funcionarioID || funcionario.id;
      const blob = await previewPasse(funcionarioId);
      
      // Convertir blob a HTML para preview
      const html = await blob.text();
      const htmlBlob = new Blob([html], { type: 'text/html' });
      const url = window.URL.createObjectURL(htmlBlob);
      setPreviewUrl(url);
      setPreviewOpen(true);
    } catch (error) {
      console.error('Erro ao gerar pré-visualização:', error);
      showNotification('Erro ao gerar pré-visualização', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleClosePreview = () => {
    setPreviewOpen(false);
    if (previewUrl) {
      window.URL.revokeObjectURL(previewUrl);
      setPreviewUrl('');
    }
  };

  const getTemaColor = (temaId: string) => {
    const tema = config?.temas_disponiveis.find(t => t.id === temaId);
    return tema?.cor_primaria || '#1976d2';
  };

  const PassContent = () => (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <BadgeIcon sx={{ mr: 2, fontSize: 32, color: 'primary.main' }} />
        <Box sx={{ flex: 1 }}>
          <Typography variant="h5" component="h1">
            Gerar Passe de Funcionário
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {funcionario.Nome || funcionario.nome} {funcionario.Apelido || funcionario.apelido} - ID: {funcionario.FuncionarioID || funcionario.funcionarioID || funcionario.id}
          </Typography>
        </Box>
        {onClose && (
          <IconButton onClick={onClose}>
            <CloseIcon />
          </IconButton>
        )}
      </Box>

      {/* Informações do Funcionário */}
      <Paper sx={{ p: 2, mb: 3, bgcolor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          Dados do Funcionário
        </Typography>
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 2 }}>
          <Box>
            <Typography variant="body2" color="textSecondary">Nome Completo</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.Nome || funcionario.nome} {funcionario.Apelido || funcionario.apelido}
            </Typography>
          </Box>
          <Box>
            <Typography variant="body2" color="textSecondary">ID</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.FuncionarioID || funcionario.funcionarioID || funcionario.id}
            </Typography>
          </Box>
          <Box>
            <Typography variant="body2" color="textSecondary">Cargo</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.cargo?.nome || funcionario.CargoNome || (funcionario.cargoID ? `ID: ${funcionario.cargoID}` : 'N/A')}
            </Typography>
          </Box>
          <Box>
            <Typography variant="body2" color="textSecondary">Departamento</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.departamento?.nome || funcionario.DepartamentoNome || (funcionario.departamentoID ? `ID: ${funcionario.departamentoID}` : 'N/A')}
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Configurações do Passe */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <SettingsIcon sx={{ mr: 1 }} />
            <Typography variant="h6">Configurações do Passe</Typography>
          </Box>

          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 3 }}>
            {/* Tema */}
            <FormControl fullWidth>
              <InputLabel>Tema</InputLabel>
              <Select
                value={tema}
                label="Tema"
                onChange={(e) => setTema(e.target.value)}
              >
                {config?.temas_disponiveis.map((t) => (
                  <MenuItem key={t.id} value={t.id}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Box
                        sx={{
                          width: 16,
                          height: 16,
                          borderRadius: '50%',
                          bgcolor: t.cor_primaria,
                        }}
                      />
                      {t.nome}
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* Formato de Saída */}
            <FormControl fullWidth>
              <InputLabel>Formato</InputLabel>
              <Select
                value={formatoSaida}
                label="Formato"
                onChange={(e) => setFormatoSaida(e.target.value as 'pdf' | 'html')}
              >
                {config?.formatos_saida.map((f) => (
                  <MenuItem key={f.id} value={f.id}>
                    {f.nome} - {f.descricao}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>

          {/* Incluir QR */}
          <Box sx={{ mt: 3 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={incluirQr}
                  onChange={(e) => setIncluirQr(e.target.checked)}
                />
              }
              label={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <QrCodeIcon fontSize="small" />
                  Incluir Código QR
                </Box>
              }
            />
          </Box>
        </CardContent>
      </Card>

      {/* Especificações Técnicas */}
      {config && (
        <Paper sx={{ p: 2, mb: 3, bgcolor: 'info.light', color: 'info.contrastText' }}>
          <Typography variant="body2" gutterBottom>
            <strong>Especificações Técnicas:</strong>
          </Typography>
          <Typography variant="body2">
            Formato: {config.dimensoes.formato} • 
            Dimensões: {config.dimensoes.largura_mm}mm × {config.dimensoes.altura_mm}mm • 
            DPI: {config.dimensoes.dpi_recomendado} • 
            Validade: {config.validade_padrao_dias} dias
          </Typography>
        </Paper>
      )}

      {/* Ações */}
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button
          variant="outlined"
          startIcon={<PreviewIcon />}
          onClick={handlePreview}
          disabled={loading}
        >
          Pré-visualizar
        </Button>
        
        <Button
          variant="contained"
          startIcon={loading ? <CircularProgress size={16} /> : <PrintIcon />}
          onClick={handleGerarPasse}
          disabled={loading}
          sx={{ bgcolor: getTemaColor(tema) }}
        >
          {loading ? 'A Gerar...' : 'Gerar Passe'}
        </Button>
      </Box>
    </Box>
  );

  return (
    <>
      {showDialog ? (
        <Dialog
          open={showDialog}
          onClose={onClose}
          maxWidth="md"
          fullWidth
        >
          <PassContent />
        </Dialog>
      ) : (
        <Card>
          <PassContent />
        </Card>
      )}

      {/* Preview Dialog */}
      <Dialog
        open={previewOpen}
        onClose={handleClosePreview}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: { height: '90vh' }
        }}
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6">Pré-visualização do Passe</Typography>
            <IconButton onClick={handleClosePreview}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent sx={{ p: 0 }}>
          {previewUrl && (
            <iframe
              src={previewUrl}
              style={{
                width: '100%',
                height: '100%',
                border: 'none',
              }}
              title="Pré-visualização do Passe"
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePreview}>Fechar</Button>
          <Button
            variant="contained"
            startIcon={<DownloadIcon />}
            onClick={() => {
              setFormatoSaida('pdf');
              handleGerarPasse();
            }}
          >
            Transferir PDF
          </Button>
        </DialogActions>
      </Dialog>

      {/* Notification */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={() => setNotification({ ...notification, open: false })}
      >
        <Alert
          onClose={() => setNotification({ ...notification, open: false })}
          severity={notification.severity}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </>
  );
};

export default EmployeePass;
