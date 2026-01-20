"""
User and Role Models
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class UserRole(str, enum.Enum):
    """User role enumeration"""
    ENGINEER = "engineer"
    SENIOR_ENGINEER = "senior_engineer"
    PROJECT_MANAGER = "project_manager"
    QUANTITY_SURVEYOR = "quantity_surveyor"
    AUDITOR = "auditor"
    GOVERNMENT_OFFICER = "government_officer"
    ADMIN = "admin"

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ENGINEER)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="created_by_user")
    calculations = relationship("Calculation", back_populates="created_by_user")
    audit_logs = relationship("AuditLog", back_populates="user")
    action_logs = relationship("ActionLog", back_populates="user")

class Role(Base):
    """Role permissions model"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(Enum(UserRole), unique=True, nullable=False)
    permissions = Column(String)  # JSON string of permissions
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
