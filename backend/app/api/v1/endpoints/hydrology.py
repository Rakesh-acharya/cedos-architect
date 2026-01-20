"""
Hydrology & Hydraulic Analysis Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.hydrology import HydrologyService
from pydantic import BaseModel

router = APIRouter()

class RationalMethodRequest(BaseModel):
    catchment_area: float
    rainfall_intensity: float
    runoff_coefficient: float = 0.7
    time_of_concentration: float = 15.0

@router.post("/runoff")
def calculate_runoff(
    request: RationalMethodRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate runoff using Rational Method"""
    service = HydrologyService()
    return service.calculate_runoff_using_rational_method(
        catchment_area=request.catchment_area,
        rainfall_intensity=request.rainfall_intensity,
        runoff_coefficient=request.runoff_coefficient,
        time_of_concentration=request.time_of_concentration
    )

@router.post("/open-channel")
def design_open_channel(
    discharge: float,
    channel_slope: float,
    manning_roughness: float = 0.013,
    channel_type: str = "rectangular",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Design open channel"""
    service = HydrologyService()
    return service.design_open_channel(
        discharge=discharge,
        channel_slope=channel_slope,
        manning_roughness=manning_roughness,
        channel_type=channel_type
    )

@router.post("/flood-routing")
def calculate_flood_routing(
    inflow_hydrograph: List[float],
    storage_capacity: float,
    outlet_capacity: float,
    time_interval: float = 1.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate flood routing"""
    service = HydrologyService()
    return service.calculate_flood_routing(
        inflow_hydrograph=inflow_hydrograph,
        storage_capacity=storage_capacity,
        outlet_capacity=outlet_capacity,
        time_interval=time_interval
    )

@router.post("/detention-pond")
def design_detention_pond(
    catchment_area: float,
    design_rainfall: float,
    required_detention_time: float = 24.0,
    infiltration_rate: float = 0.0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Design stormwater detention pond"""
    service = HydrologyService()
    return service.design_stormwater_detention_pond(
        catchment_area=catchment_area,
        design_rainfall=design_rainfall,
        required_detention_time=required_detention_time,
        infiltration_rate=infiltration_rate
    )
