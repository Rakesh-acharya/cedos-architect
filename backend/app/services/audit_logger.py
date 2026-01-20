"""
Audit Logger Service - Tamper-proof audit trail
"""

from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditLog, ActionLog, ActionType
from datetime import datetime

class AuditLogger:
    """Audit Logger Service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def log_action(
        self,
        user_id: int,
        action_type: ActionType,
        entity_type: str,
        entity_id: Optional[int] = None,
        entity_code: Optional[str] = None,
        action_description: str = "",
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log an action to audit trail
        """
        audit_log = AuditLog(
            user_id=user_id,
            action_type=action_type,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_code=entity_code,
            action_description=action_description,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.db.add(audit_log)
        self.db.commit()
    
    def log_calculation(
        self,
        user_id: int,
        calculation_id: int,
        calculation_code: str,
        action_description: str = "Calculation performed",
        ip_address: Optional[str] = None
    ):
        """Log calculation action"""
        self.log_action(
            user_id=user_id,
            action_type=ActionType.CALCULATION,
            entity_type="Calculation",
            entity_id=calculation_id,
            entity_code=calculation_code,
            action_description=action_description,
            ip_address=ip_address
        )
    
    def log_override(
        self,
        user_id: int,
        entity_type: str,
        entity_id: int,
        entity_code: str,
        override_reason: str,
        old_values: Dict,
        new_values: Dict,
        ip_address: Optional[str] = None
    ):
        """Log override action (critical for audit)"""
        self.log_action(
            user_id=user_id,
            action_type=ActionType.OVERRIDE,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_code=entity_code,
            action_description=f"Override applied: {override_reason}",
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address
        )
    
    def log_approval(
        self,
        user_id: int,
        entity_type: str,
        entity_id: int,
        entity_code: str,
        ip_address: Optional[str] = None
    ):
        """Log approval action"""
        self.log_action(
            user_id=user_id,
            action_type=ActionType.APPROVE,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_code=entity_code,
            action_description=f"{entity_type} approved",
            ip_address=ip_address
        )
    
    def get_audit_trail(
        self,
        entity_type: Optional[str] = None,
        entity_id: Optional[int] = None,
        user_id: Optional[int] = None,
        limit: int = 100
    ):
        """Get audit trail"""
        query = self.db.query(AuditLog)
        
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        if entity_id:
            query = query.filter(AuditLog.entity_id == entity_id)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
