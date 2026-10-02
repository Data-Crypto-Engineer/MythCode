"""
Story Weaver Agent (Agent 3).
Generates evolving fantasy narratives, dialogue, and choices grounded in world state and memory.
"""
from typing import Dict, Any, List, Optional
from utils.logger import setup_logger
from utils.error_handler import fallback_narrative_scene

logger = setup_logger("StoryWeaverAgent")

class StoryWeaverAgent:
    """Crafts rich story scenes and character interactions reflecting past player deeds."""

    ROLE = "Mythic Bard & World Chronicler"
    GOAL = "Compose vivid, atmospheric scenes and character dialogue that weave computational thinking into high fantasy."
    BACKSTORY = (
        "A weaver of living legends in Elarion, skilled in turning gears, runic conditions, and magical repetitions "
        "into emotional, high-stakes folklore."
    )

    def __init__(self, llm=None):
        self.llm = llm

    def generate_scene(
        self,
        director_proposal: Dict[str, Any],
        world_state: Dict[str, Any],
        player_profile: Dict[str, Any],
        character_memories: List[Dict[str, Any]],
        learning_progress: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes a structured scene containing title, description, speaker, dialogue, and choices.
        """
        location = director_proposal.get("proposed_state_changes", {}).get(
            "current_location", world_state.get("current_location", "Whispering Village")
        )
        base_scene = fallback_narrative_scene(location, "")

        # Personalize dialogue with character memories
        npc_name = base_scene.get("speaker", "Elder Thorne")
        relevant_mems = [m for m in character_memories if m.get("npc_name") == npc_name or npc_name in m.get("npc_name", "")]

        dialogue = base_scene["dialogue"]
        if relevant_mems:
            latest_mem = relevant_mems[0]["event_summary"]
            dialogue = f"(Remembering: '{latest_mem}') {dialogue}"

        # If guardian has been awakened
        if world_state.get("clockwork_guardian") in ("operational", "repaired") and location == "River Aqueduct":
            base_scene["description"] += " The Clockwork Guardian hums quietly, its crystalline core spinning in smooth rhythm."
            dialogue = "The water sluice is active! The lower reservoirs are beginning to refill."

        # If water supply has been restored
        if world_state.get("water_supply") == "restored":
            base_scene["description"] += " Crystal-clear water cascades once again through the channels of Elarion!"

        return {
            "scene_title": base_scene["title"],
            "scene_description": base_scene["description"],
            "speaker": base_scene["speaker"],
            "dialogue": dialogue,
            "choices": base_scene["choices"],
            "location": location,
            "event_category": "narrative_encounter"
        }
