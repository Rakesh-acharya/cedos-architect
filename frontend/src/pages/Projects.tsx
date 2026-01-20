import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert
} from '@mui/material';
import {
  Add,
  Folder,
  Edit,
  Delete,
  Visibility,
  Description,
  Calculate,
  TrendingUp
} from '@mui/icons-material';
import axios from 'axios';

interface Project {
  id: number;
  project_code: string;
  project_name: string;
  project_type: string;
  location: string;
  status?: string;
}

const Projects: React.FC = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleteDialog, setDeleteDialog] = useState<number | null>(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/v1/projects/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProjects(response.data);
    } catch (error) {
      console.error('Error loading projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteDialog) return;
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/api/v1/projects/${deleteDialog}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadProjects();
      setDeleteDialog(null);
    } catch (error) {
      console.error('Error deleting project:', error);
    }
  };

  const getProjectTypeLabel = (type: string) => {
    const types: Record<string, string> = {
      'residential_building': '🏠 Residential',
      'commercial_building': '🏢 Commercial',
      'road': '🛣️ Road',
      'bridge': '🌉 Bridge',
      'infrastructure': '🏗️ Infrastructure'
    };
    return types[type] || type;
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
            My Projects
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage all your civil engineering projects in one place
          </Typography>
        </Box>
        <Button
          variant="contained"
          size="large"
          startIcon={<Add />}
          onClick={() => navigate('/projects/new')}
          sx={{ px: 3 }}
        >
          New Project
        </Button>
      </Box>

      {projects.length === 0 && !loading && (
        <Card sx={{ textAlign: 'center', py: 6, bgcolor: '#f5f5f5' }}>
          <CardContent>
            <Folder sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              No Projects Yet
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Start by creating your first project. It only takes a minute!
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => navigate('/projects/new')}
            >
              Create Your First Project
            </Button>
          </CardContent>
        </Card>
      )}

      {projects.length > 0 && (
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid item xs={12} sm={6} md={4} key={project.id}>
              <Card
                sx={{
                  height: '100%',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4
                  }
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Chip
                      label={getProjectTypeLabel(project.project_type)}
                      color="primary"
                      size="small"
                    />
                    <Box>
                      <IconButton
                        size="small"
                        onClick={() => navigate(`/projects/${project.id}`)}
                        title="View Details"
                      >
                        <Visibility fontSize="small" />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => setDeleteDialog(project.id)}
                        title="Delete"
                      >
                        <Delete fontSize="small" />
                      </IconButton>
                    </Box>
                  </Box>

                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                    {project.project_name}
                  </Typography>

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    📍 {project.location}
                  </Typography>

                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 2 }}>
                    Code: {project.project_code}
                  </Typography>

                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<Calculate />}
                      onClick={() => navigate(`/calculator?projectId=${project.id}`)}
                    >
                      Calculate
                    </Button>
                    <Button
                      size="small"
                      variant="outlined"
                      startIcon={<Description />}
                      onClick={() => navigate(`/projects/${project.id}`)}
                    >
                      View
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog open={deleteDialog !== null} onClose={() => setDeleteDialog(null)}>
        <DialogTitle>Delete Project?</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this project? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialog(null)}>Cancel</Button>
          <Button onClick={handleDelete} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Projects;
