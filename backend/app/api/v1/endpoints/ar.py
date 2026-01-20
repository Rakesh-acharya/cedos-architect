"""
AR Visualization Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.calculation import Calculation
from app.services.ar_visualization import ARVisualizationService
from app.schemas.project import Project as ProjectSchema

router = APIRouter()

@router.post("/generate/{project_id}")
def generate_ar_data(
    project_id: int,
    site_length: float,
    site_width: float,
    site_height: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate AR visualization data for a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    calculations = db.query(Calculation).filter(
        Calculation.project_id == project_id,
        Calculation.status == "completed"
    ).all()
    
    if not calculations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No completed calculations found"
        )
    
    ar_service = ARVisualizationService()
    
    project_data = {
        "id": project.id,
        "project_name": project.project_name,
        "project_code": project.project_code
    }
    
    calc_data = [
        {
            "calculation_type": calc.calculation_type.value,
            "design_outputs": calc.design_outputs or {}
        }
        for calc in calculations
    ]
    
    site_dimensions = {
        "length": site_length,
        "width": site_width,
        "height": site_height or 10.0
    }
    
    ar_data = ar_service.generate_ar_data(project_data, calc_data, site_dimensions)
    
    return ar_data

@router.post("/markers/{project_id}")
def generate_ar_markers(
    project_id: int,
    site_corners: Optional[List[List[float]]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate AR marker configuration"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    ar_service = ARVisualizationService()
    
    if site_corners:
        corners = [tuple(corner) for corner in site_corners]
    else:
        # Generate default corners
        corners = None
    
    markers_config = ar_service.generate_ar_markers_config(corners)
    
    return markers_config

@router.get("/instructions/{project_id}")
def get_ar_instructions(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get AR setup instructions"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    ar_service = ARVisualizationService()
    
    project_data = {
        "id": project.id,
        "project_name": project.project_name
    }
    
    instructions = ar_service.generate_ar_instructions(project_data)
    
    return instructions
