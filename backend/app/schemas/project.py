"""
Project Schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.project import ProjectType, ProjectStatus

class ProjectBase(BaseModel):
    project_name: str
    project_type: ProjectType
    location: str
    usage_type: str
    design_life_years: int = 50

class ProjectCreate(ProjectBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    soil_zone: Optional[str] = None
    seismic_zone: Optional[str] = None
    wind_zone: Optional[str] = None
    budget_constraint: Optional[float] = None
    load_requirements: Optional[Dict[str, Any]] = None
    soil_classification: Optional[str] = None
    soil_bearing_capacity: Optional[float] = None
    description: Optional[str] = None
    client_name: Optional[str] = None

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    status: Optional[ProjectStatus] = None
    soil_zone: Optional[str] = None
    seismic_zone: Optional[str] = None
    wind_zone: Optional[str] = None
    budget_constraint: Optional[float] = None
    load_requirements: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class Project(ProjectBase):
    id: int
    project_code: str
    status: ProjectStatus
    latitude: Optional[float]
    longitude: Optional[float]
    soil_zone: Optional[str]
    seismic_zone: Optional[str]
    wind_zone: Optional[str]
    budget_constraint: Optional[float]
    load_requirements: Optional[Dict[str, Any]]
    soil_classification: Optional[str]
    soil_bearing_capacity: Optional[float]
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
