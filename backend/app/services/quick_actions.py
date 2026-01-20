"""
Quick Actions Service - Time-saving automated workflows
"""

from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.calculation import Calculation
from app.models.material import BOQ
from app.models.cost import CostEstimate
from app.models.document import Document
from app.services.document_generator import DocumentGenerator
from app.services.blueprint_generator import BlueprintGenerator

class QuickActionsService:
    """Quick Actions Service - Automated workflows to save time"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def generate_project_package(
        self,
        project_id: int,
        include_calculations: bool = True,
        include_boq: bool = True,
        include_cost: bool = True,
        include_blueprints: bool = True
    ) -> Dict:
        """
        Generate complete project package - All documents in one go
        Saves hours of manual work!
        """
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"error": "Project not found"}
        
        package = {
            "project_id": project_id,
            "project_name": project.project_name,
            "generated_at": None,
            "documents": []
        }
        
        doc_gen = DocumentGenerator()
        blueprint_gen = BlueprintGenerator()
        
        project_data = {
            "project_name": project.project_name,
            "project_code": project.project_code,
            "date": project.created_at.isoformat() if project.created_at else "N/A"
        }
        
        # Generate calculation sheets
        if include_calculations:
            calculations = self.db.query(Calculation).filter(
                Calculation.project_id == project_id,
                Calculation.status == "completed"
            ).all()
            
            for calc in calculations:
                calc_data = {
                    "calculation_code": calc.calculation_code,
                    "input_parameters": calc.input_parameters,
                    "design_outputs": calc.design_outputs,
                    "compliance_status": calc.compliance_status
                }
                pdf_bytes = doc_gen.generate_calculation_sheet(calc_data, project_data)
                package["documents"].append({
                    "type": "calculation_sheet",
                    "name": f"Calculation_{calc.calculation_code}.pdf",
                    "data": pdf_bytes
                })
        
        # Generate BOQ
        if include_boq:
            boq = self.db.query(BOQ).filter(BOQ.project_id == project_id).first()
            if boq:
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
                package["documents"].append({
                    "type": "boq",
                    "name": f"BOQ_{boq.boq_code}.pdf",
                    "data": pdf_bytes
                })
        
        # Generate cost estimate
        if include_cost:
            estimate = self.db.query(CostEstimate).filter(
                CostEstimate.project_id == project_id
            ).order_by(CostEstimate.created_at.desc()).first()
            
            if estimate:
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
                package["documents"].append({
                    "type": "cost_estimate",
                    "name": f"CostEstimate_{estimate.estimate_code}.pdf",
                    "data": pdf_bytes
                })
        
        # Generate blueprints
        if include_blueprints:
            calculations = self.db.query(Calculation).filter(
                Calculation.project_id == project_id,
                Calculation.status == "completed"
            ).all()
            
            if calculations:
                calc_data = [
                    {
                        "calculation_type": calc.calculation_type.value,
                        "design_outputs": calc.design_outputs or {}
                    }
                    for calc in calculations
                ]
                
                # Plan view
                pdf_bytes = blueprint_gen.generate_structural_plan(project_data, calc_data, "A2")
                package["documents"].append({
                    "type": "blueprint_plan",
                    "name": f"Blueprint_Plan_{project.project_code}.pdf",
                    "data": pdf_bytes
                })
                
                # Elevation view
                pdf_bytes = blueprint_gen.generate_elevation_view(project_data, calc_data, "A2")
                package["documents"].append({
                    "type": "blueprint_elevation",
                    "name": f"Blueprint_Elevation_{project.project_code}.pdf",
                    "data": pdf_bytes
                })
        
        package["generated_at"] = datetime.utcnow().isoformat()
        
        return package
    
    def create_project_from_template(
        self,
        template_name: str,
        project_name: str,
        location: str,
        user_id: int
    ) -> Dict:
        """
        Create project from template - Pre-configured project setup
        Saves setup time!
        """
        templates = {
            "residential_building": {
                "project_type": "residential_building",
                "default_calculations": ["column_design", "beam_design", "slab_design"],
                "default_materials": {"concrete": "M25", "steel": "Fe415"}
            },
            "commercial_building": {
                "project_type": "commercial_building",
                "default_calculations": ["column_design", "beam_design", "slab_design", "footing_design"],
                "default_materials": {"concrete": "M30", "steel": "Fe500"}
            },
            "road_project": {
                "project_type": "road_highway",
                "default_calculations": ["road_design"],
                "default_materials": {}
            }
        }
        
        template = templates.get(template_name)
        if not template:
            return {"error": "Template not found"}
        
        # Create project
        project = Project(
            project_name=project_name,
            project_type=template["project_type"],
            location=location,
            created_by=user_id
        )
        
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        
        return {
            "project_id": project.id,
            "project_code": project.project_code,
            "template_used": template_name,
            "default_calculations": template["default_calculations"],
            "default_materials": template["default_materials"]
        }
    
    def bulk_export_project_documents(
        self,
        project_id: int,
        format: str = "zip"
    ) -> bytes:
        """
        Export all project documents as ZIP file
        One-click export saves hours!
        """
        import zipfile
        import io
        
        package = self.generate_project_package(project_id)
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for doc in package["documents"]:
                zip_file.writestr(doc["name"], doc["data"])
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

from datetime import datetime
