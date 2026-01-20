"""
Construction Scheduling Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.construction_scheduler import ConstructionSchedulerService
from pydantic import BaseModel

router = APIRouter()

class ActivityCreate(BaseModel):
    code: str
    name: str
    type: str = "task"
    start_date: str
    duration_days: int
    predecessors: List[str] = []
    resources: dict = {}

@router.post("/{project_id}", status_code=status.HTTP_201_CREATED)
def create_schedule(
    project_id: int,
    activities: List[ActivityCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create construction schedule"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = ConstructionSchedulerService(db)
    
    activities_data = [
        {
            "code": a.code,
            "name": a.name,
            "type": a.type,
            "start_date": a.start_date,
            "duration_days": a.duration_days,
            "predecessors": a.predecessors,
            "resources": a.resources
        }
        for a in activities
    ]
    
    result = service.create_schedule(project_id, activities_data)
    
    return result

@router.put("/activity/{activity_id}/progress")
def update_activity_progress(
    activity_id: int,
    progress_percentage: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update activity progress"""
    service = ConstructionSchedulerService(db)
    result = service.update_activity_progress(activity_id, progress_percentage)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result

@router.get("/{project_id}/gantt")
def get_gantt_data(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get schedule data for Gantt chart"""
    service = ConstructionSchedulerService(db)
    return service.get_schedule_gantt_data(project_id)
