"""
Calculation Models - Structural Design Engine
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class CalculationType(str, enum.Enum):
    """Calculation type enumeration"""
    LOAD_CALCULATION = "load_calculation"
    FOOTING_DESIGN = "footing_design"
    COLUMN_DESIGN = "column_design"
    BEAM_DESIGN = "beam_design"
    SLAB_DESIGN = "slab_design"
    RETAINING_WALL_DESIGN = "retaining_wall_design"
    ROAD_DESIGN = "road_design"
    BRIDGE_DESIGN = "bridge_design"
    DRAINAGE_DESIGN = "drainage_design"

class CalculationStatus(str, enum.Enum):
    """Calculation status"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    APPROVED = "approved"
    REJECTED = "rejected"

class Calculation(Base):
    """Calculation model - Stores structural design calculations"""
    __tablename__ = "calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    calculation_code = Column(String, unique=True, index=True, nullable=False)
    calculation_type = Column(Enum(CalculationType), nullable=False)
    status = Column(Enum(CalculationStatus), default=CalculationStatus.DRAFT)
    
    # Input Parameters (JSON for flexibility)
    input_parameters = Column(JSON, nullable=False)
    
    # Calculation Results
    calculation_results = Column(JSON, nullable=False)
    
    # Design Outputs
    design_outputs = Column(JSON)  # Member sizes, reinforcement details, etc.
    
    # Safety Checks
    safety_checks = Column(JSON)  # All safety factor checks
    safety_factor_passed = Column(Boolean, default=False)
    
    # Code Compliance
    code_standard_used = Column(String)  # e.g., "IS 456:2000", "IRC 112:2011"
    compliance_status = Column(String)  # "compliant", "non_compliant", "warning"
    
    # Validation
    is_validated = Column(Boolean, default=False)
    validated_by = Column(Integer, ForeignKey("users.id"))
    validated_at = Column(DateTime(timezone=True))
    
    # Override Information (if human override was used)
    has_override = Column(Boolean, default=False)
    override_reason = Column(Text)
    override_approved_by = Column(Integer, ForeignKey("users.id"))
    
    # Metadata
    description = Column(Text)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="calculations")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="calculations")
    logs = relationship("CalculationLog", back_populates="calculation")

class CalculationLog(Base):
    """Calculation log - Detailed step-by-step calculation log"""
    __tablename__ = "calculation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    calculation_id = Column(Integer, ForeignKey("calculations.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    step_description = Column(String, nullable=False)
    formula_used = Column(String)
    input_values = Column(JSON)
    output_value = Column(Float)
    unit = Column(String)
    notes = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    calculation = relationship("Calculation", back_populates="logs")
