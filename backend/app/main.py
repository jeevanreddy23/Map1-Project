import csv
import io
import math
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .models import CalibrationRequest, FeatureCollection, GeoJsonFeature, Project, TransformRequest

app = FastAPI(title="Map1 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

projects: dict[str, Project] = {}
calibrations: dict[str, dict] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "map1-api"}


@app.get("/api/projects", response_model=list[Project])
def list_projects() -> list[Project]:
    return list(projects.values())


@app.post("/api/projects", response_model=Project)
def create_project(project: Project) -> Project:
    projects[project.id] = project
    return project


@app.get("/api/projects/{project_id}", response_model=Project)
def get_project(project_id: str) -> Project:
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id]


@app.put("/api/projects/{project_id}", response_model=Project)
def save_project(project_id: str, project: Project) -> Project:
    if project.id != project_id:
        project = project.model_copy(update={"id": project_id})
    projects[project_id] = project
    return project


@app.get("/api/projects/{project_id}/geojson", response_model=FeatureCollection)
def get_geojson(project_id: str) -> FeatureCollection:
    return get_project(project_id).geojson


@app.post("/api/projects/{project_id}/features", response_model=GeoJsonFeature)
def create_feature(project_id: str, feature: GeoJsonFeature) -> GeoJsonFeature:
    project = get_project(project_id)
    feature.properties.setdefault("id", str(uuid4()))
    project.geojson.features.append(feature)
    return feature


@app.put("/api/projects/{project_id}/features/{feature_id}", response_model=GeoJsonFeature)
def update_feature(project_id: str, feature_id: str, feature: GeoJsonFeature) -> GeoJsonFeature:
    project = get_project(project_id)
    for index, existing in enumerate(project.geojson.features):
      if existing.properties.get("id") == feature_id:
          project.geojson.features[index] = feature
          return feature
    raise HTTPException(status_code=404, detail="Feature not found")


@app.delete("/api/projects/{project_id}/features/{feature_id}")
def delete_feature(project_id: str, feature_id: str) -> dict[str, str]:
    project = get_project(project_id)
    before = len(project.geojson.features)
    project.geojson.features = [feature for feature in project.geojson.features if feature.properties.get("id") != feature_id]
    if len(project.geojson.features) == before:
        raise HTTPException(status_code=404, detail="Feature not found")
    return {"status": "deleted"}


@app.post("/api/projects/{project_id}/imports/csv", response_model=FeatureCollection)
async def import_csv(project_id: str, file: UploadFile = File(...)) -> FeatureCollection:
    project = get_project(project_id)
    text = (await file.read()).decode("utf-8-sig")
    rows = csv.DictReader(io.StringIO(text))
    for row in rows:
        lat = _to_float(row.get("latitude"))
        lng = _to_float(row.get("longitude"))
        if lat is None or lng is None:
            continue
        feature_type = row.get("type") or "borehole"
        label = row.get("id") or _next_label(project.geojson.features, feature_type)
        feature = GeoJsonFeature(
            geometry={"type": "Point", "coordinates": [lng, lat]},
            properties={
                "id": str(uuid4()),
                "feature_type": feature_type,
                "label": label,
                "borehole_id": label if feature_type == "borehole" else None,
                "latitude": lat,
                "longitude": lng,
                "easting": row.get("easting") or None,
                "northing": row.get("northing") or None,
                "mga_zone": row.get("zone") or None,
                "surface_rl": row.get("surface_rl") or None,
                "total_depth": row.get("total_depth") or None,
                "start_date": row.get("start_date") or None,
                "end_date": row.get("end_date") or None,
                "drilling_method": row.get("method") or None,
                "logged_by": row.get("logged_by") or None,
                "water_level": row.get("water_level") or None,
                "remarks": row.get("remarks") or None,
                "linked_log_pdf": row.get("linked_log_pdf") or None,
                "coordinate_system": "WGS84",
                "source": "csv_import",
            },
        )
        project.geojson.features.append(feature)
    return project.geojson


