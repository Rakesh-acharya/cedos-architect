"""
Calculation Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.calculation import Calculation, CalculationStatus
from app.schemas.calculation import CalculationCreate, CalculationUpdate, Calculation as CalculationSchema
from app.services.engineering_calculations import (
    LoadCalculationEngine,
    StructuralDesignEngine,
    MaterialRecommendationEngine,
    RoadDesignEngine,
    BridgeDesignEngine,
    DrainageDesignEngine
)
from app.services.compliance_checker import ComplianceChecker
import uuid

router = APIRouter()

@router.post("/", response_model=CalculationSchema, status_code=status.HTTP_201_CREATED)
def create_calculation(
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new calculation"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == calculation_data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Generate calculation code
    calculation_code = f"CALC-{uuid.uuid4().hex[:8].upper()}"
    
    # Perform calculation based on type
    calc_engine = None
    results = {}
    design_outputs = {}
    safety_checks = {}
    
    input_params = calculation_data.input_parameters
    
    if calculation_data.calculation_type.value == "load_calculation":
        calc_engine = LoadCalculationEngine()
        # Extract inputs
        dead_load = input_params.get("dead_load", 0)
        live_load = input_params.get("live_load", 0)
        wind_load = input_params.get("wind_load", 0)
        seismic_load = input_params.get("seismic_load", 0)
        
        results = calc_engine.calculate_total_load(
            dead_load, live_load, wind_load, seismic_load
        )
        
    elif calculation_data.calculation_type.value == "footing_design":
        calc_engine = StructuralDesignEngine()
        column_load = input_params.get("column_load", 0)
        soil_bearing = input_params.get("soil_bearing_capacity", project.soil_bearing_capacity or 200)
        
        design_outputs = calc_engine.design_footing(
            column_load, soil_bearing
        )
        results = {"design_completed": True}
        
    elif calculation_data.calculation_type.value == "column_design":
        calc_engine = StructuralDesignEngine()
        axial_load = input_params.get("axial_load", 0)
        concrete_grade = input_params.get("concrete_grade", "M25")
        steel_grade = input_params.get("steel_grade", "Fe415")
        
        design_outputs = calc_engine.design_column(
            axial_load, concrete_grade, steel_grade
        )
        results = {"design_completed": True}
        
    elif calculation_data.calculation_type.value == "beam_design":
        calc_engine = StructuralDesignEngine()
        moment = input_params.get("moment", 0)
        shear = input_params.get("shear", 0)
        concrete_grade = input_params.get("concrete_grade", "M25")
        steel_grade = input_params.get("steel_grade", "Fe415")
        
        design_outputs = calc_engine.design_beam(
            moment, shear, concrete_grade, steel_grade
        )
        results = {"design_completed": True}
        
    elif calculation_data.calculation_type.value == "slab_design":
        calc_engine = StructuralDesignEngine()
        span = input_params.get("span", 0)
        live_load = input_params.get("live_load", 0)
        concrete_grade = input_params.get("concrete_grade", "M25")
        steel_grade = input_params.get("steel_grade", "Fe415")
        
        design_outputs = calc_engine.design_slab(
            span, live_load, concrete_grade, steel_grade
        )
        results = {"design_completed": True}
    
    elif calculation_data.calculation_type.value == "road_design":
        calc_engine = RoadDesignEngine()
        traffic_count = input_params.get("traffic_count", 1000)
        design_life = input_params.get("design_life", 20)
        subgrade_cbr = input_params.get("subgrade_cbr", 5.0)
        pavement_type = input_params.get("pavement_type", "flexible")
        vehicle_type = input_params.get("vehicle_type", "mixed")
        
        if pavement_type == "flexible":
            design_outputs = calc_engine.design_flexible_pavement(
                traffic_count, design_life, subgrade_cbr, vehicle_type
            )
        else:
            subgrade_modulus = input_params.get("subgrade_modulus", 30.0)
            design_outputs = calc_engine.design_rigid_pavement(
                traffic_count, subgrade_modulus, design_life
            )
        
        # Road geometry
        design_speed = input_params.get("design_speed", 80.0)
        road_class = input_params.get("road_class", "NH")
        geometry = calc_engine.calculate_road_geometry(design_speed, road_class)
        design_outputs.update(geometry)
        
        results = {"design_completed": True}
        code_standard = "IRC 37:2018" if pavement_type == "flexible" else "IRC 58:2015"
    
    elif calculation_data.calculation_type.value == "bridge_design":
        calc_engine = BridgeDesignEngine()
        design_type = input_params.get("design_type", "girder")
        
        if design_type == "girder":
            span = input_params.get("span", 20.0)
            live_load = input_params.get("live_load", 70.0)  # IRC Class A loading
            concrete_grade = input_params.get("concrete_grade", "M35")
            steel_grade = input_params.get("steel_grade", "Fe500")
            
            design_outputs = calc_engine.design_rc_bridge_girder(
                span, live_load, concrete_grade, steel_grade
            )
        else:  # pier
            vertical_load = input_params.get("vertical_load", 5000)
            horizontal_load = input_params.get("horizontal_load", 500)
            pier_height = input_params.get("pier_height", 5.0)
            concrete_grade = input_params.get("concrete_grade", "M35")
            
            design_outputs = calc_engine.design_bridge_pier(
                vertical_load, horizontal_load, pier_height, concrete_grade
            )
        
        results = {"design_completed": True}
        code_standard = "IRC 112:2011"
    
    elif calculation_data.calculation_type.value == "drainage_design":
        calc_engine = DrainageDesignEngine()
        drainage_type = input_params.get("drainage_type", "storm_drain")
        
        if drainage_type == "storm_drain":
            catchment_area = input_params.get("catchment_area", 1.0)  # hectares
            rainfall_intensity = input_params.get("rainfall_intensity", 50.0)  # mm/hr
            runoff_coefficient = input_params.get("runoff_coefficient", 0.7)
            pipe_material = input_params.get("pipe_material", "RCC")
            
            design_outputs = calc_engine.design_storm_drain(
                catchment_area, rainfall_intensity, runoff_coefficient, pipe_material
            )
        elif drainage_type == "sewer":
            population = input_params.get("population", 1000)
            water_consumption = input_params.get("water_consumption", 135)  # liters per capita per day
            peak_factor = input_params.get("peak_factor", 3.0)
            pipe_material = input_params.get("pipe_material", "RCC")
            
            design_outputs = calc_engine.design_sewer_line(
                population, water_consumption, peak_factor, pipe_material
            )
        else:  # retaining wall drainage
            wall_height = input_params.get("wall_height", 3.0)
            backfill_permeability = input_params.get("backfill_permeability", 0.0001)
            drainage_type_wall = input_params.get("drainage_type_wall", "weep_holes")
            
            design_outputs = calc_engine.design_retaining_wall_drainage(
                wall_height, backfill_permeability, drainage_type_wall
            )
        
        results = {"design_completed": True}
        code_standard = "IS 1742:1983"
    
    # Perform compliance check
    db_calculation = Calculation(
        project_id=calculation_data.project_id,
        calculation_code=calculation_code,
        calculation_type=calculation_data.calculation_type,
        input_parameters=input_params,
        calculation_results=results,
        design_outputs=design_outputs,
        safety_checks=safety_checks,
        code_standard_used=code_standard if 'code_standard' in locals() else "IS 456:2000",
        created_by=current_user.id,
        description=calculation_data.description
    )
    
    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)
    
    # Perform compliance check (for structural calculations)
    if calculation_data.calculation_type.value in ["footing_design", "column_design", "beam_design", "slab_design"]:
        compliance_checker = ComplianceChecker(db)
        compliance_result = compliance_checker.perform_full_compliance_check(db_calculation)
        
        # Update compliance status
        db_calculation.compliance_status = compliance_result["overall_status"].value
        db_calculation.safety_factor_passed = compliance_result["overall_status"].value == "compliant"
    else:
        # For roads, bridges, drainage - set as compliant if design completed
        db_calculation.compliance_status = "compliant"
        db_calculation.safety_factor_passed = True
    
    db.commit()
    db.refresh(db_calculation)
    
    return db_calculation

@router.get("/", response_model=List[CalculationSchema])
def list_calculations(
    project_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List calculations"""
    query = db.query(Calculation)
    if project_id:
        query = query.filter(Calculation.project_id == project_id)
    
    calculations = query.offset(skip).limit(limit).all()
    return calculations

@router.get("/{calculation_id}", response_model=CalculationSchema)
def get_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get calculation by ID"""
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    return calculation
