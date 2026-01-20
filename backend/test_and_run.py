"""
Comprehensive Test and Run Script
Tests all calculations and runs the project
"""

import sys
import os
import subprocess
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def test_database_connection():
    """Test database connection"""
    print("=" * 60)
    print("Testing Database Connection...")
    print("=" * 60)
    
    try:
        from app.core.database import engine
        from app.core.config import settings
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            result.fetchone()
        
        db_host = settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Local'
        print(f"[OK] Database connected: {db_host}")
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False

def test_calculations():
    """Test all engineering calculations"""
    print("\n" + "=" * 60)
    print("Testing Engineering Calculations...")
    print("=" * 60)
    
    from app.services.engineering_calculations import (
        LoadCalculationEngine,
        StructuralDesignEngine,
        RoadDesignEngine,
        BridgeDesignEngine,
        DrainageDesignEngine
    )
    
    tests_passed = 0
    tests_failed = 0
    
    # Test Load Calculations
    print("\n1. Load Calculations:")
    try:
        engine = LoadCalculationEngine()
        dl = engine.calculate_dead_load(25, 10)
        assert dl == 250.0, f"Expected 250.0, got {dl}"
        print("   [OK] Dead load calculation: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   [FAIL] Dead load calculation: FAILED - {e}")
        tests_failed += 1
    
    try:
        ll = engine.calculate_live_load(100, 4)
        assert ll == 400.0, f"Expected 400.0, got {ll}"
        print("   ✅ Live load calculation: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Live load calculation: FAILED - {e}")
        tests_failed += 1
    
    # Test Structural Design
    print("\n2. Structural Design:")
    try:
        struct_engine = StructuralDesignEngine()
        footing = struct_engine.design_footing(1000, 200)
        assert footing["footing_size"] > 0
        assert footing["footing_size"] >= 0.5  # Minimum
        print("   ✅ Footing design: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Footing design: FAILED - {e}")
        tests_failed += 1
    
    try:
        column = struct_engine.design_column(2000, "M25", "Fe415")
        assert column["column_size"] >= 0.23
        assert column["steel_area_required"] > 0
        print("   ✅ Column design: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Column design: FAILED - {e}")
        tests_failed += 1
    
    try:
        beam = struct_engine.design_beam(100, 200, "M25", "Fe415")
        assert beam["effective_depth"] > 0
        assert beam["steel_area_required"] > 0
        print("   ✅ Beam design: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Beam design: FAILED - {e}")
        tests_failed += 1
    
    # Test Road Design
    print("\n3. Road Design:")
    try:
        road_engine = RoadDesignEngine()
        road = road_engine.design_flexible_pavement(5000, 20, 5.0)
        assert road["total_thickness"] > 0
        assert road["code_standard"] == "IRC 37:2018"
        print("   ✅ Flexible pavement design: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Flexible pavement design: FAILED - {e}")
        tests_failed += 1
    
    # Test Bridge Design
    print("\n4. Bridge Design:")
    try:
        bridge_engine = BridgeDesignEngine()
        bridge = bridge_engine.design_rc_bridge_girder(20.0, 70.0, "M35", "Fe500")
        assert bridge["girder_depth"] > 0
        assert bridge["code_standard"] == "IRC 112:2011"
        print("   ✅ Bridge girder design: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Bridge girder design: FAILED - {e}")
        tests_failed += 1
    
    # Test Drainage
    print("\n5. Drainage Design:")
    try:
        drain_engine = DrainageDesignEngine()
        drain = drain_engine.design_storm_drain(1.0, 50.0, 0.7)
        assert drain["discharge"] > 0
        assert drain["pipe_diameter"] >= 0.15  # Minimum
        print("   ✅ Storm drain design: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Storm drain design: FAILED - {e}")
        tests_failed += 1
    
    # Test Geotechnical
    print("\n6. Geotechnical Analysis:")
    try:
        from app.services.geotechnical_analysis import GeotechnicalAnalysisService
        geo_service = GeotechnicalAnalysisService()
        bearing = geo_service.analyze_soil_bearing_capacity(
            "clay", 50, 0, 18, 1.5, 2.0
        )
        assert bearing["safe_bearing_capacity"] > 0
        assert bearing["factor_of_safety"] == 3.0
        print("   ✅ Bearing capacity: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Bearing capacity: FAILED - {e}")
        tests_failed += 1
    
    # Test Hydrology
    print("\n7. Hydrology:")
    try:
        from app.services.hydrology import HydrologyService
        hydro_service = HydrologyService()
        runoff = hydro_service.calculate_runoff_using_rational_method(1.0, 50.0, 0.7)
        assert runoff["peak_discharge_m3_s"] > 0
        print("   ✅ Runoff calculation: PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Runoff calculation: FAILED - {e}")
        tests_failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {tests_passed} PASSED, {tests_failed} FAILED")
    print("=" * 60)
    
    return tests_passed, tests_failed

