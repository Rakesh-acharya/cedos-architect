"""
Compliance and Code Validation Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class CodeStandardType(str, enum.Enum):
    """Code standard type"""
    IS = "IS"  # Indian Standard
    IRC = "IRC"  # Indian Roads Congress
    NBC = "NBC"  # National Building Code
    PWD = "PWD"  # Public Works Department
    LOCAL = "LOCAL"  # Local standards

class ComplianceStatus(str, enum.Enum):
    """Compliance status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    WARNING = "warning"
    PENDING = "pending"

class CodeStandard(Base):
    """Code Standard Master Data"""
    __tablename__ = "code_standards"
    
    id = Column(Integer, primary_key=True, index=True)
    code_number = Column(String, unique=True, index=True, nullable=False)  # e.g., "IS 456:2000"
    code_name = Column(String, nullable=False)
    code_type = Column(Enum(CodeStandardType), nullable=False)
    version = Column(String)  # e.g., "2000", "2011"
    description = Column(Text)
    
    # Code Rules (JSON structure)
    rules = Column(JSON)  # Structured rules and formulas
    applicable_project_types = Column(JSON)  # Which project types this applies to
    
    # Status
    is_active = Column(Boolean, default=True)
    effective_from = Column(DateTime(timezone=True))
    effective_to = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ComplianceCheck(Base):
    """Compliance Check for Projects"""
    __tablename__ = "compliance_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    code_standard_id = Column(Integer, ForeignKey("code_standards.id"), nullable=False)
    check_code = Column(String, nullable=False)
    check_name = Column(String, nullable=False)
    
    # Check Details
    check_type = Column(String)  # e.g., "safety_factor", "dimension", "material_grade"
    parameter_checked = Column(String)  # What parameter is being checked
    required_value = Column(Float)  # Required value per code
    actual_value = Column(Float)  # Actual design value
    unit = Column(String)
    
    # Result
    status = Column(Enum(ComplianceStatus), nullable=False)
    is_passed = Column(Boolean, default=False)
    margin = Column(Float)  # Difference between required and actual
    
    # Details
    check_details = Column(JSON)  # Detailed check information
    violation_details = Column(Text)  # If non-compliant, details
    
    # Override
    has_override = Column(Boolean, default=False)
    override_reason = Column(Text)
    override_approved_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
    checked_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    project = relationship("Project", back_populates="compliance_checks")
    code_standard = relationship("CodeStandard")
    logs = relationship("ComplianceLog", back_populates="compliance_check")

class ComplianceLog(Base):
    """Compliance Check Log"""
    __tablename__ = "compliance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    compliance_check_id = Column(Integer, ForeignKey("compliance_checks.id"), nullable=False)
    action = Column(String, nullable=False)  # "check_performed", "override_applied", etc.
    details = Column(JSON)
    performed_by = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    compliance_check = relationship("ComplianceCheck", back_populates="logs")
