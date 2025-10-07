import React, { useState } from 'react';
import {
  Box,
  TextField,
  InputAdornment,
  IconButton,
  Chip,
  Typography,
  Collapse,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Clear as ClearIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon
} from '@mui/icons-material';

export interface FilterField {
  key: string;
  label: string;
  type: 'text' | 'select' | 'date' | 'dateRange';
  options?: { value: any; label: string }[];
  placeholder?: string;
}

export interface SearchFilterProps {
  searchTerm: string;
  onSearchChange: (value: string) => void;
  filters: Record<string, any>;
  onFiltersChange: (filters: Record<string, any>) => void;
  filterFields?: FilterField[];
  onClearAll: () => void;
  loading?: boolean;
  placeholder?: string;
}

const SearchFilter: React.FC<SearchFilterProps> = ({
  searchTerm,
  onSearchChange,
  filters,
  onFiltersChange,
  filterFields = [],
  onClearAll,
  loading = false,
  placeholder = 'Pesquisar...'
}) => {
  const [showFilters, setShowFilters] = useState(false);

  const handleFilterChange = (key: string, value: any) => {
    const newFilters = { ...filters };
    if (value === '' || value === null || value === undefined) {
      delete newFilters[key];
    } else {
      newFilters[key] = value;
    }
    onFiltersChange(newFilters);
  };

  const handleClearSearch = () => {
    onSearchChange('');
  };

  const handleClearFilter = (key: string) => {
    const newFilters = { ...filters };
    delete newFilters[key];
    onFiltersChange(newFilters);
  };

  const activeFiltersCount = Object.keys(filters).length;
  const hasActiveFilters = activeFiltersCount > 0 || searchTerm !== '';

  return (
    <Box sx={{ mb: 3 }}>
      {/* Search Bar */}
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder={placeholder}
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          disabled={loading}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="action" />
              </InputAdornment>
            ),
            endAdornment: searchTerm && (
              <InputAdornment position="end">
                <IconButton onClick={handleClearSearch} size="small">
                  <ClearIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        
        {filterFields.length > 0 && (
          <Button
            variant="outlined"
            startIcon={<FilterIcon />}
            endIcon={showFilters ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            onClick={() => setShowFilters(!showFilters)}
            sx={{ minWidth: 120 }}
          >
            Filtros
            {activeFiltersCount > 0 && (
              <Chip
                label={activeFiltersCount}
                size="small"
                color="primary"
                sx={{ ml: 1, height: 20, '& .MuiChip-label': { px: 1 } }}
              />
            )}
          </Button>
        )}
        
        {hasActiveFilters && (
          <Button
            variant="text"
            color="error"
            onClick={onClearAll}
            startIcon={<ClearIcon />}
          >
            Limpar
          </Button>
        )}
      </Box>

      {/* Active Filters Chips */}
      {hasActiveFilters && (
        <Box sx={{ mb: 2 }}>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {searchTerm && (
              <Chip
                label={`Busca: "${searchTerm}"`}
                onDelete={handleClearSearch}
                size="small"
                variant="outlined"
              />
            )}
            {Object.entries(filters).map(([key, value]) => {
              const field = filterFields.find(f => f.key === key);
              const label = field?.label || key;
              let displayValue = value;
              
              // Format display value for select fields
              if (field?.type === 'select' && field.options) {
                const option = field.options.find(opt => opt.value === value);
                displayValue = option?.label || value;
              }
              
              return (
                <Chip
                  key={key}
                  label={`${label}: ${displayValue}`}
                  onDelete={() => handleClearFilter(key)}
                  size="small"
                  variant="outlined"
                />
              );
            })}
          </Box>
        </Box>
      )}

      {/* Advanced Filters */}
      <Collapse in={showFilters}>
        <Paper sx={{ p: 3, mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Filtros Avançados
          </Typography>
          <Grid container spacing={3}>
            {filterFields.map((field) => (
              <Grid size={{ xs: 12, sm: 6, md: 4 }} key={field.key}>
                {field.type === 'select' ? (
                  <FormControl fullWidth>
                    <InputLabel>{field.label}</InputLabel>
                    <Select
                      value={filters[field.key] || ''}
                      onChange={(e) => handleFilterChange(field.key, e.target.value)}
                      label={field.label}
                    >
                      <MenuItem value="">
                        <em>Todos</em>
                      </MenuItem>
                      {field.options?.map((option) => (
                        <MenuItem key={option.value} value={option.value}>
                          {option.label}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                ) : field.type === 'date' ? (
                  <TextField
                    fullWidth
                    type="date"
                    label={field.label}
                    value={filters[field.key] || ''}
                    onChange={(e) => handleFilterChange(field.key, e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                ) : (
                  <TextField
                    fullWidth
                    label={field.label}
                    placeholder={field.placeholder}
                    value={filters[field.key] || ''}
                    onChange={(e) => handleFilterChange(field.key, e.target.value)}
                  />
                )}
              </Grid>
            ))}
          </Grid>
        </Paper>
      </Collapse>
    </Box>
  );
};

export default SearchFilter;
