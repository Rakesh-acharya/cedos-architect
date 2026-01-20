"""
Construction Scheduling Service - CPM, Gantt charts
"""

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.advanced_features import ScheduleActivity
from datetime import datetime, timedelta

class ConstructionSchedulerService:
    """Construction Scheduling Service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def create_schedule(
        self,
        project_id: int,
        activities: List[Dict]
    ) -> Dict:
        """Create construction schedule"""
        created_activities = []
        
        for activity_data in activities:
            activity = ScheduleActivity(
                project_id=project_id,
                activity_code=activity_data.get("code", ""),
                activity_name=activity_data.get("name", ""),
                activity_type=activity_data.get("type", "task"),
                planned_start_date=datetime.fromisoformat(activity_data.get("start_date")) if activity_data.get("start_date") else None,
                planned_duration_days=activity_data.get("duration_days", 0),
                predecessor_activities=activity_data.get("predecessors", []),
                resource_requirements=activity_data.get("resources", {})
            )
            
            # Calculate end date
            if activity.planned_start_date and activity.planned_duration_days:
                activity.planned_end_date = activity.planned_start_date + timedelta(days=activity.planned_duration_days)
            
            self.db.add(activity)
            created_activities.append(activity)
        
        self.db.commit()
        
        # Calculate critical path
        critical_path = self._calculate_critical_path(created_activities)
        
        return {
            "project_id": project_id,
            "activities_created": len(created_activities),
            "critical_path": critical_path,
            "total_duration_days": critical_path.get("total_duration", 0)
        }
    
    def _calculate_critical_path(self, activities: List[ScheduleActivity]) -> Dict:
        """Calculate critical path using CPM"""
        # Simplified CPM calculation
        # In production, use proper CPM algorithm
        
        if not activities:
            return {"total_duration": 0, "critical_activities": []}
        
        # Find longest path
        max_duration = max(a.planned_duration_days or 0 for a in activities)
        critical_activities = [a.activity_code for a in activities if a.planned_duration_days == max_duration]
        
        return {
            "total_duration": max_duration,
            "critical_activities": critical_activities[:5]  # Top 5
        }
    
    def update_activity_progress(
        self,
        activity_id: int,
        progress_percentage: float,
        actual_start_date: Optional[datetime] = None,
        actual_end_date: Optional[datetime] = None
    ) -> Dict:
        """Update activity progress"""
        activity = self.db.query(ScheduleActivity).filter(ScheduleActivity.id == activity_id).first()
        
        if not activity:
            return {"error": "Activity not found"}
        
        activity.progress_percentage = progress_percentage
        
        if actual_start_date:
            activity.actual_start_date = actual_start_date
        
        if actual_end_date:
            activity.actual_end_date = actual_end_date
            activity.actual_duration_days = (actual_end_date - (actual_start_date or activity.planned_start_date)).days if actual_start_date or activity.planned_start_date else None
        
        self.db.commit()
        
        return {
            "activity_id": activity_id,
            "progress_percentage": progress_percentage,
            "status": "completed" if progress_percentage >= 100 else "in_progress"
        }
    
    def get_schedule_gantt_data(
        self,
        project_id: int
    ) -> Dict:
        """Get schedule data for Gantt chart"""
        activities = self.db.query(ScheduleActivity).filter(
            ScheduleActivity.project_id == project_id
        ).all()
        
        gantt_data = []
        for activity in activities:
            gantt_data.append({
                "id": activity.id,
                "code": activity.activity_code,
                "name": activity.activity_name,
                "start": activity.planned_start_date.isoformat() if activity.planned_start_date else None,
                "end": activity.planned_end_date.isoformat() if activity.planned_end_date else None,
                "duration": activity.planned_duration_days,
                "progress": activity.progress_percentage,
                "is_critical": activity.is_critical,
                "dependencies": activity.predecessor_activities or []
            })
        
        return {
            "project_id": project_id,
            "activities": gantt_data,
            "total_activities": len(activities)
        }