@app.get("/api/projects/{project_id}/exports/csv")
def export_csv(project_id: str) -> StreamingResponse:
    project = get_project(project_id)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["type", "id", "latitude", "longitude", "easting", "northing", "zone", "surface_rl", "total_depth", "start_date", "end_date", "method", "logged_by", "water_level", "remarks", "linked_log_pdf"])
    for feature in project.geojson.features:
        props = feature.properties
        writer.writerow([
            props.get("feature_type"),
            props.get("borehole_id") or props.get("dcp_id") or props.get("test_pit_id") or props.get("sample_id") or props.get("label"),
            props.get("latitude"),
            props.get("longitude"),
            props.get("easting"),
            props.get("northing"),
            props.get("mga_zone"),
            props.get("surface_rl"),
            props.get("total_depth") or props.get("test_depth") or props.get("depth"),
            props.get("start_date"),
            props.get("end_date"),
            props.get("drilling_method") or props.get("excavation_method"),
            props.get("logged_by"),
            props.get("water_level"),
            props.get("remarks") or props.get("notes"),
            props.get("linked_log_pdf") or props.get("linked_report"),
        ])
    buffer.seek(0)
    return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=map1-export.csv"})


@app.post("/api/calibrations")
def create_calibration(request: CalibrationRequest) -> dict:
    calibration_id = str(uuid4())
    method = "unreferenced"
    confidence = "low"
    coefficients = None
    message = "Provide at least two anchors, or one anchor plus scale and rotation."

    if len(request.points) >= 3:
        method = "affine_pending_solver"
        confidence = "medium"
        message = "Three or more anchors supplied. Add least-squares affine solver in Phase 3."
    elif len(request.points) == 2:
        method = "two_point_similarity"
        confidence = "medium"
        coefficients = _two_point_similarity(request)
        message = "Similarity transform created from two anchors."
    elif len(request.points) == 1 and request.scale is not None and request.rotation_degrees is not None:
        method = "one_point_scale_rotation"
        confidence = "medium"
        message = "One anchor plus scale and rotation supplied."

    calibration = {
        "id": calibration_id,
        "overlay_id": request.overlay_id,
        "coordinate_system": request.coordinate_system,
        "method": method,
        "confidence": confidence,
        "coefficients": coefficients,
        "residual_error": None,
        "message": message,
    }
    calibrations[calibration_id] = calibration
    return calibration


@app.post("/api/transform/pixel-to-coordinate")
def pixel_to_coordinate(request: TransformRequest) -> dict:
    coefficients = request.coefficients
    if request.calibration_id:
        calibration = calibrations.get(request.calibration_id)
        if not calibration:
            raise HTTPException(status_code=404, detail="Calibration not found")
        coefficients = calibration.get("coefficients")
    if not coefficients:
        raise HTTPException(status_code=400, detail="No transform coefficients available")
    x_geo = coefficients["a"] * request.pixel_x + coefficients["b"] * request.pixel_y + coefficients["c"]
    y_geo = coefficients["d"] * request.pixel_x + coefficients["e"] * request.pixel_y + coefficients["f"]
    return {"x_geo": x_geo, "y_geo": y_geo, "longitude": x_geo, "latitude": y_geo}


def _to_float(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except ValueError:
        return None


def _next_label(features: list[GeoJsonFeature], feature_type: str) -> str:
    prefixes = {"borehole": "BH", "dcp": "DCP", "test_pit": "TP", "sample_point": "SP"}
    prefix = prefixes.get(feature_type, "F")
    count = len([feature for feature in features if feature.properties.get("feature_type") == feature_type]) + 1
    return f"{prefix}{count:02d}"


def _two_point_similarity(request: CalibrationRequest) -> dict[str, float] | None:
    p1, p2 = request.points[:2]
    if None in (p1.longitude, p1.latitude, p2.longitude, p2.latitude):
        return None
    dx_pixel = p2.pixel_x - p1.pixel_x
    dy_pixel = p2.pixel_y - p1.pixel_y
    dx_geo = p2.longitude - p1.longitude
    dy_geo = p2.latitude - p1.latitude
    pixel_distance = math.hypot(dx_pixel, dy_pixel)
    geo_distance = math.hypot(dx_geo, dy_geo)
    if pixel_distance == 0:
        return None
    scale = geo_distance / pixel_distance
    pixel_angle = math.atan2(dy_pixel, dx_pixel)
    geo_angle = math.atan2(dy_geo, dx_geo)
    theta = geo_angle - pixel_angle
    a = scale * math.cos(theta)
    b = -scale * math.sin(theta)
    d = scale * math.sin(theta)
    e = scale * math.cos(theta)
    c = p1.longitude - a * p1.pixel_x - b * p1.pixel_y
    f = p1.latitude - d * p1.pixel_x - e * p1.pixel_y
    return {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f}

