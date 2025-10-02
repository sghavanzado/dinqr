/**
 * Simple Color Picker Component
 * Uses HTML5 color input with Material-UI styling
 */

import React from 'react';
import { TextField, Box, Typography } from '@mui/material';
import type { TextFieldProps } from '@mui/material';

interface ColorPickerProps extends Omit<TextFieldProps, 'type' | 'onChange'> {
  label: string;
  value: string;
  onChange: (color: string) => void;
  showPreview?: boolean;
}

export const ColorPicker: React.FC<ColorPickerProps> = ({
  label,
  value,
  onChange,
  showPreview = true,
  ...textFieldProps
}) => {
  return (
    <Box>
      <TextField
        {...textFieldProps}
        type="color"
        label={label}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        InputProps={{
          sx: {
            '& input[type="color"]': {
              minHeight: '40px',
              cursor: 'pointer',
              border: 'none',
              '&::-webkit-color-swatch': {
                border: '1px solid #ccc',
                borderRadius: '4px',
              },
              '&::-webkit-color-swatch-wrapper': {
                padding: 0,
              },
            },
          },
        }}
      />
      {showPreview && (
        <Box
          sx={{
            mt: 1,
            width: '100%',
            height: '20px',
            backgroundColor: value,
            border: '1px solid #ccc',
            borderRadius: '4px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography variant="caption" sx={{ 
            color: value === '#ffffff' || value === '#FFFFFF' ? '#000' : '#fff',
            fontSize: '10px',
            fontWeight: 'bold',
            textShadow: '1px 1px 1px rgba(0,0,0,0.5)'
          }}>
            {value.toUpperCase()}
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default ColorPicker;
