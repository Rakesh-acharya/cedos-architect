"""
Advanced Features Endpoints - Market-leading capabilities
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.generative_design import GenerativeDesignService
from app.services.risk_assessment import RiskAssessmentService
from app.services.sustainability import SustainabilityService

router = APIRouter()

@router.post("/generative-design/{project_id}")
def generate_design_options(
    project_id: int,
    design_type: str,
    constraints: dict,
    num_options: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate AI-powered design options
    Returns multiple optimized design alternatives
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = GenerativeDesignService(db)
    options = service.generate_design_options(
        project_id,
        design_type,
        constraints,
        num_options
    )
    
    return {
        "project_id": project_id,
        "design_type": design_type,
        "num_options": len(options),
        "options": options
    }

@router.post("/risk-assessment/{project_id}")
def assess_project_risks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Comprehensive project risk assessment
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = RiskAssessmentService(db)
    
    project_data = {
        "project_type": project.project_type.value,
        "soil_bearing_capacity": project.soil_bearing_capacity,
        "seismic_zone": project.seismic_zone,
        "budget_constraint": project.budget_constraint
    }
    
    assessment = service.assess_project_risks(project_id, project_data)
    
    # Save risks to database
    if "risks" in assessment:
        service.save_risks_to_database(
            project_id,
            assessment["risks"],
            current_user.id
        )
    
    return assessment

@router.post("/sustainability/{project_id}")
def assess_sustainability(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sustainability and carbon footprint assessment
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = SustainabilityService(db)
    assessment = service.assess_project_sustainability(project_id)
    
    if "error" in assessment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=assessment["error"]
        )
    
    return assessment

@router.get("/risks/{project_id}")
def get_project_risks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all project risks"""
    from app.models.advanced_features import ProjectRisk
    
    risks = db.query(ProjectRisk).filter(ProjectRisk.project_id == project_id).all()
    
    return [
        {
            "id": r.id,
            "risk_name": r.risk_name,
            "category": r.risk_category.value,
            "probability": r.probability,
            "impact": r.impact,
            "risk_score": r.risk_score,
            "status": r.status,
            "mitigation_strategy": r.mitigation_strategy
        }
        for r in risks
    ]

@router.get("/design-options/{project_id}")
def get_design_options(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get generated design options"""
    from app.models.advanced_features import DesignOption
    
    options = db.query(DesignOption).filter(
        DesignOption.project_id == project_id
    ).order_by(DesignOption.overall_score.desc()).all()
    
    return [
        {
            "id": o.id,
            "option_name": o.option_name,
            "design_type": o.design_type,
            "cost_estimate": o.cost_estimate,
            "material_efficiency": o.material_efficiency,
            "sustainability_score": o.sustainability_score,
            "overall_score": o.overall_score,
            "is_selected": o.is_selected,
            "design_outputs": o.design_outputs
        }
        for o in options
    ]
