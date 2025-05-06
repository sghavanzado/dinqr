// QRTable.tsx

import { FC, useState, useEffect } from 'react';
import { DataGrid, GridRowParams, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { TextField, Button, Box, CircularProgress, Typography, IconButton, Modal, Tooltip } from '@mui/material';
import QrCodeIcon from '@mui/icons-material/QrCode';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import DownloadIcon from '@mui/icons-material/Download';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import axiosInstance from '../api/axiosInstance';
import Checkbox from '@mui/material/Checkbox';

interface Funcionario {
  id: string;
  nome: string;
  funcao?: string;
  area?: string;
  nif?: string;
  telefone?: string;
  uo?: string;
  firma?: string; // Added to differentiate static and dynamic QR codes
}

interface QRTableProps {
  funcionarios: Funcionario[];
}

const QRTable: FC<QRTableProps> = ({ funcionarios }) => {
  const [funcionariosConQR, setFuncionariosConQR] = useState<Funcionario[]>(funcionarios);
  const [funcionariosSinQR, setFuncionariosSinQR] = useState<Funcionario[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [filterConQR, setFilterConQR] = useState('');
  const [filterSinQR, setFilterSinQR] = useState('');
  const [showSinQRTable, setShowSinQRTable] = useState(false);
  const [qrModalOpen, setQrModalOpen] = useState(false);
  const [qrImage, setQrImage] = useState('');
  const [contactCardOpen, setContactCardOpen] = useState(false);
  const [contactCardHtml, setContactCardHtml] = useState('');

  useEffect(() => {
    setFuncionariosConQR(funcionarios);
  }, [funcionarios]);

  const fetchFuncionariosConQR = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/qr/funcionarios');
      setFuncionariosConQR(response.data);
    } catch (error) {
      console.error('Error fetching funcionarios con QR:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchFuncionariosSinQR = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/qr/funcionarios-sin-qr');
      setFuncionariosSinQR(response.data);
    } catch (error) {
      console.error('Error fetching funcionarios sin QR:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSinQRTable = () => {
    setShowSinQRTable((prev) => !prev);
    if (!showSinQRTable) {
      fetchFuncionariosSinQR();
    }
  };

  const handleGenerateQR = async (ids: number[]) => {
    if (!ids || ids.length === 0) {
      alert('Por favor, selecione pelo menos um funcionário para gerar os códigos QR.');
      return;
    }

    console.log('Gerando QR para os seguintes IDs:', ids);

    setLoading(true);
    try {
      await axiosInstance.post('/qr/generar', { ids });
      alert('Códigos QR gerados com sucesso.');
      fetchFuncionariosConQR();
      fetchFuncionariosSinQR();
    } catch (error) {
      console.error('Error generating QR codes:', error);
      alert('Erro ao gerar os códigos QR.');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateStaticQR = async (ids: number[]) => {
    if (!ids || ids.length === 0) {
      alert('Por favor, selecione pelo menos um funcionário para gerar os códigos QR estáticos.');
      return;
    }

    console.log('Gerando QR estático para os seguintes IDs:', ids);

    setLoading(true);
    try {
      await axiosInstance.post('/qr/generar-estatico', { ids });
      alert('Códigos QR estáticos gerados com sucesso.');
      fetchFuncionariosConQR();
      fetchFuncionariosSinQR();
    } catch (error) {
      console.error('Error generating static QR codes:', error);
      alert('Erro ao gerar os códigos QR estáticos.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteQR = async (id: number) => {
    setLoading(true);
    try {
      await axiosInstance.delete(`/qr/eliminar/${id}`);
      alert('Código QR eliminado com sucesso.');
      fetchFuncionariosConQR();
      fetchFuncionariosSinQR();
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
      const response = await axiosInstance.get(`/qr/descargar/${id}`, {
        responseType: 'blob',
      });
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
    const logoUrl = '/static/images/sonangol-logo.png'; // Ruta estática para o logo fornecido
    const headerBackgroundColor = '#F4CF0A'; // Amarelo do logo fornecido
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
          <p><strong>Área:</strong> ${funcionario.area || 'Não especificada'}</p>
          <p><strong>NIF:</strong> ${funcionario.nif || 'Não especificado'}</p>
          <p><strong>Telefone:</strong> ${funcionario.telefone || 'Não especificado'}</p>
          <p><strong>Unidad Org:</strong> ${funcionario.uo || 'Não especificado'}</p>
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

  const handleRowClickSinQR = (params: GridRowParams) => {
    const id = params.row.id as number;
    const isSelected = selectedIds.includes(id);

    if (isSelected) {
      setSelectedIds(prevIds => prevIds.filter(selectedId => selectedId !== id));
    } else {
      setSelectedIds(prevIds => [...prevIds, id]);
    }
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      const allIds = funcionariosSinQR.map((funcionario) => funcionario.id as number);
      setSelectedIds(allIds);
    } else {
      setSelectedIds([]);
    }
  };

  const handleSelectAllConQR = (checked: boolean) => {
    if (checked) {
      const allIds = funcionariosConQR.map((funcionario) => funcionario.id as number);
      setSelectedIds(allIds);
    } else {
      setSelectedIds([]);
    }
  };

  const columnsConQR = [
    {
      field: 'selection',
      headerName: (
        <Checkbox
          indeterminate={selectedIds.length > 0 && selectedIds.length < funcionariosConQR.length}
          checked={selectedIds.length === funcionariosConQR.length}
          onChange={(event) => handleSelectAllConQR(event.target.checked)}
        />
      ),
      width: 50,
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <Checkbox
          checked={selectedIds.includes(params.row.id as number)}
          onClick={(event) => {
            event.stopPropagation();
            const id = params.row.id as number;
            const isSelected = selectedIds.includes(id);
            if (isSelected) {
              setSelectedIds((prevIds) => prevIds.filter((selectedId) => selectedId !== id));
            } else {
              setSelectedIds((prevIds) => [...prevIds, id]);
            }
          }}
        />
      ),
    },
    { field: 'id', headerName: 'ID', width: 100 },
    { field: 'nome', headerName: 'Nome', width: 200 },
    { field: 'funcao', headerName: 'Função', width: 200 },
    { field: 'area', headerName: 'Área', width: 150 },
    { field: 'nif', headerName: 'NIF', width: 200 },
    { field: 'telefone', headerName: 'Telefone', width: 150 },
    { field: 'uo', headerName: 'Unidad Organ', width: 150 },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 300,
      renderCell: (params: GridRenderCellParams) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Ver QR">
            <IconButton
              color={params.row.firma === 'static' ? 'default' : 'success'} // Black for static, green for dynamic
              onClick={() => handleViewQR(params.row.id)}
            >
              <QrCodeIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Eliminar QR">
            <IconButton
              color="error"
              onClick={() => handleDeleteQR(params.row.id)}
            >
              <DeleteIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Descargar QR">
            <IconButton
              color="success"
              onClick={() => handleDownloadQR(params.row.id)}
            >
              <DownloadIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Ver Contact Card">
            <IconButton
              color="info"
              onClick={() => handleViewContactCard(params.row)}
            >
              <OpenInNewIcon />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  const columnsSinQR: GridColDef[] = [
    {
      field: 'selection',
      headerName: (
        <Checkbox
          indeterminate={selectedIds.length > 0 && selectedIds.length < funcionariosSinQR.length}
          checked={selectedIds.length === funcionariosSinQR.length}
          onChange={(event) => handleSelectAll(event.target.checked)}
        />
      ),
      width: 50,
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <Checkbox
          checked={selectedIds.includes(params.row.id as number)}
          onClick={(event) => {
            event.stopPropagation();
            const id = params.row.id as number;
            const isSelected = selectedIds.includes(id);
            if (isSelected) {
              setSelectedIds((prevIds) => prevIds.filter((selectedId) => selectedId !== id));
            } else {
              setSelectedIds((prevIds) => [...prevIds, id]);
            }
          }}
        />
      ),
    },
    { field: 'id', headerName: 'SAP', width: 100 },
    { field: 'nome', headerName: 'Nome', width: 200 },
    { field: 'funcao', headerName: 'Função', width: 200 },
    { field: 'Area', headerName: 'Área', width: 150 },
    { field: 'nif', headerName: 'NIF', width: 200 },
    { field: 'telefone', headerName: 'Telefone', width: 150 },
    { field: 'uo', headerName: 'Unidad Organ', width: 150 },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Tooltip title="Gerar QR Dinâmico">
            <IconButton
              color="primary"
              onClick={() => handleGenerateQR([params.row.id])}
            >
              <QrCodeIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Gerar QR Estático">
            <IconButton
              sx={{ color: 'black' }}
              onClick={() => handleGenerateStaticQR([params.row.id])}
            >
              <QrCodeIcon />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  const filteredFuncionariosConQR = funcionariosConQR.filter((funcionario) =>
    funcionario.nome.toLowerCase().includes(filterConQR.toLowerCase())
  );

  const filteredFuncionariosSinQR = funcionariosSinQR.filter((funcionario) =>
    funcionario.nome.toLowerCase().includes(filterSinQR.toLowerCase())
  );

  console.log('QRTable rendered with selectedIds (with checkbox):', selectedIds);

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Funcionários com QR
      </Typography>
      <Box sx={{ mb: 3, position: 'relative' }}>
        <TextField
          label="Procurar em funcionários com QR"
          variant="outlined"
          fullWidth
          value={filterConQR}
          onChange={(e) => setFilterConQR(e.target.value)}
        />
        <DataGrid
          rows={filteredFuncionariosConQR}
          columns={columnsConQR}
          initialState={{
            pagination: {
              paginationModel: { pageSize: 10 },
            },
          }}
          pageSizeOptions={[10, 20, 50]}
          autoHeight
          disableRowSelectionOnClick
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleToggleSinQRTable}
          sx={{
            position: 'absolute',
            bottom: -70,
            right: 16,
            width: 56,
            height: 56,
            borderRadius: '50%',
            minWidth: 0,
          }}
        >
          {showSinQRTable ? <RemoveIcon /> : <AddIcon />}
        </Button>
      </Box>
      {showSinQRTable && (
        <Box sx={{ mt: 5 }}>
          <Typography variant="h6" gutterBottom>
            Funcionários sem QR
          </Typography>
          <TextField
            label="Procurar em funcionários sem QR"
            variant="outlined"
            fullWidth
            value={filterSinQR}
            onChange={(e) => setFilterSinQR(e.target.value)}
            sx={{ mb: 3 }}
          />
          {loading ? (
            <CircularProgress />
          ) : (
            <>
              <DataGrid
                rows={filteredFuncionariosSinQR}
                columns={columnsSinQR}
                initialState={{
                  pagination: {
                    paginationModel: { pageSize: 10 },
                  },
                }}
                paginationModel={{ page: 0, pageSize: 10 }}
                pageSizeOptions={[10, 20, 50]}
                autoHeight
                disableRowSelectionOnClick
                onRowClick={handleRowClickSinQR}
                getRowClassName={(params) => (selectedIds.includes(params.row.id as number) ? 'Mui-selected' : '')}
              />
              <Box sx={{ mt: 3, textAlign: 'right', display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                <Button
                  variant="contained"
                  onClick={() => handleGenerateQR(selectedIds)}
                  disabled={selectedIds.length === 0}
                  startIcon={<QrCodeIcon />}
                  sx={{
                    fontSize: '0.9rem',
                    padding: '6px 12px',
                    borderRadius: '4px',
                    textTransform: 'none',
                    backgroundColor: selectedIds.length === 0 ? '#d3d3d3' : '#1976d2',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: selectedIds.length === 0 ? '#d3d3d3' : '#1565c0',
                    },
                  }}
                >
                  Gerar Dinâmico
                </Button>
                <Button
                  variant="contained"
                  onClick={() => handleGenerateStaticQR(selectedIds)}
                  disabled={selectedIds.length === 0}
                  startIcon={<QrCodeIcon />}
                  sx={{
                    fontSize: '0.9rem',
                    padding: '6px 12px',
                    borderRadius: '4px',
                    textTransform: 'none',
                    backgroundColor: selectedIds.length === 0 ? '#d3d3d3' : '#000000',
                    color: 'white',
                    '&:hover': {
                      backgroundColor: selectedIds.length === 0 ? '#d3d3d3' : '#333333',
                    },
                  }}
                >
                  Gerar Estático
                </Button>
              </Box>
            </>
          )}
        </Box>
      )}
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
          <Button
            variant="contained"
            color="primary"
            onClick={handleCloseModal}
            sx={{ mt: 2 }}
          >
            Fechar
          </Button>
        </Box>
      </Modal>
      <Dialog 
        open={contactCardOpen} 
        onClose={handleCloseContactCard} 
        maxWidth="xs" 
        fullWidth
      >
        <DialogTitle sx={{ textAlign: 'center' }}></DialogTitle>
        <DialogContent>
          <div dangerouslySetInnerHTML={{ __html: contactCardHtml }} />
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default QRTable;