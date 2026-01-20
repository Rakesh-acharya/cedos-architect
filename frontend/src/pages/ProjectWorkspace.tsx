import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Tabs,
  Tab,
  Chip
} from '@mui/material';
import {
  Upload,
  Download,
  Folder,
  InsertDriveFile,
  Delete,
  Share,
  Search,
  PictureAsPdf,
  Image as ImageIcon,
  Description
} from '@mui/icons-material';
import axios from 'axios';

const ProjectWorkspace: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [workspace, setWorkspace] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [uploadDialog, setUploadDialog] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [category, setCategory] = useState('blueprint');
  const [description, setDescription] = useState('');
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (projectId) {
      loadWorkspace();
    }
  }, [projectId]);

  const loadWorkspace = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        `/api/v1/files/workspace/${projectId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setWorkspace(response.data);
    } catch (error) {
      console.error('Error loading workspace:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !projectId) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('category', category);
    formData.append('description', description);

    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `/api/v1/files/upload/${projectId}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      setUploadDialog(false);
      setSelectedFile(null);
      setDescription('');
      loadWorkspace();
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  const handleDownload = async (fileId: number, fileName: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(
        `/api/v1/files/download/${fileId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
          responseType: 'blob'
        }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  const getFileIcon = (mimeType: string) => {
    if (mimeType.includes('pdf')) return <PictureAsPdf />;
    if (mimeType.includes('image')) return <ImageIcon />;
    return <Description />;
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const categories = [
    'blueprint',
    'calculation_sheet',
    'boq',
    'bill',
    'invoice',
    'letter',
    'contract',
    'permit',
    'certificate',
    'photo',
    'report',
    'other'
  ];

  if (loading) {
    return <Box sx={{ p: 3 }}>Loading workspace...</Box>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">
          {workspace?.project_name} - Workspace
        </Typography>
        <Button
          variant="contained"
          startIcon={<Upload />}
          onClick={() => setUploadDialog(true)}
        >
          Upload File
        </Button>
      </Box>

      {/* Statistics */}
      {workspace?.statistics && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary">Total Files</Typography>
                <Typography variant="h4">{workspace.statistics.total_files}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary">Total Size</Typography>
                <Typography variant="h4">
                  {formatFileSize(workspace.statistics.total_size)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary">Categories</Typography>
                <Typography variant="h4">
                  {Object.keys(workspace.statistics.files_by_category).length}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Search */}
      <TextField
        fullWidth
        placeholder="Search files..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        sx={{ mb: 2 }}
        InputProps={{
          startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />
        }}
      />

      {/* Files by Category */}
      <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} sx={{ mb: 2 }}>
        {categories.map((cat, idx) => (
          <Tab key={cat} label={cat.replace('_', ' ')} />
        ))}
      </Tabs>

      {workspace?.files_by_category && (
        <Paper>
          <List>
            {Object.entries(workspace.files_by_category)
              .filter(([cat]) => categories[tabValue] === cat || tabValue === 0)
              .flatMap(([cat, files]: [string, any[]]) =>
                files
                  .filter((f: any) =>
                    searchTerm === '' ||
                    f.name.toLowerCase().includes(searchTerm.toLowerCase())
                  )
                  .map((file: any) => (
                    <ListItem
                      key={file.id}
                      secondaryAction={
                        <Box>
                          <IconButton
                            onClick={() => handleDownload(file.id, file.name)}
                            edge="end"
                          >
                            <Download />
                          </IconButton>
                          <IconButton edge="end">
                            <Share />
                          </IconButton>
                          <IconButton edge="end" color="error">
                            <Delete />
                          </IconButton>
                        </Box>
                      }
                    >
                      <IconButton sx={{ mr: 2 }}>
                        {getFileIcon(file.mime_type || '')}
                      </IconButton>
                      <ListItemText
                        primary={file.name}
                        secondary={
                          <>
                            {formatFileSize(file.size)} • {file.category}
                            <Chip
                              label={file.category}
                              size="small"
                              sx={{ ml: 1 }}
                            />
                          </>
                        }
                      />
                    </ListItem>
                  ))
              )}
          </List>
        </Paper>
      )}

      {/* Upload Dialog */}
      <Dialog open={uploadDialog} onClose={() => setUploadDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Upload File</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            type="file"
            margin="normal"
            onChange={(e: any) => setSelectedFile(e.target.files[0])}
          />
          <TextField
            fullWidth
            select
            label="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            margin="normal"
            SelectProps={{ native: true }}
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.replace('_', ' ')}
              </option>
            ))}
          </TextField>
          <TextField
            fullWidth
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            margin="normal"
            multiline
            rows={3}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialog(false)}>Cancel</Button>
          <Button onClick={handleUpload} variant="contained">
            Upload
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ProjectWorkspace;
