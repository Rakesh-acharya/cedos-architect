"""
Advanced Features Models - Market-leading capabilities
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

# ========== DIGITAL TWIN & IoT ==========
class IoTDevice(Base):
    """IoT Device for Digital Twin monitoring"""
    __tablename__ = "iot_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)  # strain, vibration, temperature, etc.
    device_location = Column(JSON)  # x, y, z coordinates
    device_id = Column(String, unique=True, nullable=False)  # Physical device ID
    is_active = Column(Boolean, default=True)
    installed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="iot_devices")
    readings = relationship("IoTReading", back_populates="device")

class IoTReading(Base):
    """IoT Sensor Readings"""
    __tablename__ = "iot_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("iot_devices.id"), nullable=False)
    reading_type = Column(String, nullable=False)  # strain, vibration, etc.
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    sensor_metadata = Column(JSON)  # Additional sensor data (renamed from 'metadata' - reserved in SQLAlchemy)
    
    # Relationships
    device = relationship("IoTDevice", back_populates="readings")

class StructuralHealthAlert(Base):
    """Alerts from Digital Twin analysis"""
    __tablename__ = "structural_health_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    alert_type = Column(String, nullable=False)  # warning, critical, maintenance
    alert_message = Column(Text, nullable=False)
    severity = Column(String, nullable=False)  # low, medium, high, critical
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    project = relationship("Project", back_populates="structural_alerts")

# ========== GENERATIVE DESIGN ==========
class DesignOption(Base):
    """AI-Generated Design Options"""
    __tablename__ = "design_options"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    option_name = Column(String, nullable=False)
    design_type = Column(String, nullable=False)  # structural, road, bridge, etc.
    
    # Design Parameters
    design_parameters = Column(JSON, nullable=False)
    design_outputs = Column(JSON, nullable=False)
    
    # Optimization Metrics
    cost_estimate = Column(Float)
    material_efficiency = Column(Float)  # 0-1 score
    sustainability_score = Column(Float)  # 0-1 score
    compliance_score = Column(Float)  # 0-1 score
    overall_score = Column(Float)  # Weighted combination
    
    # Status
    is_selected = Column(Boolean, default=False)
    generated_by_ai = Column(Boolean, default=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="design_options")

# ========== RISK ASSESSMENT ==========
class RiskCategory(str, enum.Enum):
    """Risk categories"""
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    SCHEDULE = "schedule"
    SAFETY = "safety"
    ENVIRONMENTAL = "environmental"
    REGULATORY = "regulatory"
    SUPPLY_CHAIN = "supply_chain"
    WEATHER = "weather"

class ProjectRisk(Base):
    """Project Risk Assessment"""
    __tablename__ = "project_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    risk_name = Column(String, nullable=False)
    risk_category = Column(Enum(RiskCategory), nullable=False)
    description = Column(Text, nullable=False)
    
    # Risk Assessment
    probability = Column(Float, nullable=False)  # 0-1
    impact = Column(Float, nullable=False)  # 0-1
    risk_score = Column(Float, nullable=False)  # probability * impact
    
    # Mitigation
    mitigation_strategy = Column(Text)
    mitigation_cost = Column(Float)
    residual_risk = Column(Float)  # After mitigation
    
    # Status
    status = Column(String, default="identified")  # identified, mitigated, monitored, closed
    identified_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    identified_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="risks")

# ========== TENDER MANAGEMENT ==========
class Tender(Base):
    """Tender/Bid Management"""
    __tablename__ = "tenders"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    tender_number = Column(String, unique=True, nullable=False)
    tender_title = Column(String, nullable=False)
    
    # Tender Details
    tender_type = Column(String)  # open, limited, single
    estimated_value = Column(Float)
    earnest_money = Column(Float)
    tender_opening_date = Column(DateTime(timezone=True))
    tender_closing_date = Column(DateTime(timezone=True))
    
    # Status
    status = Column(String, default="draft")  # draft, published, closed, awarded, cancelled
    published_at = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", back_populates="tenders")
    bids = relationship("TenderBid", back_populates="tender")

class TenderBid(Base):
    """Tender Bids"""
    __tablename__ = "tender_bids"
    
    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    bidder_name = Column(String, nullable=False)
    bidder_company = Column(String)
    
    # Bid Details
    bid_amount = Column(Float, nullable=False)
    completion_time_days = Column(Integer)
    technical_score = Column(Float)  # 0-100
    financial_score = Column(Float)  # 0-100
    overall_score = Column(Float)  # Weighted combination
    
    # Documents
    technical_bid_path = Column(String)
    financial_bid_path = Column(String)
    
    # Status
    status = Column(String, default="submitted")  # submitted, under_evaluation, qualified, disqualified, awarded
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    evaluated_at = Column(DateTime(timezone=True))
    evaluated_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    tender = relationship("Tender", back_populates="bids")

# ========== CHANGE ORDER MANAGEMENT ==========
class ChangeOrder(Base):
    """Change Order / Variation Management"""
    __tablename__ = "change_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    change_order_number = Column(String, unique=True, nullable=False)
    change_order_title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Change Details
    change_type = Column(String)  # addition, deletion, modification, substitution
    reason = Column(String)  # client_request, site_condition, design_error, etc.
    
    # Cost Impact
    original_cost = Column(Float)
    revised_cost = Column(Float)
    cost_difference = Column(Float)  # revised - original
    
    # Time Impact
    original_duration_days = Column(Integer)
    revised_duration_days = Column(Integer)
    time_difference_days = Column(Integer)
    
    # Approval Workflow
    status = Column(String, default="draft")  # draft, submitted, approved, rejected, executed
    submitted_by = Column(Integer, ForeignKey("users.id"))
    submitted_at = Column(DateTime(timezone=True))
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", back_populates="change_orders")
    items = relationship("ChangeOrderItem", back_populates="change_order")

class ChangeOrderItem(Base):
    """Change Order Line Items"""
    __tablename__ = "change_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    change_order_id = Column(Integer, ForeignKey("change_orders.id"), nullable=False)
    item_description = Column(String, nullable=False)
    quantity_original = Column(Float)
    quantity_revised = Column(Float)
    unit_rate = Column(Float)
    amount = Column(Float)
    
    # Relationships
    change_order = relationship("ChangeOrder", back_populates="items")

# ========== CONSTRUCTION SCHEDULING ==========
class ScheduleActivity(Base):
    """Construction Schedule Activity"""
    __tablename__ = "schedule_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    activity_code = Column(String, nullable=False)
    activity_name = Column(String, nullable=False)
    activity_type = Column(String)  # task, milestone, summary
    
    # Schedule
    planned_start_date = Column(DateTime(timezone=True))
    planned_end_date = Column(DateTime(timezone=True))
    planned_duration_days = Column(Integer)
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    actual_duration_days = Column(Integer)
    
    # Dependencies
    predecessor_activities = Column(JSON)  # List of activity IDs
    successor_activities = Column(JSON)
    
    # Progress
    progress_percentage = Column(Float, default=0)
    is_critical = Column(Boolean, default=False)  # On critical path
    
    # Resources
    assigned_to = Column(Integer, ForeignKey("users.id"))
    resource_requirements = Column(JSON)  # Labor, equipment, materials
    
    # Relationships
    project = relationship("Project", back_populates="schedule_activities")

# ========== QUALITY CONTROL ==========
class QualityChecklist(Base):
    """Quality Control Checklist"""
    __tablename__ = "quality_checklists"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    checklist_name = Column(String, nullable=False)
    checklist_type = Column(String)  # material, construction, testing, final
    phase_id = Column(Integer, ForeignKey("project_phases.id"))
    
    # Status
    status = Column(String, default="pending")  # pending, in_progress, completed, failed
    completed_at = Column(DateTime(timezone=True))
    completed_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    project = relationship("Project", back_populates="quality_checklists")
    items = relationship("QualityChecklistItem", back_populates="checklist")

class QualityChecklistItem(Base):
    """Quality Checklist Items"""
    __tablename__ = "quality_checklist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(Integer, ForeignKey("quality_checklists.id"), nullable=False)
    item_description = Column(String, nullable=False)
    requirement = Column(Text)
    acceptance_criteria = Column(Text)
    
    # Status
    status = Column(String, default="pending")  # pending, pass, fail, n/a
    remarks = Column(Text)
    checked_by = Column(Integer, ForeignKey("users.id"))
    checked_at = Column(DateTime(timezone=True))
    
    # Relationships
    checklist = relationship("QualityChecklist", back_populates="items")

# ========== SUSTAINABILITY ==========
class SustainabilityAssessment(Base):
    """Sustainability & Carbon Footprint Assessment"""
    __tablename__ = "sustainability_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assessment_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Carbon Footprint
    embodied_carbon_kg = Column(Float)  # CO2 equivalent
    operational_carbon_kg = Column(Float)
    total_carbon_kg = Column(Float)
    
    # Material Impact
    material_breakdown = Column(JSON)  # Material-wise carbon
    
    # Sustainability Score
    sustainability_score = Column(Float)  # 0-100
    leed_score = Column(Float)  # If applicable
    breeam_score = Column(Float)  # If applicable
    
    # Recommendations
    improvement_suggestions = Column(JSON)
    
    # Relationships
    project = relationship("Project", back_populates="sustainability_assessments")

# ========== PAYMENT TRACKING ==========
class PaymentMilestone(Base):
    """Payment Milestones"""
    __tablename__ = "payment_milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    milestone_name = Column(String, nullable=False)
    milestone_type = Column(String)  # progress, material, completion, retention
    
    # Payment Details
    milestone_amount = Column(Float, nullable=False)
    percentage_of_total = Column(Float)  # % of total contract
    due_date = Column(DateTime(timezone=True))
    
    # Status
    status = Column(String, default="pending")  # pending, invoiced, paid, overdue
    invoiced_at = Column(DateTime(timezone=True))
    paid_at = Column(DateTime(timezone=True))
    payment_amount = Column(Float)
    payment_reference = Column(String)
    
    # Relationships
    project = relationship("Project", back_populates="payment_milestones")

# ========== WEATHER INTEGRATION ==========
class WeatherImpact(Base):
    """Weather Impact on Construction"""
    __tablename__ = "weather_impacts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    
    # Weather Data
    temperature = Column(Float)
    rainfall_mm = Column(Float)
    wind_speed = Column(Float)
    humidity = Column(Float)
    weather_condition = Column(String)  # sunny, rainy, stormy, etc.
    
    # Impact
    work_days_lost = Column(Float)  # 0-1 (fraction of day)
    impact_description = Column(Text)
    activities_affected = Column(JSON)  # List of activity IDs
    
    # Relationships
    project = relationship("Project", back_populates="weather_impacts")

# ========== DOCUMENT VERSIONING ==========
class DocumentVersion(Base):
    """Document Version Control"""
    __tablename__ = "document_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    version_label = Column(String)  # e.g., "v1.0", "draft", "final"
    
    # Version Details
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    changes_summary = Column(Text)
    diff_data = Column(JSON)  # Changes from previous version
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_current = Column(Boolean, default=False)
    
    # Relationships
    document = relationship("Document")
