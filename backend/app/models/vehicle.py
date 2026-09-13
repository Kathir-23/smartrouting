from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base

class Vehicle(Base):
    """Vehicle model - represents vehicles table"""
    
    __tablename__ = "vehicles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_number = Column(String(50), unique=True, nullable=False, 
                                 index=True)  # 'TN-01-AB-1234'
    driver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), 
                      nullable=True)
    vehicle_type = Column(String(50), nullable=False)  
    # 'ambulance', 'fire_truck', 'police_car'
    district = Column(String(100), nullable=False, index=True)
    organization_id = Column(String(255), nullable=True)
    
    # Real-time location
    current_latitude = Column(Float, nullable=True)
    current_longitude = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)  # 0-360 degrees
    speed_kmh = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(50), default='idle', nullable=False, index=True)
    # 'idle', 'en_route', 'at_incident', 'returning'
    available = Column(Boolean, default=True, index=True)
    current_incident_id = Column(UUID(as_uuid=True), ForeignKey('incidents.id'), 
                                nullable=True)
    
    # GPS tracking
    last_location_update = Column(DateTime, default=datetime.utcnow)
    last_update_source = Column(String(50), nullable=True)
    # 'gps', 'manual', 'dispatch_app'
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, 
                       onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Vehicle {self.registration_number} ({self.vehicle_type})>"
