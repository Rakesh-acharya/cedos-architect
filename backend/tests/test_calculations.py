"""
Unit Tests for Engineering Calculations
"""

import pytest
from app.services.engineering_calculations import (
    LoadCalculationEngine,
    StructuralDesignEngine,
    MaterialRecommendationEngine
)

class TestLoadCalculationEngine:
    """Test Load Calculation Engine"""
    
    def test_dead_load_calculation(self):
        engine = LoadCalculationEngine()
        density = 25  # kN/m³ (concrete)
        volume = 10  # m³
        result = engine.calculate_dead_load(density, volume)
        assert result == 250.0
    
    def test_live_load_calculation(self):
        engine = LoadCalculationEngine()
        area = 100  # m²
        live_load_per_sqm = 4  # kN/m²
        result = engine.calculate_live_load(area, live_load_per_sqm)
        assert result == 400.0
    
    def test_wind_load_calculation(self):
        engine = LoadCalculationEngine()
        wind_pressure = 1.5  # kN/m²
        area = 50  # m²
        result = engine.calculate_wind_load(wind_pressure, area)
        assert result == 75.0
    
    def test_seismic_load_calculation(self):
        engine = LoadCalculationEngine()
        result = engine.calculate_seismic_load(
            seismic_zone="Zone III",
            building_height=10,
            base_shear=1000
        )
        assert "base_shear" in result
        assert result["zone_factor"] == 0.16

class TestStructuralDesignEngine:
    """Test Structural Design Engine"""
    
    def test_footing_design(self):
        engine = StructuralDesignEngine()
        result = engine.design_footing(
            column_load=1000,  # kN
            soil_bearing_capacity=200  # kN/m²
        )
        assert "footing_size" in result
        assert result["footing_size"] > 0
    
    def test_column_design(self):
        engine = StructuralDesignEngine()
        result = engine.design_column(
            axial_load=2000,  # kN
            concrete_grade="M25",
            steel_grade="Fe415"
        )
        assert "column_size" in result
        assert "steel_area_required" in result
        assert result["column_size"] >= 0.23  # Minimum size
    
    def test_beam_design(self):
        engine = StructuralDesignEngine()
        result = engine.design_beam(
            moment=100,  # kNm
            shear=200,  # kN
            concrete_grade="M25",
            steel_grade="Fe415"
        )
        assert "effective_depth" in result
        assert "steel_area_required" in result

class TestMaterialRecommendationEngine:
    """Test Material Recommendation Engine"""
    
    def test_concrete_grade_recommendation(self):
        engine = MaterialRecommendationEngine()
        result = engine.recommend_concrete_grade(
            load_intensity=1500,
            exposure_condition="moderate"
        )
        assert result in ["M20", "M25", "M30", "M35", "M40"]
    
    def test_steel_grade_recommendation(self):
        engine = MaterialRecommendationEngine()
        result = engine.recommend_steel_grade(load_intensity=1500)
        assert result in ["Fe415", "Fe500"]
