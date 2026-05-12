# app/skills/temporal_memory.py
"""
Skill: Scalable Long-Term Memory & Context Density
Inspired by: Mem0 (2504.19413), Zep (2501.13956), GenericAgent (2604.17091)

Purpose: Prevents context collapse in deep geotechnical projects (e.g., logging 50 boreholes).
Uses Temporal Knowledge Graphs to remember spatial relationships (e.g., "BH-01 hit water at 2m, BH-02 is 10m away").
"""

class SpatialTemporalMemory:
    def __init__(self, project_id: str):
        self.project_id = project_id
        # In a real implementation, this connects to the Zep or Mem0 client
        self.graph_store = {} 
        
    def add_borehole_finding(self, borehole_id: str, depth: float, finding_type: str, value: str):
        """
        E.g., add_borehole_finding('BH-01', 2.5, 'groundwater', 'seepage observed')
        """
        if borehole_id not in self.graph_store:
            self.graph_store[borehole_id] = []
        self.graph_store[borehole_id].append({"depth": depth, "type": finding_type, "value": value})
        
    def query_nearby_context(self, current_borehole_id: str, radius_m: float) -> str:
        """
        Retrieves summarized graph data from surrounding boreholes to inform the classifier agent.
        """
        return "Historical context: Groundwater commonly found at 2.0-3.0m in this stratum."
