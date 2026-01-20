"""
Compliance Checker - Validates designs against code standards
"""

from typing import Dict, List, Optional
from app.models.compliance import ComplianceStatus, CodeStandard
from app.models.calculation import Calculation

class ComplianceChecker:
    """Compliance Checker Service"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def check_safety_factors(
        self,
        calculation: Calculation,
        code_standard: str = "IS 456:2000"
    ) -> Dict[str, any]:
        """
        Check safety factors per code
        """
        results = {
            "status": ComplianceStatus.COMPLIANT,
            "checks": [],
            "violations": []
        }
        
        design_outputs = calculation.design_outputs or {}
        safety_checks = calculation.safety_checks or {}
        
        # Check minimum safety factors per IS 456
        required_safety_factors = {
            "concrete": 1.5,
            "steel": 1.15,
            "overturning": 1.5,
            "sliding": 1.5
        }
        
        for check_name, required_value in required_safety_factors.items():
            actual_value = safety_checks.get(check_name)
            
            if actual_value is not None:
                is_passed = actual_value >= required_value
                
                check_result = {
                    "check_name": check_name,
                    "required_value": required_value,
                    "actual_value": actual_value,
                    "is_passed": is_passed,
                    "margin": round(actual_value - required_value, 3)
                }
                
                results["checks"].append(check_result)
                
                if not is_passed:
                    results["status"] = ComplianceStatus.NON_COMPLIANT
                    results["violations"].append({
                        "check": check_name,
                        "required": required_value,
                        "actual": actual_value,
                        "message": f"{check_name} safety factor {actual_value} is less than required {required_value}"
                    })
        
        return results
    
    def check_minimum_dimensions(
        self,
        calculation: Calculation,
        code_standard: str = "IS 456:2000"
    ) -> Dict[str, any]:
        """
        Check minimum dimensions per code
        """
        results = {
            "status": ComplianceStatus.COMPLIANT,
            "checks": [],
            "violations": []
        }
        
        design_outputs = calculation.design_outputs or {}
        calc_type = calculation.calculation_type.value
        
        # Minimum dimensions per IS 456
        min_dimensions = {
            "footing_design": {
                "footing_size": 0.5,  # 500mm minimum
                "effective_depth": 0.15  # 150mm minimum
            },
            "column_design": {
                "column_size": 0.23  # 230mm minimum
            },
            "beam_design": {
                "beam_width": 0.15,  # 150mm minimum
                "effective_depth": 0.15  # 150mm minimum
            },
            "slab_design": {
                "slab_thickness": 0.1  # 100mm minimum
            }
        }
        
        requirements = min_dimensions.get(calc_type, {})
        
        for dimension_name, min_value in requirements.items():
            actual_value = design_outputs.get(dimension_name)
            
            if actual_value is not None:
                is_passed = actual_value >= min_value
                
                check_result = {
                    "dimension": dimension_name,
                    "minimum_required": min_value,
                    "actual_value": actual_value,
                    "is_passed": is_passed
                }
                
                results["checks"].append(check_result)
                
                if not is_passed:
                    results["status"] = ComplianceStatus.NON_COMPLIANT
                    results["violations"].append({
                        "dimension": dimension_name,
                        "required": min_value,
                        "actual": actual_value,
                        "message": f"{dimension_name} {actual_value}m is less than minimum {min_value}m"
                    })
        
        return results
    
    def check_reinforcement_limits(
        self,
        calculation: Calculation,
        code_standard: str = "IS 456:2000"
    ) -> Dict[str, any]:
        """
        Check reinforcement limits per code
        """
        results = {
            "status": ComplianceStatus.COMPLIANT,
            "checks": [],
            "violations": []
        }
        
        design_outputs = calculation.design_outputs or {}
        calc_type = calculation.calculation_type.value
        
        # Get steel area and section dimensions
        steel_area = design_outputs.get("steel_area_required", 0)
        min_steel = design_outputs.get("minimum_steel", 0)
        
        # Maximum steel percentage (4% for columns, 4% for beams)
        max_steel_percentage = 4.0
        
        if calc_type in ["column_design", "beam_design", "slab_design"]:
            # Calculate section area
            if calc_type == "column_design":
                column_size = design_outputs.get("column_size", 0)
                section_area = column_size * column_size * 1e6  # mm²
            elif calc_type == "beam_design":
                width = design_outputs.get("beam_width", 0) * 1000  # mm
                depth = design_outputs.get("effective_depth", 0) * 1000  # mm
                section_area = width * depth  # mm²
            else:  # slab
                thickness = design_outputs.get("slab_thickness", 0) * 1000  # mm
                section_area = 1000 * thickness  # per meter width, mm²
            
            # Check minimum steel
            if steel_area < min_steel:
                results["status"] = ComplianceStatus.NON_COMPLIANT
                results["violations"].append({
                    "check": "minimum_reinforcement",
                    "required": min_steel,
                    "actual": steel_area,
                    "message": f"Steel area {steel_area} mm² is less than minimum {min_steel} mm²"
                })
            
            # Check maximum steel
            steel_percentage = (steel_area / section_area) * 100
            if steel_percentage > max_steel_percentage:
                results["status"] = ComplianceStatus.WARNING
                results["violations"].append({
                    "check": "maximum_reinforcement",
                    "maximum_percentage": max_steel_percentage,
                    "actual_percentage": round(steel_percentage, 2),
                    "message": f"Steel percentage {steel_percentage:.2f}% exceeds maximum {max_steel_percentage}%"
                })
            
            results["checks"].append({
                "check": "reinforcement_limits",
                "steel_area": steel_area,
                "minimum_steel": min_steel,
                "steel_percentage": round(steel_percentage, 2),
                "max_percentage": max_steel_percentage,
                "is_passed": min_steel <= steel_area <= (section_area * max_steel_percentage / 100)
            })
        
        return results
    
    def perform_full_compliance_check(
        self,
        calculation: Calculation,
        code_standard: str = "IS 456:2000"
    ) -> Dict[str, any]:
        """
        Perform full compliance check
        """
        results = {
            "calculation_id": calculation.id,
            "calculation_code": calculation.calculation_code,
            "code_standard": code_standard,
            "overall_status": ComplianceStatus.COMPLIANT,
            "checks_performed": [],
            "violations": []
        }
        
        # Safety factors check
        safety_check = self.check_safety_factors(calculation, code_standard)
        results["checks_performed"].append({
            "check_type": "safety_factors",
            "status": safety_check["status"].value,
            "details": safety_check["checks"]
        })
        results["violations"].extend(safety_check["violations"])
        
        # Minimum dimensions check
        dimension_check = self.check_minimum_dimensions(calculation, code_standard)
        results["checks_performed"].append({
            "check_type": "minimum_dimensions",
            "status": dimension_check["status"].value,
            "details": dimension_check["checks"]
        })
        results["violations"].extend(dimension_check["violations"])
        
        # Reinforcement limits check
        reinforcement_check = self.check_reinforcement_limits(calculation, code_standard)
        results["checks_performed"].append({
            "check_type": "reinforcement_limits",
            "status": reinforcement_check["status"].value,
            "details": reinforcement_check["checks"]
        })
        results["violations"].extend(reinforcement_check["violations"])
        
        # Determine overall status
        if any(v.get("check") for v in results["violations"] if "NON_COMPLIANT" in str(safety_check["status"])):
            results["overall_status"] = ComplianceStatus.NON_COMPLIANT
        elif any(v.get("check") for v in results["violations"]):
            results["overall_status"] = ComplianceStatus.WARNING
        
        return results
