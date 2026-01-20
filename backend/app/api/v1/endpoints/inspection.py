"""
Site Inspection Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.site_inspection import SiteInspectionService
from pydantic import BaseModel

router = APIRouter()

class ChecklistItem(BaseModel):
    description: str
    requirement: str = ""
    acceptance_criteria: str = ""

class InspectionResult(BaseModel):
    status: str  # pass, fail, pending
    remarks: str = ""

@router.post("/checklist/{project_id}", status_code=status.HTTP_201_CREATED)
def create_checklist(
    project_id: int,
    checklist_name: str,
    checklist_type: str,
    items: List[ChecklistItem],
    phase_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create inspection checklist"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = SiteInspectionService(db)
    
    items_data = [
        {
            "description": item.description,
            "requirement": item.requirement,
            "acceptance_criteria": item.acceptance_criteria
        }
        for item in items
    ]
    
    checklist = service.create_inspection_checklist(
        project_id=project_id,
        checklist_name=checklist_name,
        checklist_type=checklist_type,
        items=items_data,
        phase_id=phase_id
    )
    
    return checklist

@router.post("/perform/{checklist_id}")
def perform_inspection(
    checklist_id: int,
    results: List[InspectionResult],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Perform site inspection"""
    service = SiteInspectionService(db)
    
    results_data = [
        {
            "status": r.status,
            "remarks": r.remarks
        }
        for r in results
    ]
    
    result = service.perform_inspection(
        checklist_id=checklist_id,
        inspection_results=results_data,
        inspector_id=current_user.id
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result

@router.get("/report/{project_id}")
def get_inspection_report(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inspection report"""
    service = SiteInspectionService(db)
    return service.get_inspection_report(project_id)
