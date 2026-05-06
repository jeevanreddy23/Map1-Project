# Map1 CrewAI Prototype Crew

This folder defines a fast-prototype CrewAI workflow for developing Map1 with three focused agents:

- Architect Agent: React/Leaflet frontend implementation plan and patch brief.
- GIS Agent: affine/similarity transform design for site plan calibration.
- QA Agent: API and repo verification checklist.

This crew is intentionally outside the production frontend/backend code. It is a development accelerator, not a runtime dependency of Map1.

## Install

From this folder:

```bash
pip install -r requirements.txt
```

Set your LLM provider environment variables, for example:

```bash
set OPENAI_API_KEY=your_key_here
```

## Run

```bash
python run_crew.py
```

The crew writes its final development brief to:

```text
crewai/output/map1_crew_report.md
```

## Crew Design

The crew runs sequentially:

1. Architect Agent reviews frontend requirements and produces a UI/component implementation brief.
2. GIS Agent designs coordinate transform logic and API integration details.
3. QA Agent converts the combined plan into concrete tests, API checks, and GitHub-ready acceptance criteria.

Sequential execution keeps the prototype predictable. Later, this can become a CrewAI Flow with explicit state and separate implementation tasks.

