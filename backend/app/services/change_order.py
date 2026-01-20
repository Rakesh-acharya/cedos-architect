"""
Change Order Management Service
"""

from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.advanced_features import ChangeOrder, ChangeOrderItem
from datetime import datetime
import uuid

class ChangeOrderService:
    """Change Order Management Service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_change_order(
        self,
        project_id: int,
        change_title: str,
        description: str,
        change_type: str,
        reason: str,
        items: List[Dict],
        user_id: int
    ) -> ChangeOrder:
        """Create change order"""
        co_number = f"CO-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate cost and time impact
        original_cost = sum(item.get("original_amount", 0) for item in items)
        revised_cost = sum(item.get("revised_amount", 0) for item in items)
        cost_difference = revised_cost - original_cost
        
        change_order = ChangeOrder(
            project_id=project_id,
            change_order_number=co_number,
            change_order_title=change_title,
            description=description,
            change_type=change_type,
            reason=reason,
            original_cost=original_cost,
            revised_cost=revised_cost,
            cost_difference=cost_difference,
            status="draft",
            submitted_by=user_id
        )
        
        self.db.add(change_order)
        self.db.flush()
        
        # Add items
        for item_data in items:
            item = ChangeOrderItem(
                change_order_id=change_order.id,
                item_description=item_data.get("description", ""),
                quantity_original=item_data.get("quantity_original", 0),
                quantity_revised=item_data.get("quantity_revised", 0),
                unit_rate=item_data.get("unit_rate", 0),
                amount=item_data.get("revised_amount", 0) - item_data.get("original_amount", 0)
            )
            self.db.add(item)
        
        self.db.commit()
        self.db.refresh(change_order)
        
        return change_order
    
    def approve_change_order(
        self,
        change_order_id: int,
        user_id: int
    ) -> Dict:
        """Approve change order"""
        co = self.db.query(ChangeOrder).filter(ChangeOrder.id == change_order_id).first()
        
        if not co:
            return {"error": "Change order not found"}
        
        co.status = "approved"
        co.approved_by = user_id
        co.approved_at = datetime.utcnow()
        
        self.db.commit()
        
        return {
            "change_order_id": change_order_id,
            "status": "approved",
            "approved_by": user_id,
            "approved_at": co.approved_at.isoformat(),
            "cost_impact": co.cost_difference
        }
    
    def get_change_order_summary(
        self,
        project_id: int
    ) -> Dict:
        """Get change order summary for project"""
        change_orders = self.db.query(ChangeOrder).filter(
            ChangeOrder.project_id == project_id
        ).all()
        
        total_original = sum(co.original_cost or 0 for co in change_orders)
        total_revised = sum(co.revised_cost or 0 for co in change_orders)
        total_variation = sum(co.cost_difference or 0 for co in change_orders)
        
        approved_count = len([co for co in change_orders if co.status == "approved"])
        pending_count = len([co for co in change_orders if co.status in ["draft", "submitted"]])
        
        return {
            "project_id": project_id,
            "total_change_orders": len(change_orders),
            "approved": approved_count,
            "pending": pending_count,
            "total_original_cost": total_original,
            "total_revised_cost": total_revised,
            "total_variation": total_variation,
            "variation_percentage": (total_variation / total_original * 100) if total_original > 0 else 0
        }
