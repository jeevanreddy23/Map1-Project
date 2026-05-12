# app/agents/template_selector_agent.py

import os
import json
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from app.state.borehole import BoreholeState

SELECTOR_SYSTEM = """You are a Principal Geotechnical Engineer at STS (Sydney Test & Specification).
You have an extensive library of templates for different project types (Basements, No Basement, ASS, Pavements, etc.).

Based on the project context and logged soil profile, you must select the EXACT template path from the directory:
"C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\STS Templates"

Respond ONLY with this JSON:
{
  "selected_template_path": "<absolute_path_to_docx>",
  "reasoning": "<one sentence justification>"
}"""

TEMPLATE_LIST = """
Available Templates (subset of most common):
1. C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\STS Templates\\Geotechnical Investigations\\01 - All Templates\\Basement + ASS == Fill + Clays + Shale.docx
2. C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\STS Templates\\Geotechnical Investigations\\01 - All Templates\\Basement == Clays + Shale.docx
3. C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\STS Templates\\Geotechnical Investigations\\01 - All Templates\\No Basement == Fill + Clays + Shale (class P uncontrolled fill).docx
4. C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\Geotechnical Investigation Master Template.docx
5. C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\Basic Site Classification.docx
"""

async def template_selector_agent(state: BoreholeState) -> dict:
    """
    Selects the most appropriate Word template based on the logged soil layers and project context.
    Outputs: updates state with selected_template_path
    """
    layers = state.get("soil_layers", [])
    uscs_codes = [l.get("uscs_code", "") for l in layers]
    has_ass = "PT" in uscs_codes or "OH" in uscs_codes # simplistic proxy
    
    user_prompt = f"""Project: {state.get("project_name")} (ID: {state.get("project_id")})
Borehole: {state.get("borehole_id")}
Soil Profile USCS codes found: {uscs_codes}
Has potential Acid Sulfate Soils (ASS): {has_ass}

{TEMPLATE_LIST}

Select the most appropriate template."""

    provider = os.getenv("MODEL_PROVIDER", "openai")
    if provider == "anthropic":
        llm = ChatAnthropic(model=os.getenv("MODEL_NAME", "claude-opus-4-6"))
    else:
        llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o"))

    response = llm.invoke([
        SystemMessage(content=SELECTOR_SYSTEM),
        HumanMessage(content=user_prompt),
    ])

    raw = response.content.strip()
    if raw.startswith("```"):
        raw = raw.lstrip("`json\n").rstrip("`")

    try:
        result = json.loads(raw)
        template_path = result.get("selected_template_path")
        # Fallback to master template if selection is invalid/empty
        if not template_path or not os.path.exists(template_path):
            template_path = "C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\Geotechnical Investigation Master Template.docx"
            
        return {
            "selected_template_path": template_path,
            "last_agent": "template_selector_agent",
            "error": None
        }
    except Exception as e:
        return {
            "selected_template_path": "C:\\Users\\pored\\Downloads\\Project Geologs\\Templates\\Geotechnical Investigation Master Template.docx",
            "last_agent": "template_selector_agent",
            "error": f"Template selection error: {e}"
        }
