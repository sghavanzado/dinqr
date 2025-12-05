# SOLUCION FINAL - Instrucciones Manuales

Lo siento mucho por los intentos fallidos. Las ediciones automáticas están corrompiendo el archivo.

## OPCION 1: Usar el script Python (RECOMENDADO)

1. Ejecuta:
```powershell
python aplicar_cambios.py
```

Esto aplicará los cambios 1, 2 y 3 automáticamente.

2. Luego, abre `frontend/src/components/MainGrid.tsx` en VS Code

3. Busca la línea 559 (usa Ctrl+G y escribe 559)

4. Verás esto:
```typescript
<TableCell align="center">
  <Box sx={{ display: 'flex', gap: 0.5 }}>
```

5. Reemplaza TODA la sección desde `<TableCell align="center">` (línea 559) 
   hasta `</TableCell>` (línea 582) con esto:

```typescript
<TableCell align="center">
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
</TableCell>
```

6. Guarda el archivo (Ctrl+S)

7. Refresca el navegador

## OPCION 2: Si el script falla

Abre el archivo `CODIGO_CORRECTO_BOTONES.md` y sigue los 4 pasos manualmente.

## RESULTADO ESPERADO

- Botones de QR Normal solo aparecen si el funcionario tiene QR Normal
- Tienen etiqueta "QR:" en negro
- Los botones de CV se pueden agregar después siguiendo el mismo patrón

---

Nuevamente, disculpas por los intentos fallidos. El archivo es muy grande y las herramientas automáticas tienen dificultades.
