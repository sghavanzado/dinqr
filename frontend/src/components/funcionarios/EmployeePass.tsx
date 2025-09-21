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
  Grid,
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

interface PassConfig {
  temas_disponiveis: Array<{
    id: string;
    nome: string;
    cor_primaria: string;
  }>;
  formatos_saida: Array<{
    id: string;
    nome: string;
    descricao: string;
  }>;
  dimensoes: {
    formato: string;
    largura_mm: number;
    altura_mm: number;
    dpi_recomendado: number;
  };
  validade_padrao_dias: number;
}

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
      const response = await fetch('/api/iamc/passes/configuracao');
      if (response.ok) {
        const data = await response.json();
        setConfig(data.data);
      } else {
        throw new Error('Erro ao carregar configuração');
      }
    } catch (error) {
      showNotification('Erro ao carregar configuração de passes', 'error');
    }
  };

  const showNotification = (message: string, severity: 'success' | 'error' | 'warning' | 'info') => {
    setNotification({ open: true, message, severity });
  };

  const handleGerarPasse = async () => {
    setLoading(true);
    try {
      const requestData = {
        funcionario_id: funcionario.funcionarioID,
        incluir_qr: incluirQr,
        tema: tema,
        formato_saida: formatoSaida
      };

      const response = await fetch('/api/iamc/passes/gerar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (response.ok) {
        if (formatoSaida === 'pdf') {
          // Download PDF
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `passe_${funcionario.nome?.replace(/\s+/g, '_')}_${funcionario.funcionarioID}.pdf`;
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
          
          showNotification('Passe gerado e transferido com sucesso!', 'success');
        } else {
          // Mostrar preview HTML
          const html = await response.text();
          const blob = new Blob([html], { type: 'text/html' });
          const url = window.URL.createObjectURL(blob);
          setPreviewUrl(url);
          setPreviewOpen(true);
        }
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Erro ao gerar passe');
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
      const response = await fetch(`/api/iamc/passes/preview/${funcionario.funcionarioID}`);
      
      if (response.ok) {
        const html = await response.text();
        const blob = new Blob([html], { type: 'text/html' });
        const url = window.URL.createObjectURL(blob);
        setPreviewUrl(url);
        setPreviewOpen(true);
      } else {
        throw new Error('Erro ao gerar pré-visualização');
      }
    } catch (error) {
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
            {funcionario.nome} {funcionario.apelido} - ID: {funcionario.funcionarioID}
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
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Nome Completo</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.nome} {funcionario.apelido}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">ID</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.funcionarioID}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Cargo</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.cargoID ? `ID: ${funcionario.cargoID}` : 'N/A'}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="textSecondary">Departamento</Typography>
            <Typography variant="body1" fontWeight="medium">
              {funcionario.departamentoID ? `ID: ${funcionario.departamentoID}` : 'N/A'}
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* Configurações do Passe */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <SettingsIcon sx={{ mr: 1 }} />
            <Typography variant="h6">Configurações do Passe</Typography>
          </Box>

          <Grid container spacing={3}>
            {/* Tema */}
            <Grid item xs={12} sm={6}>
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
            </Grid>

            {/* Formato de Saída */}
            <Grid item xs={12} sm={6}>
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
            </Grid>

            {/* Incluir QR */}
            <Grid item xs={12}>
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
            </Grid>
          </Grid>
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
