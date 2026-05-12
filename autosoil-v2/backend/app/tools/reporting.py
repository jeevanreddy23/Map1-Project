# app/tools/reporting.py

import os
from datetime import datetime
from langchain_core.tools import tool
from docxtpl import DocxTemplate

@tool
def generate_borehole_log_docx(
    project_name: str,
    borehole_id: str,
    soil_layers: list,
    test_results: list,
    template_path: str,
    output_path: str,
) -> dict:
    """Generate a Word borehole log compliant with AS 1726:2017 format using an existing template."""
    try:
        if not os.path.exists(template_path):
            return {"success": False, "error": f"Template not found: {template_path}"}
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        doc = DocxTemplate(template_path)
        
        # Prepare context variables for the Jinja tags in the template
        # e.g., {{ project_name }}, {{ borehole_id }}, and a loop over {{ soil_layers }}
        context = {
            "project_name": project_name,
            "borehole_id": borehole_id,
            "date_logged": datetime.now().strftime('%d %b %Y'),
            "soil_layers": soil_layers,
            "test_results": test_results
        }
        
        doc.render(context)
        doc.save(output_path)
        
        return {"success": True, "path": output_path}
    except Exception as e:
        return {"success": False, "error": str(e)}
