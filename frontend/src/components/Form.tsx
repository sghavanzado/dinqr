// src/components/Form/index.tsx
import { styled } from '@mui/material/styles';
import {
  Box,
  InputAdornment,
  TextField,
  Typography,
  TextFieldProps
} from '@mui/material';

// Contenedor de grupo de formulario
export const FormGroup = styled(Box)(({ theme }) => ({
  marginBottom: theme.spacing(3),
  position: 'relative',
  width: '100%',
  '&:last-of-type': {
    marginBottom: theme.spacing(2)
  }
}));

// Etiqueta estilizada
export const Label = styled('label')(({ theme }) => ({
  display: 'block',
  marginBottom: theme.spacing(1),
  color: theme.palette.text.secondary,
  fontSize: '0.875rem',
  fontWeight: 500,
  lineHeight: 1.5
}));

// Wrapper para íconos en inputs
export const IconWrapper = styled(InputAdornment)(({ theme }) => ({
  color: theme.palette.action.active,
  marginRight: theme.spacing(1),
  '& .MuiSvgIcon-root': {
    fontSize: '1.25rem'
  }
}));

// Campo de texto personalizado
export const StyledTextField = styled(TextField)<TextFieldProps>(
  ({ theme }) => ({
    '& .MuiOutlinedInput-root': {
      borderRadius: theme.shape.borderRadius * 0.5,
      transition: theme.transitions.create('all', {
        duration: theme.transitions.duration.shortest
      }),
      
      '& fieldset': {
        borderColor: theme.palette.divider,
        borderWidth: 1
      },
      
      '&:hover fieldset': {
        borderColor: theme.palette.primary.main
      },
      
      '&.Mui-focused fieldset': {
        borderWidth: 1,
        boxShadow: `0 0 0 2px ${theme.palette.primary.light}`,
        borderColor: theme.palette.primary.main
      },
      
      '&.Mui-error': {
        '& fieldset': {
          borderColor: theme.palette.error.main
        }
      }
    },
    
    '& .MuiInputBase-input': {
      padding: theme.spacing(1.5, 2),
      fontSize: '0.875rem'
    },
    
    '& .MuiInputLabel-root': {
      fontSize: '0.875rem'
    }
  })
);

// Texto de error estilizado
export const ErrorText = styled(Typography)(({ theme }) => ({
  color: theme.palette.error.main,
  fontSize: '0.75rem',
  position: 'absolute',
  bottom: '-1.25rem',
  left: 0,
  fontWeight: 500,
  lineHeight: 1.5
}));
