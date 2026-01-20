"""
File Management Models - Organized project file storage
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class FileCategory(str, enum.Enum):
    """File category enumeration"""
    BLUEPRINT = "blueprint"
    CALCULATION_SHEET = "calculation_sheet"
    BOQ = "boq"
    BILL = "bill"
    INVOICE = "invoice"
    LETTER = "letter"
    CONTRACT = "contract"
    PERMIT = "permit"
    CERTIFICATE = "certificate"
    PHOTO = "photo"
    VIDEO = "video"
    REPORT = "report"
    DRAWING = "drawing"
    SPECIFICATION = "specification"
    TEST_REPORT = "test_report"
    SOIL_REPORT = "soil_report"
    OTHER = "other"

class FileType(str, enum.Enum):
    """File type enumeration"""
    PDF = "pdf"
    IMAGE = "image"  # jpg, png, etc.
    DOCUMENT = "document"  # doc, docx
    SPREADSHEET = "spreadsheet"  # xls, xlsx
    CAD = "cad"  # dwg, dxf
    VIDEO = "video"  # mp4, avi
    ARCHIVE = "archive"  # zip, rar
    OTHER = "other"

class ProjectFile(Base):
    """Project File - Organized file storage"""
    __tablename__ = "project_files"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # File Information
    file_name = Column(String, nullable=False)
    original_file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Storage path
    file_size = Column(Integer, nullable=False)  # Bytes
    mime_type = Column(String, nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    file_category = Column(Enum(FileCategory), nullable=False)
    
    # Organization
    folder_path = Column(String)  # Virtual folder path (e.g., "Blueprints/Plan Views")
    tags = Column(String)  # Comma-separated tags
    description = Column(Text)
    
    # Metadata
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Version Control
    version = Column(Integer, default=1)
    is_latest = Column(Boolean, default=True)
    parent_file_id = Column(Integer, ForeignKey("project_files.id"))  # For versioning
    
    # Access Control
    is_public = Column(Boolean, default=False)
    shared_with = Column(JSON)  # List of user IDs with access
    
    # Related Entities (optional links)
    related_calculation_id = Column(Integer, ForeignKey("calculations.id"))
    related_boq_id = Column(Integer, ForeignKey("boqs.id"))
    related_cost_estimate_id = Column(Integer, ForeignKey("cost_estimates.id"))
    related_document_id = Column(Integer, ForeignKey("documents.id"))
    
    # Relationships
    project = relationship("Project", back_populates="files")
    uploaded_by_user = relationship("User")
    parent_file = relationship("ProjectFile", remote_side=[id])
    versions = relationship("ProjectFile", backref="parent")

class ProjectFolder(Base):
    """Project Folder - Virtual folder structure"""
    __tablename__ = "project_folders"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Folder Information
    folder_name = Column(String, nullable=False)
    folder_path = Column(String, nullable=False)  # Full path
    parent_folder_id = Column(Integer, ForeignKey("project_folders.id"))
    
    # Metadata
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project")
    parent_folder = relationship("ProjectFolder", remote_side=[id])
    subfolders = relationship("ProjectFolder", backref="parent")

class FileShare(Base):
    """File Sharing - Share files with team members"""
    __tablename__ = "file_shares"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("project_files.id"), nullable=False)
    shared_with_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shared_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Permissions
    can_view = Column(Boolean, default=True)
    can_download = Column(Boolean, default=True)
    can_edit = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    
    # Expiry
    expires_at = Column(DateTime(timezone=True))
    
    # Metadata
    shared_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    file = relationship("ProjectFile")
    shared_with_user = relationship("User", foreign_keys=[shared_with_user_id])
    shared_by_user = relationship("User", foreign_keys=[shared_by_user_id])
