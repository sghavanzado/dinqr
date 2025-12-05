#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para agregar botones de CV
"""

# Leer el archivo
with open('frontend/src/components/MainGrid.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar handlers de CV después de handleViewContactCard
handlers_cv = '''
  // =============================================
  // 📇 HANDLERS PARA CV (Cartão de Visita)
  // =============================================
  const handleViewCVQR = async (id: number) => {
    try {
      const response = await axiosInstance.get(`/cv/qr/${id}`, { responseType: 'blob' });
      const qrBlob = new Blob([response.data], { type: 'image/png' });
      const qrUrl = URL.createObjectURL(qrBlob);
      setQrImage(qrUrl);
      setQrModalOpen(true);
    } catch (error) {
      console.error('Error viewing CV QR code:', error);
      alert('Erro ao mostrar o código QR do CV.');
    }
  };

  const handleDownloadCV = async (id: number) => {
    try {
      const response = await axiosInstance.get(`/cv/qr/${id}`, { responseType: 'blob' });
      const qrBlob = new Blob([response.data], { type: 'image/png' });
      const qrUrl = URL.createObjectURL(qrBlob);
      const link = document.createElement('a');
      link.href = qrUrl;
      link.download = `cv_qr_${id}.png`;
      link.click();
      URL.revokeObjectURL(qrUrl);
    } catch (error) {
      console.error('Error downloading CV QR:', error);
      alert('Erro ao descarregar o QR do CV.');
    }
  };

  const handleViewCVCard = (funcionario: Funcionario) => {
    // Por ahora, abrir en nueva ventana
    window.open(`/cv/${funcionario.id}`, '_blank');
  };

  const handleDeleteCV = async (id: number) => {
    if (!confirm('Tem certeza que deseja eliminar o CV deste funcionário?')) {
      return;
    }
    try {
      await axiosInstance.delete(`/cv/eliminar/${id}`);
      alert('CV eliminado com sucesso.');
      await Promise.all([fetchFuncionarios(), fetchDashboardData(), fetchFuncionariosConCV()]);
    } catch (error) {
      console.error('Error deleting CV:', error);
      alert('Erro ao eliminar o CV.');
    }
  };

'''

# Buscar donde insertar los handlers (después de handleViewContactCard)
marker = '  // =============================================\n  // ❌ HANDLERS PARA CERRAR MODALES\n  // ============================================='
if marker in content:
    content = content.replace(marker, handlers_cv + '\n' + marker)
    print("Handlers de CV agregados")
else:
    print("ERROR: No se encontro el marcador para insertar handlers")

# 2. Agregar botones de CV
old_buttons_section = '''                            {/* QR Normal - Solo si tiene QR Normal */}
                            {funcionariosConQRNormal.includes(String(funcionario.id)) && (
                              <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
                                <Typography variant="caption" sx={{ mr: 1, fontWeight: 'bold', minWidth: '30px' }}>QR:</Typography>
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
                            )}'''

new_buttons_section = '''                            {/* QR Normal - Solo si tiene QR Normal */}
                            {funcionariosConQRNormal.includes(String(funcionario.id)) && (
                              <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
                                <Typography variant="caption" sx={{ mr: 1, fontWeight: 'bold', minWidth: '30px' }}>QR:</Typography>
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
                            )}

                            {/* Cartão de Visita (CV) - Solo si tiene CV */}
                            {funcionariosConCV.includes(String(funcionario.id)) && (
                              <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
                                <Typography variant="caption" sx={{ mr: 1, fontWeight: 'bold', minWidth: '30px', color: '#667eea' }}>CV:</Typography>
                                <IconButton
                                  size="small"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleViewCVQR(funcionario.id);
                                  }}
                                  title="Visualizar QR do CV"
                                  sx={{ color: '#667eea' }}
                                >
                                  <QrCodeIcon fontSize="small" />
                                </IconButton>
                                <IconButton
                                  size="small"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleDownloadCV(funcionario.id);
                                  }}
                                  title="Baixar QR do CV"
                                  sx={{ color: '#667eea' }}
                                >
                                  <DownloadIcon fontSize="small" />
                                </IconButton>
                                <IconButton
                                  size="small"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleViewCVCard(funcionario);
                                  }}
                                  title="Ver Cartão de Visita"
                                  sx={{ color: '#667eea' }}
                                >
                                  <OpenInNewIcon fontSize="small" />
                                </IconButton>
                                <IconButton
                                  size="small"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleDeleteCV(funcionario.id);
                                  }}
                                  title="Eliminar CV"
                                  sx={{ color: '#764ba2' }}
                                >
                                  <DeleteIcon fontSize="small" />
                                </IconButton>
                              </Box>
                            )}'''

if old_buttons_section in content:
    content = content.replace(old_buttons_section, new_buttons_section)
    print("Botones de CV agregados")
else:
    print("ERROR: No se encontro la seccion de botones")

# Guardar
with open('frontend/src/components/MainGrid.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Completado!")
