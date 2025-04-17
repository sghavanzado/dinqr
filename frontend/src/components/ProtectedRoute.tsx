import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import LoadingBackdrop from './LoadingBackdrop';

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { token, loading } = useAuth();
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

  if (token) {
    // Render the children if the user is authenticated
    return children;
  }

  return null;
};

export default ProtectedRoute;