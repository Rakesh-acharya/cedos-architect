"""
Blueprint Generation Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.calculation import Calculation
from app.services.blueprint_generator import BlueprintGenerator

router = APIRouter()

@router.get("/plan/{project_id}")
def generate_plan_view(
    project_id: int,
    page_size: str = "A2",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate structural plan view blueprint"""
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
    
    blueprint_gen = BlueprintGenerator()
    
    project_data = {
        "project_name": project.project_name,
        "project_code": project.project_code,
        "date": project.created_at.isoformat() if project.created_at else "N/A"
    }
    
    calc_data = [
        {
            "calculation_type": calc.calculation_type.value,
            "design_outputs": calc.design_outputs or {}
        }
        for calc in calculations
    ]
    
    pdf_bytes = blueprint_gen.generate_structural_plan(project_data, calc_data, page_size)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=plan_{project.project_code}.pdf"
        }
    )

@router.get("/elevation/{project_id}")
def generate_elevation_view(
    project_id: int,
    page_size: str = "A2",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate elevation view blueprint"""
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
    
    blueprint_gen = BlueprintGenerator()
    
    project_data = {
        "project_name": project.project_name,
        "project_code": project.project_code,
        "date": project.created_at.isoformat() if project.created_at else "N/A"
    }
    
    calc_data = [
        {
            "calculation_type": calc.calculation_type.value,
            "design_outputs": calc.design_outputs or {}
        }
        for calc in calculations
    ]
    
    pdf_bytes = blueprint_gen.generate_elevation_view(project_data, calc_data, page_size)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=elevation_{project.project_code}.pdf"
        }
    )

@router.get("/section/{calculation_id}")
def generate_section_view(
    calculation_id: int,
    page_size: str = "A3",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate section view blueprint"""
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    project = db.query(Project).filter(Project.id == calculation.project_id).first()
    
    blueprint_gen = BlueprintGenerator()
    
    project_data = {
        "project_name": project.project_name if project else "N/A",
        "project_code": project.project_code if project else "N/A",
        "date": calculation.created_at.isoformat() if calculation.created_at else "N/A"
    }
    
    calc_data = {
        "calculation_type": calculation.calculation_type.value,
        "design_outputs": calculation.design_outputs or {}
    }
    
    pdf_bytes = blueprint_gen.generate_section_view(project_data, calc_data, page_size)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=section_{calculation.calculation_code}.pdf"
        }
    )

@router.get("/road/{project_id}")
def generate_road_plan(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate road plan blueprint"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get road design calculation
    road_calc = db.query(Calculation).filter(
        Calculation.project_id == project_id,
        Calculation.calculation_type == "road_design"
    ).first()
    
    if not road_calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Road design calculation not found"
        )
    
    blueprint_gen = BlueprintGenerator()
    
    project_data = {
        "project_name": project.project_name,
        "project_code": project.project_code,
        "date": project.created_at.isoformat() if project.created_at else "N/A"
    }
    
    road_design = road_calc.design_outputs or {}
    
    pdf_bytes = blueprint_gen.generate_road_plan(project_data, road_design)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=road_plan_{project.project_code}.pdf"
        }
    )
