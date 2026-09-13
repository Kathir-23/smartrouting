from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base

class Report(Base):
    """Report model - represents reports table"""
    
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), 
                    nullable=False, index=True)
    incident_id = Column(UUID(as_uuid=True), ForeignKey('incidents.id'), 
                        nullable=False, index=True)
    
    # Report details
    report_type = Column(String(50), nullable=False)
    # 'verification', 'false_positive', 'additional_info'
    description = Column(Text, nullable=True)
    photo_url = Column(Text, nullable=True)
    
    # Quality metrics
    is_helpful = Column(Boolean, nullable=True)
    helpfulness_score = Column(Integer, nullable=True)  # 0-5 stars
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Report {self.report_type}>"
