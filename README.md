# map1

AutoSoil Logger Map1 is a focused geotechnical site investigation map module for placing, editing, importing, exporting, and storing borehole, DCP, test pit, sample point, site boundary, access path, and exclusion zone data.

The MVP is intentionally lean: React + Vite on the frontend, FastAPI on the backend, GeoJSON as the interchange format, and PostgreSQL/PostGIS as the production database target.

## Purpose

Map1 supports Australian geotechnical field workflows and AS1726-style investigation data capture. It is designed for field engineers, geotechnicians, and project managers who need a clean site map that connects spatial points to AutoSoil Logger borehole logs, DCP reports, and future GINT-style reporting integration.

## MVP Features

- OpenStreetMap base map with a professional, field-friendly interface.
- Add borehole, DCP, test pit, and sample point markers by clicking the map.
- Auto-label markers as `BH01`, `BH02`, `DCP01`, `TP01`, and `SP01`.
- Edit geotechnical metadata in a side panel.
- Draw site boundaries, access paths, and exclusion zones.
- Import boreholes from CSV.
- Export all project map data to GeoJSON.
- Export investigation points to CSV.
- Save and load project data through a FastAPI backend.
- Preserve hooks for uploaded site plans, image/PDF overlays, offline mode, MGA/GDA2020, and AutoSoil Logger report links.

## Tech Stack

- Frontend: React, Vite, React-Leaflet, Leaflet, Leaflet Draw
- Backend: FastAPI, Pydantic
- Database target: PostgreSQL/PostGIS
- Interchange: GeoJSON and CSV
- Future geospatial support: pyproj, raster overlays, image calibration, affine transforms

## Quick Start

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The frontend defaults to `http://localhost:5173` and the backend defaults to `http://localhost:8000`.

Copy `.env.example` when wiring local services. The MVP backend currently uses in-memory storage; `DATABASE_URL` is reserved for the PostGIS phase.

## MVP Roadmap

### Phase 1: Usable Field Map

- OpenStreetMap base layer.
- Marker placement modes for boreholes, DCPs, test pits, and sample points.
- Side-panel editing for AS1726-style metadata.
- GeoJSON and CSV export.
- CSV borehole import.
- In-memory FastAPI project save/load.

### Phase 2: Persistence and Drawing

- PostgreSQL/PostGIS persistence.
- Site boundary polygon storage.
- Access path line storage.
- Exclusion zone polygon storage.
- Project/site list views.
- User-controlled coordinate entry.

### Phase 3: Site Plan Overlays and Calibration

- Upload image/PDF site plans.
- Display uploaded plans as Leaflet image overlays.
- Add calibration anchors.
- Support one anchor plus scale/rotation, two-point similarity transform, and three-or-more-point affine transforms.
- Report calibration residuals and confidence.

### Phase 4: Field Mode and AutoSoil Logger Integration

- Offline project cache.
- Background sync.
- Link markers to borehole log PDFs.
- Link markers to AS1726/GINT-style structured log data.
- Export bundles for reporting workflows.

## Repository Structure

```text
map1/
  frontend/           React + Vite map client
  backend/            FastAPI API
  crewai/             Optional 3-agent prototype crew
  database/           PostGIS schema and seed notes
  docs/               Architecture, API, prompts, roadmap
  examples/           Example CSV and GeoJSON files
  .github/workflows/  CI starter
```

## Frontend Component Plan

- `App`: application shell and state owner.
- `MapCanvas`: React-Leaflet map, base layer, marker placement, draw controls.
- `ToolBar`: compact field-friendly placement/export/import controls.
- `MarkerLayer`: renders investigation markers and labels.
- `DrawLayer`: site boundaries, access paths, and exclusion zones.
- `FeatureEditor`: side panel for borehole, DCP, test pit, and sample metadata.
- `CoordinateReadout`: compact WGS84 readout and future calibration status.
- `ImportExportPanel`: CSV import plus GeoJSON/CSV export actions.

