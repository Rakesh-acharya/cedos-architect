import React from 'react';
import { Card, CardContent, Typography, Box, IconButton } from '@mui/material';
import { InfoOutlined } from '@mui/icons-material';

interface InfoCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  onClick?: () => void;
  color?: string;
}

const InfoCard: React.FC<InfoCardProps> = ({
  title,
  description,
  icon,
  onClick,
  color = '#1a237e'
}) => {
  return (
    <Card
      sx={{
        cursor: onClick ? 'pointer' : 'default',
        transition: 'transform 0.2s, box-shadow 0.2s',
        '&:hover': onClick ? {
          transform: 'translateY(-4px)',
          boxShadow: 4
        } : {},
        borderLeft: `4px solid ${color}`
      }}
      onClick={onClick}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {icon && <Box sx={{ mr: 2, color }}>{icon}</Box>}
          <Typography variant="h6" sx={{ flex: 1 }}>
            {title}
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default InfoCard;
