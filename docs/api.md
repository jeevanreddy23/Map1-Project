# Map1 API Plan

## Health

`GET /health`

## Projects

`GET /api/projects`

`POST /api/projects`

`GET /api/projects/{project_id}`

`PUT /api/projects/{project_id}`

## Features

`POST /api/projects/{project_id}/features`

`PUT /api/projects/{project_id}/features/{feature_id}`

`DELETE /api/projects/{project_id}/features/{feature_id}`

## Import/Export

`POST /api/projects/{project_id}/imports/csv`

`GET /api/projects/{project_id}/exports/csv`

`GET /api/projects/{project_id}/geojson`

## Overlays and Calibration

`POST /api/overlays`

`POST /api/calibrations`

`POST /api/transform/pixel-to-coordinate`

`POST /api/transform/coordinate-to-pixel`

