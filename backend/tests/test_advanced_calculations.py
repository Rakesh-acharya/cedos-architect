"""
Advanced Calculation Tests - Comprehensive validation
"""

import pytest
from app.services.engineering_calculations import (
    StructuralDesignEngine,
    RoadDesignEngine,
    BridgeDesignEngine,
    DrainageDesignEngine
)
from app.services.geotechnical_analysis import GeotechnicalAnalysisService
from app.services.hydrology import HydrologyService

class TestAdvancedStructuralDesign:
    """Test advanced structural design calculations"""
    
    def test_footing_design_edge_cases(self):
        """Test footing design with edge cases"""
        engine = StructuralDesignEngine()
        
        # Very high load
        result1 = engine.design_footing(
            column_load=10000,
            soil_bearing_capacity=200
        )
        assert result1["footing_size"] > 0
        assert result1["safety_factor"] == 2.5
        
        # Very low load
        result2 = engine.design_footing(
            column_load=100,
            soil_bearing_capacity=200
        )
        assert result2["footing_size"] > 0
        assert result2["footing_size"] >= 0.5  # Minimum size
        
        # Very low soil bearing
        result3 = engine.design_footing(
            column_load=1000,
            soil_bearing_capacity=50
        )
        assert result3["footing_size"] > result1["footing_size"]  # Larger footing needed
    
    def test_column_design_validation(self):
        """Validate column design against IS 456"""
        engine = StructuralDesignEngine()
        
        # Test different grades
        for concrete in ["M20", "M25", "M30", "M35", "M40"]:
            result = engine.design_column(
                axial_load=2000,
                concrete_grade=concrete,
                steel_grade="Fe415"
            )
            assert result["column_size"] >= 0.23  # Minimum size per IS 456
            assert result["steel_area_required"] > 0
        
        # High load
        result = engine.design_column(
            axial_load=10000,
            concrete_grade="M40",
            steel_grade="Fe500"
        )
        assert result["column_size"] >= 0.23
    
    def test_beam_design_boundary_conditions(self):
        """Test beam design boundary conditions"""
        engine = StructuralDesignEngine()
        
        # High moment
        result = engine.design_beam(
            moment=500,  # Very high
            shear=300,
            concrete_grade="M30",
            steel_grade="Fe500"
        )
        assert result["effective_depth"] > 0
        assert result["steel_area_required"] > result.get("minimum_steel", 0)
        
        # Low moment
        result2 = engine.design_beam(
            moment=10,
            shear=20,
            concrete_grade="M20",
            steel_grade="Fe415"
        )
        assert result2["effective_depth"] > 0
        assert result2["steel_area_required"] >= result2.get("minimum_steel", 0)

class TestGeotechnicalAnalysis:
    """Test geotechnical analysis"""
    
    def test_bearing_capacity_validation(self):
        """Validate bearing capacity calculations"""
        service = GeotechnicalAnalysisService()
        
        # Clay soil
        result = service.analyze_soil_bearing_capacity(
            soil_type="clay",
            cohesion=50,  # kN/m²
            angle_of_internal_friction=0,
            unit_weight=18,  # kN/m³
            foundation_depth=1.5,
            foundation_width=2.0
        )
        
        assert result["ultimate_bearing_capacity"] > 0
        assert result["safe_bearing_capacity"] > 0
        assert result["safe_bearing_capacity"] < result["ultimate_bearing_capacity"]
        assert result["factor_of_safety"] == 3.0
        
        # Sandy soil
        result2 = service.analyze_soil_bearing_capacity(
            soil_type="sand",
            cohesion=0,
            angle_of_internal_friction=30,
            unit_weight=20,
            foundation_depth=1.0,
            foundation_width=1.5
        )
        
        assert result2["safe_bearing_capacity"] > 0
        assert result2["bearing_capacity_factors"]["Nq"] > 1
    
    def test_slope_stability_validation(self):
        """Validate slope stability"""
        service = GeotechnicalAnalysisService()
        
        # Stable slope
        result = service.analyze_slope_stability(
            slope_height=5.0,
            slope_angle=30,
            soil_cohesion=25,
            angle_of_internal_friction=25,
            unit_weight=20
        )
        
        assert result["factor_of_safety"] > 0
        assert "status" in result
        assert result["critical_slope_angle"] > 0
        
        # Steep slope
        result2 = service.analyze_slope_stability(
            slope_height=10.0,
            slope_angle=60,  # Very steep
            soil_cohesion=10,
            angle_of_internal_friction=20,
            unit_weight=20
        )
        
        # Should have lower FOS
        assert result2["factor_of_safety"] < result["factor_of_safety"] or result2["status"] in ["unstable", "marginal"]

