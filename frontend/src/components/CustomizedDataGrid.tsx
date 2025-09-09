import { useState, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import type { GridRowsProp, GridColDef } from '@mui/x-data-grid';
import { TextField, Button, Box, CircularProgress, Typography, IconButton, Modal } from '@mui/material';
import QrCodeIcon from '@mui/icons-material/QrCode';
import DeleteIcon from '@mui/icons-material/Delete';
import DownloadIcon from '@mui/icons-material/Download';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import Dialog from '@mui/material/Dialog';
import axiosInstance from '../api/axiosInstance';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

export default function CustomizedDataGrid() {
  const [funcionariosConQR, setFuncionariosConQR] = useState<GridRowsProp>([]);
  const [loading, setLoading] = useState(false);
  const [filterConQR, setFilterConQR] = useState('');
  const [qrModalOpen, setQrModalOpen] = useState(false);
  const [qrImage, setQrImage] = useState('');
  const [contactCardOpen, setContactCardOpen] = useState(false);
  const [contactCardHtml, setContactCardHtml] = useState('');
  const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 10 }); // Track pagination state

  useEffect(() => {
    fetchFuncionariosConQR();
  }, []);

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

  const handleDeleteQR = async (id: number) => {
    setLoading(true);
    try {
      await axiosInstance.delete(`/qr/eliminar/${id}`);
      alert('Código QR eliminado com sucesso.');
      fetchFuncionariosConQR();
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

  const handleViewContactCard = (funcionario: {
    id: number;
    nome: string;
    funcao?: string;
    area?: string;
    nif?: string;
    telefone?: string;
    unineg?: string;
    email?: string;
  }) => {
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
          <p><strong>Direção:</strong> ${funcionario.area || 'Não especificada'}</p>
          <p><strong>NIF:</strong> ${funcionario.nif || 'Não especificado'}</p>
          <p><strong>Telefone:</strong> ${funcionario.telefone || 'Não especificado'}</p>
          <p><strong>Unidad Org:</strong> ${funcionario.unineg || 'Não especificado'}</p>
          <p><strong>Email:</strong> ${funcionario.email || 'Não especificado'}</p>
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

  const handlePaginationChange = (model: { page: number; pageSize: number }) => {
    setPaginationModel(model); // Update pagination state
  };

  const columnsConQR: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 100 },
    { field: 'nome', headerName: 'Nome', width: 150 },
    { field: 'funcao', headerName: 'Função', width: 0 },
    { field: 'area', headerName: 'Área', width: 150 },
    { field: 'nif', headerName: 'NIF', width: 150 },
    { field: 'telefone', headerName: 'Telefone', width: 150 },
    { field: 'unineg', headerName: 'Unidad Organ', width: 150 },
    { field: 'email', headerName: 'Email', width: 200 },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 200,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton color="success" onClick={() => handleViewQR(params.row.id)}>
            <QrCodeIcon />
          </IconButton>
          <IconButton color="error" onClick={() => handleDeleteQR(params.row.id)}>
            <DeleteIcon />
          </IconButton>
          <IconButton color="success" onClick={() => handleDownloadQR(params.row.id)}>
            <DownloadIcon />
          </IconButton>
          <IconButton
            color="info"
            onClick={() => handleViewContactCard(params.row)}
          >
            <OpenInNewIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  const filteredFuncionariosConQR = funcionariosConQR.filter((funcionario) =>
    funcionario?.nome?.toLowerCase().includes(filterConQR.toLowerCase())
  );

  const paginatedFuncionariosConQR = filteredFuncionariosConQR.slice(
    paginationModel.page * paginationModel.pageSize,
    (paginationModel.page + 1) * paginationModel.pageSize
  );

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Funcionários com QR
      </Typography>
      <Box sx={{ mb: 3 }}>
        <TextField
          label="Procurar em funcionários com QR"
          variant="outlined"
          fullWidth
          value={filterConQR}
          onChange={(e) => setFilterConQR(e.target.value)}
        />
      </Box>
      <DataGrid
        checkboxSelection
        rows={paginatedFuncionariosConQR} // Use paginated rows
        columns={columnsConQR}
        pageSizeOptions={[10, 20, 50, 100]} // Enable pagination with these options
        autoHeight
        disableRowSelectionOnClick
        onPaginationModelChange={(model) => handlePaginationChange(model)} // Track pagination changes
        getRowClassName={(params) =>
          params.indexRelativeToCurrentPage % 2 === 0 ? 'even' : 'odd'
        }
      />
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
          {qrImage && <img src={qrImage} alt="QR Code" style={{ maxWidth: '100%', height: 'auto' }} />}
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
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 2 }}>
          <CircularProgress />
        </Box>
      )}
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
}
