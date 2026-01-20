"""
Site Inspection Service - Digital inspection checklists and photo documentation
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.advanced_features import QualityChecklist, QualityChecklistItem
from datetime import datetime
import uuid

class SiteInspectionService:
    """Site Inspection Service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_inspection_checklist(
        self,
        project_id: int,
        checklist_name: str,
        checklist_type: str,
        items: List[Dict],
        phase_id: int = None
    ) -> QualityChecklist:
        """Create site inspection checklist"""
        checklist = QualityChecklist(
            project_id=project_id,
            checklist_name=checklist_name,
            checklist_type=checklist_type,
            phase_id=phase_id,
            status="pending"
        )
        
        self.db.add(checklist)
        self.db.flush()
        
        # Add items
        for item_data in items:
            item = QualityChecklistItem(
                checklist_id=checklist.id,
                item_description=item_data.get("description", ""),
                requirement=item_data.get("requirement", ""),
                acceptance_criteria=item_data.get("acceptance_criteria", "")
            )
            self.db.add(item)
        
        self.db.commit()
        self.db.refresh(checklist)
        
        return checklist
    
    def perform_inspection(
        self,
        checklist_id: int,
        inspection_results: List[Dict],
        inspector_id: int,
        photos: List[str] = None
    ) -> Dict:
        """Perform site inspection"""
        checklist = self.db.query(QualityChecklist).filter(QualityChecklist.id == checklist_id).first()
        
        if not checklist:
            return {"error": "Checklist not found"}
        
        items = self.db.query(QualityChecklistItem).filter(
            QualityChecklistItem.checklist_id == checklist_id
        ).all()
        
        passed_items = 0
        failed_items = 0
        
        # Update items
        for item, result_data in zip(items, inspection_results):
            item.status = result_data.get("status", "pending")
            item.remarks = result_data.get("remarks", "")
            item.checked_by = inspector_id
            item.checked_at = datetime.utcnow()
            
            if item.status == "pass":
                passed_items += 1
            elif item.status == "fail":
                failed_items += 1
        
        # Update checklist status
        total_items = len(items)
        if passed_items == total_items:
            checklist.status = "completed"
        elif failed_items > 0:
            checklist.status = "failed"
        else:
            checklist.status = "in_progress"
        
        checklist.completed_by = inspector_id
        checklist.completed_at = datetime.utcnow()
        
        self.db.commit()
        
        return {
            "checklist_id": checklist_id,
            "total_items": total_items,
            "passed": passed_items,
            "failed": failed_items,
            "pending": total_items - passed_items - failed_items,
            "status": checklist.status,
            "completion_percentage": round((passed_items / total_items) * 100, 2) if total_items > 0 else 0
        }
    
    def get_inspection_report(
        self,
        project_id: int
    ) -> Dict:
        """Get inspection report for project"""
        checklists = self.db.query(QualityChecklist).filter(
            QualityChecklist.project_id == project_id
        ).all()
        
        total_checklists = len(checklists)
        completed = len([c for c in checklists if c.status == "completed"])
        failed = len([c for c in checklists if c.status == "failed"])
        pending = len([c for c in checklists if c.status == "pending"])
        
        return {
            "project_id": project_id,
            "total_checklists": total_checklists,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "completion_percentage": round((completed / total_checklists) * 100, 2) if total_checklists > 0 else 0,
            "checklists": [
                {
                    "id": c.id,
                    "name": c.checklist_name,
                    "type": c.checklist_type,
                    "status": c.status,
                    "completed_at": c.completed_at.isoformat() if c.completed_at else None
                }
                for c in checklists
            ]
        }
