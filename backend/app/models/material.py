"""
Material and BOQ Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class MaterialType(str, enum.Enum):
    """Material type enumeration"""
    CEMENT = "cement"
    CONCRETE = "concrete"
    STEEL = "steel"
    AGGREGATE = "aggregate"
    SAND = "sand"
    BITUMEN = "bitumen"
    BRICK = "brick"
    OTHER = "other"

class Material(Base):
    """Material master data"""
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    material_code = Column(String, unique=True, index=True, nullable=False)
    material_name = Column(String, nullable=False)
    material_type = Column(Enum(MaterialType), nullable=False)
    unit = Column(String, nullable=False)  # kg, m³, m², etc.
    description = Column(Text)
    specifications = Column(JSON)  # Additional specifications
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MaterialGrade(Base):
    """Material grade master (e.g., M20, M25, M30, Fe415, Fe500)"""
    __tablename__ = "material_grades"
    
    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    grade_code = Column(String, nullable=False)  # e.g., "M20", "M25", "Fe415"
    grade_name = Column(String, nullable=False)
    strength_value = Column(Float)  # Characteristic strength
    strength_unit = Column(String)  # MPa, N/mm²
    properties = Column(JSON)  # Additional properties
    applicable_codes = Column(JSON)  # Which codes support this grade
    cost_per_unit = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    material = relationship("Material")

class BOQ(Base):
    """Bill of Quantities"""
    __tablename__ = "boqs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    boq_code = Column(String, unique=True, index=True, nullable=False)
    boq_name = Column(String, nullable=False)
    version = Column(Integer, default=1)
    
    # Total Quantities
    total_cement_quantity = Column(Float)  # kg
    total_steel_quantity = Column(Float)  # kg
    total_concrete_quantity = Column(Float)  # m³
    total_sand_quantity = Column(Float)  # m³
    total_aggregate_quantity = Column(Float)  # m³
    total_bitumen_quantity = Column(Float)  # kg (for roads)
    total_excavation_volume = Column(Float)  # m³
    
    # Wastage Factors
    wastage_factor_cement = Column(Float, default=0.02)  # 2%
    wastage_factor_steel = Column(Float, default=0.05)  # 5%
    wastage_factor_concrete = Column(Float, default=0.02)  # 2%
    
    # Status
    is_finalized = Column(Boolean, default=False)
    finalized_at = Column(DateTime(timezone=True))
    finalized_by = Column(Integer, ForeignKey("users.id"))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="boqs")
    items = relationship("BOQItem", back_populates="boq", cascade="all, delete-orphan")

class BOQItem(Base):
    """BOQ Item - Individual line items"""
    __tablename__ = "boq_items"
    
    id = Column(Integer, primary_key=True, index=True)
    boq_id = Column(Integer, ForeignKey("boqs.id"), nullable=False)
    item_code = Column(String, nullable=False)
    item_description = Column(String, nullable=False)
    item_category = Column(String)  # e.g., "Earthwork", "Concrete", "Steel"
    
    # Material Details
    material_id = Column(Integer, ForeignKey("materials.id"))
    material_grade_id = Column(Integer, ForeignKey("material_grades.id"))
    
    # Quantities
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    unit_rate = Column(Float)  # Rate per unit
    total_amount = Column(Float)  # quantity * unit_rate
    
    # Additional Details
    specifications = Column(JSON)
    remarks = Column(String)
    
    # Relationships
    boq = relationship("BOQ", back_populates="items")
    material = relationship("Material")
    material_grade = relationship("MaterialGrade")
