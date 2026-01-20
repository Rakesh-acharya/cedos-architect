"""
BOQ Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.calculation import Calculation
from app.models.material import BOQ, BOQItem
from app.services.boq_calculator import BOQCalculator
import uuid

router = APIRouter()

@router.post("/generate/{project_id}", status_code=status.HTTP_201_CREATED)
def generate_boq(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate BOQ from project calculations"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all calculations for the project
    calculations = db.query(Calculation).filter(
        Calculation.project_id == project_id,
        Calculation.status == "completed"
    ).all()
    
    if not calculations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No completed calculations found for this project"
        )
    
    # Generate BOQ
    boq_calculator = BOQCalculator(db)
    quantities = boq_calculator.calculate_material_quantities(calculations)
    boq_items_data = boq_calculator.generate_boq_items(quantities, project_id)
    
    # Create BOQ
    boq_code = f"BOQ-{uuid.uuid4().hex[:8].upper()}"
    db_boq = BOQ(
        project_id=project_id,
        boq_code=boq_code,
        boq_name=f"BOQ for {project.project_name}",
        total_cement_quantity=quantities["cement"],
        total_steel_quantity=quantities["steel"],
        total_concrete_quantity=quantities["concrete"],
        total_sand_quantity=quantities["sand"],
        total_aggregate_quantity=quantities["aggregate"],
        total_excavation_volume=quantities["excavation"]
    )
    
    db.add(db_boq)
    db.commit()
    db.refresh(db_boq)
    
    # Create BOQ items
    for item_data in boq_items_data:
        db_item = BOQItem(
            boq_id=db_boq.id,
            item_code=item_data["item_code"],
            item_description=item_data["item_description"],
            item_category=item_data["category"],
            quantity=item_data["quantity"],
            unit=item_data["unit"]
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_boq)
    
    return db_boq

@router.get("/project/{project_id}")
def get_project_boq(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get BOQ for a project"""
    boq = db.query(BOQ).filter(BOQ.project_id == project_id).first()
    if not boq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BOQ not found for this project"
        )
    
    return boq
