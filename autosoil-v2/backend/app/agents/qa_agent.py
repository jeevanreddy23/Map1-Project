# app/agents/qa_agent.py
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from app.state.borehole import BoreholeState
from app.skills.adversarial_validator import AdversarialValidator

async def qa_agent(state: BoreholeState) -> dict:
    """
    Applies the ARIS-inspired Adversarial Validator skill.
    Uses cross-model (or cross-persona) debate to find AS 1726 flaws.
    """
    layers = state.get("soil_layers", [])
    if not layers:
        return {"error": "No layers to QA", "last_agent": "qa_agent"}

    latest_layer = layers[-1]
    
    # Initialize the new ARIS skill
    validator = AdversarialValidator()
    
    # For scaffolding, we simulate the debate output.
    # In production, this invokes LLM1 (Attacker) and LLM2 (Defender) sequentially.
    debate_result = await validator.run_assurance_loop(latest_layer)
    
    # If the defender successfully justifies it, or it passes the attacker's criteria:
    qa_score = 0.95 if debate_result["audit_passed"] else 0.4
    
    # Update the layer with the QA score
    latest_layer["_classifier_confidence"] = qa_score
    state["soil_layers"][-1] = latest_layer
    
    if qa_score < 0.7:
        state["messages"].append(HumanMessage(content=f"Auditor: The description '{latest_layer.get('description')}' fails AS 1726. Revise it."))
    
    return {
        "soil_layers": state["soil_layers"],
        "messages": state["messages"],
        "last_agent": "qa_agent",
        "error": None
    }
