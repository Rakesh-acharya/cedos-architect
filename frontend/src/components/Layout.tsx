import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Button,
  IconButton,
  Menu,
  MenuItem
} from '@mui/material';
import {
  Logout,
  Dashboard as DashboardIcon,
  Folder,
  Calculate,
  Menu as MenuIcon
} from '@mui/icons-material';

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static" sx={{ bgcolor: '#1976d2' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            🏗️ CEDOS
          </Typography>
          <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
            <Button color="inherit" component={Link} to="/" startIcon={<DashboardIcon />}>
              Dashboard
            </Button>
            <Button color="inherit" component={Link} to="/projects" startIcon={<Folder />}>
              My Projects
            </Button>
            <Button color="inherit" component={Link} to="/calculator" startIcon={<Calculate />}>
              Calculator
            </Button>
          </Box>
          <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
            <IconButton color="inherit" onClick={handleMenuOpen}>
              <MenuIcon />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItem component={Link} to="/" onClick={handleMenuClose}>
                <DashboardIcon sx={{ mr: 1 }} /> Dashboard
              </MenuItem>
              <MenuItem component={Link} to="/projects" onClick={handleMenuClose}>
                <Folder sx={{ mr: 1 }} /> My Projects
              </MenuItem>
              <MenuItem component={Link} to="/calculator" onClick={handleMenuClose}>
                <Calculate sx={{ mr: 1 }} /> Calculator
              </MenuItem>
              <MenuItem onClick={handleLogout}>
                <Logout sx={{ mr: 1 }} /> Logout
              </MenuItem>
            </Menu>
          </Box>
          <Button
            color="inherit"
            onClick={handleLogout}
            startIcon={<Logout />}
            sx={{ display: { xs: 'none', md: 'flex' } }}
          >
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flex: 1 }}>
        <Outlet />
      </Container>
    </Box>
  );
};

export default Layout;
