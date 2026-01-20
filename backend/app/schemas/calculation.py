"""
Calculation Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.calculation import CalculationType, CalculationStatus

class CalculationBase(BaseModel):
    calculation_type: CalculationType
    input_parameters: Dict[str, Any]

class CalculationCreate(CalculationBase):
    project_id: int
    description: Optional[str] = None

class CalculationUpdate(BaseModel):
    input_parameters: Optional[Dict[str, Any]] = None
    status: Optional[CalculationStatus] = None
    description: Optional[str] = None

class Calculation(CalculationBase):
    id: int
    project_id: int
    calculation_code: str
    status: CalculationStatus
    calculation_results: Dict[str, Any]
    design_outputs: Optional[Dict[str, Any]]
    safety_checks: Optional[Dict[str, Any]]
    safety_factor_passed: bool
    code_standard_used: Optional[str]
    compliance_status: Optional[str]
    is_validated: bool
    has_override: bool
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True
