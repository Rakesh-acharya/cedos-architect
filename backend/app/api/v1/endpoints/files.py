"""
File Management Endpoints - Organized project file storage
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import os
import shutil
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.file_management import ProjectFile, ProjectFolder, FileShare, FileCategory, FileType
from app.services.audit_logger import AuditLogger
from app.models.audit import ActionType

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def get_file_type(mime_type: str, file_name: str) -> FileType:
    """Determine file type from mime type and extension"""
    if mime_type.startswith("image/"):
        return FileType.IMAGE
    elif mime_type == "application/pdf":
        return FileType.PDF
    elif mime_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return FileType.DOCUMENT
    elif mime_type in ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        return FileType.SPREADSHEET
    elif mime_type in ["video/mp4", "video/avi"]:
        return FileType.VIDEO
    elif file_name.endswith((".dwg", ".dxf")):
        return FileType.CAD
    elif mime_type in ["application/zip", "application/x-rar-compressed"]:
        return FileType.ARCHIVE
    else:
        return FileType.OTHER

@router.post("/upload/{project_id}", status_code=status.HTTP_201_CREATED)
async def upload_file(
    project_id: int,
    file: UploadFile = File(...),
    category: FileCategory = Form(...),
    folder_path: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload file to project workspace"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create project-specific directory
    project_dir = UPLOAD_DIR / f"project_{project_id}"
    project_dir.mkdir(exist_ok=True)
    
    # Create category subdirectory
    category_dir = project_dir / category.value
    category_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = category_dir / unique_filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = file_path.stat().st_size
    
    # Determine file type
    file_type = get_file_type(file.content_type or "", file.filename)
    
    # Create database record
    db_file = ProjectFile(
        project_id=project_id,
        file_name=unique_filename,
        original_file_name=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        mime_type=file.content_type or "application/octet-stream",
        file_type=file_type,
        file_category=category,
        folder_path=folder_path or f"{category.value}/",
        description=description,
        tags=tags,
        uploaded_by=current_user.id
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    # Log action
    audit_logger = AuditLogger(db)
    audit_logger.log_action(
        user_id=current_user.id,
        action_type=ActionType.CREATE,
        entity_type="ProjectFile",
        entity_id=db_file.id,
        entity_code=db_file.file_name,
        action_description=f"File uploaded: {file.filename}",
        ip_address=None
    )
    
    return {
        "id": db_file.id,
        "file_name": file.filename,
        "file_size": file_size,
        "category": category.value,
        "uploaded_at": db_file.uploaded_at.isoformat()
    }

@router.get("/project/{project_id}")
def list_project_files(
    project_id: int,
    category: Optional[FileCategory] = None,
    folder_path: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List files in project workspace"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    query = db.query(ProjectFile).filter(ProjectFile.project_id == project_id)
    
    if category:
        query = query.filter(ProjectFile.file_category == category)
    
    if folder_path:
        query = query.filter(ProjectFile.folder_path.like(f"{folder_path}%"))
    
    if search:
        query = query.filter(
            (ProjectFile.original_file_name.ilike(f"%{search}%")) |
            (ProjectFile.description.ilike(f"%{search}%")) |
            (ProjectFile.tags.ilike(f"%{search}%"))
        )
    
    files = query.filter(ProjectFile.is_latest == True).offset(skip).limit(limit).all()
    
    return [
        {
            "id": f.id,
            "file_name": f.original_file_name,
            "file_size": f.file_size,
            "category": f.file_category.value,
            "folder_path": f.folder_path,
            "description": f.description,
            "tags": f.tags,
            "uploaded_by": f.uploaded_by_user.full_name if f.uploaded_by_user else "Unknown",
            "uploaded_at": f.uploaded_at.isoformat(),
            "mime_type": f.mime_type
        }
        for f in files
    ]

@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download file from project workspace"""
    file_record = db.query(ProjectFile).filter(ProjectFile.id == file_id).first()
    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check access
    if not file_record.is_public and file_record.uploaded_by != current_user.id:
        # Check if shared
        share = db.query(FileShare).filter(
            FileShare.file_id == file_id,
            FileShare.shared_with_user_id == current_user.id
        ).first()
        if not share or not share.can_download:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    file_path = Path(file_record.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server"
        )
    
    return FileResponse(
        path=file_path,
        filename=file_record.original_file_name,
        media_type=file_record.mime_type
    )

