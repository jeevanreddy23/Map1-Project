# app/agents/report_agent.py

import os
from app.state.borehole import BoreholeState
from app.tools.reporting import generate_borehole_log_docx

async def report_agent(state: BoreholeState) -> dict:
    """Generates AS 1726:2017 Word borehole log using docxtpl from logged soil_layers."""
    layers = state.get("soil_layers") or []
    if not layers:
        return {
            "error": "report_agent: No logged layers to report",
            "last_agent": "report_agent",
        }

    output_dir = os.getenv("REPORT_OUTPUT_DIR", "C:/tmp/autosoil_reports")
    filename = f"{state.get('borehole_id', 'BH-unknown')}_{state.get('project_id', 'proj')}.docx"
    output_path = os.path.join(output_dir, filename)

    template_path = state.get("selected_template_path")
    if not template_path:
        template_path = "C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\Geotechnical Investigation Master Template.docx"

    result = generate_borehole_log_docx.invoke({
        "project_name": state.get("project_name", "Unknown Project"),
        "borehole_id": state.get("borehole_id", "BH-??"),
        "soil_layers": layers,
        "test_results": state.get("test_results") or [],
        "template_path": template_path,
        "output_path": output_path,
    })

    if not result["success"]:
        return {
            "error": f"report_agent: DOCX generation failed - {result['error']}",
            "last_agent": "report_agent",
        }

    return {
        "report_path": result["path"],
        "last_agent": "report_agent",
        "error": None,
    }
