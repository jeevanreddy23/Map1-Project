from typing import Any, Literal
from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: Literal["Point", "LineString", "Polygon"]
    coordinates: Any


class GeoJsonFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: dict[str, Any] = Field(default_factory=dict)


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[GeoJsonFeature] = Field(default_factory=list)


class Project(BaseModel):
    id: str
    name: str
    site_name: str | None = None
    coordinate_system: str = "WGS84"
    geojson: FeatureCollection = Field(default_factory=FeatureCollection)


class CalibrationPoint(BaseModel):
    pixel_x: float
    pixel_y: float
    longitude: float | None = None
    latitude: float | None = None
    easting: float | None = None
    northing: float | None = None
    zone: str | None = None
    description: str | None = None


class CalibrationRequest(BaseModel):
    overlay_id: str
    coordinate_system: Literal["WGS84", "MGA_GDA2020"] = "WGS84"
    points: list[CalibrationPoint]
    scale: float | None = None
    rotation_degrees: float | None = None


class TransformRequest(BaseModel):
    calibration_id: str | None = None
    pixel_x: float
    pixel_y: float
    coefficients: dict[str, float] | None = None

