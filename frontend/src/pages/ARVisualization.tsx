import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, CircularProgress, Paper, TextField, Button } from '@mui/material';
import ARViewer from '../components/ARViewer';
import apiClient from '../api/client';

const ARVisualization: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [arData, setArData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [siteLength, setSiteLength] = useState(10);
  const [siteWidth, setSiteWidth] = useState(10);
  const [siteHeight, setSiteHeight] = useState(5);

  const generateARData = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await apiClient.post(
        `/api/v1/ar/generate/${projectId}`,
        {
          site_length: siteLength,
          site_width: siteWidth,
          site_height: siteHeight
        }
      );
      setArData(response.data);
    } catch (error) {
      console.error('Error generating AR data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (projectId) {
      generateARData();
    }
  }, [projectId]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!arData) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>AR Visualization Setup</Typography>
        <Paper sx={{ p: 3, mt: 2 }}>
          <TextField
            label="Site Length (m)"
            type="number"
            value={siteLength}
            onChange={(e) => setSiteLength(parseFloat(e.target.value))}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Site Width (m)"
            type="number"
            value={siteWidth}
            onChange={(e) => setSiteWidth(parseFloat(e.target.value))}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Site Height (m)"
            type="number"
            value={siteHeight}
            onChange={(e) => setSiteHeight(parseFloat(e.target.value))}
            fullWidth
            margin="normal"
          />
          <Button variant="contained" onClick={generateARData} sx={{ mt: 2 }}>
            Generate AR Data
          </Button>
        </Paper>
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100vh', width: '100%' }}>
      <ARViewer arData={arData} />
    </Box>
  );
};

export default ARVisualization;
