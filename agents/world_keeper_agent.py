"""
World Keeper Agent (Agent 4).
Protects the integrity, continuity, and physical laws of Elarion.
"""
from typing import Dict, Any, List
from utils.logger import setup_logger
from core.state_validator import StateValidator
from models.world import WorldState

logger = setup_logger("WorldKeeperAgent")

class WorldKeeperAgent:
    """Safeguards continuity of the fantasy kingdom, tracking locations, NPCs, and resources."""

    ROLE = "Keeper of Elarion's Laws & State"
    GOAL = "Preserve geographic continuity, track resource balances, and maintain NPC relationship states."
    BACKSTORY = (
        "An eternal archivist stationed within the heart of Elarion's celestial archives, "
        "preventing paradoxes, impossible teleportations, and contradicted world events."
    )

    def __init__(self, llm=None):
        self.llm = llm

    def evaluate_world_mutation(
        self,
        current_world: WorldState,
        proposed_changes: Dict[str, Any],
        player_action: str
    ) -> Dict[str, Any]:
        """
        Validates proposed mutations through deterministic rules and generates continuity commentary.
        """
        is_valid, issues, validated_state = StateValidator.validate_transition(
            current_world, proposed_changes
        )

        return {
            "is_valid": is_valid,
            "issues": issues,
            "validated_state": validated_state,
            "keeper_notes": "State transitions remain aligned with Elarion's physical laws." if is_valid else f"Contradictions detected: {', '.join(issues)}"
        }
