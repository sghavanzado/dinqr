import { useState, useEffect } from 'react';

// Extend the Window interface to include electronAPI
declare global {
  interface Window {
    electronAPI?: {
      selectFolder: () => Promise<string | null>;
    };
  }
}
import {
  Container,
  Typography,
  TextField,
  Button,
  Snackbar,
  Alert,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import SaveIcon from '@mui/icons-material/Save';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import axiosInstance from '../api/axiosInstance';

interface Settings {
  server: string;
  username: string;
  password: string;
  database: string;
  outputFolder: string;
  serverDomain: string;
  serverPort: string;
}

const defaultSettings: Settings = {
  server: '',
  username: '',
  password: '',
  database: '',
  outputFolder: '',
  serverDomain: 'example.com',
  serverPort: '80', // Porta padrão para HTTP
};

const SettingsPage = () => {
  const [settings, setSettings] = useState<Settings>({
    server: defaultSettings.server,
    username: defaultSettings.username,
    password: defaultSettings.password,
    database: defaultSettings.database,
    outputFolder: defaultSettings.outputFolder,
    serverDomain: defaultSettings.serverDomain,
    serverPort: defaultSettings.serverPort,
  });
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');

  useEffect(() => {
    // Load settings from the backend
    const fetchSettings = async () => {
      try {
        const response = await axiosInstance.get('/settings');
        const fetchedSettings = response.data;
        setSettings({
          server: fetchedSettings.server || '',
          username: fetchedSettings.username || '',
          password: fetchedSettings.password || '',
          database: fetchedSettings.database || '',
          outputFolder: fetchedSettings.outputFolder || '',
          serverDomain: fetchedSettings.serverDomain || defaultSettings.serverDomain,
          serverPort: fetchedSettings.serverPort || defaultSettings.serverPort,
        });
      } catch {
        setSnackbarMessage('Erro ao carregar as configurações.');
        setSnackbarSeverity('error');
        setSnackbarOpen(true);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async () => {
    const { server, username, password, database, outputFolder, serverDomain, serverPort } = settings;

    if (!server || !username || !password || !database || !outputFolder || !serverDomain || !serverPort) {
      setSnackbarMessage('Por favor, preencha todos os campos.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
      return;
    }

    // Save settings to the backend
    try {
      await axiosInstance.post('/settings', settings);
      setSnackbarMessage('Configurações guardadas com sucesso.');
      setSnackbarSeverity('success');
      setSnackbarOpen(true);
    } catch {
      setSnackbarMessage('Erro ao guardar as configurações.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
    }
  };

  const handleServerAction = async (action: string) => {
    try {
      const response = await axiosInstance.post(`/settings/server/${action}`);
      setSnackbarMessage(response.data.message || 'Ação realizada com sucesso.');
      setSnackbarSeverity('success');
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.error || error.response?.data?.message || 'Erro ao realizar a ação.';
      setSnackbarMessage(`Erro: ${errorMessage}`);
      setSnackbarSeverity('error');
    } finally {
      setSnackbarOpen(true);
    }
  };

  const handleImportCSV = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axiosInstance.post('/qr/importar-funcionarios', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSnackbarMessage(response.data.message || 'Importação realizada com sucesso.');
      setSnackbarSeverity('success');
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Erro ao importar o arquivo.';
      setSnackbarMessage(errorMessage);
      setSnackbarSeverity('error');
    } finally {
      setSnackbarOpen(true);
    }
  };

  const handleGenerateTemplate = () => {
    const csvContent = `sap,nome,funcao,area,nif,telefone,email,uo\n`;
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'template_funcionarios.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Configurações
      </Typography>
      <Grid container spacing={3}>
       
          <TextField
            label="Servidor (IP ou Nome)"
            fullWidth
            value={settings.server}
            onChange={(e) => setSettings({ ...settings, server: e.target.value })}
          />
        
        
          <TextField
            label="Utilizador"
            fullWidth
            value={settings.username}
            onChange={(e) => setSettings({ ...settings, username: e.target.value })}
          />
        
        
          <TextField
            label="Palavra-passe"
            type="password"
            fullWidth
            value={settings.password}
            onChange={(e) => setSettings({ ...settings, password: e.target.value })}
          />
       
        
          <TextField
            label="Nome da Base de Dados"
            fullWidth
            value={settings.database}
            onChange={(e) => setSettings({ ...settings, database: e.target.value })}
          />
        
        
          <TextField
            label="Pasta de Saída para os Códigos QR"
            fullWidth
            value={settings.outputFolder}
            onChange={(e) => setSettings({ ...settings, outputFolder: e.target.value })}
          />
        
        
          <TextField
            label="Domínio ou IP do servidor"
            fullWidth
            value={settings.serverDomain}
            onChange={(e) => setSettings({ ...settings, serverDomain: e.target.value })}
          />
        
       
          <TextField
            label="Porta do servidor"
            fullWidth
            value={settings.serverPort}
            onChange={(e) => setSettings({ ...settings, serverPort: e.target.value })}
          />
        
        
          <Button
            variant="contained"
            startIcon={<SaveIcon sx={{ color: 'primary.main' }} />}
            onClick={handleSave}
            sx={{
              textTransform: 'none',
              fontWeight: 'bold',
              padding: '10px 20px',
              backgroundColor: '#A9A9A9', // Gris metálico
              color: 'white',
              '&:hover': {
                backgroundColor: '#8F8F8F', // Gris metálico mais oscuro al pasar el mouse
              },
            }}
          >
            Guardar Configurações
          </Button>
        
       
          <Button
            variant="contained"
            startIcon={<PlayArrowIcon sx={{ color: 'success.main' }} />}
            onClick={() => handleServerAction('start')}
            sx={{
              textTransform: 'none',
              fontWeight: 'bold',
              padding: '10px 20px',
              marginRight: 2,
              backgroundColor: '#A9A9A9', // Gris metálico
              color: 'white',
              '&:hover': {
                backgroundColor: '#8F8F8F', // Gris metálico mais oscuro al pasar el mouse
              },
            }}
          >
            Iniciar Servidor
          </Button>
          <Button
            variant="contained"
            startIcon={<StopIcon sx={{ color: 'error.main' }} />}
            onClick={() => handleServerAction('stop')}
            sx={{
              textTransform: 'none',
              fontWeight: 'bold',
              padding: '10px 20px',
              backgroundColor: '#A9A9A9', // Gris metálico
              color: 'white',
              '&:hover': {
                backgroundColor: '#8F8F8F', // Gris metálico mais oscuro al pasar el mouse
              },
            }}
          >
            Parar Servidor
          </Button>
        
        <Grid item xs={12}>
          <Button
            variant="contained"
            startIcon={<UploadFileIcon />}
            component="label"
            sx={{
              textTransform: 'none',
              fontWeight: 'bold',
              padding: '10px 20px',
              backgroundColor: '#A9A9A9',
              color: 'white',
              '&:hover': {
                backgroundColor: '#8F8F8F',
              },
            }}
          >
            Importar Funcionários
            <input
              type="file"
              accept=".csv"
              hidden
              onChange={handleImportCSV}
            />
          </Button>
          <Button
            variant="contained"
            startIcon={<FileDownloadIcon />}
            onClick={handleGenerateTemplate}
            sx={{
              textTransform: 'none',
              fontWeight: 'bold',
              padding: '10px 20px',
              marginLeft: 2,
              backgroundColor: '#A9A9A9',
              color: 'white',
              '&:hover': {
                backgroundColor: '#8F8F8F',
              },
            }}
          >
            Gerar Template CSV
          </Button>
        </Grid>
      </Grid>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity={snackbarSeverity}>{snackbarMessage}</Alert>
      </Snackbar>
    </Container>
  );
};

export default SettingsPage;