def validate_calculation_results():
    """Validate calculation results against known engineering standards"""
    print("\n" + "=" * 60)
    print("Validating Calculation Results...")
    print("=" * 60)
    
    from app.services.engineering_calculations import StructuralDesignEngine
    
    print("\n1. Column Design Validation:")
    engine = StructuralDesignEngine()
    
    # Known test case: 2000 kN load, M25, Fe415
    result = engine.design_column(2000, "M25", "Fe415")
    
    print(f"   Column size: {result['column_size']} m")
    print(f"   Steel area: {result['steel_area_required']} mm²")
    
    # Validate against IS 456 minimums
    assert result["column_size"] >= 0.23, "Column size below minimum 230mm per IS 456"
    assert result["steel_area_required"] > 0, "Steel area should be positive"
    
    # Check steel percentage (should be 1-4%)
    column_area_mm2 = result["column_size"] * result["column_size"] * 1e6
    steel_percentage = (result["steel_area_required"] / column_area_mm2) * 100
    print(f"   Steel percentage: {steel_percentage:.2f}%")
    
    assert 1.0 <= steel_percentage <= 4.0, f"Steel percentage {steel_percentage}% outside 1-4% range"
    print("   ✅ Column design meets IS 456 requirements")
    
    print("\n2. Footing Design Validation:")
    footing = engine.design_footing(2000, 200)
    print(f"   Footing size: {footing['footing_size']} m")
    print(f"   Required area: {footing['required_area']} m²")
    
    # Verify area calculation
    expected_area = (2000 * 2.5) / 200  # Load * SF / bearing
    assert abs(footing["required_area"] - expected_area) < 0.1, "Area calculation incorrect"
    print("   ✅ Footing design calculation correct")
    
    print("\n✅ All validations passed!")

def check_api_endpoints():
    """Check if API endpoints are accessible"""
    print("\n" + "=" * 60)
    print("Checking API Endpoints...")
    print("=" * 60)
    
    import requests
    import time
    
    base_url = "http://localhost:8000"
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(2)
    
    endpoints = [
        "/",
        "/health",
        "/api/docs"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint}: OK")
            else:
                print(f"   ⚠️ {endpoint}: Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {endpoint}: Server not running")
            return False
        except Exception as e:
            print(f"   ⚠️ {endpoint}: {e}")
    
    return True

def main():
    """Main test runner"""
    print("\n" + "=" * 60)
    print("CEDOS - Comprehensive Test Suite")
    print("=" * 60)
    
    # Test database
    db_ok = test_database_connection()
    if not db_ok:
        print("\n⚠️ Database connection failed. Please check your .env file.")
        print("Using provided Supabase URL...")
        # Update config
        os.environ["DATABASE_URL"] = "postgresql://postgres:[YOUR-PASSWORD]@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
    
    # Test calculations
    passed, failed = test_calculations()
    
    # Validate results
    try:
        validate_calculation_results()
    except Exception as e:
        print(f"\n⚠️ Validation error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {failed}")
    print(f"Success Rate: {(passed/(passed+failed)*100):.1f}%" if (passed+failed) > 0 else "N/A")
    
    if failed == 0:
        print("\n✅ All tests passed! System is ready.")
    else:
        print(f"\n⚠️ {failed} test(s) failed. Please review errors above.")
    
    print("\nTo run the server:")
    print("  cd backend")
    print("  uvicorn app.main:app --reload")
    print("\nTo run pytest:")
    print("  cd backend")
    print("  pytest tests/ -v")

if __name__ == "__main__":
    main()

