# app/state/borehole.py

from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class SoilLayer(TypedDict):
    depth_from: float
    depth_to: float
    uscs_code: str
    description: str
    colour: str
    moisture: str
    consistency: str
    structure: str
    inclusions: str


class TestResult(TypedDict):
    test_type: str
    depth: float
    value: float
    unit: str
    notes: str


class BoreholeState(TypedDict):
    project_id: str
    project_name: str
    borehole_id: str
    depth_from: float
    depth_to: float
    sample_id: str
    photo_path: Optional[str]
    photo_base64: Optional[str]
    soil_layers: list[SoilLayer]
    current_layer: Optional[SoilLayer]
    test_results: list[TestResult]
    qa_score: float
    qa_feedback: str
    qa_passed: bool
    retry_count: int
    selected_template_path: Optional[str]
    report_path: Optional[str]
    messages: Annotated[list, add_messages]
    last_agent: str
    error: Optional[str]
    pending_human_review: bool

