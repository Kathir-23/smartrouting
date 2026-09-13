from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, \
    ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base

class Incident(Base):
    """Incident model - represents incidents table"""
    
    __tablename__ = "incidents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_type = Column(String(50), nullable=False, index=True)
    # 'accident', 'fire', 'medical', 'traffic_jam', 'flood', 'blockade'
    severity = Column(String(50), default='medium', nullable=False)
    # 'low', 'medium', 'high', 'critical'
    district = Column(String(100), nullable=False, index=True)
    
    # Location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_description = Column(String(255), nullable=True)
    
    # Data source
    source = Column(String(50), nullable=False)
    # 'mock', 'crowd', 'social_media', 'government_api', 'dispatch_center'
    source_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), 
                           nullable=True)
    
    # Verification
    verification_count = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False, index=True)
    is_false_positive = Column(Boolean, default=False)
    
    # Status
    status = Column(String(50), default='active', nullable=False, index=True)
    # 'active', 'resolved', 'false_positive'
    assigned_vehicle_id = Column(UUID(as_uuid=True), ForeignKey('vehicles.id'), 
                                nullable=True)
    
    # Impact on routing
    affects_roads = Column(ARRAY(String()), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                       onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Incident {self.incident_type} ({self.severity})>"
