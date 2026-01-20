"""
Material Tracking Service - Real-time inventory and consumption tracking
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.material import Material, BOQ, BOQItem
from datetime import datetime, timedelta

class MaterialTrackingService:
    """Material Tracking Service - Real-time inventory management"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def track_material_consumption(
        self,
        project_id: int,
        material_type: str,
        quantity_consumed: float,
        unit: str,
        location: str = None,
        phase_id: int = None
    ) -> Dict:
        """Track material consumption"""
        # Get project BOQ
        boq = self.db.query(BOQ).filter(BOQ.project_id == project_id).first()
        
        if not boq:
            return {"error": "BOQ not found. Generate BOQ first."}
        
        # Find material in BOQ
        boq_item = self.db.query(BOQItem).join(BOQ).filter(
            BOQ.project_id == project_id,
            BOQItem.item_category.ilike(f"%{material_type}%")
        ).first()
        
        if not boq_item:
            return {"error": "Material not found in BOQ"}
        
        # Calculate consumption percentage
        total_quantity = boq_item.quantity
        consumption_percentage = (quantity_consumed / total_quantity) * 100 if total_quantity > 0 else 0
        
        # Calculate remaining
        remaining_quantity = total_quantity - quantity_consumed
        
        # Check for overconsumption
        is_overconsumption = quantity_consumed > total_quantity
        
        return {
            "project_id": project_id,
            "material_type": material_type,
            "total_quantity": total_quantity,
            "quantity_consumed": quantity_consumed,
            "remaining_quantity": round(remaining_quantity, 2),
            "consumption_percentage": round(consumption_percentage, 2),
            "is_overconsumption": is_overconsumption,
            "location": location,
            "tracked_at": datetime.utcnow().isoformat()
        }
    
    def get_material_status(
        self,
        project_id: int
    ) -> Dict:
        """Get material status for project"""
        boq = self.db.query(BOQ).filter(BOQ.project_id == project_id).first()
        
        if not boq:
            return {"error": "BOQ not found"}
        
        # Get all BOQ items
        items = self.db.query(BOQItem).filter(BOQItem.boq_id == boq.id).all()
        
        material_status = []
        for item in items:
            # Simulated consumption (in production, this would come from tracking records)
            consumed = item.quantity * 0.3  # Assume 30% consumed
            
            material_status.append({
                "material": item.item_description,
                "category": item.item_category,
                "total_quantity": item.quantity,
                "unit": item.unit,
                "estimated_consumed": round(consumed, 2),
                "remaining": round(item.quantity - consumed, 2),
                "consumption_percentage": 30.0,  # Placeholder
                "status": "sufficient" if (item.quantity - consumed) > item.quantity * 0.1 else "low"
            })
        
        return {
            "project_id": project_id,
            "materials": material_status,
            "total_materials": len(material_status),
            "low_stock_count": len([m for m in material_status if m["status"] == "low"])
        }
    
    def predict_material_requirements(
        self,
        project_id: int,
        target_date: datetime
    ) -> Dict:
        """Predict material requirements based on schedule"""
        # Get project schedule and BOQ
        # Simplified prediction based on progress
        boq = self.db.query(BOQ).filter(BOQ.project_id == project_id).first()
        
        if not boq:
            return {"error": "BOQ not found"}
        
        # Days until target
        days_remaining = (target_date - datetime.utcnow()).days
        
        # Simplified: assume linear consumption
        daily_consumption_rate = 0.02  # 2% per day (simplified)
        projected_consumption = min(daily_consumption_rate * days_remaining, 1.0)
        
        items = self.db.query(BOQItem).filter(BOQItem.boq_id == boq.id).all()
        
        predictions = []
        for item in items:
            required_quantity = item.quantity * projected_consumption
            
            predictions.append({
                "material": item.item_description,
                "required_by_date": target_date.isoformat(),
                "required_quantity": round(required_quantity, 2),
                "unit": item.unit,
                "days_remaining": days_remaining
            })
        
        return {
            "project_id": project_id,
            "target_date": target_date.isoformat(),
            "days_remaining": days_remaining,
            "projected_consumption_percentage": round(projected_consumption * 100, 2),
            "material_requirements": predictions
        }
