"""
Tests for Road, Bridge, and Drainage Design
"""

import pytest
from app.services.engineering_calculations import (
    RoadDesignEngine,
    BridgeDesignEngine,
    DrainageDesignEngine
)

class TestRoadDesignEngine:
    """Test Road Design Engine"""
    
    def test_flexible_pavement_design(self):
        engine = RoadDesignEngine()
        result = engine.design_flexible_pavement(
            traffic_count=5000,
            design_life=20,
            subgrade_cbr=5.0
        )
        
        assert "cumulative_traffic_msa" in result
        assert "base_thickness" in result
        assert "bituminous_thickness" in result
        assert result["total_thickness"] > 0
        assert result["code_standard"] == "IRC 37:2018"
    
    def test_rigid_pavement_design(self):
        engine = RoadDesignEngine()
        result = engine.design_rigid_pavement(
            traffic_count=10000,
            subgrade_modulus=30.0
        )
        
        assert "slab_thickness" in result
        assert "joint_spacing" in result
        assert result["code_standard"] == "IRC 58:2015"
    
    def test_road_geometry(self):
        engine = RoadDesignEngine()
        result = engine.calculate_road_geometry(
            design_speed=100.0,
            road_class="NH"
        )
        
        assert "lane_width" in result
        assert "shoulder_width" in result
        assert "min_radius" in result
        assert result["code_standard"] == "IRC 73:2010"

class TestBridgeDesignEngine:
    """Test Bridge Design Engine"""
    
    def test_bridge_girder_design(self):
        engine = BridgeDesignEngine()
        result = engine.design_rc_bridge_girder(
            span=20.0,
            live_load=70.0,
            concrete_grade="M35",
            steel_grade="Fe500"
        )
        
        assert "girder_depth" in result
        assert "girder_width" in result
        assert "design_moment" in result
        assert "steel_area_required" in result
        assert result["code_standard"] == "IRC 112:2011"
    
    def test_bridge_pier_design(self):
        engine = BridgeDesignEngine()
        result = engine.design_bridge_pier(
            vertical_load=5000,
            horizontal_load=500,
            pier_height=5.0
        )
        
        assert "pier_width" in result
        assert "safety_factor_overturning" in result
        assert "safety_factor_sliding" in result
        assert result["safety_factor_overturning"] >= 1.5
        assert result["safety_factor_sliding"] >= 1.5

class TestDrainageDesignEngine:
    """Test Drainage Design Engine"""
    
    def test_storm_drain_design(self):
        engine = DrainageDesignEngine()
        result = engine.design_storm_drain(
            catchment_area=1.0,  # hectares
            rainfall_intensity=50.0,  # mm/hr
            runoff_coefficient=0.7
        )
        
        assert "discharge" in result
        assert "pipe_diameter" in result
        assert "pipe_velocity" in result
        assert result["pipe_velocity"] >= 0.6  # Minimum self-cleansing velocity
        assert result["code_standard"] == "IS 1742:1983"
    
    def test_sewer_design(self):
        engine = DrainageDesignEngine()
        result = engine.design_sewer_line(
            population=1000,
            water_consumption=135,  # liters per capita per day
            peak_factor=3.0
        )
        
        assert "peak_flow" in result
        assert "pipe_diameter" in result
        assert "pipe_velocity" in result
        assert result["pipe_velocity"] >= 0.6
    
    def test_retaining_wall_drainage(self):
        engine = DrainageDesignEngine()
        result = engine.design_retaining_wall_drainage(
            wall_height=3.0,
            drainage_type="weep_holes"
        )
        
        assert "drainage_type" in result
        assert "weep_hole_diameter" in result or "drain_width" in result
        assert result["code_standard"] == "IS 14458:1997"
