"""
Cost Estimation Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.material import BOQ, BOQItem
from app.models.cost import CostEstimate, CostItem, EstimateType
import uuid

router = APIRouter()

@router.post("/estimate/{project_id}", status_code=status.HTTP_201_CREATED)
def create_cost_estimate(
    project_id: int,
    estimate_type: EstimateType = EstimateType.DETAILED,
    contingency_percentage: float = 0.10,
    escalation_percentage: float = 0.05,
    gst_percentage: float = 0.18,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create cost estimate from BOQ"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get BOQ
    boq = db.query(BOQ).filter(BOQ.project_id == project_id).first()
    if not boq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BOQ not found. Please generate BOQ first."
        )
    
    # Get BOQ items
    boq_items = db.query(BOQItem).filter(BOQItem.boq_id == boq.id).all()
    
    # Calculate base cost (simplified - using default rates)
    # In production, these would come from SOR or market rates
    default_rates = {
        "concrete": 5000,  # per m³
        "steel": 60,  # per kg
        "cement": 8,  # per kg
        "sand": 800,  # per m³
        "aggregate": 1000,  # per m³
        "excavation": 200  # per m³
    }
    
    base_cost = 0.0
    cost_items = []
    
    for item in boq_items:
        # Determine rate based on material type
        unit_rate = default_rates.get(item.item_category.lower(), 100)
        total_amount = item.quantity * unit_rate
        base_cost += total_amount
        
        cost_items.append({
            "item_code": item.item_code,
            "item_description": item.item_description,
            "category": item.item_category,
            "quantity": item.quantity,
            "unit": item.unit,
            "unit_rate": unit_rate,
            "total_amount": total_amount
        })
    
    # Calculate additional costs
    contingency_amount = base_cost * contingency_percentage
    escalation_amount = base_cost * escalation_percentage
    gst_amount = (base_cost + contingency_amount + escalation_amount) * gst_percentage
    
    total_cost = base_cost + contingency_amount + escalation_amount + gst_amount
    
    # Create cost estimate
    estimate_code = f"EST-{uuid.uuid4().hex[:8].upper()}"
    db_estimate = CostEstimate(
        project_id=project_id,
        estimate_code=estimate_code,
        estimate_name=f"Cost Estimate for {project.project_name}",
        estimate_type=estimate_type,
        base_cost=base_cost,
        contingency_percentage=contingency_percentage,
        contingency_amount=contingency_amount,
        escalation_percentage=escalation_percentage,
        escalation_amount=escalation_amount,
        gst_percentage=gst_percentage,
        gst_amount=gst_amount,
        total_cost=total_cost
    )
    
    db.add(db_estimate)
    db.commit()
    db.refresh(db_estimate)
    
    # Create cost items
    for item_data in cost_items:
        db_cost_item = CostItem(
            cost_estimate_id=db_estimate.id,
            item_code=item_data["item_code"],
            item_description=item_data["item_description"],
            category=item_data["category"],
            quantity=item_data["quantity"],
            unit=item_data["unit"],
            unit_rate=item_data["unit_rate"],
            total_amount=item_data["total_amount"]
        )
        db.add(db_cost_item)
    
    db.commit()
    db.refresh(db_estimate)
    
    return db_estimate

@router.get("/project/{project_id}")
def get_project_cost_estimate(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get cost estimate for a project"""
    estimate = db.query(CostEstimate).filter(
        CostEstimate.project_id == project_id
    ).order_by(CostEstimate.created_at.desc()).first()
    
    if not estimate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost estimate not found for this project"
        )
    
    return estimate
