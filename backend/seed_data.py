"""
Seed database with mock data for testing

Usage:
    python seed_data.py
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Import models
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.incident import Incident
from app.models.route import Route
from app.models.report import Report

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL", 
    "postgresql://postgres:password123@localhost:5432/smartrouting")

# Create database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_users():
    """Create test users"""
    
    users = [
        # Admin user
        User(
            id=uuid.uuid4(),
            email="admin@smartrouting.local",
            password_hash="hashed_password",  # We'll hash this properly later
            role="admin",
            district="chengalpattu",
            is_active=True
        ),
        # Dispatcher
        User(
            id=uuid.uuid4(),
            email="dispatcher@chengalpattu.local",
            password_hash="hashed_password",
            role="dispatch",
            district="chengalpattu",
            organization="Chengalpattu Ambulance HQ",
            is_active=True
        ),
        # Drivers
        User(
            id=uuid.uuid4(),
            email="driver1@smartrouting.local",
            password_hash="hashed_password",
            role="driver",
            district="chengalpattu",
            is_active=True
        ),
        User(
            id=uuid.uuid4(),
            email="driver2@smartrouting.local",
            password_hash="hashed_password",
            role="driver",
            district="chengalpattu",
            is_active=True
        ),
        # Crowd reporters
        User(
            id=uuid.uuid4(),
            email="citizen1@smartrouting.local",
            password_hash="hashed_password",
            role="crowd_reporter",
            district="chengalpattu",
            is_active=True
        ),
    ]
    
    session.add_all(users)
    session.commit()
    print(f"✅ Created {len(users)} users")
    
    return users[1]  # Return dispatcher for vehicle creation

def create_vehicles(dispatcher_user):
    """Create mock vehicles"""
    
    import random
    
    # Chengalpattu coordinates (approximate center)
    base_lat = 12.6704
    base_lng = 79.9657
    
    vehicles = []
    for i in range(1, 11):  # Create 10 ambulances
        vehicle = Vehicle(
            id=uuid.uuid4(),
            registration_number=f"TN-01-AB-{1000 + i}",
            vehicle_type="ambulance",
            district="chengalpattu",
            # Randomize location around Chengalpattu
            current_latitude=base_lat + random.uniform(-0.05, 0.05),
            current_longitude=base_lng + random.uniform(-0.05, 0.05),
            heading=random.randint(0, 360),
            speed_kmh=0,
            status=random.choice(["idle", "idle", "idle", "en_route"]),
            available=True,
            last_update_source="manual"
        )
        vehicles.append(vehicle)
    
    session.add_all(vehicles)
    session.commit()
    print(f"✅ Created {len(vehicles)} mock vehicles")
    
    return vehicles

def create_incidents(dispatcher_user):
    """Create mock incidents"""
    
    import random
    
    # Chengalpattu coordinates
    base_lat = 12.6704
    base_lng = 79.9657
    
    incidents = []
    
    # Create variety of incidents
    incident_types = ["accident", "fire", "medical", "traffic_jam", "flood"]
    
    for i in range(1, 6):  # Create 5 incidents
        incident = Incident(
            id=uuid.uuid4(),
            incident_type=incident_types[i-1],
            severity=random.choice(["low", "medium", "high", "critical"]),
            district="chengalpattu",
            latitude=base_lat + random.uniform(-0.03, 0.03),
            longitude=base_lng + random.uniform(-0.03, 0.03),
            location_description=f"Test Location {i}",
            source="mock",  # This is seed data
            verification_count=random.randint(0, 5),
            is_verified=random.choice([True, True, False]),
            status=random.choice(["active", "active", "active", "resolved"]),
        )
        incidents.append(incident)
    
    session.add_all(incidents)
    session.commit()
    print(f"✅ Created {len(incidents)} mock incidents")
    
    return incidents

def main():
    """Run all seed functions"""
    print("\n🌱 Seeding database...\n")
    
    try:
        # Clear existing data
        session.query(Report).delete()
        session.query(Route).delete()
        session.query(Incident).delete()
        session.query(Vehicle).delete()
        session.query(User).delete()
        session.commit()
        print("🗑️  Cleared existing data\n")
        
        dispatcher = create_users()
        vehicles = create_vehicles(dispatcher)
        incidents = create_incidents(dispatcher)
        
        print("\n✅ Seeding complete!")
        print(f"   - Users created")
        print(f"   - {len(vehicles)} vehicles created")
        print(f"   - {len(incidents)} incidents created")
        print("\n🔗 Database is ready for testing!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
