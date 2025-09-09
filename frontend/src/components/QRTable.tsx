// =============================================
// 📋 QRTable.tsx - TABLA DE FUNCIONARIOS SIN QR
// =============================================
// Este componente maneja la visualización y generación de códigos QR
// para funcionarios que aún no tienen QR asignado.

import { useState, useEffect } from 'react';
import type { FC } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  CircularProgress,
  IconButton,
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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import QrCodeIcon from '@mui/icons-material/QrCode';
import SearchIcon from '@mui/icons-material/Search';
import axiosInstance from '../api/axiosInstance';
import type { Funcionario } from '../types/Funcionario';
import Checkbox from '@mui/material/Checkbox';

interface QRTableProps {
  funcionarios?: Funcionario[]; // Props opcional (no utilizado actualmente)
}

const QRTable: FC<QRTableProps> = () => {
  // =============================================
  // 📋 ESTADOS PARA FUNCIONARIOS SIN QR
  // =============================================
  const [funcionariosSinQR, setFuncionariosSinQR] = useState<Funcionario[]>([]); // Lista completa
  const [selectedIdsSinQR, setSelectedIdsSinQR] = useState<number[]>([]);        // IDs seleccionados
  const [loading, setLoading] = useState(false);                                 // Estado de carga
  const [filterSinQR, setFilterSinQR] = useState('');                           // Filtro de búsqueda

  // =============================================
  // 🔥 ESTADOS PARA PAGINACIÓN Y FILAS POR PÁGINA
  // =============================================
  const [pageSinQR, setPageSinQR] = useState(1);                               // Página actual (inicia en 1)
  const [rowsPerPageSinQR, setRowsPerPageSinQR] = useState(10);                // Filas por página

  // =============================================
  // 🔥 LÓGICA DE FILTRADO Y PAGINACIÓN
  // =============================================
  // Filtrar funcionarios sin QR basado en el texto de búsqueda
  const filteredFuncionariosSinQR = funcionariosSinQR.filter(
    (funcionario) =>
      funcionario.nome.toLowerCase().includes(filterSinQR.toLowerCase()) ||
      funcionario.funcao?.toLowerCase().includes(filterSinQR.toLowerCase()) ||
      funcionario.area?.toLowerCase().includes(filterSinQR.toLowerCase())
  );

  // 🔥 CALCULAR TOTAL DE PÁGINAS BASADO EN FUNCIONARIOS FILTRADOS
  const totalPagesSinQR = Math.ceil(filteredFuncionariosSinQR.length / rowsPerPageSinQR);

  // 🔥 OBTENER FUNCIONARIOS PARA LA PÁGINA ACTUAL (SLICE PAGINADO)
  const paginatedFuncionariosSinQR = filteredFuncionariosSinQR.slice(
    (pageSinQR - 1) * rowsPerPageSinQR,    // Índice de inicio
    pageSinQR * rowsPerPageSinQR           // Índice de fin
  );

  // =============================================
  // 🔄 FUNCIÓN PARA OBTENER FUNCIONARIOS SIN QR
  // =============================================
  const fetchFuncionariosSinQR = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/qr/funcionarios-sin-qr');
      if (response.status === 200) {
        setFuncionariosSinQR(response.data);
      } else {
        console.error('Unexpected response:', response);
        alert('Erro ao carregar funcionários sem QR. Verifique o console para mais detalhes.');
      }
    } catch (error) {
      console.error('Error fetching funcionarios sin QR:', error);
      alert('Erro ao carregar funcionários sem QR. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // =============================================
  // 🚀 EFFECT PARA CARGAR DATOS AL MONTAR EL COMPONENTE
  // =============================================
  useEffect(() => {
    fetchFuncionariosSinQR(); // Cargar funcionarios sin QR
  }, []);

  // =============================================
  // 🎯 FUNCIÓN PARA GENERAR CÓDIGOS QR
  // =============================================
  const handleGenerateQR = async (ids: number[]) => {
    if (!ids || ids.length === 0) {
      alert('Por favor, selecione pelo menos um funcionário para gerar os códigos QR.');
      return;
    }
    setLoading(true);
    try {
      await axiosInstance.post('/qr/generar', { ids });
      alert('Códigos QR gerados com sucesso.');
      await fetchFuncionariosSinQR(); // Recargar lista después de generar QR
      setSelectedIdsSinQR([]);        // Limpiar selección
    } catch (error) {
      console.error('Error generating QR codes:', error);
      alert('Erro ao gerar os códigos QR. Verifique o console para mais detalhes.');
    } finally {
      setLoading(false);
    }
  };

  // =============================================
  // ✅ HANDLERS PARA SELECCIÓN DE FUNCIONARIOS SIN QR
  // =============================================
  // Handler para seleccionar/deseleccionar todos los funcionarios visibles
  const handleSelectAllSinQR = (checked: boolean) => {
    const visibleRows = paginatedFuncionariosSinQR; // 🔥 USA FUNCIONARIOS PAGINADOS
    if (checked) {
      const allIds = visibleRows.map((funcionario) => funcionario.id as number);
      setSelectedIdsSinQR((prevIds) => Array.from(new Set([...prevIds, ...allIds])));
    } else {
      const visibleIds = visibleRows.map((funcionario) => Number(funcionario.id));
      setSelectedIdsSinQR((prevIds) => prevIds.filter((id) => !visibleIds.includes(id)));
    }
  };

  // Handler para seleccionar/deseleccionar un funcionario individual
  const handleRowCheckboxChangeSinQR = (id: number, checked: boolean) => {
    if (checked) {
      setSelectedIdsSinQR((prevIds) => [...prevIds, id]);
    } else {
      setSelectedIdsSinQR((prevIds) => prevIds.filter((selectedId) => selectedId !== id));
    }
  };

  // =============================================
  // 🔍 LÓGICA PARA DETERMINAR ESTADO DE SELECCIÓN
  // =============================================
  // Verificar si todos los funcionarios visibles están seleccionados
  const isAllSelectedSinQR = paginatedFuncionariosSinQR.length > 0 && paginatedFuncionariosSinQR.every((funcionario) => selectedIdsSinQR.includes(funcionario.id));
  // Verificar si algunos (pero no todos) funcionarios visibles están seleccionados
  const isIndeterminateSinQR = paginatedFuncionariosSinQR.some((funcionario) => selectedIdsSinQR.includes(funcionario.id)) && !isAllSelectedSinQR;

  return (
    <Box>
  
      {/* ============================================= */}
      {/* 📋 TABLA: Funcionários sem QR */}
      {/* ============================================= */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Funcionários sem QR
        </Typography>
        
        {/* Barra de búsqueda */}
        <Box sx={{ mb: 2 }}>
          <TextField
            fullWidth
            placeholder="Pesquisar por nome, função ou direção..."
            value={filterSinQR}
            onChange={(e) => {
              setFilterSinQR(e.target.value);
              setPageSinQR(1); // 🔥 RESETEAR A PÁGINA 1 AL FILTRAR
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Box>
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
                        checked={isAllSelectedSinQR}
                        indeterminate={isIndeterminateSinQR}
                        onChange={(e) => handleSelectAllSinQR(e.target.checked)}
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
                  {/* 🔥 RENDERIZAR SOLO LOS FUNCIONARIOS PAGINADOS */}
                  {paginatedFuncionariosSinQR.length > 0 ? (
                    /* 🔥 ITERAR SOBRE FUNCIONARIOS PAGINADOS */
                    paginatedFuncionariosSinQR.map((funcionario) => (
                      <TableRow
                        key={funcionario.id}
                        hover
                        onClick={() => handleRowCheckboxChangeSinQR(funcionario.id, !selectedIdsSinQR.includes(funcionario.id))}
                        sx={{ cursor: 'pointer', backgroundColor: selectedIdsSinQR.includes(funcionario.id) ? 'rgba(0, 0, 0, 0.04)' : 'inherit' }}
                      >
                        <TableCell padding="checkbox">
                          <Checkbox
                            checked={selectedIdsSinQR.includes(funcionario.id)}
                            onChange={(e) => handleRowCheckboxChangeSinQR(funcionario.id, e.target.checked)}
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
                          <IconButton
                            size="small"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleGenerateQR([funcionario.id]);
                            }}
                            title="Gerar QR"
                            color="primary"
                          >
                            <QrCodeIcon fontSize="small" />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={8} align="center">
                        <Box sx={{ py: 4 }}>
                          <QrCodeIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                          <Typography variant="h6" color="text.secondary">
                            Nenhum funcionário sem QR encontrado.
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
              {totalPagesSinQR > 1 && (
                <Pagination
                  count={totalPagesSinQR}                    // Total de páginas calculado
                  page={pageSinQR}                           // Página actual
                  onChange={(_, newPage) => setPageSinQR(newPage)}  // Handler para cambio de página
                  color="primary"
                />
              )}
              
              {/* 🔥 SELECTOR DE FILAS POR PÁGINA */}
              <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel>Filas por página</InputLabel>
                <Select
                  value={rowsPerPageSinQR}
                  label="Filas por página"
                  onChange={(e) => {
                    setRowsPerPageSinQR(Number(e.target.value));
                    setPageSinQR(1); // 🔥 RESETEAR A PÁGINA 1 AL CAMBIAR FILAS POR PÁGINA
                  }}
                >
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={30}>30</MenuItem>
                  <MenuItem value={60}>60</MenuItem>
                </Select>
              </FormControl>
            </Box>

            {/* ============================================= */}
            {/* 🎯 BOTÓN PARA GENERAR QR DE FUNCIONARIOS SELECCIONADOS */}
            {/* ============================================= */}
            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                onClick={() => handleGenerateQR(selectedIdsSinQR)}
                disabled={selectedIdsSinQR.length === 0}
                startIcon={<QrCodeIcon />}
              >
                Gerar Selecionados ({selectedIdsSinQR.length})
              </Button>
            </Box>
          </>
        )}
      </Paper>
      {/* ============================================= */}
      {/* 📋 FIN TABLA: Funcionários sem QR */}
      {/* ============================================= */}
    </Box>
  );
};

export default QRTable;
