"""
Project Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class ProjectType(str, enum.Enum):
    """Project type enumeration"""
    RESIDENTIAL_BUILDING = "residential_building"
    COMMERCIAL_BUILDING = "commercial_building"
    INDUSTRIAL_STRUCTURE = "industrial_structure"
    ROAD_HIGHWAY = "road_highway"
    BRIDGE_FLYOVER = "bridge_flyover"
    DRAINAGE_SEWER = "drainage_sewer"
    WATER_SUPPLY = "water_supply"
    GOVERNMENT_INFRASTRUCTURE = "government_infrastructure"

class ProjectStatus(str, enum.Enum):
    """Project status enumeration"""
    DRAFT = "draft"
    DESIGN = "design"
    APPROVED = "approved"
    EXECUTION = "execution"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String, unique=True, index=True, nullable=False)
    project_name = Column(String, nullable=False)
    project_type = Column(Enum(ProjectType), nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT)
    
    # Location & Environmental Data
    location = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    soil_zone = Column(String)  # e.g., "Zone II", "Zone III"
    seismic_zone = Column(String)  # e.g., "Zone II", "Zone III", "Zone IV", "Zone V"
    wind_zone = Column(String)  # e.g., "Zone I", "Zone II", "Zone III", "Zone IV", "Zone V", "Zone VI"
    climate_data = Column(JSON)  # Temperature, rainfall, etc.
    
    # Project Requirements
    usage_type = Column(String)  # residential, commercial, public, etc.
    design_life_years = Column(Integer, default=50)
    budget_constraint = Column(Float)  # in currency units
    
    # Load Requirements (JSON for flexibility)
    load_requirements = Column(JSON)  # Dead load, live load, wind load, seismic load
    
    # Soil Classification (from reports)
    soil_classification = Column(String)
    soil_bearing_capacity = Column(Float)  # kN/m²
    soil_data = Column(JSON)  # Detailed soil test data
    
    # Project Metadata
    description = Column(Text)
    client_name = Column(String)
    client_address = Column(String)
    consultant_name = Column(String)
    contractor_name = Column(String)
    
    # Timestamps
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True))
    approved_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="projects")
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    calculations = relationship("Calculation", back_populates="project")
    boqs = relationship("BOQ", back_populates="project")
    cost_estimates = relationship("CostEstimate", back_populates="project")
    compliance_checks = relationship("ComplianceCheck", back_populates="project")
    documents = relationship("Document", back_populates="project")
    phases = relationship("ProjectPhase", back_populates="project")
    progress_tracking = relationship("ProgressTracking", back_populates="project")
    files = relationship("ProjectFile", back_populates="project")
    folders = relationship("ProjectFolder", back_populates="project")
    # Advanced Features Relationships
    iot_devices = relationship("IoTDevice", back_populates="project")
    design_options = relationship("DesignOption", back_populates="project")
    risks = relationship("ProjectRisk", back_populates="project")
    tenders = relationship("Tender", back_populates="project")
    change_orders = relationship("ChangeOrder", back_populates="project")
    schedule_activities = relationship("ScheduleActivity", back_populates="project")
    quality_checklists = relationship("QualityChecklist", back_populates="project")
    sustainability_assessments = relationship("SustainabilityAssessment", back_populates="project")
    payment_milestones = relationship("PaymentMilestone", back_populates="project")
    weather_impacts = relationship("WeatherImpact", back_populates="project")
    structural_alerts = relationship("StructuralHealthAlert", back_populates="project")