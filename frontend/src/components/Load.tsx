import { useState, lazy, Suspense } from 'react'
import { Box, Toolbar, AppBar, Typography, Drawer, List, ListItem, 
  ListItemButton, ListItemIcon, ListItemText, Divider, IconButton, CircularProgress } from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import DashboardIcon from '@mui/icons-material/Dashboard'
import PeopleIcon from '@mui/icons-material/People'
import ReceiptIcon from '@mui/icons-material/Receipt'
import { Routes, Route, Link } from 'react-router-dom'

const drawerWidth = 240

// 1. Carga dinámica de componentes
const DashboardPage = lazy(() => import('../pages/Dashboard'))
const InvoicesPage = lazy(() => import('../pages/Factura'))
const CustomersPage = lazy(() => import('../pages/Checkout'))

// 2. Componente de carga
const Loader = () => (
  <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
    <CircularProgress />
  </Box>
)

export default function Load() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const [selectedItem, setSelectedItem] = useState('dashboard')

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  // 3. Actualización de estructura de items
  const menuItems = [
    {
      text: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/df',
      component: <DashboardPage />
    },
    {
      text: 'Facturas',
      icon: <ReceiptIcon />,
      path: '/invoices',
      component: <InvoicesPage />
    },
    {
      text: 'Clientes',
      icon: <PeopleIcon />,
      path: '/customers',
      component: <CustomersPage />
    }
  ]

  const drawer = (
    <div>
      <Toolbar />
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              component={Link}
              to={item.path}
              selected={selectedItem === item.text.toLowerCase()}
              onClick={() => setSelectedItem(item.text.toLowerCase())}
              sx={{
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'white',
                  '&:hover': {
                    backgroundColor: 'primary.dark'
                  }
                }
              }}
            >
              <ListItemIcon sx={{ color: 'inherit' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Mi Toolpad
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` }
        }}
      >
       
        {/* 4. Implementación de Suspense */}
        <Suspense fallback={<Loader />}>
          <Routes>
            {menuItems.map((item) => (
              <Route
                key={item.path}
                path={item.path}
                element={item.component}
              />
            ))}
          </Routes>
        </Suspense>
      </Box>
    </Box>
  )
}