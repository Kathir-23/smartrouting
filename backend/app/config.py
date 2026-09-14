"""
Application configuration

Loads settings from environment variables
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # App settings
    APP_NAME: str = "Smart Emergency Routing"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    ENV: str = os.getenv("ENV", "development")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password123@localhost:5432/smartrouting"
    )
    
    # JWT/Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "jwt-secret-key-change-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "1"))
    JWT_REFRESH_EXPIRATION_DAYS: int = int(os.getenv("JWT_REFRESH_EXPIRATION_DAYS", "7"))
    
    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # External APIs
    GOVERNMENT_API_KEY: str = ""
    TWITTER_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    """
    Get settings (cached)
    
    Returns: Settings instance
    """
    return Settings()

# Create settings instance
settings = get_settings()
