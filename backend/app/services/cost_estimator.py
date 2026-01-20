"""
Cost Estimation Service
"""

from typing import Dict, List, Optional
from app.models.material import BOQItem
from app.models.cost import ScheduleOfRates

class CostEstimator:
    """Cost Estimation Service"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def get_unit_rate(
        self,
        item_code: str,
        rate_source: str = "SOR"
    ) -> float:
        """
        Get unit rate from SOR or market rates
        """
        if rate_source == "SOR":
            # Query SOR
            sor_item = self.db.query(ScheduleOfRates).filter(
                ScheduleOfRates.item_code == item_code,
                ScheduleOfRates.is_active == True
            ).first()
            
            if sor_item:
                return sor_item.unit_rate
        
        # Default rates (fallback)
        default_rates = {
            "CONC": 5000,  # Concrete per m³
            "STL": 60,    # Steel per kg
            "CEM": 8,     # Cement per kg
            "SAND": 800,  # Sand per m³
            "AGG": 1000,  # Aggregate per m³
            "EXC": 200    # Excavation per m³
        }
        
        # Extract prefix from item code
        prefix = item_code.split("-")[0]
        return default_rates.get(prefix, 100)
    
    def calculate_cost_with_escalation(
        self,
        base_cost: float,
        escalation_percentage: float,
        months: int = 12
    ) -> float:
        """
        Calculate escalated cost
        """
        # Simple escalation (monthly compounding)
        escalated_cost = base_cost * ((1 + escalation_percentage / 12) ** months)
        return escalated_cost
    
    def calculate_gst(
        self,
        taxable_amount: float,
        gst_percentage: float = 0.18
    ) -> Dict[str, float]:
        """
        Calculate GST breakdown
        """
        cgst = taxable_amount * (gst_percentage / 2)
        sgst = taxable_amount * (gst_percentage / 2)
        igst = 0  # IGST for inter-state
        
        total_gst = cgst + sgst + igst
        
        return {
            "cgst": round(cgst, 2),
            "sgst": round(sgst, 2),
            "igst": round(igst, 2),
            "total_gst": round(total_gst, 2),
            "total_with_gst": round(taxable_amount + total_gst, 2)
        }
