from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

class FeatureCreate(BaseModel):
    project_id: uuid.UUID
    feature_type: str = Field(..., description="borehole, dcp, test_pit, boundary")
    label: Optional[str] = None
    geom: Dict[str, Any] = Field(..., description="GeoJSON Geometry object")
    properties: Dict[str, Any] = Field(default_factory=dict)
    created_by: Optional[str] = None

class FeatureResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    feature_type: str
    label: Optional[str]
    properties: Dict[str, Any]
    created_at: datetime
    
    class Config:
        orm_mode = True