import React, { useRef, useEffect, useState } from 'react';
import { Box, Button, Typography, Paper } from '@mui/material';
import { CameraAlt, Stop } from '@mui/icons-material';

interface ARElement {
  type: string;
  position: { x: number; y: number; z: number };
  dimensions: { width: number; length: number; height: number };
  color: number[];
  wireframe: boolean;
}

interface ARViewerProps {
  arData: {
    elements: ARElement[];
    site_dimensions: { length: number; width: number; height: number };
    scale: number;
  };
}

const ARViewer: React.FC<ARViewerProps> = ({ arData }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isActive, setIsActive] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isActive && videoRef.current) {
      startCamera();
    } else {
      stopCamera();
    }
    return () => stopCamera();
  }, [isActive]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        drawAROverlay();
      }
    } catch (err) {
      setError('Camera access denied. Please allow camera access.');
      console.error('Camera error:', err);
    }
  };

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
  };

  const drawAROverlay = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (!canvas || !video) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const draw = () => {
      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Draw AR elements (simplified - in production use WebXR/Three.js)
        arData.elements.forEach((element, index) => {
          const x = (element.position.x / arData.site_dimensions.width) * canvas.width;
          const y = (element.position.y / arData.site_dimensions.length) * canvas.height;
          const width = (element.dimensions.width / arData.site_dimensions.width) * canvas.width;
          const height = (element.dimensions.height / arData.site_dimensions.height) * canvas.height;
          
          ctx.strokeStyle = `rgba(${element.color[0] * 255}, ${element.color[1] * 255}, ${element.color[2] * 255}, ${element.color[3]})`;
          ctx.lineWidth = 3;
          ctx.strokeRect(x, y, width, height);
          
          // Label
          ctx.fillStyle = 'white';
          ctx.font = '14px Arial';
          ctx.fillText(element.type.toUpperCase(), x, y - 5);
        });
      }
      
      if (isActive) {
        requestAnimationFrame(draw);
      }
    };
    
    draw();
  };

  return (
    <Box sx={{ width: '100%', height: '100vh', position: 'relative' }}>
      <Paper sx={{ p: 2, position: 'absolute', top: 10, left: 10, zIndex: 1000, bgcolor: 'rgba(255,255,255,0.9)' }}>
        <Typography variant="h6">AR Blueprint Viewer</Typography>
        <Typography variant="body2" color="text.secondary">
          Point camera at site markers to view blueprint overlay
        </Typography>
      </Paper>

      <video
        ref={videoRef}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          display: isActive ? 'block' : 'none'
        }}
        playsInline
        muted
      />

      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none'
        }}
      />

      {error && (
        <Paper sx={{ p: 2, position: 'absolute', bottom: 80, left: 10, right: 10, bgcolor: 'error.light', color: 'white' }}>
          <Typography>{error}</Typography>
        </Paper>
      )}

      <Box sx={{ position: 'absolute', bottom: 20, left: '50%', transform: 'translateX(-50%)' }}>
        <Button
          variant="contained"
          size="large"
          startIcon={isActive ? <Stop /> : <CameraAlt />}
          onClick={() => setIsActive(!isActive)}
          sx={{ minWidth: 200 }}
        >
          {isActive ? 'Stop AR' : 'Start AR View'}
        </Button>
      </Box>
    </Box>
  );
};

export default ARViewer;
