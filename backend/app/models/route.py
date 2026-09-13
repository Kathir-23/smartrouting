from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base

class Route(Base):
    """Route model - represents routes table"""
    
    __tablename__ = "routes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey('vehicles.id'), 
                       nullable=False, index=True)
    incident_id = Column(UUID(as_uuid=True), ForeignKey('incidents.id'), 
                        nullable=False, index=True)
    
    # Route information
    polyline = Column(Text, nullable=False)
    # Encoded polyline (can be decoded by frontend with polyline library)
    distance_km = Column(Float, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    eta = Column(DateTime, nullable=True)
    
    # Optimization metrics
    avoided_incidents = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    traffic_factor = Column(Float, default=1.0)
    # 1.0 = normal, >1.0 = congestion
    
    # Status
    status = Column(String(50), default='pending', nullable=False, index=True)
    # 'pending', 'active', 'completed', 'cancelled'
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Performance tracking
    actual_distance_km = Column(Float, nullable=True)
    actual_duration_seconds = Column(Integer, nullable=True)
    response_time_seconds = Column(Integer, nullable=True)
    # Time from incident creation to vehicle dispatch
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                       onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Route {self.status} ({self.distance_km}km)>"
