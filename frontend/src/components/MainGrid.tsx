// src/components/MainGrid.tsx
import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  CircularProgress,
  IconButton,
  Modal,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  InputAdornment,
  Pagination,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox
} from '@mui/material';
import QrCodeIcon from '@mui/icons-material/QrCode';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import SearchIcon from '@mui/icons-material/Search';
import ServerStatus from './ServerStatus';
import StatCard from './StatCard';
import type { StatCardProps } from './StatCard';
import axiosInstance from '../api/axiosInstance';
import type { DashboardFuncionario } from '../types/Funcionario';

export default function MainGrid() {
  // =============================================
  // 📊 ESTADOS PARA ESTADÍSTICAS DEL DASHBOARD
  // =============================================
  const [totalFuncionarios, setTotalFuncionarios] = useState<number | null>(null);
  const [funcionariosSemQR, setFuncionariosSemQR] = useState<number | null>(null);
  const [totalFuncionariosComQR, setTotalFuncionariosComQR] = useState<number | null>(null);

  // =============================================
  // 📋 ESTADOS PARA LA TABLA DE FUNCIONARIOS
  // =============================================
  const [funcionariosComQR, setFuncionariosComQR] = useState<DashboardFuncionario[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);            // IDs de funcionarios seleccionados
  const [loading, setLoading] = useState(false);                          // Estado de carga
  const [filter, setFilter] = useState('');                               // Texto de filtro/búsqueda
  
  // =============================================
  // 🎭 ESTADOS PARA MODALES Y DIALOGS
  // =============================================
  const [qrModalOpen, setQrModalOpen] = useState(false);                  // Modal para mostrar QR
  const [qrImage, setQrImage] = useState('');                             // URL de la imagen QR
  const [contactCardOpen, setContactCardOpen] = useState(false);          // Dialog para tarjeta de contacto
  const [contactCardHtml, setContactCardHtml] = useState('');             // HTML de la tarjeta de contacto

  // =============================================
  // 🔥 ESTADOS PARA PAGINACIÓN Y FILAS POR PÁGINA
  // =============================================
  const [pageComQR, setPageComQR] = useState(1);                    // Página actual (inicia en 1)
  const [rowsPerPageComQR, setRowsPerPageComQR] = useState(10);     // Número de filas por página

  // =============================================
  // 🔥 LÓGICA DE FILTRADO Y PAGINACIÓN (SOLO FRONTEND)
  // =============================================
  // NOTA: Ahora usamos /qr/funcionarios-com-qr que retorna TODOS los datos
  // y manejamos la paginación completamente en el frontend (igual que QRTable.tsx)
  
  // Filtrar funcionarios basado en el texto de búsqueda
  const filteredFuncionariosComQR = funcionariosComQR.filter(
    (funcionario) =>
      funcionario.nome.toLowerCase().includes(filter.toLowerCase()) ||
      funcionario.apelido.toLowerCase().includes(filter.toLowerCase()) ||
      funcionario.cargo?.toLowerCase().includes(filter.toLowerCase()) ||
      funcionario.departamento?.toLowerCase().includes(filter.toLowerCase()) ||
      funcionario.email?.toLowerCase().includes(filter.toLowerCase())
  );

  // 🔥 CALCULAR TOTAL DE PÁGINAS BASADO EN FUNCIONARIOS FILTRADOS
  const totalPages = Math.ceil(filteredFuncionariosComQR.length / rowsPerPageComQR);

  // 🔥 OBTENER FUNCIONARIOS PARA LA PÁGINA ACTUAL (SLICE PAGINADO FRONTEND)
  const paginatedFuncionarios = filteredFuncionariosComQR.slice(
    (pageComQR - 1) * rowsPerPageComQR,    // Índice de inicio
    pageComQR * rowsPerPageComQR           // Índice de fin
  );

  // =============================================
  // 🔄 FUNÇÃO PARA OBTENER ESTADÍSTICAS DEL DASHBOARD
  // =============================================
  const fetchDashboardData = async () => {
    try {
      // Obtener total de funcionarios desde QR endpoints (ahora usando IAMC)
      const totalResponse = await axiosInstance.get('/qr/funcionarios/total');
      const total = totalResponse.data.total;
      setTotalFuncionarios(total);

      // Obtener total de funcionarios con QR desde QR endpoints
      const qrResponse = await axiosInstance.get('/qr/funcionarios/total-con-qr');
      const totalConQR = qrResponse.data.total;
      setTotalFuncionariosComQR(totalConQR);

      // Calcular funcionarios sin QR
      setFuncionariosSemQR(total - totalConQR);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  // =============================================
  // 🔄 FUNCIÓN PARA OBTENER FUNCIONARIOS CON QR
  // =============================================
  const fetchFuncionarios = async () => {
    setLoading(true);
    try {
      // 🔥 USAR ENDPOINT QR ORIGINAL (ahora modificado para usar datos IAMC)
      const response = await axiosInstance.get('/qr/funcionarios-com-qr');
      if (response.status === 200) {
        setFuncionariosComQR(response.data); // Ahora recibe datos IAMC con joins
        console.log('Funcionarios com QR cargados desde IAMC:', response.data.length);
      } else {
        console.error('Unexpected response:', response);
        alert('Erro ao carregar funcionários com QR. Verifique o console para mais detalhes.');
      }
    } catch (error) {
      console.error('Error fetching funcionarios con QR:', error);
      alert('Erro ao carregar funcionários com QR. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // =============================================
  // 🚀 EFFECT PARA CARGAR DATOS AL MONTAR EL COMPONENTE
  // =============================================
  useEffect(() => {
    fetchDashboardData();  // Cargar estadísticas del dashboard
    fetchFuncionarios();   // Cargar funcionarios con QR
  }, []);

  // =============================================
  // 🗑️ HANDLERS PARA ACCIONES DE QR
  // =============================================
  const handleDeleteQR = async (id: number) => {
    setLoading(true);
    try {
      await axiosInstance.delete(`/qr/eliminar/${id}`);
      alert('Código QR eliminado com sucesso.');
      // Actualizar tanto la lista como las estadísticas
      await Promise.all([fetchFuncionarios(), fetchDashboardData()]);
      setSelectedIds([]); // Limpiar selección
    } catch (error) {
      console.error('Error deleting QR code:', error);
      alert('Erro ao eliminar o código QR.');
    } finally {
      setLoading(false);
    }
  };

  // =============================================
  // 👁️ HANDLER PARA VISUALIZAR QR EN MODAL
  // =============================================
  const handleViewQR = async (id: number) => {
    try {
      const response = await axiosInstance.get(`/qr/descargar/${id}`, { responseType: 'blob' });
      const qrBlob = new Blob([response.data], { type: 'image/png' });
      const qrUrl = URL.createObjectURL(qrBlob);
      setQrImage(qrUrl);
      setQrModalOpen(true);
    } catch (error) {
      console.error('Error viewing QR code:', error);
      alert('Erro ao mostrar o código QR.');
    }
  };

  // =============================================
  // 💾 HANDLER PARA DESCARGAR QR
  // =============================================
  const handleDownloadQR = async (id: number) => {
    try {
      const response = await axiosInstance.get(`/qr/descargar/${id}`, { responseType: 'blob' });
      const qrBlob = new Blob([response.data], { type: 'image/png' });
      const qrUrl = URL.createObjectURL(qrBlob);
      const link = document.createElement('a');
      link.href = qrUrl;
      link.download = `qr_${id}.png`;
      link.click();
      URL.revokeObjectURL(qrUrl);
    } catch (error) {
      console.error('Error downloading QR code:', error);
      alert('Erro ao descarregar o código QR.');
    }
  };

  // =============================================
  // 👤 HANDLER PARA MOSTRAR TARJETA DE CONTACTO
  // =============================================
  const handleViewContactCard = (funcionario: DashboardFuncionario) => {
    const logoUrl = '/static/images/sonangol-logo.png';
    const headerBackgroundColor = '#F4CF0A';
    // Generar HTML para la tarjeta de contacto
    const htmlContent = `
      <div style="font-family: Arial, sans-serif; max-width: 400px; margin: auto; border: 1px solid #ccc; border-radius: 10px; overflow: hidden;">
        <div style="background-color: ${headerBackgroundColor}; padding: 10px; display: flex; align-items: center; justify-content: center;">
          <img src="${logoUrl}" alt="Sonangol Logo" style="height: 50px; max-width: 50px; object-fit: contain; margin-right: 10px;">
          <span style="font-size: 2rem; font-weight: bold; color: #000; font-family: 'Arial', sans-serif;">Sonangol</span>
        </div>
        <div style="background-color: #e6e6e6; padding: 5px; text-align: center; font-size: 0.9rem;">
          Sociedade Nacional de Combustíveis de Angola
        </div>
        <div style="padding: 20px; text-align: left;">
        <p><strong>Nome:</strong> ${funcionario.nome} ${funcionario.apelido}</p>
          <p><strong>ID:</strong> ${funcionario.funcionarioId}</p>
          <p><strong>Email:</strong> ${funcionario.email}</p>
          <p><strong>Telefone:</strong> ${funcionario.telefone}</p>
          <p><strong>Cargo:</strong> ${funcionario.cargo || 'Não especificado'}</p>
          <p><strong>Departamento:</strong> ${funcionario.departamento || 'Não especificado'}</p>
        </div>
      </div>
    `;
    setContactCardHtml(htmlContent);
    setContactCardOpen(true);
  };

  // =============================================
  // ❌ HANDLERS PARA CERRAR MODALES
  // =============================================
  const handleCloseContactCard = () => {
    setContactCardOpen(false);
    setContactCardHtml('');
  };

  const handleCloseModal = () => {
    setQrModalOpen(false);
    setQrImage('');
  };

  // =============================================
  // ✅ HANDLERS PARA SELECCIÓN DE FUNCIONARIOS
  // =============================================
  // Handler para seleccionar/deseleccionar todos los funcionarios visibles
  const handleSelectAll = (checked: boolean) => {
    const visibleRows = paginatedFuncionarios; // 🔥 USA FUNCIONARIOS PAGINADOS
    if (checked) {
      const allIds = visibleRows.map((funcionario) => funcionario.id as number);
      setSelectedIds((prevIds) => Array.from(new Set([...prevIds, ...allIds])));
    } else {
      const visibleIds = visibleRows.map((funcionario) => Number(funcionario.id));
      setSelectedIds((prevIds) => prevIds.filter((id) => !visibleIds.includes(id)));
    }
  };

  // Handler para seleccionar/deseleccionar un funcionario individual
  const handleRowCheckboxChange = (id: number, checked: boolean) => {
    if (checked) {
      setSelectedIds((prevIds) => [...prevIds, id]);
    } else {
      setSelectedIds((prevIds) => prevIds.filter((selectedId) => selectedId !== id));
    }
  };

  // =============================================
  // 🔍 LÓGICA PARA DETERMINAR ESTADO DE SELECCIÓN
  // =============================================
  // Verificar si todos los funcionarios visibles están seleccionados
  const isAllSelected = paginatedFuncionarios.length > 0 && paginatedFuncionarios.every((funcionario) => selectedIds.includes(funcionario.id));
  // Verificar si algunos (pero no todos) funcionarios visibles están seleccionados
  const isIndeterminate = paginatedFuncionarios.some((funcionario) => selectedIds.includes(funcionario.id)) && !isAllSelected;

  // =============================================
  // 📊 DATOS PARA LAS TARJETAS DE ESTADÍSTICAS
  // =============================================
  const data: StatCardProps[] = [
    {
      title: 'Total Funcionarios',
      value: totalFuncionarios !== null ? totalFuncionarios.toString() : 'Cargando...',
      trend: 'up',
    },
    {
      title: 'Funcionários sem QR',
      value: funcionariosSemQR !== null ? funcionariosSemQR.toString() : 'Cargando...',
      trend: 'down',
    },
    {
      title: 'Funcionários com QR',
      value: totalFuncionariosComQR !== null ? totalFuncionariosComQR.toString() : 'Cargando...',
      trend: 'neutral',
    },
  ];

  return (
    <Box sx={{ width: '100%', maxWidth: { sm: '100%', md: '1700px' } }}>
      {/* ============================================= */}
      {/* 📊 SECCIÓN DEL DASHBOARD - ESTADÍSTICAS */}
      {/* ============================================= */}
      <Typography component="h2" variant="h6" sx={{ mb: 2 }}>
        Dashboard
      </Typography>
      
      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 1,
          mb: 2,
        }}
      >
        {data.map((card, index) => (
          <Box key={index} sx={{ flex: '1 1 23%', minWidth: 200 }}>
            <StatCard {...card} />
          </Box>
        ))}
        <Box sx={{ flex: '1 1 23%', minWidth: 200 }}>
          <ServerStatus />
        </Box>
      </Box>

      {/* ============================================= */}
      {/* 📋 SECCIÓN DE LA TABLA DE FUNCIONARIOS */}
      {/* ============================================= */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Funcionários com QR
        </Typography>
        {/* Barra de búsqueda */}
        <TextField
          fullWidth
          placeholder="Pesquisar por nome, apelido, cargo, departamento ou email..."
          value={filter}
          onChange={(e) => {
            setFilter(e.target.value);
            setPageComQR(1); // 🔥 RESETEAR A PÁGINA 1 AL FILTRAR
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{ mb: 2 }}
        />
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={isAllSelected}
                        indeterminate={isIndeterminate}
                        onChange={(e) => handleSelectAll(e.target.checked)}
                      />
                    </TableCell>
                    <TableCell>
                      <strong>ID</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Nome</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Apelido</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Email</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Telefone</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Cargo</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Departamento</strong>
                    </TableCell>
                    <TableCell align="center">
                      <strong>Ações</strong>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {/* 🔥 RENDERIZAR SOLO LOS FUNCIONARIOS PAGINADOS */}
                  {paginatedFuncionarios.length > 0 ? (
                    paginatedFuncionarios.map((funcionario) => (
                      <TableRow
                        key={funcionario.id}
                        hover
                        onClick={() => handleRowCheckboxChange(funcionario.id, !selectedIds.includes(funcionario.id))}
                        sx={{ cursor: 'pointer', backgroundColor: selectedIds.includes(funcionario.id) ? 'rgba(0, 0, 0, 0.04)' : 'inherit' }}
                      >
                        <TableCell padding="checkbox">
                          <Checkbox
                            checked={selectedIds.includes(funcionario.id)}
                            onChange={(e) => handleRowCheckboxChange(funcionario.id, e.target.checked)}
                          />
                        </TableCell>
                        <TableCell>{funcionario.funcionarioId}</TableCell>
                        <TableCell>
                          <Typography variant="body2" fontWeight="bold">
                            {funcionario.nome}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {funcionario.apelido}
                          </Typography>
                        </TableCell>
                        <TableCell>{funcionario.email}</TableCell>
                        <TableCell>{funcionario.telefone}</TableCell>
                        <TableCell>
                          <Chip label={funcionario.cargo} size="small" />
                        </TableCell>
                        <TableCell>{funcionario.departamento}</TableCell>
                        <TableCell align="center">
                          <Box sx={{ display: 'flex', gap: 0.5 }}>
                            <IconButton size="small" onClick={() => handleViewQR(funcionario.id)} title="Visualizar QR">
                              <QrCodeIcon fontSize="small" />
                            </IconButton>
                            <IconButton size="small" onClick={() => handleDownloadQR(funcionario.id)} title="Baixar QR">
                              <DownloadIcon fontSize="small" />
                            </IconButton>
                            <IconButton size="small" onClick={() => handleViewContactCard(funcionario)} title="Ver Cartão">
                              <OpenInNewIcon fontSize="small" />
                            </IconButton>
                            <IconButton
                              size="small"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteQR(funcionario.id);
                              }}
                              title="Eliminar QR"
                              color="error"
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Box>
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={9} align="center">
                        <Box sx={{ py: 4 }}>
                          <QrCodeIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                          <Typography variant="h6" color="text.secondary">
                            Nenhum funcionário com QR encontrado.
                          </Typography>
                        </Box>
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>

            {/* ============================================= */}
            {/* 🔥 CONTROLES DE PAGINACIÓN Y FILAS POR PÁGINA */}
            {/* ============================================= */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 3, p: 2 }}>
              {/* 🔥 COMPONENTE DE PAGINACIÓN (solo se muestra si hay más de 1 página) */}
              {totalPages > 1 && (
                <Pagination
                  count={totalPages}                    // Total de páginas calculado
                  page={pageComQR}                           // Página actual
                  onChange={(_, newPage) => setPageComQR(newPage)}  // Handler para cambio de página
                  color="primary"
                />
              )}
              
              {/* 🔥 SELECTOR DE FILAS POR PÁGINA */}
              <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel>Filas por página</InputLabel>
                <Select
                  value={rowsPerPageComQR}
                  label="Filas por página"
                  onChange={(e) => {
                   setRowsPerPageComQR(Number(e.target.value));
                    setPageComQR(1); // 🔥 RESETEAR A PÁGINA 1 AL CAMBIAR FILAS POR PÁGINA
                  }}
                >
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={30}>30</MenuItem>
                  <MenuItem value={60}>60</MenuItem>
                </Select>
              </FormControl>
            </Box>
            
            {/* ============================================= */}
            {/* 🗑️ BOTÓN PARA ELIMINAR FUNCIONARIOS SELECCIONADOS */}
            {/* ============================================= */}
            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                onClick={() => {
                  if (selectedIds.length > 0) {
                    alert(`Eliminar ${selectedIds.length} códigos QR.`);
                  }
                }}
                disabled={selectedIds.length === 0}
                startIcon={<DeleteIcon />}
                color="error"
              >
                Eliminar Selecionados ({selectedIds.length})
              </Button>
            </Box>
          </>
        )}
      </Paper>

      {/* ============================================= */}
      {/* 🎭 MODALES Y DIALOGS */}
      {/* ============================================= */}
      {/* Modal para mostrar código QR */}
      <Modal
        open={qrModalOpen}
        onClose={handleCloseModal}
        sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
      >
        <Box
          sx={{
            backgroundColor: 'white',
            padding: 2,
            borderRadius: 2,
            boxShadow: 24,
            textAlign: 'center',
            width: 300,
            maxWidth: '90%',
          }}
        >
          <Typography variant="h6" gutterBottom>
            Código QR
          </Typography>
          <img src={qrImage} alt="QR Code" style={{ maxWidth: '100%', height: 'auto' }} />
          <Button variant="contained" color="primary" onClick={handleCloseModal} sx={{ mt: 2 }}>
            Fechar
          </Button>
        </Box>
      </Modal>

      {/* Dialog para mostrar tarjeta de contacto */}
      <Dialog open={contactCardOpen} onClose={handleCloseContactCard} maxWidth="xs" fullWidth>
        <DialogTitle sx={{ textAlign: 'center' }}>Cartão de Contacto</DialogTitle>
        <DialogContent>
          <div dangerouslySetInnerHTML={{ __html: contactCardHtml }} />
        </DialogContent>
      </Dialog>
    </Box>
  );
}
