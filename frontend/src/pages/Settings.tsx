import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  TextField,
  Button,
  Grid,
  Snackbar,
  Alert,
} from '@mui/material';
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
  serverPort: '80', // Puerto predeterminado para HTTP
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
      } catch (error) {
        setSnackbarMessage('Error al cargar la configuración.');
        setSnackbarSeverity('error');
        setSnackbarOpen(true);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async () => {
    const { server, username, password, database, outputFolder, serverDomain, serverPort } = settings;

    if (!server || !username || !password || !database || !outputFolder || !serverDomain || !serverPort) {
      setSnackbarMessage('Por favor complete todos los campos.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
      return;
    }

    // Save settings to the backend
    try {
      await axiosInstance.post('/settings', settings);
      setSnackbarMessage('Configuración guardada exitosamente.');
      setSnackbarSeverity('success');
      setSnackbarOpen(true);
    } catch (error) {
      setSnackbarMessage('Error al guardar la configuración.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
    }
  };

  const handleServerAction = async (action: string) => {
    try {
      const response = await axiosInstance.post(`/settings/server/${action}`);
      setSnackbarMessage(response.data.message || 'Acción realizada con éxito.');
      setSnackbarSeverity('success');
    } catch (error: any) {
      const errorMessage =
        error.response?.data?.error || error.response?.data?.message || 'Error al realizar la acción.';
      setSnackbarMessage(`Error: ${errorMessage}`);
      setSnackbarSeverity('error');
    } finally {
      setSnackbarOpen(true);
    }
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Configuración
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            label="Servidor (IP o Nombre)"
            fullWidth
            value={settings.server}
            onChange={(e) => setSettings({ ...settings, server: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Usuario"
            fullWidth
            value={settings.username}
            onChange={(e) => setSettings({ ...settings, username: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Contraseña"
            type="password"
            fullWidth
            value={settings.password}
            onChange={(e) => setSettings({ ...settings, password: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Nombre de la Base de Datos"
            fullWidth
            value={settings.database}
            onChange={(e) => setSettings({ ...settings, database: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Carpeta de Salida para los Códigos QR"
            fullWidth
            value={settings.outputFolder}
            onChange={(e) => setSettings({ ...settings, outputFolder: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Dominio o IP del servidor"
            fullWidth
            value={settings.serverDomain}
            onChange={(e) => setSettings({ ...settings, serverDomain: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            label="Puerto del servidor"
            fullWidth
            value={settings.serverPort}
            onChange={(e) => setSettings({ ...settings, serverPort: e.target.value })}
          />
        </Grid>
        <Grid item xs={12}>
          <Button variant="contained" color="primary" onClick={handleSave}>
            Guardar Configuración
          </Button>
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => handleServerAction('start')}
            sx={{ marginRight: 2 }}
          >
            Iniciar Servidor
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={() => handleServerAction('stop')}
          >
            Detener Servidor
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
