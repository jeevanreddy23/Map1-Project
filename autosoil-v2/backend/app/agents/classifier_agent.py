# app/agents/classifier_agent.py
import os
import json
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from app.state.borehole import BoreholeState
from app.skills.temporal_memory import SpatialTemporalMemory

CLASSIFIER_SYS = """You are a Geotechnical Engineer.
Based on visual descriptors, depth, and historical site memory, output a valid AS 1726:2017 description.
Return ONLY JSON:
{"uscs_code": "...", "description": "...", "colour": "...", "moisture": "...", "consistency": "..."}
"""

async def classifier_agent(state: BoreholeState) -> dict:
    """Classifies soil utilizing both visual data and Temporal Graph Memory (Mem0/Zep style)."""
    
    # Initialize Memory Skill
    memory = SpatialTemporalMemory(state.get("project_id", "default_proj"))
    site_context = memory.query_nearby_context(state.get("borehole_id"), radius_m=50.0)
    
    user_msg = f"""
    Depth: {state.get("current_depth", "Unknown")}
    Visual extraction: {state.get("current_visual_descriptors", {})}
    Site Memory Context: {site_context}
    """
    
    provider = os.getenv("MODEL_PROVIDER", "openai")
    if provider == "anthropic":
        llm = ChatAnthropic(model=os.getenv("MODEL_NAME", "claude-opus-4-6"))
    else:
        llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"))

    response = llm.invoke([
        SystemMessage(content=CLASSIFIER_SYS),
        HumanMessage(content=user_msg)
    ])
    
    raw = response.content.strip()
    if raw.startswith("```"):
        raw = raw.lstrip("`json\n").rstrip("`")
        
    try:
        layer_data = json.loads(raw)
        
        # Add to state
        layers = state.get("soil_layers", [])
        # In a real workflow, we'd merge depth info from state into layer_data here
        layers.append(layer_data)
        
        return {
            "soil_layers": layers,
            "last_agent": "classifier_agent",
            "error": None
        }
    except Exception as e:
        return {
            "error": f"Classification failed: {e}",
            "last_agent": "classifier_agent"
        }
