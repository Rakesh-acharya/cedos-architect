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
  Card,
  CardContent,
  Grid,
  Paper
} from '@mui/material';
import { Calculate, ArrowForward } from '@mui/icons-material';
import HelpTooltip from '../components/HelpTooltip';
import apiClient from '../api/client';

const Calculator: React.FC = () => {
  const navigate = useNavigate();
  const [projectId, setProjectId] = useState('');
  const [calcType, setCalcType] = useState('');
  const [inputs, setInputs] = useState<any>({});
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const calculationTypes = [
    {
      value: 'column_design',
      label: 'Column Design',
      description: 'Design reinforced concrete columns',
      icon: '🏗️',
      inputs: [
        { key: 'axial_load', label: 'Axial Load', unit: 'kN', help: 'Total weight coming down on the column' },
        { key: 'concrete_grade', label: 'Concrete Grade', type: 'select', options: ['M20', 'M25', 'M30', 'M35', 'M40'], help: 'Strength of concrete - M25 is commonly used' },
        { key: 'steel_grade', label: 'Steel Grade', type: 'select', options: ['Fe415', 'Fe500', 'Fe550'], help: 'Strength of reinforcement steel - Fe415 is standard' }
      ]
    },
    {
      value: 'footing_design',
      label: 'Footing Design',
      description: 'Design foundation footings',
      icon: '🏛️',
      inputs: [
        { key: 'column_load', label: 'Column Load', unit: 'kN', help: 'Weight from the column above' },
        { key: 'soil_bearing_capacity', label: 'Soil Bearing Capacity', unit: 'kN/m²', help: 'How much weight your soil can support (usually 150-300)' }
      ]
    },
    {
      value: 'beam_design',
      label: 'Beam Design',
      description: 'Design beams and girders',
      icon: '📐',
      inputs: [
        { key: 'moment', label: 'Bending Moment', unit: 'kNm', help: 'The bending force on the beam' },
        { key: 'shear', label: 'Shear Force', unit: 'kN', help: 'The cutting force on the beam' },
        { key: 'concrete_grade', label: 'Concrete Grade', type: 'select', options: ['M20', 'M25', 'M30'], help: 'Strength of concrete' },
        { key: 'steel_grade', label: 'Steel Grade', type: 'select', options: ['Fe415', 'Fe500'], help: 'Strength of steel' }
      ]
    },
    {
      value: 'road_design',
      label: 'Road Design',
      description: 'Design flexible pavements',
      icon: '🛣️',
      inputs: [
        { key: 'traffic_count', label: 'Daily Traffic', unit: 'vehicles/day', help: 'Number of vehicles per day' },
        { key: 'design_life', label: 'Design Life', unit: 'years', help: 'How long the road should last (typically 15-20 years)' },
        { key: 'subgrade_cbr', label: 'Soil CBR Value', unit: '%', help: 'Soil strength - typical values: 3-10%' }
      ]
    }
  ];

  const selectedCalc = calculationTypes.find(c => c.value === calcType);

  const handleCalculate = async () => {
    if (!projectId || !calcType) {
      setError('Please select a project and calculation type');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      const response = await apiClient.post('/api/v1/calculations/', {
        project_id: parseInt(projectId),
        calculation_type: calcType,
        input_parameters: inputs
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Calculation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
        Design Calculator
      </Typography>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          <strong>Easy to Use:</strong> Just select your project, choose what you want to design, 
          enter the numbers, and click Calculate! Our system does all the complex engineering math for you.
        </Typography>
      </Alert>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Step 1: Select Your Project
              </Typography>
              <TextField
                fullWidth
                label="Project ID"
                value={projectId}
                onChange={(e) => setProjectId(e.target.value)}
                placeholder="Enter project ID (find it in 'My Projects')"
                sx={{ mb: 3 }}
                helperText="You can find your project ID in the Projects page"
              />

              <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                Step 2: Choose What to Design
              </Typography>
              <FormControl fullWidth sx={{ mb: 3 }}>
                <InputLabel>Calculation Type</InputLabel>
                <Select
                  value={calcType}
                  onChange={(e) => {
                    setCalcType(e.target.value);
                    setInputs({});
                    setResult(null);
                  }}
                  label="Calculation Type"
                >
                  {calculationTypes.map(type => (
                    <MenuItem key={type.value} value={type.value}>
                      <Box>
                        <Typography variant="body1">
                          {type.icon} {type.label}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {type.description}
                        </Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {selectedCalc && (
                <>
                  <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                    Step 3: Enter Your Numbers
                  </Typography>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    <Typography variant="body2">
                      Don't know what values to use? Click the ? icon next to each field for help!
                    </Typography>
                  </Alert>
                  {selectedCalc.inputs.map((input: any) => (
                    <Box key={input.key} sx={{ mb: 2 }}>
                      {input.type === 'select' ? (
                        <FormControl fullWidth>
                          <InputLabel>{input.label}</InputLabel>
                          <Select
                            value={inputs[input.key] || ''}
                            onChange={(e) => setInputs({ ...inputs, [input.key]: e.target.value })}
                            label={input.label}
                          >
                            {input.options.map((opt: string) => (
                              <MenuItem key={opt} value={opt}>{opt}</MenuItem>
                            ))}
                          </Select>
                          <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                            <Typography variant="caption" color="text.secondary">
                              {input.help}
                            </Typography>
                            <HelpTooltip title={input.help} />
                          </Box>
                        </FormControl>
                      ) : (
                        <>
                          <TextField
                            fullWidth
                            label={input.label}
                            type="number"
                            value={inputs[input.key] || ''}
                            onChange={(e) => setInputs({ ...inputs, [input.key]: parseFloat(e.target.value) })}
                            helperText={input.help}
                            InputProps={{
                              endAdornment: input.unit && (
                                <Typography variant="body2" sx={{ ml: 1 }}>
                                  {input.unit}
                                </Typography>
                              )
                            }}
                          />
                          <Box sx={{ display: 'flex', alignItems: 'center', mt: 0.5 }}>
                            <HelpTooltip title={input.help} />
                          </Box>
                        </>
                      )}
                    </Box>
                  ))}

                  <Button
                    fullWidth
                    variant="contained"
                    size="large"
                    startIcon={<Calculate />}
                    onClick={handleCalculate}
                    disabled={loading || !projectId || !calcType}
                    sx={{ mt: 3 }}
                  >
                    {loading ? 'Calculating...' : 'Calculate Design'}
                  </Button>
                </>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Results
              </Typography>
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              {!result && !error && (
                <Alert severity="info">
                  <Typography variant="body2">
                    Enter your project details and values, then click "Calculate Design" to see results here.
                  </Typography>
                </Alert>
              )}
              {result && (
                <Paper sx={{ p: 3, bgcolor: '#f5f5f5' }}>
                  <Typography variant="h6" gutterBottom sx={{ color: '#1976d2' }}>
                    ✅ Design Complete!
                  </Typography>
                  {result.design_outputs && Object.entries(result.design_outputs).map(([key, value]) => (
                    <Box key={key} sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:
                      </Typography>
                      <Typography variant="h6">
                        {typeof value === 'number' ? value.toFixed(2) : String(value)}
                        {key.includes('size') && ' m'}
                        {key.includes('area') && ' mm²'}
                        {key.includes('thickness') && ' mm'}
                      </Typography>
                    </Box>
                  ))}
                  <Button
                    variant="outlined"
                    fullWidth
                    sx={{ mt: 2 }}
                    onClick={() => navigate(`/projects/${projectId}`)}
                  >
                    View Full Details
                  </Button>
                </Paper>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Calculator;
