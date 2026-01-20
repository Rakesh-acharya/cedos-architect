"""
Document Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.document import Document, DocumentType
from app.models.calculation import Calculation
from app.models.material import BOQ
from app.models.cost import CostEstimate
from app.services.document_generator import DocumentGenerator
from app.services.blueprint_generator import BlueprintGenerator
import uuid

router = APIRouter()

@router.post("/generate/{project_id}")
def generate_document(
    project_id: int,
    document_type: DocumentType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a document for a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Generate document code
    document_code = f"DOC-{uuid.uuid4().hex[:8].upper()}"
    
    # Create document record
    # In production, this would generate actual PDF/DOCX files
    db_document = Document(
        project_id=project_id,
        document_code=document_code,
        document_name=f"{document_type.value.replace('_', ' ').title()} for {project.project_name}",
        document_type=document_type,
        content_data={},  # Would contain structured data for document generation
        created_by=current_user.id
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return {
        "document_id": db_document.id,
        "document_code": db_document.document_code,
        "message": "Document generation initiated. Use document generation service to create actual file."
    }

@router.get("/project/{project_id}")
def get_project_documents(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all documents for a project"""
    documents = db.query(Document).filter(Document.project_id == project_id).all()
    return documents

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document

@router.get("/download/calculation/{calculation_id}")
def download_calculation_pdf(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download calculation sheet as PDF"""
    calculation = db.query(Calculation).filter(Calculation.id == calculation_id).first()
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    project = db.query(Project).filter(Project.id == calculation.project_id).first()
    
    doc_gen = DocumentGenerator()
    
    project_data = {
        "project_name": project.project_name if project else "N/A",
        "project_code": project.project_code if project else "N/A"
    }
    
    calc_data = {
        "calculation_code": calculation.calculation_code,
        "input_parameters": calculation.input_parameters,
        "design_outputs": calculation.design_outputs,
        "compliance_status": calculation.compliance_status
    }
    
    pdf_bytes = doc_gen.generate_calculation_sheet(calc_data, project_data)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=calculation_{calculation.calculation_code}.pdf"
        }
    )

@router.get("/download/boq/{boq_id}")
def download_boq_pdf(
    boq_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download BOQ as PDF"""
    boq = db.query(BOQ).filter(BOQ.id == boq_id).first()
    if not boq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="BOQ not found"
        )
    
    project = db.query(Project).filter(Project.id == boq.project_id).first()
    
    doc_gen = DocumentGenerator()
    
    project_data = {
        "project_name": project.project_name if project else "N/A",
        "project_code": project.project_code if project else "N/A"
    }
    
    boq_data = {
        "boq_code": boq.boq_code,
        "items": [
            {
                "item_code": item.item_code,
                "item_description": item.item_description,
                "quantity": item.quantity,
                "unit": item.unit
            }
            for item in boq.items
        ]
    }
    
    pdf_bytes = doc_gen.generate_boq_pdf(boq_data, project_data)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=boq_{boq.boq_code}.pdf"
        }
    )

@router.get("/download/cost-estimate/{estimate_id}")
def download_cost_estimate_pdf(
    estimate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download cost estimate as PDF"""
    estimate = db.query(CostEstimate).filter(CostEstimate.id == estimate_id).first()
    if not estimate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost estimate not found"
        )
    
    project = db.query(Project).filter(Project.id == estimate.project_id).first()
    
    doc_gen = DocumentGenerator()
    
    project_data = {
        "project_name": project.project_name if project else "N/A",
        "project_code": project.project_code if project else "N/A"
    }
    
    estimate_data = {
        "estimate_code": estimate.estimate_code,
        "base_cost": estimate.base_cost,
        "contingency_amount": estimate.contingency_amount,
        "escalation_amount": estimate.escalation_amount,
        "gst_amount": estimate.gst_amount,
        "total_cost": estimate.total_cost,
        "items": [
            {
                "item_code": item.item_code,
                "item_description": item.item_description,
                "quantity": item.quantity,
                "unit": item.unit,
                "unit_rate": item.unit_rate,
                "total_amount": item.total_amount
            }
            for item in estimate.items
        ]
    }
    
    pdf_bytes = doc_gen.generate_cost_estimate_pdf(estimate_data, project_data)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=cost_estimate_{estimate.estimate_code}.pdf"
        }
    )
