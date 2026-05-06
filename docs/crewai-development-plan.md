# CrewAI Development Plan

CrewAI is the fast prototype path for Map1. The production app remains React/FastAPI/PostGIS, while CrewAI acts as a development orchestration layer.

Reference implementation: [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

## Three-Agent Crew

### Architect Agent

Owns the React/Leaflet frontend direction.

Responsibilities:

- Map canvas layout.
- Marker placement flow.
- Side panel editing.
- Mobile field UI.
- Drawing tools for boundary, access path, and exclusion zone features.
- Clean geotechnical visual language.

Outputs:

- Component plan.
- UX acceptance criteria.
- Frontend issue list.

### GIS Agent

Owns geospatial math and calibration.

Responsibilities:

- WGS84 coordinate handling.
- Manual coordinate entry rules.
- CSV coordinate import validation.
- Site plan overlay calibration.
- One-anchor plus scale/rotation workflow.
- Two-point similarity transform.
- Three-or-more-point affine transform.
- Residual error and confidence reporting.
- Future MGA/GDA2020 support.

Outputs:

- Transform formulas.
- API payload design.
- Calibration schema.
- Validation and edge-case list.

### QA Agent

Owns verification and GitHub readiness.

Responsibilities:

- FastAPI endpoint smoke tests.
- GeoJSON validity checks.
- CSV round-trip checks.
- Marker auto-label tests.
- Mobile viewport checks.
- GitHub issue breakdown.
- Pull request acceptance criteria.

Outputs:

- QA checklist.
- Test cases.
- GitHub issue plan.
- Release readiness summary.

## Execution Model

Use sequential execution first:

1. Architect Agent produces the frontend brief.
2. GIS Agent produces the calibration and coordinate brief.
3. QA Agent combines both into a verifiable development plan.

Sequential mode is easier to debug for a prototype. Later, convert this into a CrewAI Flow if Map1 needs stateful runs, human approval gates, or recurring repo analysis.

## Suggested GitHub Issues

1. Implement marker placement and side-panel editing.
2. Add DrawLayer persistence for boundaries, access paths, and exclusion zones.
3. Add backend feature CRUD with PostGIS persistence.
4. Add CSV import/export tests.
5. Implement calibration API with two-point similarity transform.
6. Add affine transform solver and residual error report.
7. Add uploaded image/PDF overlay support.
8. Add offline field cache and sync queue.
9. Add AutoSoil Logger borehole log/report linking.

