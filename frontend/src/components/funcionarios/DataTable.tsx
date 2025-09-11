import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Paper,
  Checkbox,
  IconButton,
  Box,
  Typography,
  Skeleton
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Visibility as ViewIcon } from '@mui/icons-material';

export interface Column {
  id: string;
  label: string;
  align?: 'left' | 'right' | 'center';
  minWidth?: number;
  format?: (value: any) => string;
}

export interface DataTableProps {
  columns: Column[];
  data?: any[];
  loading?: boolean;
  selectable?: boolean;
  selectedItems?: string[];
  onSelectionChange?: (selected: string[]) => void;
  onEdit?: (item: any) => void;
  onDelete?: (item: any) => void;
  onView?: (item: any) => void;
  page: number;
  rowsPerPage: number;
  totalCount: number;
  onPageChange: (event: unknown, newPage: number) => void;
  onRowsPerPageChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  emptyMessage?: string;
  title?: string;
}

const DataTable: React.FC<DataTableProps> = ({
  columns,
  data = [],
  loading = false,
  selectable = false,
  selectedItems = [],
  onSelectionChange,
  onEdit,
  onDelete,
  onView,
  page,
  rowsPerPage,
  totalCount,
  onPageChange,
  onRowsPerPageChange,
  emptyMessage = 'Nenhum registro encontrado',
  title
}) => {
  const handleSelectAll = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (onSelectionChange && data) {
      if (event.target.checked) {
        const newSelected = data.map((item) => item.id.toString());
        onSelectionChange(newSelected);
      } else {
        onSelectionChange([]);
      }
    }
  };

  const handleSelectOne = (id: string) => {
    if (onSelectionChange) {
      const selectedIndex = selectedItems.indexOf(id);
      let newSelected: string[] = [];

      if (selectedIndex === -1) {
        newSelected = newSelected.concat(selectedItems, id);
      } else if (selectedIndex === 0) {
        newSelected = newSelected.concat(selectedItems.slice(1));
      } else if (selectedIndex === selectedItems.length - 1) {
        newSelected = newSelected.concat(selectedItems.slice(0, -1));
      } else if (selectedIndex > 0) {
        newSelected = newSelected.concat(
          selectedItems.slice(0, selectedIndex),
          selectedItems.slice(selectedIndex + 1),
        );
      }
      onSelectionChange(newSelected);
    }
  };

  const isSelected = (id: string) => selectedItems.indexOf(id) !== -1;

  if (loading) {
    return (
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        {title && (
          <Box sx={{ p: 2 }}>
            <Typography variant="h6">{title}</Typography>
          </Box>
        )}
        <TableContainer>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                {selectable && <TableCell padding="checkbox" />}
                {columns.map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align}
                    style={{ minWidth: column.minWidth }}
                  >
                    {column.label}
                  </TableCell>
                ))}
                {(onEdit || onDelete || onView) && <TableCell>Ações</TableCell>}
              </TableRow>
            </TableHead>
            <TableBody>
              {Array.from(new Array(rowsPerPage)).map((_, index) => (
                <TableRow key={index}>
                  {selectable && (
                    <TableCell padding="checkbox">
                      <Skeleton variant="rectangular" width={24} height={24} />
                    </TableCell>
                  )}
                  {columns.map((column) => (
                    <TableCell key={column.id}>
                      <Skeleton variant="text" />
                    </TableCell>
                  ))}
                  {(onEdit || onDelete || onView) && (
                    <TableCell>
                      <Skeleton variant="text" />
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    );
  }

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      {title && (
        <Box sx={{ p: 2 }}>
          <Typography variant="h6">{title}</Typography>
        </Box>
      )}
      <TableContainer>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {selectable && (
                <TableCell padding="checkbox">
                  <Checkbox
                    indeterminate={selectedItems.length > 0 && selectedItems.length < (data?.length || 0)}
                    checked={(data?.length || 0) > 0 && selectedItems.length === (data?.length || 0)}
                    onChange={handleSelectAll}
                  />
                </TableCell>
              )}
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align={column.align}
                  style={{ minWidth: column.minWidth }}
                >
                  {column.label}
                </TableCell>
              ))}
              {(onEdit || onDelete || onView) && <TableCell>Ações</TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {!data || data.length === 0 ? (
              <TableRow>
                <TableCell 
                  colSpan={columns.length + (selectable ? 1 : 0) + ((onEdit || onDelete || onView) ? 1 : 0)}
                  align="center"
                  sx={{ py: 3 }}
                >
                  <Typography variant="body2" color="text.secondary">
                    {emptyMessage}
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              data.map((row) => {
                const isItemSelected = isSelected(row.id.toString());
                return (
                  <TableRow hover key={row.id} selected={isItemSelected}>
                    {selectable && (
                      <TableCell padding="checkbox">
                        <Checkbox
                          checked={isItemSelected}
                          onChange={() => handleSelectOne(row.id.toString())}
                        />
                      </TableCell>
                    )}
                    {columns.map((column) => {
                      const value = row[column.id];
                      return (
                        <TableCell key={column.id} align={column.align}>
                          {column.format ? column.format(value) : value}
                        </TableCell>
                      );
                    })}
                    {(onEdit || onDelete || onView) && (
                      <TableCell>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          {onView && (
                            <IconButton
                              size="small"
                              color="primary"
                              onClick={() => onView(row)}
                              title="Visualizar"
                            >
                              <ViewIcon />
                            </IconButton>
                          )}
                          {onEdit && (
                            <IconButton
                              size="small"
                              color="primary"
                              onClick={() => onEdit(row)}
                              title="Editar"
                            >
                              <EditIcon />
                            </IconButton>
                          )}
                          {onDelete && (
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => onDelete(row)}
                              title="Excluir"
                            >
                              <DeleteIcon />
                            </IconButton>
                          )}
                        </Box>
                      </TableCell>
                    )}
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 50, 100]}
        component="div"
        count={totalCount}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={onPageChange}
        onRowsPerPageChange={onRowsPerPageChange}
        labelRowsPerPage="Registros por página:"
        labelDisplayedRows={({ from, to, count }) => 
          `${from}-${to} de ${count !== -1 ? count : `mais de ${to}`}`
        }
      />
    </Paper>
  );
};

export default DataTable;
