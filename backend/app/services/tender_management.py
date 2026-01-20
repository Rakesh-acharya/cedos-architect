"""
Tender Management Service - Bid evaluation and comparison
"""

from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.advanced_features import Tender, TenderBid
from datetime import datetime
import uuid

class TenderManagementService:
    """Tender Management Service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_tender(
        self,
        project_id: int,
        tender_title: str,
        tender_type: str,
        estimated_value: float,
        opening_date: datetime,
        closing_date: datetime,
        earnest_money: float = 0
    ) -> Tender:
        """Create new tender"""
        tender_number = f"TEN-{uuid.uuid4().hex[:8].upper()}"
        
        tender = Tender(
            project_id=project_id,
            tender_number=tender_number,
            tender_title=tender_title,
            tender_type=tender_type,
            estimated_value=estimated_value,
            earnest_money=earnest_money,
            tender_opening_date=opening_date,
            tender_closing_date=closing_date,
            status="draft"
        )
        
        self.db.add(tender)
        self.db.commit()
        self.db.refresh(tender)
        
        return tender
    
    def evaluate_bids(
        self,
        tender_id: int,
        technical_weight: float = 0.6,
        financial_weight: float = 0.4
    ) -> Dict:
        """Evaluate and rank tender bids"""
        tender = self.db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            return {"error": "Tender not found"}
        
        bids = self.db.query(TenderBid).filter(
            TenderBid.tender_id == tender_id,
            TenderBid.status == "submitted"
        ).all()
        
        if not bids:
            return {"error": "No bids found"}
        
        # Normalize financial scores (lower bid = higher score)
        min_bid = min(b.bid_amount for b in bids)
        max_bid = max(b.bid_amount for b in bids)
        bid_range = max_bid - min_bid if max_bid != min_bid else 1
        
        evaluated_bids = []
        for bid in bids:
            # Financial score (inverted - lower is better)
            financial_score = 100 * (1 - (bid.bid_amount - min_bid) / bid_range)
            
            # Overall score
            overall_score = (
                technical_weight * bid.technical_score +
                financial_weight * financial_score
            )
            
            bid.financial_score = financial_score
            bid.overall_score = overall_score
            bid.status = "under_evaluation"
            
            evaluated_bids.append({
                "bid_id": bid.id,
                "bidder_name": bid.bidder_name,
                "bid_amount": bid.bid_amount,
                "technical_score": bid.technical_score,
                "financial_score": round(financial_score, 2),
                "overall_score": round(overall_score, 2)
            })
        
        # Sort by overall score
        evaluated_bids.sort(key=lambda x: x["overall_score"], reverse=True)
        
        self.db.commit()
        
        return {
            "tender_id": tender_id,
            "tender_number": tender.tender_number,
            "total_bids": len(bids),
            "evaluation_criteria": {
                "technical_weight": technical_weight,
                "financial_weight": financial_weight
            },
            "ranked_bids": evaluated_bids,
            "recommended_bid": evaluated_bids[0] if evaluated_bids else None
        }
    
    def award_tender(
        self,
        tender_id: int,
        bid_id: int,
        user_id: int
    ) -> Dict:
        """Award tender to selected bid"""
        tender = self.db.query(Tender).filter(Tender.id == tender_id).first()
        bid = self.db.query(TenderBid).filter(TenderBid.id == bid_id).first()
        
        if not tender or not bid:
            return {"error": "Tender or bid not found"}
        
        # Update bid status
        bid.status = "awarded"
        bid.evaluated_by = user_id
        bid.evaluated_at = datetime.utcnow()
        
        # Update tender status
        tender.status = "awarded"
        tender.closed_at = datetime.utcnow()
        
        self.db.commit()
        
        return {
            "tender_id": tender_id,
            "awarded_bid": {
                "bidder_name": bid.bidder_name,
                "bid_amount": bid.bid_amount,
                "overall_score": bid.overall_score
            },
            "awarded_at": datetime.utcnow().isoformat()
        }
