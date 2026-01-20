"""
Risk Assessment Service - Project risk analysis and mitigation
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.advanced_features import ProjectRisk, RiskCategory
from datetime import datetime

class RiskAssessmentService:
    """Risk Assessment Service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def assess_project_risks(
        self,
        project_id: int,
        project_data: Dict
    ) -> Dict:
        """
        Comprehensive project risk assessment
        """
        risks = []
        
        # Technical Risks
        risks.extend(self._assess_technical_risks(project_id, project_data))
        
        # Financial Risks
        risks.extend(self._assess_financial_risks(project_id, project_data))
        
        # Schedule Risks
        risks.extend(self._assess_schedule_risks(project_id, project_data))
        
        # Safety Risks
        risks.extend(self._assess_safety_risks(project_id, project_data))
        
        # Environmental Risks
        risks.extend(self._assess_environmental_risks(project_id, project_data))
        
        # Regulatory Risks
        risks.extend(self._assess_regulatory_risks(project_id, project_data))
        
        # Calculate overall risk score
        overall_risk = self._calculate_overall_risk(risks)
        
        return {
            "project_id": project_id,
            "overall_risk_score": overall_risk,
            "risk_level": self._get_risk_level(overall_risk),
            "risks": risks,
            "recommendations": self._generate_risk_recommendations(risks)
        }
    
    def _assess_technical_risks(self, project_id: int, project_data: Dict) -> List[Dict]:
        """Assess technical risks"""
        risks = []
        
        # Soil bearing capacity risk
        if project_data.get("soil_bearing_capacity", 0) < 150:
            risks.append({
                "name": "Low Soil Bearing Capacity",
                "category": RiskCategory.TECHNICAL,
                "description": "Soil bearing capacity is below recommended minimum",
                "probability": 0.7,
                "impact": 0.8,
                "mitigation": "Conduct detailed soil investigation, consider pile foundation"
            })
        
        # Seismic zone risk
        if project_data.get("seismic_zone") in ["Zone IV", "Zone V"]:
            risks.append({
                "name": "High Seismic Risk",
                "category": RiskCategory.TECHNICAL,
                "description": "Project in high seismic zone",
                "probability": 0.6,
                "impact": 0.9,
                "mitigation": "Design for higher seismic forces, use ductile detailing"
            })
        
        return risks
    
    def _assess_financial_risks(self, project_id: int, project_data: Dict) -> List[Dict]:
        """Assess financial risks"""
        risks = []
        
        # Budget constraint risk
        if project_data.get("budget_constraint", 0) < 1000000:
            risks.append({
                "name": "Tight Budget",
                "category": RiskCategory.FINANCIAL,
                "description": "Budget may be insufficient for project scope",
                "probability": 0.6,
                "impact": 0.7,
                "mitigation": "Review scope, identify cost-saving alternatives"
            })
        
        # Material cost escalation
        risks.append({
            "name": "Material Cost Escalation",
            "category": RiskCategory.FINANCIAL,
            "description": "Rising material costs may impact budget",
            "probability": 0.5,
            "impact": 0.6,
            "mitigation": "Lock in material prices early, include escalation clause"
        })
        
        return risks
    
    def _assess_schedule_risks(self, project_id: int, project_data: Dict) -> List[Dict]:
        """Assess schedule risks"""
        risks = []
        
        risks.append({
            "name": "Weather Delays",
            "category": RiskCategory.SCHEDULE,
            "description": "Monsoon/weather may cause construction delays",
            "probability": 0.5,
            "impact": 0.6,
            "mitigation": "Plan for weather contingencies, indoor work during bad weather"
        })
        
        risks.append({
            "name": "Material Delivery Delays",
            "category": RiskCategory.SCHEDULE,
            "description": "Delayed material delivery may impact schedule",
            "probability": 0.4,
            "impact": 0.5,
            "mitigation": "Order materials well in advance, maintain buffer stock"
        })
        
        return risks
    
    def _assess_safety_risks(self, project_id: int, project_data: Dict) -> List[Dict]:
        """Assess safety risks"""
        risks = []
        
        project_type = project_data.get("project_type", "")
        
        if "bridge" in project_type.lower() or "highway" in project_type.lower():
            risks.append({
                "name": "High-Risk Construction",
                "category": RiskCategory.SAFETY,
                "description": "Bridge/highway construction involves high safety risks",
                "probability": 0.4,
                "impact": 0.9,
                "mitigation": "Strict safety protocols, regular safety audits, worker training"
            })
        
        return risks
    
    def _assess_environmental_risks(self, project_id: int, project_data: Dict) -> List[Dict]:
        """Assess environmental risks"""
        risks = []
        
        risks.append({
            "name": "Environmental Impact",
            "category": RiskCategory.ENVIRONMENTAL,
            "description": "Construction may impact local environment",
            "probability": 0.5,
            "impact": 0.6,
            "mitigation": "Environmental impact assessment, mitigation measures"
        })
        
        return risks
    
    def _assess_regulatory_risks(self, project_id: int, project_data: Dict) -> List[Dict]:
        """Assess regulatory risks"""
        risks = []
        
        risks.append({
            "name": "Permit Delays",
            "category": RiskCategory.REGULATORY,
            "description": "Delays in obtaining permits may impact project",
            "probability": 0.4,
            "impact": 0.7,
            "mitigation": "Apply for permits early, maintain good relations with authorities"
        })
        
        return risks
    
    def _calculate_overall_risk(self, risks: List[Dict]) -> float:
        """Calculate overall project risk score"""
        if not risks:
            return 0.0
        
        total_risk = sum(r["probability"] * r["impact"] for r in risks)
        return round(total_risk / len(risks), 3)
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level from score"""
        if risk_score < 0.3:
            return "Low"
        elif risk_score < 0.6:
            return "Medium"
        elif risk_score < 0.8:
            return "High"
        else:
            return "Critical"
    
    def _generate_risk_recommendations(self, risks: List[Dict]) -> List[str]:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        # Sort by risk score
        sorted_risks = sorted(risks, key=lambda x: x["probability"] * x["impact"], reverse=True)
        
        # Top 3 risks
        for risk in sorted_risks[:3]:
            recommendations.append(f"Priority: {risk['name']} - {risk.get('mitigation', 'Review and mitigate')}")
        
        return recommendations
    
    def save_risks_to_database(self, project_id: int, risks: List[Dict], user_id: int):
        """Save risks to database"""
        for risk_data in risks:
            risk = ProjectRisk(
                project_id=project_id,
                risk_name=risk_data["name"],
                risk_category=risk_data["category"],
                description=risk_data["description"],
                probability=risk_data["probability"],
                impact=risk_data["impact"],
                risk_score=risk_data["probability"] * risk_data["impact"],
                mitigation_strategy=risk_data.get("mitigation", ""),
                identified_by=user_id
            )
            self.db.add(risk)
        
        self.db.commit()
