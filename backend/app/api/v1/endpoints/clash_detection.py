"""
Clash Detection Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.services.clash_detection import ClashDetectionService
from pydantic import BaseModel

router = APIRouter()

class Element(BaseModel):
    name: str
    position: dict
    dimensions: dict

class ClashDetectionRequest(BaseModel):
    structural_elements: List[Element] = []
    mep_elements: List[Element] = []
    drainage_elements: List[Element] = []

@router.post("/detect")
def detect_clashes(
    request: ClashDetectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Detect spatial clashes"""
    service = ClashDetectionService()
    
    struct_elements = [e.dict() for e in request.structural_elements]
    mep_elements = [e.dict() for e in request.mep_elements]
    drain_elements = [e.dict() for e in request.drainage_elements]
    
    result = service.detect_structural_clashes(
        structural_elements=struct_elements,
        mep_elements=mep_elements,
        drainage_elements=drain_elements
    )
    
    # Add resolution suggestions
    for clash in result.get("clashes", []):
        resolution = service.suggest_clash_resolution(clash)
        clash["resolution"] = resolution
    
    return result
