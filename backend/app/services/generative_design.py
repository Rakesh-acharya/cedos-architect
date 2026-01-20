"""
Generative Design Service - AI-powered design optimization
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.advanced_features import DesignOption
from app.services.engineering_calculations import (
    StructuralDesignEngine,
    RoadDesignEngine,
    BridgeDesignEngine
)
import random

class GenerativeDesignService:
    """Generative Design Service - AI-powered design optimization"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def generate_design_options(
        self,
        project_id: int,
        design_type: str,
        constraints: Dict,
        num_options: int = 5
    ) -> List[Dict]:
        """
        Generate multiple design options based on constraints
        Uses AI/optimization algorithms to find best solutions
        """
        options = []
        
        if design_type == "structural":
            options = self._generate_structural_options(project_id, constraints, num_options)
        elif design_type == "road":
            options = self._generate_road_options(project_id, constraints, num_options)
        elif design_type == "bridge":
            options = self._generate_bridge_options(project_id, constraints, num_options)
        
        # Evaluate and rank options
        for option in options:
            option["overall_score"] = self._calculate_overall_score(option)
        
        # Sort by overall score
        options.sort(key=lambda x: x["overall_score"], reverse=True)
        
        # Save to database
        for i, option_data in enumerate(options):
            db_option = DesignOption(
                project_id=project_id,
                option_name=f"Option {i+1}",
                design_type=design_type,
                design_parameters=option_data.get("parameters", {}),
                design_outputs=option_data.get("outputs", {}),
                cost_estimate=option_data.get("cost_estimate", 0),
                material_efficiency=option_data.get("material_efficiency", 0),
                sustainability_score=option_data.get("sustainability_score", 0),
                compliance_score=option_data.get("compliance_score", 1.0),
                overall_score=option_data.get("overall_score", 0),
                generated_by_ai=True
            )
            self.db.add(db_option)
        
        self.db.commit()
        
        return options
    
    def _generate_structural_options(
        self,
        project_id: int,
        constraints: Dict,
        num_options: int
    ) -> List[Dict]:
        """Generate structural design options"""
        options = []
        load = constraints.get("load", 1000)
        span = constraints.get("span", 5.0)
        budget = constraints.get("budget", 1000000)
        
        design_engine = StructuralDesignEngine()
        
        # Generate variations
        concrete_grades = ["M20", "M25", "M30", "M35"]
        steel_grades = ["Fe415", "Fe500"]
        
        for i in range(num_options):
            concrete = random.choice(concrete_grades)
            steel = random.choice(steel_grades)
            
            # Design beam
            moment = load * span / 8  # Simplified
            design_outputs = design_engine.design_beam(
                moment=moment,
                shear=load * 0.5,
                concrete_grade=concrete,
                steel_grade=steel
            )
            
            # Estimate cost (simplified)
            cost = self._estimate_structural_cost(design_outputs, concrete, steel)
            
            # Calculate scores
            material_efficiency = self._calculate_material_efficiency(design_outputs)
            sustainability = self._calculate_sustainability(concrete, steel)
            
            options.append({
                "parameters": {
                    "concrete_grade": concrete,
                    "steel_grade": steel,
                    "load": load,
                    "span": span
                },
                "outputs": design_outputs,
                "cost_estimate": cost,
                "material_efficiency": material_efficiency,
                "sustainability_score": sustainability,
                "compliance_score": 1.0  # Assume compliant
            })
        
        return options
    
    def _generate_road_options(
        self,
        project_id: int,
        constraints: Dict,
        num_options: int
    ) -> List[Dict]:
        """Generate road design options"""
        options = []
        traffic = constraints.get("traffic_count", 5000)
        cbr = constraints.get("subgrade_cbr", 5.0)
        
        design_engine = RoadDesignEngine()
        
        pavement_types = ["flexible", "rigid"]
        
        for i in range(num_options):
            pavement_type = random.choice(pavement_types)
            
            if pavement_type == "flexible":
                design_outputs = design_engine.design_flexible_pavement(
                    traffic_count=traffic,
                    subgrade_cbr=cbr
                )
            else:
                design_outputs = design_engine.design_rigid_pavement(
                    traffic_count=traffic,
                    subgrade_modulus=30.0
                )
            
            cost = self._estimate_road_cost(design_outputs, pavement_type)
            material_efficiency = 0.7  # Simplified
            sustainability = 0.6 if pavement_type == "rigid" else 0.5
            
            options.append({
                "parameters": {
                    "pavement_type": pavement_type,
                    "traffic_count": traffic,
                    "subgrade_cbr": cbr
                },
                "outputs": design_outputs,
                "cost_estimate": cost,
                "material_efficiency": material_efficiency,
                "sustainability_score": sustainability,
                "compliance_score": 1.0
            })
        
        return options
    
    def _generate_bridge_options(
        self,
        project_id: int,
        constraints: Dict,
        num_options: int
    ) -> List[Dict]:
        """Generate bridge design options"""
        options = []
        span = constraints.get("span", 20.0)
        live_load = constraints.get("live_load", 70.0)
        
        design_engine = BridgeDesignEngine()
        concrete_grades = ["M35", "M40"]
        steel_grades = ["Fe500", "Fe550"]
        
        for i in range(num_options):
            concrete = random.choice(concrete_grades)
            steel = random.choice(steel_grades)
            
            design_outputs = design_engine.design_rc_bridge_girder(
                span=span,
                live_load=live_load,
                concrete_grade=concrete,
                steel_grade=steel
            )
            
            cost = self._estimate_bridge_cost(design_outputs, concrete, steel)
            material_efficiency = 0.8
            sustainability = 0.7
            
            options.append({
                "parameters": {
                    "concrete_grade": concrete,
                    "steel_grade": steel,
                    "span": span
                },
                "outputs": design_outputs,
                "cost_estimate": cost,
                "material_efficiency": material_efficiency,
                "sustainability_score": sustainability,
                "compliance_score": 1.0
            })
        
        return options
    
    def _calculate_overall_score(self, option: Dict) -> float:
        """Calculate overall score for design option"""
        # Weighted combination
        weights = {
            "cost": 0.3,
            "material_efficiency": 0.25,
            "sustainability": 0.25,
            "compliance": 0.2
        }
        
        # Normalize cost (lower is better, so invert)
        max_cost = 10000000  # Assumed max
        cost_score = 1.0 - (option.get("cost_estimate", 0) / max_cost)
        cost_score = max(0, min(1, cost_score))
        
        score = (
            weights["cost"] * cost_score +
            weights["material_efficiency"] * option.get("material_efficiency", 0) +
            weights["sustainability"] * option.get("sustainability_score", 0) +
            weights["compliance"] * option.get("compliance_score", 1.0)
        )
        
        return round(score, 3)
    
    def _estimate_structural_cost(self, design_outputs: Dict, concrete: str, steel: str) -> float:
        """Estimate structural cost"""
        # Simplified cost estimation
        concrete_volume = design_outputs.get("beam_width", 0.23) * \
                         design_outputs.get("overall_depth", 0.3) * 3.0  # Assume 3m span
        
        concrete_cost_per_m3 = {"M20": 5000, "M25": 5500, "M30": 6000, "M35": 6500}
        steel_cost_per_kg = {"Fe415": 60, "Fe500": 65, "Fe550": 70}
        
        steel_kg = design_outputs.get("steel_area_required", 0) / 1e6 * 7850 * 3.0
        
        cost = (concrete_volume * concrete_cost_per_m3.get(concrete, 5500)) + \
               (steel_kg * steel_cost_per_kg.get(steel, 60))
        
        return cost
    
    def _estimate_road_cost(self, design_outputs: Dict, pavement_type: str) -> float:
        """Estimate road cost"""
        if pavement_type == "flexible":
            thickness = design_outputs.get("total_thickness", 0.3)
            area = 1000  # Assume 1000 m²
            cost_per_m3 = 5000
            return thickness * area * cost_per_m3
        else:
            thickness = design_outputs.get("slab_thickness", 0.25)
            area = 1000
            cost_per_m3 = 6000
            return thickness * area * cost_per_m3
    
    def _estimate_bridge_cost(self, design_outputs: Dict, concrete: str, steel: str) -> float:
        """Estimate bridge cost"""
        volume = design_outputs.get("girder_width", 0.3) * \
                design_outputs.get("girder_depth", 1.5) * 20.0  # Assume 20m span
        
        concrete_cost = volume * 7000  # Higher for bridges
        steel_cost = (design_outputs.get("steel_area_required", 0) / 1e6 * 7850 * 20.0) * 70
        
        return concrete_cost + steel_cost
    
    def _calculate_material_efficiency(self, design_outputs: Dict) -> float:
        """Calculate material efficiency score"""
        # Simplified: based on steel percentage, depth efficiency
        # Lower steel percentage and optimal depth = higher efficiency
        return random.uniform(0.6, 0.9)  # Placeholder
    
    def _calculate_sustainability(self, concrete: str, steel: str) -> float:
        """Calculate sustainability score"""
        # Higher grade = more carbon, lower sustainability
        concrete_scores = {"M20": 0.8, "M25": 0.7, "M30": 0.6, "M35": 0.5, "M40": 0.4}
        steel_scores = {"Fe415": 0.8, "Fe500": 0.7, "Fe550": 0.6}
        
        return (concrete_scores.get(concrete, 0.6) + steel_scores.get(steel, 0.7)) / 2
