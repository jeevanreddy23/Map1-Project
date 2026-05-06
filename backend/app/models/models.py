from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base, relationship
import uuid
import datetime

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    client = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    features = relationship('Feature', back_populates='project')

class Feature(Base):
    __tablename__ = 'features'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'))
    feature_type = Column(String, nullable=False) # borehole, dcp, test_pit, boundary
    label = Column(String)
    geom = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
    properties = Column(JSONB, default={})
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    project = relationship('Project', back_populates='features')