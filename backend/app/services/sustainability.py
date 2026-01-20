"""
Sustainability Assessment Service - Carbon footprint and environmental impact
"""

from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.advanced_features import SustainabilityAssessment
from app.models.material import BOQ, BOQItem

class SustainabilityService:
    """Sustainability Assessment Service"""
    
    # Carbon factors (kg CO2 per unit)
    CARBON_FACTORS = {
        "concrete": {
            "M20": 300,  # kg CO2 per m³
            "M25": 320,
            "M30": 340,
            "M35": 360,
            "M40": 380
        },
        "steel": {
            "Fe415": 2.0,  # kg CO2 per kg
            "Fe500": 2.1,
            "Fe550": 2.2
        },
        "cement": 0.9,  # kg CO2 per kg
        "aggregate": 0.01,  # kg CO2 per kg
        "sand": 0.01,
        "bitumen": 0.4  # kg CO2 per kg
    }
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def assess_project_sustainability(
        self,
        project_id: int
    ) -> Dict:
        """
        Comprehensive sustainability assessment
        """
        # Get BOQ
        boq = self.db.query(BOQ).filter(BOQ.project_id == project_id).first()
        
        if not boq:
            return {"error": "BOQ not found. Generate BOQ first."}
        
        # Calculate embodied carbon
        embodied_carbon = self._calculate_embodied_carbon(boq)
        
        # Calculate operational carbon (simplified)
        operational_carbon = self._estimate_operational_carbon(project_id)
        
        total_carbon = embodied_carbon + operational_carbon
        
        # Calculate sustainability score
        sustainability_score = self._calculate_sustainability_score(total_carbon, project_id)
        
        # Material breakdown
        material_breakdown = self._get_material_breakdown(boq)
        
        # Improvement suggestions
        suggestions = self._generate_improvement_suggestions(boq, total_carbon)
        
        # Save assessment
        assessment = SustainabilityAssessment(
            project_id=project_id,
            embodied_carbon_kg=embodied_carbon,
            operational_carbon_kg=operational_carbon,
            total_carbon_kg=total_carbon,
            material_breakdown=material_breakdown,
            sustainability_score=sustainability_score,
            improvement_suggestions=suggestions
        )
        
        self.db.add(assessment)
        self.db.commit()
        
        return {
            "project_id": project_id,
            "embodied_carbon_kg": round(embodied_carbon, 2),
            "operational_carbon_kg": round(operational_carbon, 2),
            "total_carbon_kg": round(total_carbon, 2),
            "sustainability_score": round(sustainability_score, 2),
            "material_breakdown": material_breakdown,
            "improvement_suggestions": suggestions,
            "carbon_equivalent": {
                "trees_required": round(total_carbon / 21.77, 0),  # 1 tree = 21.77 kg CO2/year
                "car_miles": round(total_carbon / 0.411, 0)  # 1 mile = 0.411 kg CO2
            }
        }
    
    def _calculate_embodied_carbon(self, boq: BOQ) -> float:
        """Calculate embodied carbon from BOQ"""
        total_carbon = 0.0
        
        for item in boq.items:
            material_type = item.item_category.lower()
            quantity = item.quantity
            unit = item.unit.lower()
            
            if "concrete" in material_type:
                # Extract grade from description
                grade = self._extract_concrete_grade(item.item_description)
                factor = self.CARBON_FACTORS["concrete"].get(grade, 320)
                if unit == "m³":
                    total_carbon += quantity * factor
                elif unit == "kg":
                    total_carbon += (quantity / 2400) * factor  # Convert kg to m³
            
            elif "steel" in material_type:
                grade = self._extract_steel_grade(item.item_description)
                factor = self.CARBON_FACTORS["steel"].get(grade, 2.0)
                if unit == "kg":
                    total_carbon += quantity * factor
            
            elif "cement" in material_type:
                factor = self.CARBON_FACTORS["cement"]
                if unit == "kg":
                    total_carbon += quantity * factor
            
            elif "aggregate" in material_type or "sand" in material_type:
                factor = self.CARBON_FACTORS.get(material_type, 0.01)
                if unit == "m³":
                    # Convert m³ to kg (assume 1600 kg/m³)
                    total_carbon += quantity * 1600 * factor
                elif unit == "kg":
                    total_carbon += quantity * factor
            
            elif "bitumen" in material_type:
                factor = self.CARBON_FACTORS["bitumen"]
                if unit == "kg":
                    total_carbon += quantity * factor
        
        return total_carbon
    
    def _extract_concrete_grade(self, description: str) -> str:
        """Extract concrete grade from description"""
        for grade in ["M40", "M35", "M30", "M25", "M20"]:
            if grade in description:
                return grade
        return "M25"  # Default
    
    def _extract_steel_grade(self, description: str) -> str:
        """Extract steel grade from description"""
        for grade in ["Fe550", "Fe500", "Fe415"]:
            if grade in description:
                return grade
        return "Fe415"  # Default
    
    def _estimate_operational_carbon(self, project_id: int) -> float:
        """Estimate operational carbon (simplified)"""
        # For buildings: energy consumption over lifetime
        # For roads: vehicle emissions reduction/enhancement
        # Simplified: assume 20% of embodied carbon
        return 0  # Placeholder - would need project type and usage data
    
    def _calculate_sustainability_score(self, total_carbon: float, project_id: int) -> float:
        """Calculate sustainability score (0-100)"""
        # Normalize based on project size
        # Lower carbon = higher score
        # Simplified scoring
        if total_carbon < 100000:
            return 90
        elif total_carbon < 500000:
            return 75
        elif total_carbon < 1000000:
            return 60
        else:
            return 45
    
    def _get_material_breakdown(self, boq: BOQ) -> Dict:
        """Get carbon breakdown by material"""
        breakdown = {}
        
        for item in boq.items:
            material_type = item.item_category.lower()
            if material_type not in breakdown:
                breakdown[material_type] = {
                    "quantity": 0,
                    "unit": item.unit,
                    "carbon_kg": 0
                }
            
            breakdown[material_type]["quantity"] += item.quantity
            
            # Calculate carbon (simplified)
            if "concrete" in material_type:
                grade = self._extract_concrete_grade(item.item_description)
                factor = self.CARBON_FACTORS["concrete"].get(grade, 320)
                breakdown[material_type]["carbon_kg"] += item.quantity * factor
        
        return breakdown
    
    def _generate_improvement_suggestions(self, boq: BOQ, total_carbon: float) -> List[str]:
        """Generate sustainability improvement suggestions"""
        suggestions = []
        
        # Check for high-carbon materials
        for item in boq.items:
            if "concrete" in item.item_category.lower():
                grade = self._extract_concrete_grade(item.item_description)
                if grade in ["M35", "M40"]:
                    suggestions.append(
                        f"Consider using {grade.replace('M', 'M')} with supplementary cementitious materials (SCM) to reduce carbon"
                    )
            
            if "steel" in item.item_category.lower():
                suggestions.append(
                    "Consider using recycled steel to reduce embodied carbon"
                )
        
        if total_carbon > 1000000:
            suggestions.append(
                "High carbon footprint. Consider: 1) Using lower-grade concrete where possible, "
                "2) Optimizing design to reduce material quantities, 3) Using sustainable materials"
            )
        
        if not suggestions:
            suggestions.append("Project has good sustainability practices. Continue optimizing.")
        
        return suggestions
