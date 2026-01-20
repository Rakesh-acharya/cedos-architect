"""
Cost Estimation Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class EstimateType(str, enum.Enum):
    """Estimate type"""
    PRELIMINARY = "preliminary"
    DETAILED = "detailed"
    REVISED = "revised"
    FINAL = "final"

class CostEstimate(Base):
    """Cost Estimate"""
    __tablename__ = "cost_estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    estimate_code = Column(String, unique=True, index=True, nullable=False)
    estimate_name = Column(String, nullable=False)
    estimate_type = Column(Enum(EstimateType), nullable=False)
    version = Column(Integer, default=1)
    
    # Base Costs
    base_cost = Column(Float, nullable=False)  # Sum of all cost items
    
    # Additional Costs
    contingency_percentage = Column(Float, default=0.10)  # 10%
    contingency_amount = Column(Float)
    escalation_percentage = Column(Float, default=0.05)  # 5%
    escalation_amount = Column(Float)
    
    # Taxes
    gst_percentage = Column(Float, default=0.18)  # 18% GST
    gst_amount = Column(Float)
    other_taxes = Column(Float, default=0)
    
    # Total Cost
    total_cost = Column(Float, nullable=False)
    
    # Currency
    currency = Column(String, default="INR")
    
    # Rate Source
    rate_source = Column(String)  # "SOR", "Market", "Tender"
    sor_version = Column(String)  # If using SOR
    
    # Phase-wise Costs (JSON)
    phase_wise_costs = Column(JSON)
    
    # Status
    is_approved = Column(Boolean, default=False)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="cost_estimates")
    items = relationship("CostItem", back_populates="cost_estimate", cascade="all, delete-orphan")

class CostItem(Base):
    """Cost Item - Individual cost line items"""
    __tablename__ = "cost_items"
    
    id = Column(Integer, primary_key=True, index=True)
    cost_estimate_id = Column(Integer, ForeignKey("cost_estimates.id"), nullable=False)
    item_code = Column(String, nullable=False)
    item_description = Column(String, nullable=False)
    category = Column(String)  # e.g., "Material", "Labor", "Equipment"
    
    # Quantities and Rates
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_rate = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)  # quantity * unit_rate
    
    # Rate Source
    rate_source = Column(String)  # "SOR", "Market", "Tender"
    sor_item_code = Column(String)  # If from SOR
    
    # Additional Details
    specifications = Column(JSON)
    remarks = Column(String)
    
    # Relationships
    cost_estimate = relationship("CostEstimate", back_populates="items")

class ScheduleOfRates(Base):
    """Schedule of Rates (SOR) Master Data"""
    __tablename__ = "schedule_of_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    sor_code = Column(String, unique=True, index=True, nullable=False)
    sor_name = Column(String, nullable=False)
    version = Column(String, nullable=False)  # e.g., "2023-2024"
    authority = Column(String)  # e.g., "CPWD", "State PWD"
    effective_from = Column(DateTime(timezone=True))
    effective_to = Column(DateTime(timezone=True))
    
    # Item Details
    item_code = Column(String, nullable=False)
    item_description = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    unit_rate = Column(Float, nullable=False)
    
    # Breakdown (if available)
    material_rate = Column(Float)
    labor_rate = Column(Float)
    equipment_rate = Column(Float)
    
    # Additional Info
    specifications = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
