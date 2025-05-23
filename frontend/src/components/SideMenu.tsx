import { styled } from '@mui/material/styles';
import Avatar from '@mui/material/Avatar';
import MuiDrawer, { drawerClasses } from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import LogoutIcon from '@mui/icons-material/Logout';
import { useNavigate } from 'react-router-dom';
import MenuContent from './MenuContent';
import { useAuth } from './AuthContext'; // Import the AuthContext to access user data

const drawerWidth = 340;

const Drawer = styled(MuiDrawer)({
  width: drawerWidth,
  flexShrink: 0,
  boxSizing: 'border-box',
  mt: 10,
  [`& .${drawerClasses.paper}`]: {
    width: drawerWidth,
    boxSizing: 'border-box',
  },
});

export default function SideMenu() {
  const { user, logout } = useAuth(); // Access the logout function from AuthContext
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/signin'); // Redirect to the sign-in page after logout
  };

  // If the user is not logged in, do not render the side menu
  if (!user) {
    return null;
  }

  return (
    <Drawer
      variant="permanent"
      sx={{
        display: { xs: 'none', md: 'block' },
        [`& .${drawerClasses.paper}`]: {
          backgroundColor: 'background.paper',
        },
      }}
    >
      <Divider />
      <Box
        sx={{
          overflow: 'auto',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        {/* Render the menu content */}
        <MenuContent />
      </Box>
      <Stack
        direction="row"
        sx={{
          p: 2,
          gap: 1,
          alignItems: 'center',
          borderTop: '1px solid',
          borderColor: 'divider',
        }}
      >
        {/* Display the user's avatar */}
        <Avatar
          sizes="small"
          alt={user.name}
          src={user.avatar || ''} // Use the user's avatar if available
          sx={{ width: 36, height: 36 }}
        />
        <Box sx={{ mr: 'auto' }}>
          {/* Display the user's name */}
          <Typography variant="body2" sx={{ fontWeight: 500, lineHeight: '16px' }}>
            {user.name}
          </Typography>
          {/* Display the user's email */}
          <Typography variant="caption" sx={{ color: 'text.secondary' }}>
            {user.email}
          </Typography>
        </Box>
        {/* Render the Logout button */}
        <IconButton onClick={handleLogout} color="error">
          <LogoutIcon />
        </IconButton>
      </Stack>
    </Drawer>
  );
}
