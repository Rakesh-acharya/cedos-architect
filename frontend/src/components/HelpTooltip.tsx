import React from 'react';
import { Tooltip, IconButton } from '@mui/material';
import { HelpOutline } from '@mui/icons-material';

interface HelpTooltipProps {
  title: string;
  placement?: 'top' | 'bottom' | 'left' | 'right';
}

const HelpTooltip: React.FC<HelpTooltipProps> = ({ title, placement = 'top' }) => {
  return (
    <Tooltip title={title} placement={placement} arrow>
      <IconButton size="small" sx={{ ml: 0.5, color: 'text.secondary' }}>
        <HelpOutline fontSize="small" />
      </IconButton>
    </Tooltip>
  );
};

export default HelpTooltip;
