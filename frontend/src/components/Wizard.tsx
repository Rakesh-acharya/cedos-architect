import React from 'react';
import { Box, Stepper, Step, StepLabel, Button, Typography } from '@mui/material';

interface WizardProps {
  steps: string[];
  activeStep: number;
  onNext: () => void;
  onBack: () => void;
  onFinish: () => void;
  children: React.ReactNode;
  canProceed?: boolean;
}

const Wizard: React.FC<WizardProps> = ({
  steps,
  activeStep,
  onNext,
  onBack,
  onFinish,
  children,
  canProceed = true
}) => {
  const isLastStep = activeStep === steps.length - 1;

  return (
    <Box>
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      
      <Box sx={{ mb: 4 }}>
        {children}
      </Box>
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button
          disabled={activeStep === 0}
          onClick={onBack}
        >
          Back
        </Button>
        <Button
          variant="contained"
          onClick={isLastStep ? onFinish : onNext}
          disabled={!canProceed}
        >
          {isLastStep ? 'Finish' : 'Next'}
        </Button>
      </Box>
    </Box>
  );
};

export default Wizard;
