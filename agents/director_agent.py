"""
Director Agent (Agent 1).
Central experience coordinator proposing narrative transitions and pacing.
Accurately distinguishes dialogue, investigation, movement, and puzzle triggers.
"""
from typing import Dict, Any, List, Optional
from utils.logger import setup_logger

logger = setup_logger("DirectorAgent")

class DirectorAgent:
    """Interprets player actions, aligns with quest progression, and coordinates agents."""

    ROLE = "Central Narrative & Experience Director"
    GOAL = "Synthesize world state, quest milestones, and player learning needs into a compelling next chapter."
    BACKSTORY = (
        "An ancient cosmic chronicler of Elarion who balances tension, curiosity, and computational enlightenment "
        "without violating the laws of the realm."
    )

    def __init__(self, llm=None):
        self.llm = llm

    def plan_next_beat(
        self,
        player_action: str,
        world_state: Dict[str, Any],
        player_profile: Dict[str, Any],
        quest_state: Dict[str, Any],
        learning_progress: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes the next narrative event, required agents, and proposed state changes.
        """
        location = world_state.get("current_location", "Whispering Village")
        traits = player_profile.get("traits", {})
        action_lower = player_action.lower()

        suggested_challenge = None
        target_location = location
        proposed_state_changes = {}
        beat_id = "general_exploration"
        active_challenge = None

        # 1. Whispering Village actions
        if "fountain" in action_lower or "pipes" in action_lower or "stonework" in action_lower:
            target_location = "Whispering Village"
            beat_id = "inspect_fountain"
            objective = "Analyze the dried conduits of the village fountain."

        elif "mira" in action_lower or "workshop" in action_lower:
            target_location = "Whispering Village"
            beat_id = "dialogue_mira"
            objective = "Confer with Mira at her workshop about the waterwheel mechanism."

        elif "elder" in action_lower or "thorne" in action_lower or "morale" in action_lower:
            target_location = "Whispering Village"
            beat_id = "dialogue_thorne"
            objective = "Speak with Elder Thorne regarding the town's diminishing rations."

        # 2. Movement to River Aqueduct
        elif "travel downstream" in action_lower or "aqueduct" in action_lower or "head_to_river" in action_lower or "go to aqueduct" in action_lower:
            target_location = "River Aqueduct"
            beat_id = "aqueduct_arrival"
            objective = "Reach the seized sluice gates at the River Aqueduct."

        # 3. Sequence Challenge Trigger
        elif "guardian" in action_lower or "sequence" in action_lower or "control altar" in action_lower or "puzzle_sequence" in action_lower:
            target_location = "River Aqueduct"
            beat_id = "challenge_sequence"
            suggested_challenge = "puzzle_sequence_guardian"
            active_challenge = "puzzle_sequence_guardian"
            objective = "Assemble the ordered sequence of movement commands to guide the guardian."

        # 4. Movement to Ancient Grove
        elif "ancient grove" in action_lower or "venture into the misty" in action_lower or "head to grove" in action_lower:
            target_location = "Ancient Grove"
            beat_id = "grove_arrival"
            objective = "Seek audience with Sylvan the Forest Spirit under the ancient canopy."

        # 5. Condition Challenge Trigger
        elif "runic portal" in action_lower or "condition" in action_lower or "emerald seal" in action_lower or "puzzle_conditional" in action_lower or "gate" in action_lower:
            target_location = "Ancient Grove"
            beat_id = "challenge_conditions"
            suggested_challenge = "puzzle_conditional_door"
            active_challenge = "puzzle_conditional_door"
            objective = "Evaluate the condition required to safely unseal the Sylvan gateway."

        # 6. Movement to Clockwork Ruins
        elif "ruins" in action_lower or "subterranean" in action_lower or "vault" in action_lower or "conduit chamber" in action_lower:
            target_location = "Clockwork Ruins"
            beat_id = "ruins_arrival"
            objective = "Explore the subterranean energy vault beneath the dried reservoir."

        # 7. Loop Challenge Trigger
        elif "tiles" in action_lower or "loop" in action_lower or "repetitive" in action_lower or "puzzle_loop" in action_lower or "harmonize" in action_lower:
            target_location = "Clockwork Ruins"
            beat_id = "challenge_loops"
            suggested_challenge = "puzzle_loop_tiles"
            active_challenge = "puzzle_loop_tiles"
            objective = "Channel a continuous repetitive loop across all 5 resonance tiles."

        # 8. Return to Whispering Village
        elif "return to whispering village" in action_lower or "return_village" in action_lower or "walk back" in action_lower:
            target_location = "Whispering Village"
            beat_id = "village_return"
            objective = "Return to Whispering Village square."

        else:
            objective = f"Continue exploring {location}."
            beat_id = f"{location.lower().replace(' ', '_')}_default"

        proposed_state_changes["current_location"] = target_location

        proposal = {
            "proposed_next_event": f"Beat '{beat_id}' at {target_location}: {objective}",
            "beat_id": beat_id,
            "narrative_objective": objective,
            "target_location": target_location,
            "active_challenge": active_challenge,
            "suggested_challenge_category": suggested_challenge,
            "proposed_state_changes": proposed_state_changes,
            "rationale": (
                f"Player action '{player_action}' routed to beat '{beat_id}' at {target_location}."
            )
        }

        logger.info(f"Director planned beat '{beat_id}' at {target_location}")
        return proposal
