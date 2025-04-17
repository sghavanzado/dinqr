import React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box } from '@mui/material';

interface CustomizedDataGridProps {
  rows: any[];
  columns: GridColDef[];
}

const CustomizedDataGrid: React.FC<CustomizedDataGridProps> = ({ rows, columns }) => {
  return (
    <Box sx={{ height: 600, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10, 20, 50]}
        disableSelectionOnClick
        getRowId={(row) => row.id} // Ensure unique row IDs
      />
    </Box>
  );
};

export default CustomizedDataGrid;
