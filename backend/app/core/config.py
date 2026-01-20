"""
Application Configuration Settings
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional, Union
import json

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "CEDOS"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://cedos_user:cedos_pass@localhost/cedos_db"
    # Can be overridden by environment variable
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS - Can be JSON array or comma-separated string
    # Default to allowing all origins for production (mobile/web access)
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from env variable"""
        if isinstance(v, str):
            # Try JSON first
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            
            # Fall back to comma-separated
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v if isinstance(v, list) else []
    
    # AI Configuration
    OPENAI_API_KEY: Optional[str] = None
    AI_ENABLED: bool = True
    AI_MAX_TOKENS: int = 1000
    
    # Engineering Codes
    DEFAULT_COUNTRY_CODE: str = "IN"  # India
    SUPPORTED_CODES: List[str] = ["IS", "IRC", "NBC", "PWD"]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