@router.post("/folder/{project_id}", status_code=status.HTTP_201_CREATED)
def create_folder(
    project_id: int,
    folder_name: str,
    parent_folder_id: Optional[int] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create folder in project workspace"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Build folder path
    if parent_folder_id:
        parent = db.query(ProjectFolder).filter(ProjectFolder.id == parent_folder_id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent folder not found"
            )
        folder_path = f"{parent.folder_path}/{folder_name}"
    else:
        folder_path = folder_name
    
    db_folder = ProjectFolder(
        project_id=project_id,
        folder_name=folder_name,
        folder_path=folder_path,
        parent_folder_id=parent_folder_id,
        description=description,
        created_by=current_user.id
    )
    
    db.add(db_folder)
    db.commit()
    db.refresh(db_folder)
    
    return db_folder

@router.get("/folders/{project_id}")
def list_folders(
    project_id: int,
    parent_folder_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List folders in project workspace"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    query = db.query(ProjectFolder).filter(ProjectFolder.project_id == project_id)
    
    if parent_folder_id:
        query = query.filter(ProjectFolder.parent_folder_id == parent_folder_id)
    else:
        query = query.filter(ProjectFolder.parent_folder_id == None)
    
    folders = query.all()
    
    return [
        {
            "id": f.id,
            "folder_name": f.folder_name,
            "folder_path": f.folder_path,
            "description": f.description,
            "created_at": f.created_at.isoformat()
        }
        for f in folders
    ]

@router.get("/workspace/{project_id}")
def get_project_workspace(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get complete project workspace structure"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get all folders
    folders = db.query(ProjectFolder).filter(ProjectFolder.project_id == project_id).all()
    
    # Get all files grouped by category
    files = db.query(ProjectFile).filter(
        ProjectFile.project_id == project_id,
        ProjectFile.is_latest == True
    ).all()
    
    # Organize by category
    workspace = {
        "project_id": project_id,
        "project_name": project.project_name,
        "folders": [
            {
                "id": f.id,
                "name": f.folder_name,
                "path": f.folder_path,
                "description": f.description
            }
            for f in folders
        ],
        "files_by_category": {}
    }
    
    for category in FileCategory:
        category_files = [f for f in files if f.file_category == category]
        workspace["files_by_category"][category.value] = [
            {
                "id": f.id,
                "name": f.original_file_name,
                "size": f.file_size,
                "uploaded_at": f.uploaded_at.isoformat(),
                "folder": f.folder_path
            }
            for f in category_files
        ]
    
    # Statistics
    workspace["statistics"] = {
        "total_files": len(files),
        "total_size": sum(f.file_size for f in files),
        "files_by_category": {cat.value: len([f for f in files if f.file_category == cat]) for cat in FileCategory}
    }
    
    return workspace

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete file from project workspace"""
    file_record = db.query(ProjectFile).filter(ProjectFile.id == file_id).first()
    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check permissions
    if file_record.uploaded_by != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    
    # Delete physical file
    file_path = Path(file_record.file_path)
    if file_path.exists():
        file_path.unlink()
    
    # Delete database record
    db.delete(file_record)
    db.commit()
    
    return {"message": "File deleted successfully"}

@router.post("/share/{file_id}")
def share_file(
    file_id: int,
    user_id: int,
    can_view: bool = True,
    can_download: bool = True,
    can_edit: bool = False,
    expires_at: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Share file with another user"""
    file_record = db.query(ProjectFile).filter(ProjectFile.id == file_id).first()
    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    # Check if already shared
    existing_share = db.query(FileShare).filter(
        FileShare.file_id == file_id,
        FileShare.shared_with_user_id == user_id
    ).first()
    
    if existing_share:
        # Update existing share
        existing_share.can_view = can_view
        existing_share.can_download = can_download
        existing_share.can_edit = can_edit
        existing_share.expires_at = expires_at
    else:
        # Create new share
        share = FileShare(
            file_id=file_id,
            shared_with_user_id=user_id,
            shared_by_user_id=current_user.id,
            can_view=can_view,
            can_download=can_download,
            can_edit=can_edit,
            expires_at=expires_at
        )
        db.add(share)
    
    db.commit()
    
    return {"message": "File shared successfully"}
