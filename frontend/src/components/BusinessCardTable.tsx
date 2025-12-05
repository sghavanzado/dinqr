// =============================================
// 📋 BusinessCardTable.tsx - TABLA DE FUNCIONARIOS SIN CARTÓN DE VISITA
// =============================================
// Este componente maneja la visualización y generación de cartones de visita
// para funcionarios que aún no tienen cartón asignado.

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

interface BusinessCardTableProps {
  funcionarios?: Funcionario[]; // Props opcional (no utilizado actualmente)
}

const BusinessCardTable: FC<BusinessCardTableProps> = () => {
  // =============================================
  // 📋 ESTADOS PARA FUNCIONARIOS SIN CARTÓN
  // =============================================
  const [funcionariosSinCarton, setFuncionariosSinCarton] = useState<Funcionario[]>([]); // Lista completa
  const [selectedIdsSinCarton, setSelectedIdsSinCarton] = useState<number[]>([]);        // IDs seleccionados
  const [loading, setLoading] = useState(false);                                         // Estado de carga
  const [filterSinCarton, setFilterSinCarton] = useState('');                           // Filtro de búsqueda

  // =============================================
  // 🔥 ESTADOS PARA PAGINACIÓN Y FILAS POR PÁGINA
  // =============================================
  const [pageSinCarton, setPageSinCarton] = useState(1);                               // Página actual (inicia en 1)
  const [rowsPerPageSinCarton, setRowsPerPageSinCarton] = useState(10);                // Filas por página

  // =============================================
  // 🔥 LÓGICA DE FILTRADO Y PAGINACIÓN
  // =============================================
  // Filtrar funcionarios sin cartón basado en el texto de búsqueda
  const filteredFuncionariosSinCarton = funcionariosSinCarton.filter(
    (funcionario) =>
      funcionario.nome.toLowerCase().includes(filterSinCarton.toLowerCase()) ||
      funcionario.funcao?.toLowerCase().includes(filterSinCarton.toLowerCase()) ||
      funcionario.area?.toLowerCase().includes(filterSinCarton.toLowerCase())
  );

  // 🔥 CALCULAR TOTAL DE PÁGINAS BASADO EN FUNCIONARIOS FILTRADOS
  const totalPagesSinCarton = Math.ceil(filteredFuncionariosSinCarton.length / rowsPerPageSinCarton);

  // 🔥 OBTENER FUNCIONARIOS PARA LA PÁGINA ACTUAL (SLICE PAGINADO)
  const paginatedFuncionariosSinCarton = filteredFuncionariosSinCarton.slice(
    (pageSinCarton - 1) * rowsPerPageSinCarton,    // Índice de inicio
    pageSinCarton * rowsPerPageSinCarton           // Índice de fin
  );

  // =============================================
  // 🔄 FUNCIÓN PARA OBTENER FUNCIONARIOS SIN CARTÓN
  // =============================================
  const fetchFuncionariosSinCarton = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/cv/funcionarios-sin-cv');
      if (response.status === 200) {
        setFuncionariosSinCarton(response.data);
      } else {
        console.error('Unexpected response:', response);
        alert('Erro ao carregar funcionários sem Cartão de Visita. Verifique o console para mais detalhes.');
      }
    } catch (error) {
      console.error('Error fetching funcionarios sin Cartón:', error);
      alert('Erro ao carregar funcionários sem Cartão de Visita. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // =============================================
  // 🚀 EFFECT PARA CARGAR DATOS AL MONTAR EL COMPONENTE
  // =============================================
  useEffect(() => {
    fetchFuncionariosSinCarton(); // Cargar funcionarios sin cartón
  }, []);

  // =============================================
  // 🎯 FUNCIÓN PARA GENERAR CARTONES DE VISITA
  // =============================================
  const handleGenerateBusinessCard = async (ids: number[]) => {
    if (!ids || ids.length === 0) {
      alert('Por favor, selecione pelo menos um funcionário para gerar os Cartões de Visita.');
      return;
    }
    setLoading(true);
    try {
      await axiosInstance.post('/cv/generar', { ids });
      alert('Cartões de Visita gerados com sucesso.');
      await fetchFuncionariosSinCarton(); // Recargar lista después de generar
      setSelectedIdsSinCarton([]);        // Limpiar selección
    } catch (error) {
      console.error('Error generating Business Cards:', error);
      alert('Erro ao gerar os Cartões de Visita. Verifique o console para mais detalhes.');
    } finally {
      setLoading(false);
    }
  };

  // =============================================
  // ✅ HANDLERS PARA SELECCIÓN DE FUNCIONARIOS SIN CARTÓN
  // =============================================
  // Handler para seleccionar/deseleccionar todos los funcionarios visibles
  const handleSelectAllSinCarton = (checked: boolean) => {
    const visibleRows = paginatedFuncionariosSinCarton; // 🔥 USA FUNCIONARIOS PAGINADOS
    if (checked) {
      const allIds = visibleRows.map((funcionario) => funcionario.id as number);
      setSelectedIdsSinCarton((prevIds) => Array.from(new Set([...prevIds, ...allIds])));
    } else {
      const visibleIds = visibleRows.map((funcionario) => Number(funcionario.id));
      setSelectedIdsSinCarton((prevIds) => prevIds.filter((id) => !visibleIds.includes(id)));
    }
  };

  // Handler para seleccionar/deseleccionar un funcionario individual
  const handleRowCheckboxChangeSinCarton = (id: number, checked: boolean) => {
    if (checked) {
      setSelectedIdsSinCarton((prevIds) => [...prevIds, id]);
    } else {
      setSelectedIdsSinCarton((prevIds) => prevIds.filter((selectedId) => selectedId !== id));
    }
  };

  // =============================================
  // 🔍 LÓGICA PARA DETERMINAR ESTADO DE SELECCIÓN
  // =============================================
  // Verificar si todos los funcionarios visibles están seleccionados
  const isAllSelectedSinCarton = paginatedFuncionariosSinCarton.length > 0 && paginatedFuncionariosSinCarton.every((funcionario) => selectedIdsSinCarton.includes(funcionario.id));
  // Verificar si algunos (pero no todos) funcionarios visibles están seleccionados
  const isIndeterminateSinCarton = paginatedFuncionariosSinCarton.some((funcionario) => selectedIdsSinCarton.includes(funcionario.id)) && !isAllSelectedSinCarton;

  return (
    <Box>

      {/* ============================================= */}
      {/* 📋 TABLA: Funcionários sem Cartão de Visita */}
      {/* ============================================= */}
      <Paper sx={{ p: 3, backgroundColor: '#f8f9ff' }}>
        <Typography variant="h6" gutterBottom sx={{ color: '#667eea' }}>
          📇 Funcionários sem Cartão de Visita
        </Typography>

        {/* Barra de búsqueda */}
        <Box sx={{ mb: 2 }}>
          <TextField
            fullWidth
            placeholder="Pesquisar por nome, função ou direção..."
            value={filterSinCarton}
            onChange={(e) => {
              setFilterSinCarton(e.target.value);
              setPageSinCarton(1); // 🔥 RESETEAR A PÁGINA 1 AL FILTRAR
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
                        checked={isAllSelectedSinCarton}
                        indeterminate={isIndeterminateSinCarton}
                        onChange={(e) => handleSelectAllSinCarton(e.target.checked)}
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
                  {paginatedFuncionariosSinCarton.length > 0 ? (
                    /* 🔥 ITERAR SOBRE FUNCIONARIOS PAGINADOS */
                    paginatedFuncionariosSinCarton.map((funcionario) => (
                      <TableRow
                        key={funcionario.id}
                        hover
                        onClick={() => handleRowCheckboxChangeSinCarton(funcionario.id, !selectedIdsSinCarton.includes(funcionario.id))}
                        sx={{ cursor: 'pointer', backgroundColor: selectedIdsSinCarton.includes(funcionario.id) ? 'rgba(102, 126, 234, 0.1)' : 'inherit' }}
                      >
                        <TableCell padding="checkbox">
                          <Checkbox
                            checked={selectedIdsSinCarton.includes(funcionario.id)}
                            onChange={(e) => handleRowCheckboxChangeSinCarton(funcionario.id, e.target.checked)}
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
                          <Chip label={funcionario.funcao || 'Não especificada'} size="small" color="primary" variant="outlined" />
                        </TableCell>
                        <TableCell>{funcionario.area || 'Não especificada'}</TableCell>
                        <TableCell>{funcionario.nif || 'Não especificado'}</TableCell>
                        <TableCell>{funcionario.telefone || 'Não especificado'}</TableCell>
                        <TableCell align="center">
                          <IconButton
                            size="small"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleGenerateBusinessCard([funcionario.id]);
                            }}
                            title="Gerar Cartão de Visita"
                            sx={{ color: '#667eea' }}
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
                            Nenhum funcionário sem Cartão de Visita encontrado.
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
              {totalPagesSinCarton > 1 && (
                <Pagination
                  count={totalPagesSinCarton}                    // Total de páginas calculado
                  page={pageSinCarton}                           // Página actual
                  onChange={(_, newPage) => setPageSinCarton(newPage)}  // Handler para cambio de página
                  color="primary"
                />
              )}

              {/* 🔥 SELECTOR DE FILAS POR PÁGINA */}
              <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel>Filas por página</InputLabel>
                <Select
                  value={rowsPerPageSinCarton}
                  label="Filas por página"
                  onChange={(e) => {
                    setRowsPerPageSinCarton(Number(e.target.value));
                    setPageSinCarton(1); // 🔥 RESETEAR A PÁGINA 1 AL CAMBIAR FILAS POR PÁGINA
                  }}
                >
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={30}>30</MenuItem>
                  <MenuItem value={60}>60</MenuItem>
                </Select>
              </FormControl>
            </Box>

            {/* ============================================= */}
            {/* 🎯 BOTÓN PARA GENERAR CARTONES DE FUNCIONARIOS SELECCIONADOS */}
            {/* ============================================= */}
            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                onClick={() => handleGenerateBusinessCard(selectedIdsSinCarton)}
                disabled={selectedIdsSinCarton.length === 0}
                startIcon={<QrCodeIcon />}
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5568d3 0%, #654091 100%)',
                  }
                }}
              >
                Gerar Selecionados ({selectedIdsSinCarton.length})
              </Button>
            </Box>
          </>
        )}
      </Paper>
      {/* ============================================= */}
      {/* 📋 FIN TABLA: Funcionários sem Cartão de Visita */}
      {/* ============================================= */}
    </Box>
  );
};

export default BusinessCardTable;
