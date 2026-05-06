from pathlib import Path

from map1_crew.crew import build_map1_crew


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    inputs = {
        "repo_root": str(repo_root),
        "project_name": "AutoSoil Logger Map1",
        "frontend_stack": "React, Vite, React-Leaflet, Leaflet Draw",
        "backend_stack": "FastAPI, GeoJSON, CSV, PostgreSQL/PostGIS",
        "domain_context": "Australian AS1726-style geotechnical site investigation mapping",
    }

    result = build_map1_crew().kickoff(inputs=inputs)
    report_path = output_dir / "map1_crew_report.md"
    if not report_path.exists():
        report_path.write_text(str(result), encoding="utf-8")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
