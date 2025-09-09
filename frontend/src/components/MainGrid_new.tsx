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
import type { Funcionario } from '../types/Funcionario';

export default function MainGrid() {
  // Estados para las estadísticas del dashboard
  const [totalFuncionarios, setTotalFuncionarios] = useState<number | null>(null);
  const [funcionariosComQR, setFuncionariosComQR] = useState<number | null>(null);
  const [funcionariosSemQR, setFuncionariosSemQR] = useState<number | null>(null);

  // Estados para la tabla de funcionarios
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('');
  const [qrModalOpen, setQrModalOpen] = useState(false);
  const [qrImage, setQrImage] = useState('');
  const [contactCardOpen, setContactCardOpen] = useState(false);
  const [contactCardHtml, setContactCardHtml] = useState('');

  // Estados para la paginación y filas por página
  const [page, setPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  // Filtrado y paginación
  const filteredFuncionarios = funcionarios.filter(
    (funcionario) =>
      funcionario.nome.toLowerCase().includes(filter.toLowerCase()) ||
      funcionario.funcao?.toLowerCase().includes(filter.toLowerCase()) ||
      funcionario.area?.toLowerCase().includes(filter.toLowerCase())
  );

  const totalPages = Math.ceil(filteredFuncionarios.length / rowsPerPage);

  const paginatedFuncionarios = filteredFuncionarios.slice(
    (page - 1) * rowsPerPage,
    page * rowsPerPage
  );

  // Función para obtener las estadísticas del dashboard
  const fetchDashboardData = async () => {
    try {
      const totalResponse = await axiosInstance.get('/qr/funcionarios/total');
      const total = totalResponse.data.total;
      setTotalFuncionarios(total);

      const qrResponse = await axiosInstance.get('/qr/funcionarios/total-con-qr');
      const totalConQR = qrResponse.data.total;
      setFuncionariosComQR(totalConQR);

      setFuncionariosSemQR(total - totalConQR);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  // Función para obtener los funcionarios con QR
  const fetchFuncionarios = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/qr/funcionarios');
      if (response.status === 200) {
        setFuncionarios(response.data);
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

  useEffect(() => {
    fetchDashboardData();
    fetchFuncionarios();
  }, []);

  // Handlers para la tabla de funcionarios
  const handleDeleteQR = async (id: number) => {
    setLoading(true);
    try {
      await axiosInstance.delete(`/qr/eliminar/${id}`);
      alert('Código QR eliminado com sucesso.');
      await Promise.all([fetchFuncionarios(), fetchDashboardData()]);
      setSelectedIds([]);
    } catch (error) {
      console.error('Error deleting QR code:', error);
      alert('Erro ao eliminar o código QR.');
    } finally {
      setLoading(false);
    }
  };

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

  const handleViewContactCard = (funcionario: Funcionario) => {
    const logoUrl = '/static/images/sonangol-logo.png';
    const headerBackgroundColor = '#F4CF0A';
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
        <p><strong>Nome:</strong> ${funcionario.nome}</p>
          <p><strong>SAP:</strong> ${funcionario.id}</p>
          <p><strong>Função:</strong> ${funcionario.funcao || 'Não especificada'}</p>
          <p><strong>Direção:</strong> ${funcionario.area || 'Não especificada'}</p>
          <p><strong>U.Neg:</strong> ${funcionario.unineg || 'Não especificada'}</p>
          <p><strong>NIF:</strong> ${funcionario.nif || 'Não especificado'}</p>
          <p><strong>Telefone:</strong> ${funcionario.telefone || 'Não especificado'}</p>
        </div>
      </div>
    `;
    setContactCardHtml(htmlContent);
    setContactCardOpen(true);
  };

  const handleCloseContactCard = () => {
    setContactCardOpen(false);
    setContactCardHtml('');
  };

  const handleCloseModal = () => {
    setQrModalOpen(false);
    setQrImage('');
  };

  const handleSelectAll = (checked: boolean) => {
    const visibleRows = paginatedFuncionarios;
    if (checked) {
      const allIds = visibleRows.map((funcionario) => funcionario.id as number);
      setSelectedIds((prevIds) => Array.from(new Set([...prevIds, ...allIds])));
    } else {
      const visibleIds = visibleRows.map((funcionario) => Number(funcionario.id));
      setSelectedIds((prevIds) => prevIds.filter((id) => !visibleIds.includes(id)));
    }
  };

  const handleRowCheckboxChange = (id: number, checked: boolean) => {
    if (checked) {
      setSelectedIds((prevIds) => [...prevIds, id]);
    } else {
      setSelectedIds((prevIds) => prevIds.filter((selectedId) => selectedId !== id));
    }
  };

  const isAllSelected = paginatedFuncionarios.length > 0 && paginatedFuncionarios.every((funcionario) => selectedIds.includes(funcionario.id));
  const isIndeterminate = paginatedFuncionarios.some((funcionario) => selectedIds.includes(funcionario.id)) && !isAllSelected;

  // Datos para las tarjetas de estadísticas
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
      value: funcionariosComQR !== null ? funcionariosComQR.toString() : 'Cargando...',
      trend: 'neutral',
    },
  ];

  return (
    <Box sx={{ width: '100%', maxWidth: { sm: '100%', md: '1700px' } }}>
      {/* Dashboard Statistics */}
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

      {/* Funcionarios Table */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Funcionários com QR
        </Typography>
        <TextField
          fullWidth
          placeholder="Pesquisar por nome, função ou direção..."
          value={filter}
          onChange={(e) => {
            setFilter(e.target.value);
            setPage(1);
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
                      <strong>SAP</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Nome</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Função</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Direção</strong>
                    </TableCell>
                    <TableCell>
                      <strong>NIF</strong>
                    </TableCell>
                    <TableCell>
                      <strong>Telefone</strong>
                    </TableCell>
                    <TableCell align="center">
                      <strong>Ações</strong>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
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
                        <TableCell>{funcionario.id}</TableCell>
                        <TableCell>
                          <Box>
                            <Typography variant="body2" fontWeight="bold">
                              {funcionario.nome}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip label={funcionario.funcao || 'Não especificada'} size="small" />
                        </TableCell>
                        <TableCell>{funcionario.area || 'Não especificada'}</TableCell>
                        <TableCell>{funcionario.nif || 'Não especificado'}</TableCell>
                        <TableCell>{funcionario.telefone || 'Não especificado'}</TableCell>
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
                      <TableCell colSpan={8} align="center">
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

            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 3, p: 2 }}>
              {totalPages > 1 && (
                <Pagination
                  count={totalPages}
                  page={page}
                  onChange={(_, newPage) => setPage(newPage)}
                  color="primary"
                />
              )}
              <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel>Filas por página</InputLabel>
                <Select
                  value={rowsPerPage}
                  label="Filas por página"
                  onChange={(e) => {
                    setRowsPerPage(Number(e.target.value));
                    setPage(1);
                  }}
                >
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={30}>30</MenuItem>
                  <MenuItem value={60}>60</MenuItem>
                </Select>
              </FormControl>
            </Box>
            
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

      {/* Modals */}
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

      <Dialog open={contactCardOpen} onClose={handleCloseContactCard} maxWidth="xs" fullWidth>
        <DialogTitle sx={{ textAlign: 'center' }}>Cartão de Contacto</DialogTitle>
        <DialogContent>
          <div dangerouslySetInnerHTML={{ __html: contactCardHtml }} />
        </DialogContent>
      </Dialog>
    </Box>
  );
}
