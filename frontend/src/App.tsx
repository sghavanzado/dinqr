import { useEffect, useState } from 'react';
import { useNavigate, Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import { AuthProvider, useAuth } from './components/AuthContext';
import SideMenu from './components/SideMenu';
import SignInSide from './pages/SignInSide';
import LoadingBackdrop from './components/LoadingBackdrop';
import ContentArea from './components/ContentArea'; // Import ContentArea

const AppWrapper = () => {
  const [isInitialLoad, setIsInitialLoad] = useState(true); // Track initial load
  const { token, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && isInitialLoad) {
      const currentPath = window.location.pathname;
      if (token) {
        // Only redirect to dashboard if user is at root path
        if (currentPath === '/' || currentPath === '') {
          navigate('/dashboard');
        }
        // If user has token but is at a specific path, let them stay there
      } else {
        // If no token, redirect to login regardless of path
        navigate('/');
      }
      setIsInitialLoad(false); // Prevent further redirects
    }
  }, [token, loading, isInitialLoad, navigate]);

  if (loading) {
    return <LoadingBackdrop open />;
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {token && <SideMenu />}
      <Routes>
        <Route path="/" element={<SignInSide />} />
        <Route path="/*" element={<ContentArea />} /> {/* Delegate routes to ContentArea */}
      </Routes>
    </Box>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <AppWrapper />
    </AuthProvider>
  );
};

export default App;