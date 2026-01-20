"""
Audit and Logging Models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class ActionType(str, enum.Enum):
    """Action type"""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    OVERRIDE = "override"
    CALCULATION = "calculation"
    COMPLIANCE_CHECK = "compliance_check"
    DOCUMENT_GENERATE = "document_generate"
    LOGIN = "login"
    LOGOUT = "logout"
    OTHER = "other"

class AuditLog(Base):
    """Audit Log - High-level audit trail"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(Enum(ActionType), nullable=False)
    
    # Entity Information
    entity_type = Column(String, nullable=False)  # e.g., "Project", "Calculation", "BOQ"
    entity_id = Column(Integer)
    entity_code = Column(String)  # e.g., project_code, calculation_code
    
    # Action Details
    action_description = Column(String, nullable=False)
    old_values = Column(JSON)  # Values before change
    new_values = Column(JSON)  # Values after change
    
    # IP and Session
    ip_address = Column(String)
    user_agent = Column(String)
    session_id = Column(String)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

class ActionLog(Base):
    """Action Log - Detailed action log"""
    __tablename__ = "action_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(Enum(ActionType), nullable=False)
    
    # Context
    module = Column(String)  # e.g., "Design", "Cost", "Compliance"
    function_name = Column(String)  # Function/method name
    parameters = Column(JSON)  # Function parameters
    
    # Result
    result_status = Column(String)  # "success", "failure", "warning"
    result_data = Column(JSON)
    error_message = Column(Text)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="action_logs")
