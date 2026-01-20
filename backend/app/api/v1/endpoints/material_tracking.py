"""
Material Tracking Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.material_tracking import MaterialTrackingService

router = APIRouter()

@router.post("/consume/{project_id}")
def track_consumption(
    project_id: int,
    material_type: str,
    quantity_consumed: float,
    unit: str,
    location: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Track material consumption"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = MaterialTrackingService(db)
    result = service.track_material_consumption(
        project_id=project_id,
        material_type=material_type,
        quantity_consumed=quantity_consumed,
        unit=unit,
        location=location
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result

@router.get("/status/{project_id}")
def get_material_status(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get material status for project"""
    service = MaterialTrackingService(db)
    return service.get_material_status(project_id)

@router.post("/predict/{project_id}")
def predict_requirements(
    project_id: int,
    target_date: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict material requirements"""
    target = datetime.fromisoformat(target_date)
    service = MaterialTrackingService(db)
    return service.predict_material_requirements(project_id, target)
