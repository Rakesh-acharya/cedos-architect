"""
API v1 Routes
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, projects, calculations, boq, cost, compliance, documents, execution,
    blueprints, ar, files, quick_actions, advanced_features, tenders, change_orders,
    schedule, geotechnical, material_tracking, inspection, hydrology, clash_detection
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(calculations.router, prefix="/calculations", tags=["calculations"])
api_router.include_router(boq.router, prefix="/boq", tags=["boq"])
api_router.include_router(cost.router, prefix="/cost", tags=["cost"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(execution.router, prefix="/execution", tags=["execution"])
api_router.include_router(blueprints.router, prefix="/blueprints", tags=["blueprints"])
api_router.include_router(ar.router, prefix="/ar", tags=["ar-visualization"])
api_router.include_router(files.router, prefix="/files", tags=["file-management"])
api_router.include_router(quick_actions.router, prefix="/quick-actions", tags=["quick-actions"])
api_router.include_router(advanced_features.router, prefix="/advanced", tags=["advanced-features"])
api_router.include_router(tenders.router, prefix="/tenders", tags=["tender-management"])
api_router.include_router(change_orders.router, prefix="/change-orders", tags=["change-orders"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["scheduling"])
api_router.include_router(geotechnical.router, prefix="/geotechnical", tags=["geotechnical"])
api_router.include_router(material_tracking.router, prefix="/materials", tags=["material-tracking"])
api_router.include_router(inspection.router, prefix="/inspection", tags=["inspection"])
api_router.include_router(hydrology.router, prefix="/hydrology", tags=["hydrology"])
api_router.include_router(clash_detection.router, prefix="/clash", tags=["clash-detection"])