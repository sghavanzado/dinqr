#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para aplicar SOLO el cambio de botones
"""

# Leer el archivo
with open('frontend/src/components/MainGrid.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Código antiguo de botones (lo que queremos reemplazar)
old_buttons = '''                        <TableCell align="center">
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
                        </TableCell>'''

# Código nuevo de botones (con condicional)
new_buttons = '''                        <TableCell align="center">
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                            {/* QR Normal - Solo si tiene QR Normal */}
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
                          </Box>
                        </TableCell>'''

# Reemplazar
if old_buttons in content:
    content = content.replace(old_buttons, new_buttons)
    print("Botones actualizados correctamente")
else:
    print("ERROR: No se encontro la seccion de botones antigua")
    print("El archivo puede haber sido modificado")

# Guardar
with open('frontend/src/components/MainGrid.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Listo!")
