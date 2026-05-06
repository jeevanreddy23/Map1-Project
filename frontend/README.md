# Map1 Frontend

React + Vite frontend for the AutoSoil Logger Map1 field map.

## Run

```bash
npm install
npm run dev
```

Open `http://localhost:5173`.

## Build

```bash
npm run build
```

## Notes

- The app uses WGS84 latitude/longitude in the MVP.
- CSV import preserves blank coordinate-system fields so borehole CSVs can include empty `easting`, `northing`, and `zone` columns while still importing valid latitude/longitude.
- Leaflet Draw is wired for site boundary polygons, access path lines, and exclusion/safety zone polygons.
- Uploaded site plan overlays and calibration tools are reserved for the next phase.

