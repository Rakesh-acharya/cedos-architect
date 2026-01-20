"""
Geotechnical Analysis Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.geotechnical_analysis import GeotechnicalAnalysisService
from pydantic import BaseModel

router = APIRouter()

class SoilBearingRequest(BaseModel):
    soil_type: str
    cohesion: float
    angle_of_internal_friction: float
    unit_weight: float
    foundation_depth: float
    foundation_width: float
    foundation_length: float = 0.0

class SlopeStabilityRequest(BaseModel):
    slope_height: float
    slope_angle: float
    soil_cohesion: float
    angle_of_internal_friction: float
    unit_weight: float
    water_table_depth: float = None

@router.post("/bearing-capacity")
def calculate_bearing_capacity(
    request: SoilBearingRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate soil bearing capacity"""
    service = GeotechnicalAnalysisService()
    result = service.analyze_soil_bearing_capacity(
        soil_type=request.soil_type,
        cohesion=request.cohesion,
        angle_of_internal_friction=request.angle_of_internal_friction,
        unit_weight=request.unit_weight,
        foundation_depth=request.foundation_depth,
        foundation_width=request.foundation_width,
        foundation_length=request.foundation_length
    )
    return result

@router.post("/slope-stability")
def analyze_slope_stability(
    request: SlopeStabilityRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze slope stability"""
    service = GeotechnicalAnalysisService()
    result = service.analyze_slope_stability(
        slope_height=request.slope_height,
        slope_angle=request.slope_angle,
        soil_cohesion=request.soil_cohesion,
        angle_of_internal_friction=request.angle_of_internal_friction,
        unit_weight=request.unit_weight,
        water_table_depth=request.water_table_depth
    )
    return result

@router.post("/settlement")
def calculate_settlement(
    foundation_width: float,
    foundation_length: float,
    applied_pressure: float,
    soil_elastic_modulus: float,
    poisson_ratio: float = 0.3,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate foundation settlement"""
    service = GeotechnicalAnalysisService()
    result = service.calculate_settlement(
        foundation_width=foundation_width,
        foundation_length=foundation_length,
        applied_pressure=applied_pressure,
        soil_elastic_modulus=soil_elastic_modulus,
        poisson_ratio=poisson_ratio
    )
    return result

@router.post("/pile-foundation")
def design_pile_foundation(
    axial_load: float,
    soil_type: str,
    pile_type: str = "bored",
    pile_diameter: float = 0.6,
    pile_length: float = 10.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Design pile foundation"""
    service = GeotechnicalAnalysisService()
    result = service.design_pile_foundation(
        axial_load=axial_load,
        soil_type=soil_type,
        pile_type=pile_type,
        pile_diameter=pile_diameter,
        pile_length=pile_length
    )
    return result
