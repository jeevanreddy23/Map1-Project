"""
Agent 5 - Export Agent: FastAPI export routes
CSV and GeoJSON server-side export endpoints
"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.db import SessionLocal
from app.models.models import Feature
import json, csv, io

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_project_geojson(project_id: str, db: Session):
    rows = db.query(
        Feature.id,
        Feature.feature_type,
        Feature.label,
        Feature.properties,
        func.ST_AsGeoJSON(Feature.geom).label('geom')
    ).filter(Feature.project_id == project_id).all()

    features = []
    for f in rows:
        geom = json.loads(f.geom) if f.geom else None
        features.append({
            "type": "Feature",
            "id": str(f.id),
            "geometry": geom,
            "properties": {
                "feature_type": f.feature_type,
                "label": f.label,
                **(f.properties or {})
            }
        })
    return {"type": "FeatureCollection", "features": features}

@router.get("/projects/{project_id}/export/geojson")
def export_geojson(project_id: str, db: Session = Depends(get_db)):
    collection = get_project_geojson(project_id, db)
    content = json.dumps(collection, indent=2)
    return StreamingResponse(
        io.StringIO(content),
        media_type="application/geo+json",
        headers={"Content-Disposition": f"attachment; filename=map1_{project_id}.geojson"}
    )

@router.get("/projects/{project_id}/export/csv")
def export_csv(project_id: str, db: Session = Depends(get_db)):
    collection = get_project_geojson(project_id, db)
    
    headers = [
        'label', 'type', 'latitude', 'longitude',
        'surface_rl', 'total_depth', 'drilling_method', 'water_level',
        'start_date', 'end_date', 'logged_by',
        'test_depth', 'refusal_depth', 'blows_per_100mm', 'pit_depth', 'remarks'
    ]
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    
    for f in collection["features"]:
        if f["geometry"] and f["geometry"]["type"] == "Point":
            lng, lat = f["geometry"]["coordinates"]
            p = f["properties"]
            writer.writerow({
                "label": p.get("label", ""),
                "type": p.get("feature_type", ""),
                "latitude": round(lat, 6),
                "longitude": round(lng, 6),
                "surface_rl": p.get("surface_rl", ""),
                "total_depth": p.get("total_depth", ""),
                "drilling_method": p.get("drilling_method", ""),
                "water_level": p.get("water_level", ""),
                "start_date": p.get("start_date", ""),
                "end_date": p.get("end_date", ""),
                "logged_by": p.get("logged_by", ""),
                "test_depth": p.get("test_depth", ""),
                "refusal_depth": p.get("refusal_depth", ""),
                "blows_per_100mm": p.get("blows_per_100mm", ""),
                "pit_depth": p.get("pit_depth", ""),
                "remarks": p.get("remarks", ""),
            })
    
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=map1_{project_id}.csv"}
    )