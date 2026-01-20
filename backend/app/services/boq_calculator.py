"""
BOQ Calculator - Automatically generates Bill of Quantities
"""

from typing import Dict, List
from app.models.calculation import Calculation
from app.models.material import BOQ, BOQItem, Material, MaterialGrade
from app.services.engineering_calculations import StructuralDesignEngine

class BOQCalculator:
    """BOQ Calculator Service"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def calculate_material_quantities(
        self,
        calculations: List[Calculation],
        wastage_factors: Dict[str, float] = None
    ) -> Dict[str, float]:
        """
        Calculate total material quantities from calculations
        """
        if wastage_factors is None:
            wastage_factors = {
                "cement": 0.02,  # 2%
                "steel": 0.05,   # 5%
                "concrete": 0.02, # 2%
                "sand": 0.02,
                "aggregate": 0.02
            }
        
        quantities = {
            "cement": 0.0,
            "steel": 0.0,
            "concrete": 0.0,
            "sand": 0.0,
            "aggregate": 0.0,
            "excavation": 0.0
        }
        
        for calc in calculations:
            design_outputs = calc.design_outputs or {}
            calc_type = calc.calculation_type
            
            if calc_type.value == "footing_design":
                # Extract footing quantities
                footing_size = design_outputs.get("footing_size", 0)
                depth = design_outputs.get("effective_depth", 0)
                volume = footing_size * footing_size * depth
                quantities["concrete"] += volume
                quantities["excavation"] += volume * 1.2  # 20% extra for excavation
                
            elif calc_type.value == "column_design":
                # Extract column quantities
                column_size = design_outputs.get("column_size", 0)
                # Assume column height from project
                height = 3.0  # Default, should come from project
                volume = column_size * column_size * height
                quantities["concrete"] += volume
                
                # Steel
                steel_area = design_outputs.get("steel_area_required", 0) / 1e6  # Convert mm² to m²
                steel_density = 7850  # kg/m³
                steel_volume = steel_area * height
                quantities["steel"] += steel_volume * steel_density
                
            elif calc_type.value == "beam_design":
                # Extract beam quantities
                width = design_outputs.get("beam_width", 0)
                depth = design_outputs.get("overall_depth", 0)
                # Assume span from inputs
                span = calc.input_parameters.get("span", 5.0)
                volume = width * depth * span
                quantities["concrete"] += volume
                
                # Steel
                steel_area = design_outputs.get("steel_area_required", 0) / 1e6
                steel_volume = steel_area * span
                quantities["steel"] += steel_volume * 7850
                
            elif calc_type.value == "slab_design":
                # Extract slab quantities
                thickness = design_outputs.get("slab_thickness", 0)
                # Assume area from inputs
                area = calc.input_parameters.get("area", 100.0)
                volume = thickness * area
                quantities["concrete"] += volume
                
                # Steel
                steel_area = design_outputs.get("steel_area_required", 0) / 1e6
                quantities["steel"] += steel_area * area * 7850
        
        # Calculate cement from concrete (assuming 1:2:4 mix for M25)
        # 1 m³ concrete ≈ 300-350 kg cement (varies by grade)
        cement_per_cubic_meter = 350  # kg/m³ (approximate for M25)
        quantities["cement"] = quantities["concrete"] * cement_per_cubic_meter
        
        # Calculate sand and aggregate (assuming 1:2:4 mix)
        quantities["sand"] = quantities["concrete"] * 0.5  # m³
        quantities["aggregate"] = quantities["concrete"] * 1.0  # m³
        
        # Apply wastage factors
        quantities["cement"] *= (1 + wastage_factors["cement"])
        quantities["steel"] *= (1 + wastage_factors["steel"])
        quantities["concrete"] *= (1 + wastage_factors["concrete"])
        quantities["sand"] *= (1 + wastage_factors["sand"])
        quantities["aggregate"] *= (1 + wastage_factors["aggregate"])
        
        return quantities
    
    def generate_boq_items(
        self,
        quantities: Dict[str, float],
        project_id: int,
        material_grades: Dict[str, str] = None
    ) -> List[Dict]:
        """
        Generate BOQ items from quantities
        """
        if material_grades is None:
            material_grades = {
                "concrete": "M25",
                "steel": "Fe415",
                "cement": "OPC 43"
            }
        
        boq_items = []
        
        # Concrete
        if quantities["concrete"] > 0:
            boq_items.append({
                "item_code": "CONC-001",
                "item_description": f"Concrete {material_grades['concrete']}",
                "category": "Concrete",
                "quantity": round(quantities["concrete"], 3),
                "unit": "m³",
                "material_type": "concrete",
                "grade": material_grades["concrete"]
            })
        
        # Steel
        if quantities["steel"] > 0:
            boq_items.append({
                "item_code": "STL-001",
                "item_description": f"Steel Reinforcement {material_grades['steel']}",
                "category": "Steel",
                "quantity": round(quantities["steel"], 2),
                "unit": "kg",
                "material_type": "steel",
                "grade": material_grades["steel"]
            })
        
        # Cement
        if quantities["cement"] > 0:
            boq_items.append({
                "item_code": "CEM-001",
                "item_description": f"Cement {material_grades['cement']}",
                "category": "Cement",
                "quantity": round(quantities["cement"], 2),
                "unit": "kg",
                "material_type": "cement",
                "grade": material_grades["cement"]
            })
        
        # Sand
        if quantities["sand"] > 0:
            boq_items.append({
                "item_code": "SAND-001",
                "item_description": "Fine Aggregate (Sand)",
                "category": "Aggregate",
                "quantity": round(quantities["sand"], 3),
                "unit": "m³",
                "material_type": "sand"
            })
        
        # Aggregate
        if quantities["aggregate"] > 0:
            boq_items.append({
                "item_code": "AGG-001",
                "item_description": "Coarse Aggregate",
                "category": "Aggregate",
                "quantity": round(quantities["aggregate"], 3),
                "unit": "m³",
                "material_type": "aggregate"
            })
        
        # Excavation
        if quantities["excavation"] > 0:
            boq_items.append({
                "item_code": "EXC-001",
                "item_description": "Earthwork Excavation",
                "category": "Earthwork",
                "quantity": round(quantities["excavation"], 3),
                "unit": "m³",
                "material_type": "excavation"
            })
        
        return boq_items
