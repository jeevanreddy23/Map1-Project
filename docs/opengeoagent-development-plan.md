# OpenGeoAgent Development Plan

OpenGeoAgent is Map1's geospatial specialist path. It replaces the previous generic multi-agent prototype with a focused spatial reasoning role for site investigation mapping.

This plan is inspired by the OpenGeoAI/GeoAgent direction: geospatial agents with mapping, GeoJSON, and spatial analysis tool awareness. Map1 keeps the production stack simple while using the OpenGeoAgent pattern to guide coordinate-heavy implementation.

## Specialist Role

OpenGeoAgent acts as the geospatial reviewer and implementation guide for:

- coordinate reference systems
- site plan calibration
- pixel-to-coordinate transforms
- GeoJSON structure
- PostGIS schema design
- CSV coordinate import validation
- borehole, DCP, test pit, sample point, boundary, access path, and exclusion zone geometry rules
- Australian WGS84 now and MGA/GDA2020 later

## Map1 Responsibilities

### Coordinate Discipline

- Store MVP GeoJSON in WGS84 longitude/latitude.
- Preserve manual easting/northing and MGA zone fields.
- Never treat site-plan pixels as real-world coordinates without calibration metadata.
- Track coordinate source: map click, CSV import, manual entry, overlay calibration, or detected-from-plan.

### Site Plan Calibration

Supported calibration modes:

- one anchor plus known scale and rotation
- two anchors for a similarity transform
- three or more anchors for an affine transform
- four or more anchors for best-fit transform and residual reporting

One anchor alone is not enough to calculate scale and rotation.

### Transform Logic

Affine transform:

```text
X_geo = A * x_pixel + B * y_pixel + C
Y_geo = D * x_pixel + E * y_pixel + F
```

Similarity transform from two anchors:

- calculate pixel vector
- calculate coordinate vector
- derive uniform scale
- derive rotation
- derive translation

Every transform response should include:

- method
- coefficients
- coordinate system
- residual error where available
- confidence level
- calibration point count

### API Guidance

OpenGeoAgent should review or generate specs for:

- `POST /api/calibrations`
- `POST /api/transform/pixel-to-coordinate`
- `POST /api/transform/coordinate-to-pixel`
- `POST /api/overlays`
- `GET /api/projects/{project_id}/geojson`
- `POST /api/projects/{project_id}/imports/csv`
- `GET /api/projects/{project_id}/exports/csv`

### QA Checks

- GeoJSON exports are valid `FeatureCollection` objects.
- Borehole, DCP, test pit, and sample points have practical geotechnical metadata.
- CSV imports preserve blank easting/northing/zone fields.
- Two-point transform produces expected midpoint coordinates.
- Affine calibration refuses underdetermined inputs.
- Site-plan overlay features report calibration confidence.
- Mobile field marker placement remains one-tap and readable.

## Development Sequence

1. Implement transform service with unit tests.
2. Add calibration model and database tables.
3. Add overlay upload metadata.
4. Add frontend calibration anchor capture.
5. Add residual error reporting.
6. Add MGA/GDA2020 conversion through a dedicated CRS library.
7. Add AutoSoil Logger report linking and export bundles.

