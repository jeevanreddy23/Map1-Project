# app/tools/as1726.py

from langchain_core.tools import tool
from typing import Optional


USCS_CODES = {
    "GW": "Well-graded gravel",
    "GP": "Poorly graded gravel",
    "GM": "Silty gravel",
    "GC": "Clayey gravel",
    "SW": "Well-graded sand",
    "SP": "Poorly graded sand",
    "SM": "Silty sand",
    "SC": "Clayey sand",
    "ML": "Low plasticity silt",
    "CL": "Low plasticity clay",
    "OL": "Organic low plasticity",
    "MH": "High plasticity silt",
    "CH": "High plasticity clay",
    "OH": "Organic high plasticity",
    "PT": "Peat",
}

MOISTURE_STATES = ["dry", "slightly moist", "moist", "very moist", "wet"]
CONSISTENCY_STATES = {
    "cohesive": ["very soft", "soft", "firm", "stiff", "very stiff", "hard"],
    "granular": ["very loose", "loose", "medium dense", "dense", "very dense"],
}
COLOUR_DESCRIPTORS = [
    "brown", "dark brown", "light brown", "grey", "dark grey", "light grey",
    "red", "orange", "yellow", "black", "white", "green", "mottled",
]


@tool
def validate_uscs_code(code: str) -> dict:
    """Validate a USCS classification code against AS 1726:2017 table."""
    code = code.upper().strip()
    if code in USCS_CODES:
        return {"valid": True, "description": USCS_CODES[code], "code": code}
    return {"valid": False, "description": None, "code": code,
            "suggestion": "Check AS 1726 Table 2 — closest valid codes: " +
                          ", ".join(list(USCS_CODES.keys())[:5])}


@tool
def validate_depth_interval(depth_from: float, depth_to: float,
                             existing_layers: list) -> dict:
    """Check depth interval is valid and does not overlap existing logged layers."""
    if depth_to <= depth_from:
        return {"valid": False, "error": "depth_to must be greater than depth_from"}
    if depth_from < 0:
        return {"valid": False, "error": "depth_from cannot be negative"}

    for layer in existing_layers:
        if not (depth_to <= layer["depth_from"] or depth_from >= layer["depth_to"]):
            return {
                "valid": False,
                "error": f"Overlaps existing layer {layer['depth_from']}-{layer['depth_to']}m"
            }
    return {"valid": True, "error": None}


@tool
def get_consistency_options(uscs_code: str) -> dict:
    """Return valid consistency descriptors for a given USCS soil type."""
    code = uscs_code.upper().strip()
    if code in ["CH", "CL", "MH", "ML", "OH", "OL", "PT"]:
        soil_type = "cohesive"
    else:
        soil_type = "granular"
    return {
        "soil_type": soil_type,
        "consistency_options": CONSISTENCY_STATES[soil_type],
        "moisture_options": MOISTURE_STATES,
        "colour_options": COLOUR_DESCRIPTORS,
    }


@tool
def build_soil_description(
    uscs_code: str,
    colour: str,
    moisture: str,
    consistency: str,
    structure: Optional[str] = None,
    inclusions: Optional[str] = None,
) -> str:
    """Build a formal AS 1726:2017 soil description string from components."""
    code = uscs_code.upper().strip()
    soil_name = USCS_CODES.get(code, "Unknown soil")
    parts = [f"{consistency.capitalize()},", colour, moisture, soil_name]
    if structure:
        parts.append(f"- {structure}")
    if inclusions:
        parts.append(f"with {inclusions}")
    return " ".join(parts) + f" ({code})"
