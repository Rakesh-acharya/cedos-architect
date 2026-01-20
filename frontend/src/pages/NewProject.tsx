import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Alert,
  Paper
} from '@mui/material';
import Wizard from '../components/Wizard';
import HelpTooltip from '../components/HelpTooltip';
import apiClient from '../api/client';

const NewProject: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({
    projectName: '',
    projectType: '',
    location: '',
    description: '',
    seismicZone: 'Zone III',
    soilBearingCapacity: '200'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const steps = ['Basic Information', 'Location & Site Details', 'Review & Create'];

  const projectTypes = [
    { value: 'residential_building', label: 'Residential Building', description: 'Houses, apartments, residential complexes' },
    { value: 'commercial_building', label: 'Commercial Building', description: 'Offices, malls, shops' },
    { value: 'road', label: 'Road Project', description: 'Highways, city roads, rural roads' },
    { value: 'bridge', label: 'Bridge Project', description: 'Road bridges, rail bridges' },
    { value: 'infrastructure', label: 'Infrastructure', description: 'Dams, tunnels, other infrastructure' }
  ];

  const seismicZones = [
    { value: 'Zone I', label: 'Zone I - Low Risk' },
    { value: 'Zone II', label: 'Zone II - Moderate Risk' },
    { value: 'Zone III', label: 'Zone III - Moderate-High Risk' },
    { value: 'Zone IV', label: 'Zone IV - High Risk' },
    { value: 'Zone V', label: 'Zone V - Very High Risk' }
  ];

  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setError('');
  };

  const canProceed = () => {
    if (step === 0) {
      return formData.projectName && formData.projectType;
    }
    if (step === 1) {
      return formData.location && formData.soilBearingCapacity;
    }
    return true;
  };

  const handleNext = () => {
    if (canProceed()) {
      setStep(prev => prev + 1);
    }
  };

  const handleBack = () => {
    setStep(prev => prev - 1);
  };

  const handleFinish = async () => {
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      await apiClient.post('/api/v1/projects/', {
        project_name: formData.projectName,
        project_type: formData.projectType,
        location: formData.location,
        description: formData.description,
        seismic_zone: formData.seismicZone,
        soil_bearing_capacity: parseFloat(formData.soilBearingCapacity)
      });
      navigate('/projects');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Let's start with the basics
            </Typography>
            <Alert severity="info" sx={{ mb: 3 }}>
              Just tell us your project name and what type of project you're working on. 
              Don't worry - you can always change these later!
            </Alert>
            
            <TextField
              fullWidth
              label="Project Name"
              value={formData.projectName}
              onChange={(e) => handleChange('projectName', e.target.value)}
              placeholder="e.g., My House, City Highway, Office Complex"
              sx={{ mb: 3 }}
              required
              helperText="Give your project a memorable name"
            />
            
            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Project Type</InputLabel>
              <Select
                value={formData.projectType}
                onChange={(e) => handleChange('projectType', e.target.value)}
                label="Project Type"
                required
              >
                {projectTypes.map(type => (
                  <MenuItem key={type.value} value={type.value}>
                    <Box>
                      <Typography variant="body1">{type.label}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {type.description}
                      </Typography>
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              fullWidth
              label="Description (Optional)"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              multiline
              rows={3}
              placeholder="Any additional details about your project..."
            />
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Where is your project located?
            </Typography>
            <Alert severity="info" sx={{ mb: 3 }}>
              This helps us calculate the right loads and design for your location's conditions.
            </Alert>
            
            <TextField
              fullWidth
              label="Location"
              value={formData.location}
              onChange={(e) => handleChange('location', e.target.value)}
              placeholder="e.g., Mumbai, Delhi, Bangalore"
              sx={{ mb: 3 }}
              required
              helperText="City or area where the project is located"
            />

            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Seismic Zone</InputLabel>
              <Select
                value={formData.seismicZone}
                onChange={(e) => handleChange('seismicZone', e.target.value)}
                label="Seismic Zone"
              >
                {seismicZones.map(zone => (
                  <MenuItem key={zone.value} value={zone.value}>
                    {zone.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Typography variant="caption" color="text.secondary" sx={{ mb: 3, display: 'block' }}>
              Seismic zones tell us how earthquake-prone your area is. 
              Zone III is most common in India.
              <HelpTooltip title="Higher zones need stronger designs for earthquake safety" />
            </Typography>

            <TextField
              fullWidth
              label="Soil Bearing Capacity"
              value={formData.soilBearingCapacity}
              onChange={(e) => handleChange('soilBearingCapacity', e.target.value)}
              type="number"
              required
              helperText="Typical values: 150-300 kN/m² (if unsure, use 200)"
              InputProps={{
                endAdornment: (
                  <Typography variant="body2" sx={{ ml: 1 }}>
                    kN/m²
                  </Typography>
                )
              }}
            />
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              This tells us how much weight your soil can support. 
              <HelpTooltip title="Softer soils have lower values (150-200), hard soils have higher (250-300)" />
            </Typography>
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Review Your Project Details
            </Typography>
            <Alert severity="success" sx={{ mb: 3 }}>
              Everything looks good! Click "Finish" to create your project.
            </Alert>

            <Paper sx={{ p: 3, bgcolor: '#f5f5f5' }}>
              <Typography variant="subtitle1" gutterBottom><strong>Project Name:</strong></Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>{formData.projectName}</Typography>

              <Typography variant="subtitle1" gutterBottom><strong>Project Type:</strong></Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                {projectTypes.find(t => t.value === formData.projectType)?.label}
              </Typography>

              <Typography variant="subtitle1" gutterBottom><strong>Location:</strong></Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>{formData.location}</Typography>

              <Typography variant="subtitle1" gutterBottom><strong>Seismic Zone:</strong></Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>{formData.seismicZone}</Typography>

              <Typography variant="subtitle1" gutterBottom><strong>Soil Bearing Capacity:</strong></Typography>
              <Typography variant="body1">{formData.soilBearingCapacity} kN/m²</Typography>
            </Paper>
          </Box>
        );

      default:
        return null;
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        Create New Project
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Wizard
        steps={steps}
        activeStep={step}
        onNext={handleNext}
        onBack={handleBack}
        onFinish={handleFinish}
        canProceed={!!canProceed() && !loading}
      >
        {renderStep()}
      </Wizard>
    </Box>
  );
};

export default NewProject;