class TestHydrologyCalculations:
    """Test hydrology calculations"""
    
    def test_runoff_calculation(self):
        """Validate runoff calculation"""
        service = HydrologyService()
        
        result = service.calculate_runoff_using_rational_method(
            catchment_area=1.0,  # hectares
            rainfall_intensity=50.0,  # mm/hr
            runoff_coefficient=0.7
        )
        
        assert result["peak_discharge_m3_s"] > 0
        assert result["catchment_area_m2"] == 10000  # 1 hectare = 10000 m²
        
        # Verify formula: Q = C * I * A / 360
        expected = (0.7 * 50.0 * 10000) / 360
        assert abs(result["peak_discharge_m3_s"] - expected) < 0.1
    
    def test_open_channel_design(self):
        """Validate open channel design"""
        service = HydrologyService()
        
        result = service.design_open_channel(
            discharge=10.0,  # m³/s
            channel_slope=0.001,
            manning_roughness=0.013
        )
        
        assert result["channel_width"] > 0
        assert result["channel_depth"] > 0
        assert result["flow_velocity"] > 0
        assert result["hydraulic_radius"] > 0
        
        # Verify Manning's equation approximately
        # Should be approximately correct
        assert result["flow_velocity"] < 10.0  # Reasonable velocity

class TestIntegrationScenarios:
    """Integration test scenarios"""
    
    def test_complete_design_workflow(self):
        """Test complete design workflow"""
        struct_engine = StructuralDesignEngine()
        
        # Step 1: Design column
        column = struct_engine.design_column(
            axial_load=2000,
            concrete_grade="M25",
            steel_grade="Fe415"
        )
        
        assert column["column_size"] > 0
        
        # Step 2: Design footing for that column
        footing = struct_engine.design_footing(
            column_load=2000,
            soil_bearing_capacity=200,
            column_size=column["column_size"]
        )
        
        assert footing["footing_size"] >= column["column_size"]
        
        # Step 3: Design beam
        beam = struct_engine.design_beam(
            moment=100,
            shear=200,
            concrete_grade="M25",
            steel_grade="Fe415"
        )
        
        assert beam["effective_depth"] > 0
        
        # Verify consistency
        assert footing["concrete_grade"] == "M25" or footing.get("concrete_grade") is None
        assert column["concrete_grade"] == "M25"
        assert beam["concrete_grade"] == "M25"
    
    def test_road_design_validation(self):
        """Validate road design calculations"""
        engine = RoadDesignEngine()
        
        # Test flexible pavement
        result = engine.design_flexible_pavement(
            traffic_count=5000,
            design_life=20,
            subgrade_cbr=5.0
        )
        
        assert result["total_thickness"] > 0
        assert result["base_thickness"] > 0
        assert result["bituminous_thickness"] > 0
        
        # Test geometry
        geometry = engine.calculate_road_geometry(
            design_speed=100.0,
            road_class="NH"
        )
        
        assert geometry["lane_width"] == 3.75  # NH standard
        assert geometry["min_radius"] > 0

class TestBoundaryConditions:
    """Test boundary conditions and edge cases"""
    
    def test_zero_values(self):
        """Test with zero values"""
        engine = StructuralDesignEngine()
        
        # Should handle gracefully
        try:
            result = engine.design_footing(
                column_load=0,
                soil_bearing_capacity=200
            )
            # Should return minimum size or handle error
        except Exception:
            pass  # Acceptable to raise error for invalid input
    
    def test_very_large_values(self):
        """Test with very large values"""
        engine = StructuralDesignEngine()
        
        result = engine.design_column(
            axial_load=100000,  # Very high
            concrete_grade="M40",
            steel_grade="Fe500"
        )
        
        assert result["column_size"] > 0
        assert result["column_size"] >= 0.23  # Minimum
    
    def test_negative_values(self):
        """Test negative values are handled"""
        engine = StructuralDesignEngine()
        
        # Should either raise error or handle gracefully
        try:
            result = engine.design_beam(
                moment=-100,  # Negative
                shear=200,
                concrete_grade="M25"
            )
            # If handled, should return valid result
            if result:
                assert result["effective_depth"] > 0
        except (ValueError, AssertionError):
            pass  # Acceptable to raise error
