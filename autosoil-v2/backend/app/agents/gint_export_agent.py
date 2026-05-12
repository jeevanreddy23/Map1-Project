# app/agents/gint_export_agent.py

import os
import csv
from app.state.borehole import BoreholeState

async def gint_export_agent(state: BoreholeState) -> dict:
    """
    Exports the logged soil layers into a structured CSV format ready for GINT import.
    Matches standard stratigraphy sheet columns.
    """
    layers = state.get("soil_layers") or []
    if not layers:
        return {
            "error": "gint_export_agent: No logged layers to export",
            "last_agent": "gint_export_agent",
        }

    output_dir = os.getenv("REPORT_OUTPUT_DIR", "C:/tmp/autosoil_reports")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{state.get('borehole_id', 'BH-unknown')}_GINT_export.csv"
    output_path = os.path.join(output_dir, filename)

    try:
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Standard GINT headers
            writer.writerow(["PointID", "Depth", "Bottom", "USCS", "Description", "Graphic", "Moisture", "Consistency"])
            
            for layer in layers:
                writer.writerow([
                    state.get("borehole_id"),
                    layer.get("depth_from"),
                    layer.get("depth_to"),
                    layer.get("uscs_code"),
                    layer.get("description"),
                    layer.get("uscs_code"), # Graphic often maps to USCS
                    layer.get("moisture"),
                    layer.get("consistency")
                ])

        return {
            "report_path": output_path, # Reusing report_path or creating a new export_path
            "last_agent": "gint_export_agent",
            "error": None,
        }
    except Exception as e:
        return {
            "error": f"gint_export_agent: CSV generation failed - {str(e)}",
            "last_agent": "gint_export_agent",
        }
