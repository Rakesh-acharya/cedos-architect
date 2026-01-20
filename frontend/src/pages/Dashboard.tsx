import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  Alert
} from '@mui/material';
import {
  AddCircle,
  Folder,
  Calculate,
  Assessment,
  Upload,
  PhotoCamera,
  Dashboard as DashboardIcon,
  TrendingUp
} from '@mui/icons-material';
import InfoCard from '../components/InfoCard';
import apiClient from '../api/client';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    projects: 0,
    calculations: 0,
    compliance: 0
  });

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [projectsRes] = await Promise.all([
        apiClient.get('/api/v1/projects/')
      ]);
      setStats({
        projects: projectsRes.data.length || 0,
        calculations: 0,
        compliance: 0
      });
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const quickActions = [
    {
      title: 'New Project',
      description: 'Start a new building, road, or bridge project',
      icon: <AddCircle />,
      color: '#1976d2',
      onClick: () => navigate('/projects/new')
    },
    {
      title: 'My Projects',
      description: 'View and manage all your projects',
      icon: <Folder />,
      color: '#388e3c',
      onClick: () => navigate('/projects')
    },
    {
      title: 'Design Calculator',
      description: 'Calculate columns, beams, footings, and more',
      icon: <Calculate />,
      color: '#f57c00',
      onClick: () => navigate('/calculator')
    },
    {
      title: 'View Reports',
      description: 'See all your project reports and documents',
      icon: <Assessment />,
      color: '#7b1fa2',
      onClick: () => navigate('/reports')
    }
  ];

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
          Welcome to CEDOS
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Your smart assistant for civil engineering projects. Everything you need in one place.
        </Typography>
      </Box>

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#e3f2fd' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Total Projects
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    {stats.projects}
                  </Typography>
                </Box>
                <Folder sx={{ fontSize: 48, color: '#1976d2', opacity: 0.5 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#fff3e0' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Calculations
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    {stats.calculations}
                  </Typography>
                </Box>
                <Calculate sx={{ fontSize: 48, color: '#f57c00', opacity: 0.5 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#e8f5e9' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Compliance Checks
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    {stats.compliance}
                  </Typography>
                </Box>
                <Assessment sx={{ fontSize: 48, color: '#388e3c', opacity: 0.5 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ bgcolor: '#f3e5f5' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Time Saved
                  </Typography>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
                    20+ hrs
                  </Typography>
                </Box>
                <TrendingUp sx={{ fontSize: 48, color: '#7b1fa2', opacity: 0.5 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Typography variant="h5" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
        Quick Actions
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {quickActions.map((action, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <InfoCard {...action} />
          </Grid>
        ))}
      </Grid>

      {/* Getting Started Guide */}
      <Card sx={{ bgcolor: '#f5f5f5', mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
            Getting Started
          </Typography>
          <Box component="ol" sx={{ pl: 2 }}>
            <Typography component="li" variant="body1" sx={{ mb: 1 }}>
              <strong>Create a Project:</strong> Click "New Project" and fill in basic details like project name and type
            </Typography>
            <Typography component="li" variant="body1" sx={{ mb: 1 }}>
              <strong>Add Calculations:</strong> Use the calculator to design columns, beams, footings, or roads
            </Typography>
            <Typography component="li" variant="body1" sx={{ mb: 1 }}>
              <strong>View Reports:</strong> Automatically generated reports show all your calculations and costs
            </Typography>
            <Typography component="li" variant="body1">
              <strong>Download PDFs:</strong> Export your designs and reports as PDF files anytime
            </Typography>
          </Box>
        </CardContent>
      </Card>

      {/* Help Section */}
      <Alert severity="info" sx={{ mb: 2 }}>
        <Typography variant="body2">
          <strong>Need Help?</strong> Every field has a help icon (?) that explains what it means. 
          Don't worry if you're not an engineer - our system guides you step by step!
        </Typography>
      </Alert>
    </Box>
  );
};

export default Dashboard;
