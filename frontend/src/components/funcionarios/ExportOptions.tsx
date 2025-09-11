import React, { useState } from 'react';
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Checkbox,
  FormGroup,
  Box
} from '@mui/material';
import {
  GetApp as ExportIcon,
  PictureAsPdf as PdfIcon,
  TableChart as ExcelIcon,
  Description as CsvIcon
} from '@mui/icons-material';

export interface ExportColumn {
  key: string;
  label: string;
  selected?: boolean;
}

export interface ExportOptionsProps {
  data: any[];
  filename?: string;
  columns?: ExportColumn[];
  onExport?: (format: 'pdf' | 'excel' | 'csv', selectedColumns?: string[]) => Promise<void>;
  disabled?: boolean;
  loading?: boolean;
}

const ExportOptions: React.FC<ExportOptionsProps> = ({
  data = [],
  filename = 'export',
  columns = [],
  onExport,
  disabled = false,
  loading = false
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedFormat, setSelectedFormat] = useState<'pdf' | 'excel' | 'csv'>('excel');
  const [selectedColumns, setSelectedColumns] = useState<string[]>(
    columns.filter(col => col.selected !== false).map(col => col.key)
  );
  const [isExporting, setIsExporting] = useState(false);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleQuickExport = async (format: 'pdf' | 'excel' | 'csv') => {
    handleClose();
    if (onExport) {
      try {
        setIsExporting(true);
        await onExport(format);
      } finally {
        setIsExporting(false);
      }
    } else {
      // Default export behavior
      await defaultExport(format, data, filename);
    }
  };

  const handleAdvancedExport = () => {
    handleClose();
    setDialogOpen(true);
  };

  const handleDialogExport = async () => {
    if (onExport) {
      try {
        setIsExporting(true);
        await onExport(selectedFormat, selectedColumns);
      } finally {
        setIsExporting(false);
      }
    } else {
      // Default export behavior with selected columns
      const filteredData = data.map(row => {
        const filteredRow: any = {};
        selectedColumns.forEach(key => {
          filteredRow[key] = row[key];
        });
        return filteredRow;
      });
      await defaultExport(selectedFormat, filteredData, filename);
    }
    setDialogOpen(false);
  };

  const defaultExport = async (format: 'pdf' | 'excel' | 'csv', exportData: any[], fileName: string) => {
    // This is a basic implementation - in a real app you'd use libraries like jsPDF, xlsx, etc.
    if (format === 'csv') {
      const csv = convertToCSV(exportData);
      downloadFile(csv, `${fileName}.csv`, 'text/csv');
    } else if (format === 'excel') {
      // Placeholder for Excel export - you'd use a library like xlsx
      console.log('Excel export would be implemented with xlsx library');
    } else if (format === 'pdf') {
      // Placeholder for PDF export - you'd use a library like jsPDF
      console.log('PDF export would be implemented with jsPDF library');
    }
  };

  const convertToCSV = (data: any[]): string => {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvContent = [
      headers.join(','),
      ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
    ].join('\n');
    
    return csvContent;
  };

  const downloadFile = (content: string, fileName: string, mimeType: string) => {
    const blob = new Blob([content], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  const handleColumnToggle = (columnKey: string) => {
    setSelectedColumns(prev => 
      prev.includes(columnKey)
        ? prev.filter(key => key !== columnKey)
        : [...prev, columnKey]
    );
  };

  const open = Boolean(anchorEl);

  return (
    <>
      <Button
        variant="outlined"
        startIcon={isExporting ? <CircularProgress size={16} /> : <ExportIcon />}
        onClick={handleClick}
        disabled={disabled || loading || isExporting || data.length === 0}
      >
        {isExporting ? 'Exportando...' : 'Exportar'}
      </Button>

      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={() => handleQuickExport('excel')}>
          <ListItemIcon>
            <ExcelIcon color="success" />
          </ListItemIcon>
          <ListItemText>Excel (.xlsx)</ListItemText>
        </MenuItem>
        <MenuItem onClick={() => handleQuickExport('csv')}>
          <ListItemIcon>
            <CsvIcon color="info" />
          </ListItemIcon>
          <ListItemText>CSV (.csv)</ListItemText>
        </MenuItem>
        <MenuItem onClick={() => handleQuickExport('pdf')}>
          <ListItemIcon>
            <PdfIcon color="error" />
          </ListItemIcon>
          <ListItemText>PDF (.pdf)</ListItemText>
        </MenuItem>
        {columns.length > 0 && (
          <MenuItem onClick={handleAdvancedExport}>
            <ListItemIcon>
              <ExportIcon />
            </ListItemIcon>
            <ListItemText>Opções Avançadas...</ListItemText>
          </MenuItem>
        )}
      </Menu>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Opções de Exportação</DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 3 }}>
            <FormControl component="fieldset">
              <FormLabel component="legend">Formato</FormLabel>
              <RadioGroup
                value={selectedFormat}
                onChange={(e) => setSelectedFormat(e.target.value as 'pdf' | 'excel' | 'csv')}
              >
                <FormControlLabel value="excel" control={<Radio />} label="Excel (.xlsx)" />
                <FormControlLabel value="csv" control={<Radio />} label="CSV (.csv)" />
                <FormControlLabel value="pdf" control={<Radio />} label="PDF (.pdf)" />
              </RadioGroup>
            </FormControl>
          </Box>

          {columns.length > 0 && (
            <Box>
              <FormLabel component="legend" sx={{ mb: 2 }}>
                Colunas para Exportar
              </FormLabel>
              <FormGroup>
                {columns.map((column) => (
                  <FormControlLabel
                    key={column.key}
                    control={
                      <Checkbox
                        checked={selectedColumns.includes(column.key)}
                        onChange={() => handleColumnToggle(column.key)}
                      />
                    }
                    label={column.label}
                  />
                ))}
              </FormGroup>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancelar</Button>
          <Button
            onClick={handleDialogExport}
            variant="contained"
            disabled={selectedColumns.length === 0 || isExporting}
            startIcon={isExporting ? <CircularProgress size={16} /> : undefined}
          >
            {isExporting ? 'Exportando...' : 'Exportar'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ExportOptions;
