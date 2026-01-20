"""
Change Order Management Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.change_order import ChangeOrderService
from pydantic import BaseModel

router = APIRouter()

class ChangeOrderCreate(BaseModel):
    change_title: str
    description: str
    change_type: str
    reason: str
    items: List[dict]

@router.post("/{project_id}", status_code=status.HTTP_201_CREATED)
def create_change_order(
    project_id: int,
    change_data: ChangeOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create change order"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = ChangeOrderService(db)
    change_order = service.create_change_order(
        project_id=project_id,
        change_title=change_data.change_title,
        description=change_data.description,
        change_type=change_data.change_type,
        reason=change_data.reason,
        items=change_data.items,
        user_id=current_user.id
    )
    
    return change_order

@router.post("/{change_order_id}/approve")
def approve_change_order(
    change_order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve change order"""
    service = ChangeOrderService(db)
    result = service.approve_change_order(change_order_id, current_user.id)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result

@router.get("/summary/{project_id}")
def get_change_order_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get change order summary"""
    service = ChangeOrderService(db)
    return service.get_change_order_summary(project_id)

@router.get("/project/{project_id}")
def get_project_change_orders(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all change orders for project"""
    from app.models.advanced_features import ChangeOrder
    
    change_orders = db.query(ChangeOrder).filter(
        ChangeOrder.project_id == project_id
    ).all()
    
    return [
        {
            "id": co.id,
            "change_order_number": co.change_order_number,
            "change_title": co.change_order_title,
            "cost_difference": co.cost_difference,
            "status": co.status,
            "submitted_at": co.submitted_at.isoformat() if co.submitted_at else None
        }
        for co in change_orders
    ]
