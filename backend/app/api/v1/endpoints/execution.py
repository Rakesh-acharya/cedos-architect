"""
Project Execution & Monitoring Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.execution import ProjectPhase, ProgressTracking, MeasurementBook, PhaseStatus
import uuid

router = APIRouter()

@router.post("/phases/{project_id}", status_code=status.HTTP_201_CREATED)
def create_project_phase(
    project_id: int,
    phase_name: str,
    phase_number: int,
    planned_start_date: datetime,
    planned_end_date: datetime,
    planned_cost: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a project phase"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    phase_code = f"PHASE-{uuid.uuid4().hex[:8].upper()}"
    
    db_phase = ProjectPhase(
        project_id=project_id,
        phase_code=phase_code,
        phase_name=phase_name,
        phase_number=phase_number,
        planned_start_date=planned_start_date,
        planned_end_date=planned_end_date,
        planned_cost=planned_cost,
        status=PhaseStatus.NOT_STARTED
    )
    
    db.add(db_phase)
    db.commit()
    db.refresh(db_phase)
    
    return db_phase

@router.post("/progress/{project_id}", status_code=status.HTTP_201_CREATED)
def record_progress(
    project_id: int,
    progress_percentage: float,
    work_completed: str,
    work_remaining: Optional[str] = None,
    phase_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Record project progress"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_progress = ProgressTracking(
        project_id=project_id,
        phase_id=phase_id,
        tracking_date=datetime.utcnow(),
        progress_percentage=progress_percentage,
        work_completed=work_completed,
        work_remaining=work_remaining,
        reported_by=current_user.id
    )
    
    db.add(db_progress)
    
    # Update phase status if phase_id provided
    if phase_id:
        phase = db.query(ProjectPhase).filter(ProjectPhase.id == phase_id).first()
        if phase:
            phase.actual_progress_percentage = progress_percentage
            if progress_percentage >= 100:
                phase.status = PhaseStatus.COMPLETED
                phase.actual_end_date = datetime.utcnow()
            elif progress_percentage > 0:
                phase.status = PhaseStatus.IN_PROGRESS
                if not phase.actual_start_date:
                    phase.actual_start_date = datetime.utcnow()
    
    db.commit()
    db.refresh(db_progress)
    
    return db_progress

@router.post("/measurement-book/{project_id}", status_code=status.HTTP_201_CREATED)
def create_measurement_book(
    project_id: int,
    work_description: str,
    item_code: str,
    item_description: str,
    quantity: float,
    unit: str,
    unit_rate: float,
    contractor_name: Optional[str] = None,
    contractor_bill_number: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create measurement book entry"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    mb_number = f"MB-{uuid.uuid4().hex[:8].upper()}"
    total_amount = quantity * unit_rate
    
    db_mb = MeasurementBook(
        project_id=project_id,
        mb_number=mb_number,
        mb_date=datetime.utcnow(),
        work_description=work_description,
        item_code=item_code,
        item_description=item_description,
        quantity=quantity,
        unit=unit,
        unit_rate=unit_rate,
        total_amount=total_amount,
        contractor_name=contractor_name,
        contractor_bill_number=contractor_bill_number,
        created_by=current_user.id
    )
    
    db.add(db_mb)
    db.commit()
    db.refresh(db_mb)
    
    return db_mb

@router.get("/progress/{project_id}")
def get_project_progress(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get project progress tracking"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    progress_records = db.query(ProgressTracking).filter(
        ProgressTracking.project_id == project_id
    ).order_by(ProgressTracking.tracking_date.desc()).all()
    
    phases = db.query(ProjectPhase).filter(
        ProjectPhase.project_id == project_id
    ).all()
    
    return {
        "project_id": project_id,
        "phases": [
            {
                "phase_id": phase.id,
                "phase_name": phase.phase_name,
                "status": phase.status.value,
                "planned_progress": phase.planned_progress_percentage,
                "actual_progress": phase.actual_progress_percentage
            }
            for phase in phases
        ],
        "progress_records": [
            {
                "date": record.tracking_date.isoformat(),
                "progress_percentage": record.progress_percentage,
                "work_completed": record.work_completed
            }
            for record in progress_records
        ]
    }
