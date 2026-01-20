"""
Compliance Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.calculation import Calculation
from app.models.compliance import ComplianceCheck, CodeStandard
from app.services.compliance_checker import ComplianceChecker

router = APIRouter()

@router.post("/check/{calculation_id}")
def check_compliance(
    calculation_id: int,
    code_standard: str = "IS 456:2000",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Perform compliance check on a calculation"""
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    compliance_checker = ComplianceChecker(db)
    result = compliance_checker.perform_full_compliance_check(calculation, code_standard)
    
    return result

@router.get("/project/{project_id}")
def get_project_compliance(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get compliance status for all calculations in a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    calculations = db.query(Calculation).filter(Calculation.project_id == project_id).all()
    compliance_checks = db.query(ComplianceCheck).filter(
        ComplianceCheck.project_id == project_id
    ).all()
    
    return {
        "project_id": project_id,
        "total_calculations": len(calculations),
        "compliance_checks": [
            {
                "check_id": check.id,
                "check_name": check.check_name,
                "status": check.status.value,
                "is_passed": check.is_passed
            }
            for check in compliance_checks
        ]
    }
