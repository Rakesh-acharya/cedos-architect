"""
Tender Management Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.advanced_features import Tender, TenderBid
from app.services.tender_management import TenderManagementService
from pydantic import BaseModel

router = APIRouter()

class TenderCreate(BaseModel):
    tender_title: str
    tender_type: str = "open"
    estimated_value: float
    tender_opening_date: datetime
    tender_closing_date: datetime
    earnest_money: float = 0

class BidCreate(BaseModel):
    bidder_name: str
    bidder_company: str
    bid_amount: float
    completion_time_days: int
    technical_score: float = 0
    technical_bid_path: Optional[str] = None
    financial_bid_path: Optional[str] = None

@router.post("/{project_id}", status_code=status.HTTP_201_CREATED)
def create_tender(
    project_id: int,
    tender_data: TenderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new tender"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = TenderManagementService(db)
    tender = service.create_tender(
        project_id=project_id,
        tender_title=tender_data.tender_title,
        tender_type=tender_data.tender_type,
        estimated_value=tender_data.estimated_value,
        opening_date=tender_data.tender_opening_date,
        closing_date=tender_data.tender_closing_date,
        earnest_money=tender_data.earnest_money
    )
    
    return tender

@router.post("/{tender_id}/bids", status_code=status.HTTP_201_CREATED)
def submit_bid(
    tender_id: int,
    bid_data: BidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit bid for tender"""
    tender = db.query(Tender).filter(Tender.id == tender_id).first()
    if not tender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tender not found"
        )
    
    bid = TenderBid(
        tender_id=tender_id,
        bidder_name=bid_data.bidder_name,
        bidder_company=bid_data.bidder_company,
        bid_amount=bid_data.bid_amount,
        completion_time_days=bid_data.completion_time_days,
        technical_score=bid_data.technical_score,
        technical_bid_path=bid_data.technical_bid_path,
        financial_bid_path=bid_data.financial_bid_path,
        status="submitted"
    )
    
    db.add(bid)
    db.commit()
    db.refresh(bid)
    
    return bid

@router.post("/{tender_id}/evaluate")
def evaluate_tender(
    tender_id: int,
    technical_weight: float = 0.6,
    financial_weight: float = 0.4,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Evaluate and rank tender bids"""
    service = TenderManagementService(db)
    result = service.evaluate_bids(tender_id, technical_weight, financial_weight)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result

@router.post("/{tender_id}/award/{bid_id}")
def award_tender(
    tender_id: int,
    bid_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Award tender to selected bid"""
    service = TenderManagementService(db)
    result = service.award_tender(tender_id, bid_id, current_user.id)
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result

@router.get("/project/{project_id}")
def get_project_tenders(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tenders for a project"""
    tenders = db.query(Tender).filter(Tender.project_id == project_id).all()
    
    return [
        {
            "id": t.id,
            "tender_number": t.tender_number,
            "tender_title": t.tender_title,
            "estimated_value": t.estimated_value,
            "status": t.status,
            "closing_date": t.tender_closing_date.isoformat() if t.tender_closing_date else None
        }
        for t in tenders
    ]
