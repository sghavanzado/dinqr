import React, { useEffect } from 'react'; // Added React import
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import LoadingBackdrop from './LoadingBackdrop';
import { Box, Typography } from '@mui/material';

interface ProtectedRouteProps {
  children: React.ReactElement;
  requiredRole?: string;
}

const ProtectedRoute = ({ children, requiredRole }: ProtectedRouteProps) => {
  const { token, loading, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to login if the user is not authenticated
    if (!loading && !token) {
      navigate('/');
    }
  }, [token, loading, navigate]);

  if (loading) {
    // Show a loading backdrop while authentication status is being verified
    return <LoadingBackdrop open={true} />;
  }

  if (!token) {
    return null;
  }

  // Check role-based access if requiredRole is specified
  if (requiredRole && user) {
    const hasRequiredRole = user.role === requiredRole || 
                           user.roles?.includes(requiredRole) ||
                           user.role === 'ADMIN' || // Admin can access everything
                           user.roles?.includes('ADMIN');

    if (!hasRequiredRole) {
      return (
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          minHeight="200px"
          flexDirection="column"
          gap={2}
          sx={{ p: 3 }}
        >
          <Typography variant="h6" color="error">
            Acesso Negado
          </Typography>
          <Typography variant="body2" color="text.secondary" textAlign="center">
            Você não tem permissão para acessar esta seção.
          </Typography>
        </Box>
      );
    }
  }

  if (token) {
    // Render the children if the user is authenticated
    return children;
  }

  return null;
};

export default ProtectedRoute;