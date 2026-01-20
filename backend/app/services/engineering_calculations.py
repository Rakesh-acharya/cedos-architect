"""
Engineering Calculation Engine
Rule-based calculations following IS codes and engineering principles
"""

from typing import Dict, List, Optional
from app.models.calculation import CalculationType
import math

class LoadCalculationEngine:
    """Load Calculation Engine - Calculates various loads per IS codes"""
    
    @staticmethod
    def calculate_dead_load(material_density: float, volume: float) -> float:
        """
        Calculate dead load
        DL = density × volume
        """
        return material_density * volume
    
    @staticmethod
    def calculate_live_load(area: float, live_load_per_sqm: float) -> float:
        """
        Calculate live load per IS 875 Part 2
        LL = area × live_load_per_sqm
        """
        return area * live_load_per_sqm
    
    @staticmethod
    def calculate_wind_load(
        wind_pressure: float,
        area: float,
        shape_factor: float = 1.0
    ) -> float:
        """
        Calculate wind load per IS 875 Part 3
        WL = wind_pressure × area × shape_factor
        """
        return wind_pressure * area * shape_factor
    
    @staticmethod
    def calculate_seismic_load(
        seismic_zone: str,
        building_height: float,
        base_shear: float,
        response_reduction_factor: float = 5.0
    ) -> Dict[str, float]:
        """
        Calculate seismic load per IS 1893
        Returns seismic force distribution
        """
        # Zone factors (simplified)
        zone_factors = {
            "Zone II": 0.10,
            "Zone III": 0.16,
            "Zone IV": 0.24,
            "Zone V": 0.36
        }
        
        zone_factor = zone_factors.get(seismic_zone, 0.10)
        
        # Design horizontal seismic coefficient
        ah = zone_factor / (2 * response_reduction_factor)
        
        # Base shear
        vb = base_shear * ah
        
        return {
            "zone_factor": zone_factor,
            "design_horizontal_coefficient": ah,
            "base_shear": vb,
            "seismic_force": vb
        }
    
    @staticmethod
    def calculate_total_load(
        dead_load: float,
        live_load: float,
        wind_load: float = 0.0,
        seismic_load: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate total load combinations per IS 456
        """
        # Load combinations as per IS 456
        load_combinations = {
            "DL + LL": dead_load + live_load,
            "DL + LL + WL": dead_load + live_load + wind_load,
            "DL + LL + SL": dead_load + live_load + seismic_load,
            "DL + WL": dead_load + wind_load,
            "DL + SL": dead_load + seismic_load,
            "0.9DL + WL": 0.9 * dead_load + wind_load,
            "0.9DL + SL": 0.9 * dead_load + seismic_load
        }
        
        # Critical load (maximum)
        critical_load = max(load_combinations.values())
        
        return {
            "load_combinations": load_combinations,
            "critical_load": critical_load,
            "dead_load": dead_load,
            "live_load": live_load,
            "wind_load": wind_load,
            "seismic_load": seismic_load
        }

class StructuralDesignEngine:
    """Structural Design Engine - Designs structural members"""
    
    @staticmethod
    def design_footing(
        column_load: float,
        soil_bearing_capacity: float,
        column_size: float = 0.0,
        safety_factor: float = 2.5
    ) -> Dict[str, float]:
        """
        Design isolated footing per IS 456
        """
        # Required area
        required_area = (column_load * safety_factor) / soil_bearing_capacity
        
        # Footing size (assuming square footing)
        footing_size = math.sqrt(required_area)
        
        # Minimum size check
        if column_size > 0:
            min_size = column_size + 0.3  # Minimum 150mm projection on each side
            footing_size = max(footing_size, min_size)
        
        # Effective depth (simplified)
        effective_depth = footing_size / 8  # Approximate
        
        return {
            "footing_size": round(footing_size, 3),
            "required_area": round(required_area, 3),
            "effective_depth": round(effective_depth, 3),
            "safety_factor": safety_factor,
            "soil_bearing_capacity": soil_bearing_capacity
        }
    
    @staticmethod
    def design_column(
        axial_load: float,
        concrete_grade: str,
        steel_grade: str = "Fe415",
        column_length: float = 3.0,
        effective_length_factor: float = 0.65
    ) -> Dict[str, float]:
        """
        Design column per IS 456
        """
        # Material properties
        concrete_strength = {
            "M20": 20.0,
            "M25": 25.0,
            "M30": 30.0,
            "M35": 35.0,
            "M40": 40.0
        }
        
        steel_strength = {
            "Fe415": 415.0,
            "Fe500": 500.0,
            "Fe550": 550.0
        }
        
        fck = concrete_strength.get(concrete_grade, 25.0)
        fy = steel_strength.get(steel_grade, 415.0)
        
        # Effective length
        leff = column_length * effective_length_factor
        
        # Assume slenderness ratio < 12 (short column)
        # Pu = 0.4 * fck * Ac + 0.67 * fy * Asc
        
        # Assume 1% steel
        p = 0.01
        
        # Required area
        ac_required = axial_load / (0.4 * fck + 0.67 * fy * p)
        
        # Column size (assuming square)
        column_size = math.sqrt(ac_required)
        
        # Minimum size check
        column_size = max(column_size, 0.23)  # Minimum 230mm
        
        # Steel area
        ast_required = p * column_size * column_size * 1000000  # mm²
        
        return {
            "column_size": round(column_size, 3),
            "steel_area_required": round(ast_required, 2),
            "concrete_grade": concrete_grade,
            "steel_grade": steel_grade,
            "effective_length": round(leff, 2)
        }
    
    @staticmethod
    def design_beam(
        moment: float,
        shear: float,
        concrete_grade: str,
        steel_grade: str = "Fe415",
        beam_width: float = 0.23,
        effective_depth: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Design beam per IS 456
        """
        # Material properties
        concrete_strength = {
            "M20": 20.0,
            "M25": 25.0,
            "M30": 30.0,
            "M35": 35.0,
            "M40": 40.0
        }
        
        steel_strength = {
            "Fe415": 415.0,
            "Fe500": 500.0,
            "Fe550": 550.0
        }
        
        fck = concrete_strength.get(concrete_grade, 25.0)
        fy = steel_strength.get(steel_grade, 415.0)
        
        # Constants
        xu_max_by_d = 0.48 if fy == 415 else 0.46 if fy == 500 else 0.44
        
        # Calculate effective depth if not provided
        if effective_depth is None:
            # Mu = 0.138 * fck * b * d² (for balanced section)
            d_required = math.sqrt(moment * 1e6 / (0.138 * fck * beam_width * 1000))
            effective_depth = d_required / 1000  # Convert to meters
        
        d = effective_depth * 1000  # mm
        
        # Moment capacity check
        mu_lim = 0.138 * fck * beam_width * 1000 * d * d / 1e6
        
        if moment > mu_lim:
            # Doubly reinforced or increase depth
            # Simplified: increase depth
            d_required = math.sqrt(moment * 1e6 / (0.138 * fck * beam_width * 1000))
            effective_depth = d_required / 1000
        
        d = effective_depth * 1000  # mm
        
        # Calculate steel area
        # Mu = 0.87 * fy * Ast * (d - 0.42 * xu)
        # Simplified calculation
        ast_required = (moment * 1e6) / (0.87 * fy * (d - 0.42 * xu_max_by_d * d))
        
        # Minimum steel
        ast_min = 0.85 * beam_width * 1000 * d / fy
        
        ast_required = max(ast_required, ast_min)
        
        # Shear reinforcement (simplified)
        tau_c = 0.25 * math.sqrt(fck)  # N/mm² (simplified)
        vu = shear * 1000  # N
        vc = tau_c * beam_width * 1000 * d
        
        shear_reinforcement_required = vu > vc
        
        return {
            "beam_width": round(beam_width, 3),
            "effective_depth": round(effective_depth, 3),
            "overall_depth": round(effective_depth + 0.05, 3),  # Add cover
            "steel_area_required": round(ast_required, 2),
            "minimum_steel": round(ast_min, 2),
            "shear_reinforcement_required": shear_reinforcement_required,
            "concrete_grade": concrete_grade,
            "steel_grade": steel_grade
        }
    
    @staticmethod
    def design_slab(
        span: float,
        live_load: float,
        concrete_grade: str,
        steel_grade: str = "Fe415",
        slab_type: str = "one_way"  # "one_way" or "two_way"
    ) -> Dict[str, float]:
        """
        Design slab per IS 456
        """
        # Material properties
        concrete_strength = {
            "M20": 20.0,
            "M25": 25.0,
            "M30": 30.0
        }
        
        steel_strength = {
            "Fe415": 415.0,
            "Fe500": 500.0
        }
        
        fck = concrete_strength.get(concrete_grade, 25.0)
        fy = steel_strength.get(steel_grade, 415.0)
        
        # Dead load (self-weight)
        # Assume slab thickness = span/25 (simplified)
        slab_thickness = span / 25
        slab_thickness = max(slab_thickness, 0.1)  # Minimum 100mm
        
        dead_load = 25 * slab_thickness  # kN/m² (concrete density = 25 kN/m³)
        
        # Total load
        total_load = dead_load + live_load
        
        # Moment calculation
        if slab_type == "one_way":
            moment = total_load * span * span / 8  # Simply supported
        else:
            # Two-way slab (simplified)
            moment = total_load * span * span / 10
        
        # Effective depth
        d = slab_thickness * 1000 - 20  # Assume 20mm cover (mm)
        
        # Steel area
        ast_required = (moment * 1e6) / (0.87 * fy * 0.9 * d)
        
        # Minimum steel
        ast_min = 0.12 * 1000 * slab_thickness * 1000 / 100  # 0.12% of gross area
        
        ast_required = max(ast_required, ast_min)
        
        return {
            "slab_thickness": round(slab_thickness, 3),
            "effective_depth": round(d / 1000, 3),
            "steel_area_required": round(ast_required, 2),
            "minimum_steel": round(ast_min, 2),
            "concrete_grade": concrete_grade,
            "steel_grade": steel_grade,
            "dead_load": round(dead_load, 2),
            "total_load": round(total_load, 2)
        }

class MaterialRecommendationEngine:
    """Material Grade Recommendation Engine"""
    
    @staticmethod
    def recommend_concrete_grade(
        load_intensity: float,
        exposure_condition: str = "moderate",
        durability_requirement: str = "standard"
    ) -> str:
        """
        Recommend concrete grade based on load and exposure
        """
        # Exposure conditions
        exposure_grades = {
            "mild": "M20",
            "moderate": "M25",
            "severe": "M30",
            "very_severe": "M35",
            "extreme": "M40"
        }
        
        # Load-based recommendation
        if load_intensity < 1000:  # kN
            load_grade = "M20"
        elif load_intensity < 2000:
            load_grade = "M25"
        elif load_intensity < 3000:
            load_grade = "M30"
        elif load_intensity < 4000:
            load_grade = "M35"
        else:
            load_grade = "M40"
        
        # Exposure-based recommendation
        exposure_grade = exposure_grades.get(exposure_condition, "M25")
        
        # Take higher grade
        grade_values = {"M20": 20, "M25": 25, "M30": 30, "M35": 35, "M40": 40}
        
        recommended = max(
            [load_grade, exposure_grade],
            key=lambda x: grade_values.get(x, 25)
        )
        
        return recommended
    
    @staticmethod
    def recommend_steel_grade(
        load_intensity: float,
        cost_optimization: bool = True
    ) -> str:
        """
        Recommend steel grade
        """
        if cost_optimization and load_intensity < 2000:
            return "Fe415"  # Standard grade, cost-effective
        elif load_intensity < 3000:
            return "Fe415"
        else:
            return "Fe500"  # Higher strength for heavy loads
    
    @staticmethod
    def recommend_cement_grade(
        concrete_grade: str,
        exposure_condition: str = "moderate"
    ) -> str:
        """
        Recommend cement grade
        """
        # For M20-M25: OPC 43
        # For M30+: OPC 53 or PPC
        
        grade_values = {
            "M20": 20,
            "M25": 25,
            "M30": 30,
            "M35": 35,
            "M40": 40
        }
        
        concrete_value = grade_values.get(concrete_grade, 25)
        
        if concrete_value <= 25:
            return "OPC 43"
        else:
            return "OPC 53"

class RoadDesignEngine:
    """Road Design Engine - Per IRC standards"""
    
    @staticmethod
    def design_flexible_pavement(
        traffic_count: int,
        design_life: int = 20,
        subgrade_cbr: float = 5.0,
        vehicle_type: str = "mixed"
    ) -> Dict[str, any]:
        """
        Design flexible pavement per IRC 37
        """
        # Traffic classification
        # Convert to million standard axles (MSA)
        if vehicle_type == "heavy":
            msa_factor = 0.0001
        elif vehicle_type == "mixed":
            msa_factor = 0.00005
        else:
            msa_factor = 0.00002
        
        cumulative_traffic = traffic_count * 365 * design_life * msa_factor
        
        # Pavement thickness based on CBR and traffic
        # Simplified IRC 37 method
        if subgrade_cbr < 2:
            base_thickness = 0.25  # 250mm
            subbase_thickness = 0.15  # 150mm
        elif subgrade_cbr < 5:
            base_thickness = 0.20  # 200mm
            subbase_thickness = 0.10  # 100mm
        else:
            base_thickness = 0.15  # 150mm
            subbase_thickness = 0.075  # 75mm
        
        # Bituminous layer thickness
        if cumulative_traffic < 1:
            bituminous_thickness = 0.05  # 50mm
        elif cumulative_traffic < 10:
            bituminous_thickness = 0.075  # 75mm
        else:
            bituminous_thickness = 0.10  # 100mm
        
        total_thickness = base_thickness + subbase_thickness + bituminous_thickness
        
        return {
            "cumulative_traffic_msa": round(cumulative_traffic, 2),
            "subgrade_cbr": subgrade_cbr,
            "base_thickness": round(base_thickness, 3),
            "subbase_thickness": round(subbase_thickness, 3),
            "bituminous_thickness": round(bituminous_thickness, 3),
            "total_thickness": round(total_thickness, 3),
            "design_life": design_life,
            "code_standard": "IRC 37:2018"
        }
    
    @staticmethod
    def design_rigid_pavement(
        traffic_count: int,
        subgrade_modulus: float = 30.0,
        design_life: int = 20
    ) -> Dict[str, any]:
        """
        Design rigid pavement per IRC 58
        """
        # Traffic classification
        cumulative_traffic = traffic_count * 365 * design_life * 0.0001  # Simplified
        
        # Slab thickness based on traffic and subgrade
        if cumulative_traffic < 1:
            slab_thickness = 0.20  # 200mm
        elif cumulative_traffic < 10:
            slab_thickness = 0.25  # 250mm
        elif cumulative_traffic < 50:
            slab_thickness = 0.30  # 300mm
        else:
            slab_thickness = 0.35  # 350mm
        
        # Joint spacing
        joint_spacing = min(4.5, slab_thickness * 15)  # meters
        
        return {
            "cumulative_traffic_msa": round(cumulative_traffic, 2),
            "subgrade_modulus": subgrade_modulus,
            "slab_thickness": round(slab_thickness, 3),
            "joint_spacing": round(joint_spacing, 2),
            "design_life": design_life,
            "code_standard": "IRC 58:2015"
        }
    
    @staticmethod
    def calculate_road_geometry(
        design_speed: float,
        road_class: str = "NH"  # NH, SH, MDR, ODR
    ) -> Dict[str, float]:
        """
        Calculate road geometry per IRC 73
        """
        # Lane width
        if road_class == "NH":
            lane_width = 3.75  # meters
        elif road_class == "SH":
            lane_width = 3.5
        else:
            lane_width = 3.0
        
        # Shoulder width
        if design_speed >= 100:
            shoulder_width = 2.5
        elif design_speed >= 80:
            shoulder_width = 2.0
        else:
            shoulder_width = 1.5
        
        # Superelevation
        if design_speed >= 100:
            max_superelevation = 0.07  # 7%
        else:
            max_superelevation = 0.06  # 6%
        
        # Minimum radius
        min_radius = (design_speed ** 2) / (127 * (0.15 + max_superelevation))
        
        return {
            "design_speed": design_speed,
            "lane_width": lane_width,
            "shoulder_width": shoulder_width,
            "max_superelevation": max_superelevation,
            "min_radius": round(min_radius, 2),
            "code_standard": "IRC 73:2010"
        }

class BridgeDesignEngine:
    """Bridge Design Engine - Per IRC standards"""
    
    @staticmethod
    def design_rc_bridge_girder(
        span: float,
        live_load: float,
        concrete_grade: str = "M35",
        steel_grade: str = "Fe500"
    ) -> Dict[str, any]:
        """
        Design RC bridge girder per IRC 112
        """
        # Girder depth (simplified)
        # For simply supported: L/12 to L/15
        girder_depth = span / 12
        girder_depth = max(girder_depth, 0.6)  # Minimum 600mm
        
        # Girder width
        girder_width = girder_depth / 2
        girder_width = max(girder_width, 0.3)  # Minimum 300mm
        
        # Load factors per IRC 112
        dead_load_factor = 1.35
        live_load_factor = 1.5
        
        # Design moment
        dead_load = 25 * girder_width * girder_depth  # kN/m
        total_load = (dead_load * dead_load_factor) + (live_load * live_load_factor)
        design_moment = total_load * span * span / 8
        
        # Steel area (simplified)
        fck = 35.0 if concrete_grade == "M35" else 40.0
        fy = 500.0 if steel_grade == "Fe500" else 415.0
        
        d = girder_depth * 1000 - 50  # Effective depth (mm)
        ast_required = (design_moment * 1e6) / (0.87 * fy * 0.9 * d)
        
        return {
            "span": span,
            "girder_depth": round(girder_depth, 3),
            "girder_width": round(girder_width, 3),
            "design_moment": round(design_moment, 2),
            "steel_area_required": round(ast_required, 2),
            "concrete_grade": concrete_grade,
            "steel_grade": steel_grade,
            "code_standard": "IRC 112:2011"
        }
    
    @staticmethod
    def design_bridge_pier(
        vertical_load: float,
        horizontal_load: float,
        pier_height: float,
        concrete_grade: str = "M35"
    ) -> Dict[str, any]:
        """
        Design bridge pier per IRC 78
        """
        # Pier dimensions (simplified)
        # Based on load and stability
        required_area = (vertical_load * 1.5) / (0.4 * 35 * 1000)  # Simplified
        
        pier_width = math.sqrt(required_area)
        pier_width = max(pier_width, 0.8)  # Minimum 800mm
        
        # Check overturning
        overturning_moment = horizontal_load * pier_height
        resisting_moment = vertical_load * (pier_width / 2)
        safety_factor_overturning = resisting_moment / overturning_moment if overturning_moment > 0 else 999
        
        # Check sliding
        friction_coefficient = 0.6
        sliding_resistance = vertical_load * friction_coefficient
        safety_factor_sliding = sliding_resistance / horizontal_load if horizontal_load > 0 else 999
        
        return {
            "pier_width": round(pier_width, 3),
            "pier_height": pier_height,
            "safety_factor_overturning": round(safety_factor_overturning, 2),
            "safety_factor_sliding": round(safety_factor_sliding, 2),
            "concrete_grade": concrete_grade,
            "code_standard": "IRC 78:2014"
        }

class DrainageDesignEngine:
    """Drainage Design Engine"""
    
    @staticmethod
    def design_storm_drain(
        catchment_area: float,
        rainfall_intensity: float,
        runoff_coefficient: float = 0.7,
        pipe_material: str = "RCC"
    ) -> Dict[str, any]:
        """
        Design storm drain per IS 1742
        """
        # Calculate discharge (Rational method)
        # Q = C * I * A / 360
        discharge = (runoff_coefficient * rainfall_intensity * catchment_area) / 360
        
        # Pipe diameter (Manning's equation simplified)
        # Q = (1/n) * A * R^(2/3) * S^(1/2)
        # Simplified: D = (Q * n / (0.311 * S^0.5))^(3/8)
        
        manning_n = 0.013 if pipe_material == "RCC" else 0.015
        slope = 0.01  # 1% minimum slope
        
        pipe_diameter = ((discharge * manning_n) / (0.311 * (slope ** 0.5))) ** (3/8)
        pipe_diameter = max(pipe_diameter, 0.15)  # Minimum 150mm
        
        # Pipe velocity check
        area = math.pi * (pipe_diameter / 2) ** 2
        velocity = discharge / area
        
        # Minimum velocity: 0.6 m/s, Maximum: 3 m/s
        if velocity < 0.6:
            pipe_diameter = pipe_diameter * 0.9  # Reduce to increase velocity
            area = math.pi * (pipe_diameter / 2) ** 2
            velocity = discharge / area
        
        return {
            "catchment_area": catchment_area,
            "rainfall_intensity": rainfall_intensity,
            "discharge": round(discharge, 3),
            "pipe_diameter": round(pipe_diameter, 3),
            "pipe_velocity": round(velocity, 2),
            "slope": slope,
            "pipe_material": pipe_material,
            "code_standard": "IS 1742:1983"
        }
    
    @staticmethod
    def design_sewer_line(
        population: int,
        water_consumption: float,
        peak_factor: float = 3.0,
        pipe_material: str = "RCC"
    ) -> Dict[str, any]:
        """
        Design sewer line per IS 1742
        """
        # Average flow
        average_flow = (population * water_consumption * 0.8) / (24 * 3600)  # 80% becomes sewage
        
        # Peak flow
        peak_flow = average_flow * peak_factor
        
        # Pipe diameter (simplified)
        manning_n = 0.013 if pipe_material == "RCC" else 0.015
        slope = 0.005  # 0.5% minimum slope
        
        pipe_diameter = ((peak_flow * manning_n) / (0.311 * (slope ** 0.5))) ** (3/8)
        pipe_diameter = max(pipe_diameter, 0.15)  # Minimum 150mm
        
        # Velocity check
        area = math.pi * (pipe_diameter / 2) ** 2
        velocity = peak_flow / area
        
        # Minimum self-cleansing velocity: 0.6 m/s
        if velocity < 0.6:
            pipe_diameter = pipe_diameter * 0.85
            area = math.pi * (pipe_diameter / 2) ** 2
            velocity = peak_flow / area
        
        return {
            "population": population,
            "average_flow": round(average_flow, 3),
            "peak_flow": round(peak_flow, 3),
            "pipe_diameter": round(pipe_diameter, 3),
            "pipe_velocity": round(velocity, 2),
            "slope": slope,
            "pipe_material": pipe_material,
            "code_standard": "IS 1742:1983"
        }
    
    @staticmethod
    def design_retaining_wall_drainage(
        wall_height: float,
        backfill_permeability: float = 0.0001,
        drainage_type: str = "weep_holes"
    ) -> Dict[str, any]:
        """
        Design drainage for retaining wall
        """
        # Weep holes spacing
        if drainage_type == "weep_holes":
            weep_hole_diameter = 0.075  # 75mm
            weep_hole_spacing = min(2.0, wall_height * 0.5)  # meters
            
            # Number of weep holes
            num_weep_holes = max(2, int(wall_height / weep_hole_spacing))
            
            return {
                "drainage_type": "weep_holes",
                "weep_hole_diameter": weep_hole_diameter,
                "weep_hole_spacing": round(weep_hole_spacing, 2),
                "num_weep_holes": num_weep_holes,
                "code_standard": "IS 14458:1997"
            }
        
        # French drain
        else:
            drain_width = 0.3  # 300mm
            drain_depth = 0.3  # 300mm
            drain_spacing = min(3.0, wall_height * 0.6)
            
            return {
                "drainage_type": "french_drain",
                "drain_width": drain_width,
                "drain_depth": drain_depth,
                "drain_spacing": round(drain_spacing, 2),
                "code_standard": "IS 14458:1997"
            }
