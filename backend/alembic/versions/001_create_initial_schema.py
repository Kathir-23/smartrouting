"""Create initial schema with 5 tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# This is required by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create tables"""
    
    # ===== TABLE 1: USERS =====
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.VARCHAR(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.VARCHAR(255), nullable=False),
        sa.Column('role', sa.VARCHAR(50), nullable=False),  
        # role values: 'admin', 'dispatch', 'driver', 'crowd_reporter'
        sa.Column('district', sa.VARCHAR(100), nullable=False),
        sa.Column('organization', sa.VARCHAR(255), nullable=True),
        sa.Column('phone', sa.VARCHAR(20), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), 
                  onupdate=sa.func.now()),
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_role', 'users', ['role'])
    op.create_index('idx_users_district', 'users', ['district'])
    
    # ===== TABLE 2: VEHICLES =====
    op.create_table(
        'vehicles',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  primary_key=True, default=uuid.uuid4),
        sa.Column('registration_number', sa.VARCHAR(50), unique=True, 
                  nullable=False),  # 'TN-01-AB-1234'
        sa.Column('driver_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('users.id'), nullable=True),
        sa.Column('vehicle_type', sa.VARCHAR(50), nullable=False),
        # 'ambulance', 'fire_truck', 'police_car'
        sa.Column('district', sa.VARCHAR(100), nullable=False),
        sa.Column('organization_id', sa.VARCHAR(255), nullable=True),
        
        # Real-time location
        sa.Column('current_latitude', sa.DECIMAL(10, 8), nullable=True),
        sa.Column('current_longitude', sa.DECIMAL(11, 8), nullable=True),
        sa.Column('heading', sa.DECIMAL(4, 1), nullable=True),  # 0-360 degrees
        sa.Column('speed_kmh', sa.Integer(), nullable=True),
        
        # Status
        sa.Column('status', sa.VARCHAR(50), default='idle', nullable=False),
        # 'idle', 'en_route', 'at_incident', 'returning'
        sa.Column('available', sa.Boolean(), default=True),
        sa.Column('current_incident_id', postgresql.UUID(as_uuid=True), 
                  nullable=True),  # Will add FK after incidents table created
        
        # GPS tracking
        sa.Column('last_location_update', sa.DateTime(), 
                  default=sa.func.now()),
        sa.Column('last_update_source', sa.VARCHAR(50), nullable=True),
        # 'gps', 'manual', 'dispatch_app'
        
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), 
                  onupdate=sa.func.now()),
    )
    op.create_index('idx_vehicles_district', 'vehicles', ['district'])
    op.create_index('idx_vehicles_status', 'vehicles', ['status'])
    op.create_index('idx_vehicles_available', 'vehicles', ['available'])
    op.create_index('idx_vehicles_registration', 'vehicles', 
                   ['registration_number'])
    
    # ===== TABLE 3: INCIDENTS =====
    op.create_table(
        'incidents',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  primary_key=True, default=uuid.uuid4),
        sa.Column('incident_type', sa.VARCHAR(50), nullable=False),
        # 'accident', 'fire', 'medical', 'traffic_jam', 'flood', 'blockade'
        sa.Column('severity', sa.VARCHAR(50), default='medium', nullable=False),
        # 'low', 'medium', 'high', 'critical'
        sa.Column('district', sa.VARCHAR(100), nullable=False),
        
        # Location
        sa.Column('latitude', sa.DECIMAL(10, 8), nullable=False),
        sa.Column('longitude', sa.DECIMAL(11, 8), nullable=False),
        sa.Column('location_description', sa.VARCHAR(255), nullable=True),
        
        # Data source
        sa.Column('source', sa.VARCHAR(50), nullable=False),
        # 'mock', 'crowd', 'social_media', 'government_api', 'dispatch_center'
        sa.Column('source_user_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('users.id'), nullable=True),
        
        # Verification
        sa.Column('verification_count', sa.Integer(), default=0),
        sa.Column('is_verified', sa.Boolean(), default=False),
        sa.Column('is_false_positive', sa.Boolean(), default=False),
        
        # Status
        sa.Column('status', sa.VARCHAR(50), default='active', nullable=False),
        # 'active', 'resolved', 'false_positive'
        sa.Column('assigned_vehicle_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('vehicles.id'), nullable=True),
        
        # Impact on routing
        sa.Column('affects_roads', postgresql.ARRAY(sa.String()), 
                  nullable=True),
        
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), 
                  onupdate=sa.func.now()),
    )
    op.create_index('idx_incidents_district', 'incidents', ['district'])
    op.create_index('idx_incidents_status', 'incidents', ['status'])
    op.create_index('idx_incidents_type', 'incidents', ['incident_type'])
    op.create_index('idx_incidents_verified', 'incidents', ['is_verified'])
    
    # ===== TABLE 4: ROUTES =====
    op.create_table(
        'routes',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  primary_key=True, default=uuid.uuid4),
        sa.Column('vehicle_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('vehicles.id'), nullable=False),
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('incidents.id'), nullable=False),
        
        # Route information
        sa.Column('polyline', sa.Text(), nullable=False),
        # Encoded polyline (can be decoded by frontend with polyline library)
        sa.Column('distance_km', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('eta', sa.DateTime(), nullable=True),
        
        # Optimization metrics
        sa.Column('avoided_incidents', postgresql.ARRAY(
            postgresql.UUID(as_uuid=True)), nullable=True),
        sa.Column('traffic_factor', sa.DECIMAL(3, 2), default=1.0),
        # 1.0 = normal, >1.0 = congestion
        
        # Status
        sa.Column('status', sa.VARCHAR(50), default='pending', nullable=False),
        # 'pending', 'active', 'completed', 'cancelled'
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        
        # Performance tracking
        sa.Column('actual_distance_km', sa.DECIMAL(10, 2), nullable=True),
        sa.Column('actual_duration_seconds', sa.Integer(), nullable=True),
        sa.Column('response_time_seconds', sa.Integer(), nullable=True),
        # Time from incident creation to dispatch
        
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), default=sa.func.now(), 
                  onupdate=sa.func.now()),
    )
    op.create_index('idx_routes_vehicle_id', 'routes', ['vehicle_id'])
    op.create_index('idx_routes_incident_id', 'routes', ['incident_id'])
    op.create_index('idx_routes_status', 'routes', ['status'])
    
    # ===== TABLE 5: REPORTS =====
    op.create_table(
        'reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), 
                  primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), 
                  sa.ForeignKey('incidents.id'), nullable=False),
        
        # Report details
        sa.Column('report_type', sa.VARCHAR(50), nullable=False),
        # 'verification', 'false_positive', 'additional_info'
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('photo_url', sa.Text(), nullable=True),
        
        # Quality metrics
        sa.Column('is_helpful', sa.Boolean(), nullable=True),
        sa.Column('helpfulness_score', sa.Integer(), nullable=True),  # 0-5 stars
        
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
    )
    op.create_index('idx_reports_user_id', 'reports', ['user_id'])
    op.create_index('idx_reports_incident_id', 'reports', ['incident_id'])
    
    # ===== ADD FOREIGN KEY from vehicles to incidents =====
    # (We deferred this to avoid circular reference)
    op.create_foreign_key(
        'fk_vehicles_incident',
        'vehicles', 'incidents',
        ['current_incident_id'], ['id']
    )


def downgrade():
    """Drop all tables (for rollback)"""
    
    # Drop in reverse order (respecting foreign keys)
    op.drop_table('reports')
    op.drop_table('routes')
    op.drop_table('incidents')
    op.drop_table('vehicles')
    op.drop_table('users')
