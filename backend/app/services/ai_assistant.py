"""
AI Assistant Service - Controlled AI assistance for explanations and suggestions
"""

from typing import Dict, Optional
from app.core.config import settings
import json

class AIAssistant:
    """AI Assistant Service - Provides controlled AI assistance"""
    
    def __init__(self):
        self.enabled = settings.AI_ENABLED
        # In production, initialize OpenAI client here
        # self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
    
    def explain_design_logic(
        self,
        calculation_type: str,
        input_parameters: Dict,
        design_outputs: Dict,
        code_standard: str = "IS 456:2000"
    ) -> str:
        """
        Explain why a particular design decision was made
        """
        if not self.enabled:
            return "AI assistance is disabled. Please contact your system administrator."
        
        # Rule-based explanations (AI would enhance this)
        explanations = {
            "footing_design": f"""
            The footing design follows {code_standard}:
            - Required area calculated based on column load and soil bearing capacity
            - Safety factor of 2.5 applied as per code requirements
            - Footing size ensures adequate load distribution
            - Effective depth calculated to resist bending moments
            """,
            "column_design": f"""
            The column design follows {code_standard}:
            - Column size determined from axial load and material strengths
            - Steel percentage maintained between 1-4% as per code
            - Effective length considered for slenderness
            - Material grades selected based on load intensity
            """,
            "beam_design": f"""
            The beam design follows {code_standard}:
            - Section dimensions calculated to resist bending moments
            - Steel reinforcement designed for moment and shear
            - Minimum steel requirements checked
            - Shear reinforcement provided where required
            """,
            "slab_design": f"""
            The slab design follows {code_standard}:
            - Thickness determined from span and loading
            - Minimum thickness requirements satisfied
            - Steel reinforcement designed for bending
            - Load combinations considered as per code
            """
        }
        
        return explanations.get(calculation_type, "Design follows standard engineering principles.")
    
    def suggest_optimization(
        self,
        calculation_type: str,
        current_design: Dict,
        constraints: Dict
    ) -> Dict[str, any]:
        """
        Suggest design optimizations
        """
        suggestions = []
        
        if calculation_type == "column_design":
            # Check if steel percentage is too high
            if current_design.get("steel_percentage", 0) > 3.0:
                suggestions.append({
                    "type": "material_optimization",
                    "message": "Consider increasing column size to reduce steel percentage",
                    "potential_savings": "5-10% material cost"
                })
        
        elif calculation_type == "beam_design":
            # Check if depth can be optimized
            if current_design.get("effective_depth", 0) > 0.5:
                suggestions.append({
                    "type": "dimension_optimization",
                    "message": "Consider increasing beam width to reduce depth",
                    "potential_savings": "Better formwork efficiency"
                })
        
        return {
            "suggestions": suggestions,
            "note": "All suggestions must be validated against code requirements"
        }
    
    def answer_query(
        self,
        query: str,
        context: Dict
    ) -> str:
        """
        Answer natural language queries about design
        """
        # Rule-based Q&A (AI would enhance this)
        query_lower = query.lower()
        
        if "why" in query_lower and "m30" in query_lower:
            return """
            M30 concrete is recommended based on:
            1. Load intensity exceeding M25 capacity
            2. Exposure conditions requiring higher durability
            3. Code requirements for the given application
            
            M30 provides:
            - Higher compressive strength (30 MPa)
            - Better durability in severe environments
            - Compliance with IS 456:2000 requirements
            """
        
        elif "safety" in query_lower and "factor" in query_lower:
            return """
            Safety factors per IS 456:2000:
            - Concrete: 1.5
            - Steel: 1.15
            - Overturning: 1.5
            - Sliding: 1.5
            
            These factors account for:
            - Material variability
            - Load uncertainties
            - Construction tolerances
            - Long-term effects
            """
        
        else:
            return """
            I can help explain:
            - Design logic and calculations
            - Code compliance requirements
            - Material grade selection
            - Optimization opportunities
            
            Please ask a specific question about your design.
            """
