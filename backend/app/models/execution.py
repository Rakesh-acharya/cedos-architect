"""
Project Execution and Monitoring Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class PhaseStatus(str, enum.Enum):
    """Phase status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DELAYED = "delayed"

class ProjectPhase(Base):
    """Project Phase"""
    __tablename__ = "project_phases"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    phase_code = Column(String, nullable=False)
    phase_name = Column(String, nullable=False)
    phase_number = Column(Integer, nullable=False)
    
    # Schedule
    planned_start_date = Column(DateTime(timezone=True))
    planned_end_date = Column(DateTime(timezone=True))
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    
    # Progress
    planned_progress_percentage = Column(Float, default=0)
    actual_progress_percentage = Column(Float, default=0)
    status = Column(Enum(PhaseStatus), default=PhaseStatus.NOT_STARTED)
    
    # Budget
    planned_cost = Column(Float)
    actual_cost = Column(Float)
    
    # Details
    description = Column(Text)
    deliverables = Column(JSON)  # List of deliverables
    dependencies = Column(JSON)  # Dependencies on other phases
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="phases")

class ProgressTracking(Base):
    """Progress Tracking"""
    __tablename__ = "progress_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    phase_id = Column(Integer, ForeignKey("project_phases.id"))
    
    # Progress Data
    tracking_date = Column(DateTime(timezone=True), nullable=False)
    progress_percentage = Column(Float, nullable=False)
    work_completed = Column(Text)
    work_remaining = Column(Text)
    
    # Material Consumption
    material_consumption = Column(JSON)  # Material-wise consumption
    
    # Issues
    issues_encountered = Column(Text)
    resolution = Column(Text)
    
    # Reported By
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="progress_tracking")

class MeasurementBook(Base):
    """Measurement Book (MB) - For contractor billing"""
    __tablename__ = "measurement_books"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    mb_number = Column(String, unique=True, index=True, nullable=False)
    mb_date = Column(DateTime(timezone=True), nullable=False)
    
    # Work Details
    work_description = Column(Text, nullable=False)
    item_code = Column(String)
    item_description = Column(String)
    
    # Measurements
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_rate = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Approval
    is_approved = Column(Boolean, default=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    
    # Contractor
    contractor_name = Column(String)
    contractor_bill_number = Column(String)
    
    # Remarks
    remarks = Column(Text)
    
    # Created By
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project")
