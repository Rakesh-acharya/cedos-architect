"""
Geotechnical Analysis Service - Advanced soil analysis and foundation design
"""

from typing import Dict, List
import math

class GeotechnicalAnalysisService:
    """Geotechnical Analysis Service - Advanced soil mechanics"""
    
    def analyze_soil_bearing_capacity(
        self,
        soil_type: str,
        cohesion: float,
        angle_of_internal_friction: float,
        unit_weight: float,
        foundation_depth: float,
        foundation_width: float,
        foundation_length: float = 0.0
    ) -> Dict:
        """
        Calculate soil bearing capacity using Terzaghi's method (IS 6403)
        """
        # Bearing capacity factors
        phi_rad = math.radians(angle_of_internal_friction)
        
        Nc = (math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.pi/4 + phi_rad/2))**2 - 1) * (1 / math.tan(phi_rad))
        Nq = math.exp(math.pi * math.tan(phi_rad)) * (math.tan(math.pi/4 + phi_rad/2))**2
        Ngamma = 2 * (Nq + 1) * math.tan(phi_rad)
        
        # Shape factors
        if foundation_length > 0:
            # Rectangular footing
            shape_factor_c = 1 + 0.2 * (foundation_width / foundation_length)
            shape_factor_q = 1 + 0.2 * (foundation_width / foundation_length)
            shape_factor_gamma = 1 - 0.4 * (foundation_width / foundation_length)
        else:
            # Square/circular footing
            shape_factor_c = 1.3
            shape_factor_q = 1.0
            shape_factor_gamma = 0.8
        
        # Depth factors (simplified)
        depth_factor_q = 1 + 2 * math.tan(phi_rad) * (1 - math.sin(phi_rad))**2 * (foundation_depth / foundation_width)
        depth_factor_q = min(depth_factor_q, 1.0)  # Cap at 1.0 for shallow foundations
        
        # Terzaghi's bearing capacity equation
        # q_ult = c*Nc*sc*dc + q*Nq*sq*dq + 0.5*gamma*B*Ngamma*sgamma
        q = unit_weight * foundation_depth  # Surcharge
        
        q_ult = (
            cohesion * Nc * shape_factor_c +
            q * Nq * shape_factor_q * depth_factor_q +
            0.5 * unit_weight * foundation_width * Ngamma * shape_factor_gamma
        )
        
        # Safe bearing capacity (with factor of safety = 3)
        safe_bearing_capacity = q_ult / 3.0
        
        return {
            "soil_type": soil_type,
            "ultimate_bearing_capacity": round(q_ult, 2),  # kN/m²
            "safe_bearing_capacity": round(safe_bearing_capacity, 2),  # kN/m²
            "bearing_capacity_factors": {
                "Nc": round(Nc, 2),
                "Nq": round(Nq, 2),
                "Ngamma": round(Ngamma, 2)
            },
            "shape_factors": {
                "sc": round(shape_factor_c, 2),
                "sq": round(shape_factor_q, 2),
                "sgamma": round(shape_factor_gamma, 2)
            },
            "depth_factors": {
                "dq": round(depth_factor_q, 2)
            },
            "factor_of_safety": 3.0,
            "code_standard": "IS 6403:1981"
        }
    
    def analyze_slope_stability(
        self,
        slope_height: float,
        slope_angle: float,
        soil_cohesion: float,
        angle_of_internal_friction: float,
        unit_weight: float,
        water_table_depth: float = None
    ) -> Dict:
        """
        Analyze slope stability using simplified Bishop's method
        """
        phi_rad = math.radians(angle_of_internal_friction)
        beta_rad = math.radians(slope_angle)
        
        # Simplified stability analysis
        # Factor of safety = (c + sigma*tan(phi)) / (gamma*H*sin(beta)*cos(beta))
        
        # Average stress
        sigma = 0.5 * unit_weight * slope_height
        
        # Factor of safety (simplified)
        numerator = soil_cohesion + sigma * math.tan(phi_rad)
        denominator = unit_weight * slope_height * math.sin(beta_rad) * math.cos(beta_rad)
        
        factor_of_safety = numerator / denominator if denominator > 0 else 999
        
        # Critical slope angle
        critical_angle = math.degrees(math.atan(math.tan(phi_rad) + (soil_cohesion / (unit_weight * slope_height))))
        
        # Stability status
        if factor_of_safety >= 1.5:
            status = "stable"
        elif factor_of_safety >= 1.2:
            status = "marginal"
        else:
            status = "unstable"
        
        return {
            "slope_height": slope_height,
            "slope_angle": slope_angle,
            "factor_of_safety": round(factor_of_safety, 3),
            "critical_slope_angle": round(critical_angle, 2),
            "status": status,
            "recommendation": self._get_slope_recommendation(factor_of_safety),
            "code_standard": "IS 7894:1975"
        }
    
    def _get_slope_recommendation(self, fos: float) -> str:
        """Get slope stability recommendation"""
        if fos >= 1.5:
            return "Slope is stable. No remedial measures required."
        elif fos >= 1.2:
            return "Slope is marginally stable. Consider slope reduction or reinforcement."
        else:
            return "Slope is unstable. Immediate remedial measures required: slope reduction, retaining wall, or soil stabilization."
    
    def calculate_settlement(
        self,
        foundation_width: float,
        foundation_length: float,
        applied_pressure: float,
        soil_elastic_modulus: float,
        poisson_ratio: float = 0.3,
        foundation_type: str = "flexible"
    ) -> Dict:
        """
        Calculate foundation settlement using elastic theory
        """
        # Influence factor (depends on foundation shape)
        if foundation_length > foundation_width * 10:
            # Strip foundation
            influence_factor = 1.0
        elif foundation_length == foundation_width:
            # Square foundation
            influence_factor = 0.88
        else:
            # Rectangular foundation
            L_by_B = foundation_length / foundation_width
            influence_factor = 1.12 - 0.16 * math.log10(L_by_B)
        
        # Settlement calculation (simplified elastic settlement)
        # S = (q * B * I * (1 - mu²)) / E
        settlement = (applied_pressure * foundation_width * influence_factor * (1 - poisson_ratio**2)) / soil_elastic_modulus
        
        # Convert to mm
        settlement_mm = settlement * 1000
        
        # Allowable settlement check (IS 1904)
        if foundation_width < 3.0:
            allowable_settlement = 50  # mm for isolated footings
        else:
            allowable_settlement = 75  # mm for rafts
        
        is_acceptable = settlement_mm <= allowable_settlement
        
        return {
            "foundation_type": foundation_type,
            "applied_pressure": applied_pressure,
            "settlement_mm": round(settlement_mm, 2),
            "settlement_m": round(settlement, 4),
            "allowable_settlement_mm": allowable_settlement,
            "is_acceptable": is_acceptable,
            "influence_factor": round(influence_factor, 3),
            "code_standard": "IS 1904:1986"
        }
    
    def design_pile_foundation(
        self,
        axial_load: float,
        soil_type: str,
        pile_type: str = "bored",  # bored, driven
        pile_diameter: float = 0.6,
        pile_length: float = 10.0,
        skin_friction_coefficient: float = 0.5
    ) -> Dict:
        """
        Design pile foundation (simplified)
        """
        # Unit skin friction (simplified)
        # Values depend on soil type
        unit_skin_friction = {
            "clay": 20,  # kN/m²
            "silt": 25,
            "sand": 30,
            "gravel": 40
        }
        
        fs = unit_skin_friction.get(soil_type.lower(), 25)
        
        # Skin friction capacity
        pile_perimeter = math.pi * pile_diameter
        skin_friction_capacity = fs * pile_perimeter * pile_length * skin_friction_coefficient
        
        # End bearing capacity (simplified)
        # For cohesive soils: Qb = 9 * cu * Ab
        # For granular: Qb = Nq * sigma_v * Ab
        pile_area = math.pi * (pile_diameter / 2)**2
        end_bearing_capacity = 9 * 50 * pile_area  # Simplified (assuming cu = 50 kN/m²)
        
        # Total capacity
        total_capacity = skin_friction_capacity + end_bearing_capacity
        
        # Factor of safety
        factor_of_safety = 2.5
        safe_capacity = total_capacity / factor_of_safety
        
        # Number of piles required
        num_piles = math.ceil(axial_load / safe_capacity)
        
        return {
            "pile_type": pile_type,
            "pile_diameter": pile_diameter,
            "pile_length": pile_length,
            "skin_friction_capacity": round(skin_friction_capacity, 2),
            "end_bearing_capacity": round(end_bearing_capacity, 2),
            "total_capacity": round(total_capacity, 2),
            "safe_capacity": round(safe_capacity, 2),
            "factor_of_safety": factor_of_safety,
            "number_of_piles_required": int(num_piles),
            "code_standard": "IS 2911:2010"
        }
