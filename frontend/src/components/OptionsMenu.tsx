import * as React from 'react';
import { styled } from '@mui/material/styles';
import Divider, { dividerClasses } from '@mui/material/Divider';
import Menu from '@mui/material/Menu';
import MuiMenuItem from '@mui/material/MenuItem';
import { paperClasses } from '@mui/material/Paper';
import { listClasses } from '@mui/material/List';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon, { listItemIconClasses } from '@mui/material/ListItemIcon';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import MoreVertRoundedIcon from '@mui/icons-material/MoreVertRounded';
import MenuButton from './MenuButton';
import { Dialog, DialogTitle, DialogContent, IconButton } from '@mui/material';
import ProfileForm from './ProfileForm';
import UserManagement from '../pages/UserManagement';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';

const MenuItem = styled(MuiMenuItem)({
  margin: '2px 0',
});

export default function OptionsMenu() {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [openProfileDialog, setOpenProfileDialog] = React.useState(false);
  const [openUserManagementDialog, setOpenUserManagementDialog] = React.useState(false);
  const { logout } = useAuth();
  const navigate = useNavigate(); // Hook for navigation
  const open = Boolean(anchorEl);
  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleProfileOpen = () => {
    setOpenProfileDialog(true);
    handleClose();
  };

  const handleUserManagementOpen = () => {
    setOpenUserManagementDialog(true);
    handleClose();
  };

  const handleSettingsClick = () => {
    navigate('/settings'); // Navigate to the Settings page
    handleClose();
  };

  const handleLogout = () => {
    logout();
    handleClose();
  };

  return (
    <React.Fragment>
      <MenuButton
        aria-label="Open menu"
        onClick={handleClick}
        sx={{ borderColor: 'transparent' }}
      >
        <MoreVertRoundedIcon />
      </MenuButton>
      <Menu
        anchorEl={anchorEl}
        id="menu"
        open={open}
        onClose={handleClose}
        onClick={handleClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        sx={{
          [`& .${listClasses.root}`]: {
            padding: '4px',
          },
          [`& .${paperClasses.root}`]: {
            padding: 0,
          },
          [`& .${dividerClasses.root}`]: {
            margin: '4px -4px',
          },
        }}
      >
        
        <MenuItem onClick={handleProfileOpen}>My account</MenuItem>
        <Divider />
        <MenuItem onClick={handleUserManagementOpen}>Add another account</MenuItem>
        <MenuItem onClick={handleSettingsClick}>Settings</MenuItem>
        <Divider />
        <MenuItem
          onClick={handleLogout}
          sx={{
            [`& .${listItemIconClasses.root}`]: {
              ml: 'auto',
              minWidth: 0,
            },
          }}
        >
          <ListItemText>Logout</ListItemText>
          <ListItemIcon>
            <LogoutRoundedIcon fontSize="small" />
          </ListItemIcon>
        </MenuItem>
      </Menu>

      {/* Dialog for Profile Form */}
      <Dialog open={openProfileDialog} onClose={() => setOpenProfileDialog(false)} fullWidth maxWidth="sm">
        <DialogTitle>My Account</DialogTitle>
        <DialogContent>
          <ProfileForm onClose={() => setOpenProfileDialog(false)} />
        </DialogContent>
      </Dialog>

      {/* Dialog for User Management */}
      <Dialog open={openUserManagementDialog} onClose={() => setOpenUserManagementDialog(false)} fullWidth maxWidth="lg">
        <DialogTitle>User Management</DialogTitle>
        <DialogContent>
          <UserManagement />
        </DialogContent>
      </Dialog>
    </React.Fragment>
  );
}
