# app/tools/vision.py

import base64
from pathlib import Path
from langchain_core.tools import tool


@tool
def encode_image_for_vision(image_path: str) -> str:
    """Read an image file and return base64 encoded string for vision API."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


@tool
def extract_visual_descriptors_prompt(base64_image: str) -> str:
    """
    Returns a structured prompt to send to vision model for soil description.
    Caller passes this to the vision API alongside the image.
    """
    return """You are an expert geotechnical engineer trained in AS 1726:2017.
Analyse this field photograph of a soil sample and provide ONLY the following JSON:
{
  "colour": "<primary colour from AS 1726 colour chart>",
  "secondary_colour": "<secondary colour if mottled, else null>",
  "texture": "<fine / medium / coarse / mixed>",
  "visible_particles": "<gravel / sand / fines / mixed>",
  "moisture_visual": "<dry / moist / wet>",
  "structure_visible": "<massive / stratified / fissured / laminated / null>",
  "inclusions_visible": "<describe visible inclusions or null>",
  "confidence": <0.0 to 1.0>
}
Respond ONLY with the JSON object. No markdown, no explanation."""
