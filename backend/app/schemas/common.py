"""
Common schemas used across all endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar
from datetime import datetime

# ===== GENERIC RESPONSE WRAPPER =====
T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response format"""
    success: bool = True
    data: T
    message: str = "Success"

class ErrorResponse(BaseModel):
    """Standard error response format"""
    success: bool = False
    error: str
    detail: Optional[str] = None

# ===== PAGINATION =====
class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints"""
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(10, ge=1, le=100, description="Number of items to return")
    district: Optional[str] = Field(None, description="Filter by district")

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response"""
    items: list[T]
    total: int
    skip: int
    limit: int
    has_more: bool

# ===== TIMESTAMPS =====
class TimestampMixin(BaseModel):
    """Base model with created_at and updated_at"""
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ===== ID RESPONSE =====
class IDResponse(BaseModel):
    """Response containing just an ID"""
    id: str

# ===== MESSAGE RESPONSE =====
class MessageResponse(BaseModel):
    """Simple message response"""
    message: str