## Backend API Plan

- `GET /health`
- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{project_id}`
- `PUT /api/projects/{project_id}`
- `GET /api/projects/{project_id}/geojson`
- `POST /api/projects/{project_id}/features`
- `PUT /api/projects/{project_id}/features/{feature_id}`
- `DELETE /api/projects/{project_id}/features/{feature_id}`
- `POST /api/projects/{project_id}/imports/csv`
- `GET /api/projects/{project_id}/exports/csv`
- `POST /api/transform/pixel-to-coordinate`
- `POST /api/transform/coordinate-to-pixel`
- `POST /api/overlays`
- `POST /api/calibrations`

## Database Schema Summary

Production persistence targets PostgreSQL/PostGIS:

- `projects`
- `sites`
- `features`
- `feature_properties`
- `overlays`
- `calibrations`
- `calibration_points`
- `attachments`

See [database/schema.sql](database/schema.sql).

## GeoJSON Structure

Map1 uses a GeoJSON `FeatureCollection`. Each investigation point is a `Feature` with a `Point` geometry and geotechnical metadata in `properties`.

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [151.2093, -33.8688]
  },
  "properties": {
    "feature_type": "borehole",
    "label": "BH01",
    "borehole_id": "BH01",
    "surface_rl": null,
    "total_depth": null,
    "drilling_method": null,
    "logged_by": null,
    "linked_log_pdf": null,
    "linked_gint_data": null,
    "coordinate_system": "WGS84"
  }
}
```

## Example CSV Format

See [examples/boreholes.csv](examples/boreholes.csv).

Required fields:

```csv
type,id,latitude,longitude,easting,northing,zone,surface_rl,total_depth,start_date,end_date,method,logged_by,water_level,remarks,linked_log_pdf
borehole,BH01,-33.8688,151.2093,,,,12.4,8.5,2026-05-06,2026-05-06,Solid flight auger,J Smith,2.1,Near existing slab,
```

## Swarm-Agent Development Plan

The optional CrewAI prototype is in [crewai/](crewai/). It defines:

- Architect Agent: React/Leaflet frontend implementation.
- GIS Agent: affine transform and coordinate calibration design.
- QA Agent: API, GeoJSON, CSV, and GitHub readiness checks.

1. Frontend map agent: implement placement modes, marker labels, side panel editing, drawing UX.
2. Backend API agent: implement FastAPI routes, validation, GeoJSON serialization, CSV import/export.
3. Database agent: convert in-memory API to SQLAlchemy/PostGIS persistence.
4. Calibration agent: implement overlay upload, anchor capture, similarity/affine transforms, residual reporting.
5. QA agent: mobile layout testing, GeoJSON validation, CSV round-trip tests, field-user workflow review.
6. Integration agent: connect marker IDs to AutoSoil Logger logs, PDFs, and GINT-style structured exports.

## Cursor/Codex Repo Generation Prompt

```text
Build the `map1` repository for AutoSoil Logger.

Create a production-ready starter implementation using React + Vite, React-Leaflet, Leaflet Draw, FastAPI, GeoJSON, CSV import/export, and a PostgreSQL/PostGIS-ready schema.

The product is not a generic map app. It is a geotechnical site investigation map for Australian AS1726-style workflows. Users must be able to add boreholes, DCPs, test pits, sample points, site boundaries, access paths, and exclusion zones. Boreholes require metadata including ID, coordinates, RL, depth, dates, drilling method, logged by, water level, remarks, linked PDF, and linked structured log data.

Keep the MVP simple, professional, mobile-friendly, and easy to extend. Use WGS84 now, preserve structure for MGA/GDA2020, manual coordinate entry, uploaded site plan overlays, calibration anchors, offline field mode, and AutoSoil Logger reporting integration.

Deliver:
- clear README
- frontend starter app
- backend starter API
- PostGIS schema
- example CSV and GeoJSON
- roadmap and agent development plan
- sensible tests or validation hooks where practical
```
