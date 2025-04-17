import React, { useState } from 'react';
import { IconButton, Menu, MenuItem } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { useTheme } from '@mui/material/styles';

interface ColorModeIconDropdownProps {
  onToggleColorMode?: () => void; // Optional callback for toggling color mode
}

const ColorModeIconDropdown: React.FC<ColorModeIconDropdownProps> = ({ onToggleColorMode }) => {
  const theme = useTheme();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleOpenMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  const handleToggleColorMode = () => {
    if (onToggleColorMode) {
      onToggleColorMode();
    }
    handleCloseMenu();
  };

  return (
    <>
      <IconButton onClick={handleOpenMenu} color="inherit">
        {theme.palette.mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
      </IconButton>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleCloseMenu}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <MenuItem onClick={handleToggleColorMode}>
          {theme.palette.mode === 'dark' ? 'Light Mode' : 'Dark Mode'}
        </MenuItem>
      </Menu>
    </>
  );
};

export default ColorModeIconDropdown;
