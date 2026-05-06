# Map1 Architecture

Map1 separates field interaction from persistence and reporting.

## Frontend

The frontend owns the immediate field workflow:

- placement mode
- marker labels
- side-panel editing
- CSV import
- GeoJSON/CSV export
- local/offline cache in a later phase

The map emits GeoJSON features so the backend and reporting tools do not need to understand Leaflet internals.

## Backend

The backend owns:

- project save/load
- validation
- CSV import/export
- future PostGIS persistence
- overlay metadata
- calibration transforms
- AutoSoil Logger report links

## Coordinate Strategy

Version 1 stores WGS84 latitude/longitude in GeoJSON.

Future coordinate support:

- manual MGA/GDA2020 entry
- pyproj transformations
- calibration anchors for uploaded site plans
- residual error reporting

One anchor alone is not enough for scale and rotation unless scale and rotation are separately supplied. Two anchors support a similarity transform. Three or more anchors support an affine transform.

