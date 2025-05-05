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
      if (token) {
        navigate('/dashboard'); // Redirect to dashboard only on initial load
      } else {
        navigate('/'); // Redirect to login if no token
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