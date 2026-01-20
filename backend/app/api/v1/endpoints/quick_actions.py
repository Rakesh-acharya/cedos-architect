"""
Quick Actions Endpoints - Time-saving automated workflows
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.services.quick_actions import QuickActionsService

router = APIRouter()

@router.post("/generate-package/{project_id}")
def generate_project_package(
    project_id: int,
    include_calculations: bool = True,
    include_boq: bool = True,
    include_cost: bool = True,
    include_blueprints: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate complete project package - All documents in one go
    Saves hours of manual work!
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = QuickActionsService(db)
    package = service.generate_project_package(
        project_id,
        include_calculations,
        include_boq,
        include_cost,
        include_blueprints
    )
    
    return package

@router.get("/export-zip/{project_id}")
def export_project_zip(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Export all project documents as ZIP file
    One-click export saves hours!
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    service = QuickActionsService(db)
    zip_bytes = service.bulk_export_project_documents(project_id)
    
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename=project_{project.project_code}_package.zip"
        }
    )

@router.post("/create-from-template")
def create_project_from_template(
    template_name: str,
    project_name: str,
    location: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create project from template - Pre-configured project setup
    Saves setup time!
    """
    service = QuickActionsService(db)
    result = service.create_project_from_template(
        template_name,
        project_name,
        location,
        current_user.id
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result

@router.get("/templates")
def list_templates():
    """List available project templates"""
    return {
        "templates": [
            {
                "name": "residential_building",
                "description": "Residential building project template",
                "default_calculations": ["column_design", "beam_design", "slab_design"],
                "default_materials": {"concrete": "M25", "steel": "Fe415"}
            },
            {
                "name": "commercial_building",
                "description": "Commercial building project template",
                "default_calculations": ["column_design", "beam_design", "slab_design", "footing_design"],
                "default_materials": {"concrete": "M30", "steel": "Fe500"}
            },
            {
                "name": "road_project",
                "description": "Road/highway project template",
                "default_calculations": ["road_design"],
                "default_materials": {}
            },
            {
                "name": "bridge_project",
                "description": "Bridge project template",
                "default_calculations": ["bridge_design"],
                "default_materials": {"concrete": "M35", "steel": "Fe500"}
            }
        ]
    }
