from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.models import Feature, Project
from app.schemas.schemas import FeatureCreate, FeatureResponse
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FeatureResponse)
def create_feature(feature: FeatureCreate, db: Session = Depends(get_db)):
    # Convert dict geom to GeoJSON string for PostGIS
    geom_str = json.dumps(feature.geom)
    
    # ST_GeomFromGeoJSON takes a GeoJSON string
    from sqlalchemy import func
    
    db_feature = Feature(
        project_id=feature.project_id,
        feature_type=feature.feature_type,
        label=feature.label,
        geom=func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom_str), 4326),
        properties=feature.properties,
        created_by=feature.created_by
    )
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature

@router.get("/project/{project_id}")
def get_features(project_id: str, db: Session = Depends(get_db)):
    from sqlalchemy import func
    # We return raw GeoJSON features
    features = db.query(
        Feature.id,
        Feature.feature_type,
        Feature.label,
        Feature.properties,
        func.ST_AsGeoJSON(Feature.geom).label('geom')
    ).filter(Feature.project_id == project_id).all()
    
    feature_collection = {
        "type": "FeatureCollection",
        "features": []
    }
    for f in features:
        feature_collection["features"].append({
            "type": "Feature",
            "id": str(f.id),
            "geometry": json.loads(f.geom),
            "properties": {
                "feature_type": f.feature_type,
                "label": f.label,
                **f.properties
            }
        })
    return feature_collection