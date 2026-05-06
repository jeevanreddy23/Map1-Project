from crewai import Agent, Crew, Process, Task


def architect_agent() -> Agent:
    return Agent(
        role="Lead Geospatial UI Architect",
        goal=(
            "Design and guide a clean, field-ready React/Leaflet frontend for Map1 "
            "that is specific to geotechnical site investigation workflows."
        ),
        backstory=(
            "You are a senior frontend architect with deep experience in mapping UX, "
            "mobile field tools, and professional engineering software. You avoid generic "
            "map-app clutter and keep workflows fast for geotechnicians placing boreholes, "
            "DCPs, test pits, and sampling points."
        ),
        verbose=True,
        allow_delegation=False,
    )


def gis_agent() -> Agent:
    return Agent(
        role="Geospatial Calibration Engineer",
        goal=(
            "Specify robust image-to-world coordinate transformation logic for uploaded "
            "site plans, including one-anchor, two-anchor, and affine calibration modes."
        ),
        backstory=(
            "You are a GIS engineer specialising in site plan calibration, pixel-to-coordinate "
            "transforms, GeoJSON interchange, PostGIS storage, and Australian coordinate systems "
            "including WGS84 and future MGA/GDA2020 support."
        ),
        verbose=True,
        allow_delegation=False,
    )


def qa_agent() -> Agent:
    return Agent(
        role="Map1 QA and GitHub Readiness Lead",
        goal=(
            "Turn the Map1 prototype into a verifiable GitHub-ready starter repo with clear "
            "API tests, frontend smoke tests, GeoJSON validation, and acceptance criteria."
        ),
        backstory=(
            "You are a pragmatic QA lead for engineering SaaS tools. You care about API correctness, "
            "CSV round trips, valid GeoJSON, mobile usability, and preserving future integration hooks "
            "for AutoSoil Logger and GINT-style reports."
        ),
        verbose=True,
        allow_delegation=False,
    )


def build_map1_crew() -> Crew:
    architect = architect_agent()
    gis = gis_agent()
    qa = qa_agent()

    frontend_task = Task(
        description=(
            "Review the Map1 repo at {repo_root}. Produce a practical frontend implementation brief "
            "for {frontend_stack}. Focus on a minimal geotechnical mapping workflow: OSM base map, "
            "borehole/DCP/test pit/sample placement, auto labels, side-panel editing, drawn site "
            "boundaries/access paths/exclusion zones, mobile field usability, and clean visual hierarchy."
        ),
        expected_output=(
            "A concise markdown section with component responsibilities, state model, UX acceptance "
            "criteria, and the next 5 frontend implementation steps."
        ),
        agent=architect,
    )

    gis_task = Task(
        description=(
            "Using the Map1 context at {repo_root}, design the coordinate and calibration approach. "
            "Cover WGS84 now, MGA/GDA2020 later, manual coordinate entry, CSV import, GeoJSON output, "
            "site plan overlays, one anchor plus scale/rotation, two-point similarity transform, "
            "three-or-more-point affine transform, and calibration confidence/residual reporting."
        ),
        expected_output=(
            "A concise markdown section containing the transform formulas, required API payloads, "
            "data model fields, validation rules, and edge cases."
        ),
        agent=gis,
    )

    qa_task = Task(
        description=(
            "Combine the Architect and GIS outputs into a GitHub-ready QA plan for Map1. "
            "Focus on FastAPI endpoint checks, valid GeoJSON export, CSV import/export round trips, "
            "marker label sequencing, mobile UI smoke testing, and future AutoSoil Logger report links."
        ),
        expected_output=(
            "A final markdown report with test checklist, acceptance criteria, GitHub issue breakdown, "
            "and risks. Keep it specific to {project_name} and {domain_context}."
        ),
        agent=qa,
        output_file="output/map1_crew_report.md",
        context=[frontend_task, gis_task],
    )

    return Crew(
        agents=[architect, gis, qa],
        tasks=[frontend_task, gis_task, qa_task],
        process=Process.sequential,
        verbose=True,
    )

