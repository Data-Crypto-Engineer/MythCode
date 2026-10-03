"""
Director Agent (Agent 1).
Central experience coordinator proposing narrative transitions and pacing.
Accurately routes using explicit, stable choice IDs (Requirement 3) with fallback to natural text.
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
        learning_progress: Dict[str, Any],
        action_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes the next narrative event, required agents, and proposed state changes.
        Prefers explicit action_id if provided.
        """
        location = world_state.get("current_location", "Whispering Village")
        traits = player_profile.get("traits", {})
        action_lower = player_action.lower()
        a_id = (action_id or "").strip().lower()

        suggested_challenge = None
        target_location = location
        proposed_state_changes = {}
        beat_id = "general_exploration"
        active_challenge = None
        objective = "Explore Elarion and investigate the water mystery."

        # Explicit Choice ID Mapping (Requirement 3: Stable IDs independent of text changes)
        if a_id in ("examine_fountain", "inspect_fountain"):
            target_location = "Whispering Village"
            beat_id = "inspect_fountain"
            objective = "Analyze the dried conduits and runes of the village fountain."

        elif a_id in ("speak_mira", "visit_mira"):
            target_location = "Whispering Village"
            # Route to triumph beat if waterwheel/springs are already restored
            is_mira_helped = (
                world_state.get("clockwork_guardian") == "operational" or
                world_state.get("water_supply") == "restored" or
                world_state.get("npc_relationships", {}).get("Mira") in ("helped", "allied")
            )
            beat_id = "dialogue_mira_triumph" if is_mira_helped else "dialogue_mira"
            objective = "Celebrate the awakened waterwheel with Mira." if is_mira_helped else "Confer with Mira at her workshop about the waterwheel mechanism."

        elif a_id in ("help_mira_prep", "assist_mira_blueprints"):
            target_location = "Whispering Village"
            beat_id = "help_mira_prep"
            objective = "Assist Mira in verifying the clockwork movement schematics."
            proposed_state_changes["village_morale"] = min(100, world_state.get("village_morale", 60) + 5)

        elif a_id in ("confer_mira_grove", "ask_mira_forest"):
            target_location = "Whispering Village"
            beat_id = "confer_mira_grove"
            objective = "Consult Mira on her knowledge of the Ancient Grove and Sylvan's portal."

        elif a_id in ("inspect_mira_inventions", "mira_workshop_gadgets"):
            target_location = "Whispering Village"
            beat_id = "inspect_mira_inventions"
            objective = "Inspect Mira's clockwork inventions and gear prototypes."

        elif a_id in ("thank_mira", "celebrate_mira"):
            target_location = "Whispering Village"
            beat_id = "thank_mira"
            objective = "Share credit with Mira for saving the village springs."

        elif a_id in ("ask_mira_clues", "ask_mechanism_clues"):
            target_location = "Whispering Village"
            beat_id = "ask_mira_clues"
            objective = "Learn how the sentinel's command dais executes movement instructions."

        elif a_id in ("bypass_mira", "ignore_mira"):
            target_location = "River Aqueduct"
            beat_id = "aqueduct_arrival"
            objective = "March directly to the River Aqueduct without consulting Mira."

        elif a_id in ("speak_thorne", "dialogue_thorne"):
            target_location = "Whispering Village"
            beat_id = "dialogue_thorne"
            objective = "Speak with Elder Thorne regarding village morale and rations."

        elif a_id in ("follow_aqueduct", "head_to_river", "goto_aqueduct", "waterwheel_inspect", "travel_aqueduct"):
            target_location = "River Aqueduct"
            beat_id = "aqueduct_arrival"
            objective = "Reach the seized waterwheel at the River Aqueduct."

        elif a_id in ("interact_sentinel", "solve_guardian_puzzle", "solve_sequence", "examine_sentinel"):
            target_location = "River Aqueduct"
            beat_id = "challenge_sequence"
            suggested_challenge = "puzzle_sequence_guardian"
            active_challenge = "puzzle_sequence_guardian"
            objective = "Arrange the sequential movement runes to guide the Clockwork Sentinel to the altar."

        elif a_id in ("examine_gears", "inspect_cogs"):
            target_location = "River Aqueduct"
            beat_id = "examine_gears"
            objective = "Inspect the seized waterwheel gear teeth and clutch mechanism."

        elif a_id in ("return_village_triumph", "celebrate_village"):
            target_location = "Whispering Village"
            beat_id = "village_return_triumph"
            objective = "Return to Whispering Village as water gushes back into the fountains."

        elif a_id in ("return_village", "walk_back_village"):
            target_location = "Whispering Village"
            beat_id = "village_return"
            objective = "Walk back to the Whispering Village square."

        elif a_id in ("goto_grove", "venture_grove"):
            target_location = "Ancient Grove"
            beat_id = "grove_arrival"
            objective = "Seek audience with Sylvan the Forest Spirit under the ancient canopy."

        elif a_id in ("solve_door_puzzle", "solve_condition", "evaluate_gate"):
            target_location = "Ancient Grove"
            beat_id = "challenge_conditions"
            suggested_challenge = "puzzle_conditional_door"
            active_challenge = "puzzle_conditional_door"
            objective = "Evaluate the condition required to unseal the Sylvan gateway."

        elif a_id in ("goto_ruins", "delve_ruins"):
            target_location = "Clockwork Ruins"
            beat_id = "ruins_arrival"
            objective = "Explore the subterranean energy vault beneath the dried reservoir."

        elif a_id in ("solve_loop_puzzle", "solve_loop", "activate_loop"):
            target_location = "Clockwork Ruins"
            beat_id = "challenge_loops"
            suggested_challenge = "puzzle_loop_tiles"
            active_challenge = "puzzle_loop_tiles"
            objective = "Channel a continuous repetitive loop across all 5 resonance tiles."

        # Fallback Text Matching (for backward compatibility)
        elif "fountain" in action_lower or "pipes" in action_lower or "stonework" in action_lower:
            target_location = "Whispering Village"
            beat_id = "inspect_fountain"
            objective = "Analyze the dried conduits of the village fountain."

        elif "mira" in action_lower or "workshop" in action_lower:
            target_location = "Whispering Village"
            beat_id = "dialogue_mira"
            objective = "Confer with Mira at her workshop about the waterwheel mechanism."

        elif "clue" in action_lower or "how the sentinel" in action_lower:
            target_location = "Whispering Village"
            beat_id = "ask_mira_clues"
            objective = "Learn how the sentinel's command dais works."

        elif "elder" in action_lower or "thorne" in action_lower:
            target_location = "Whispering Village"
            beat_id = "dialogue_thorne"
            objective = "Speak with Elder Thorne regarding the town's diminishing rations."

        elif "travel downstream" in action_lower or "aqueduct" in action_lower or "head_to_river" in action_lower:
            target_location = "River Aqueduct"
            beat_id = "aqueduct_arrival"
            objective = "Reach the seized sluice gates at the River Aqueduct."

        elif "guardian" in action_lower or "sequence" in action_lower or "control altar" in action_lower or "sentinel" in action_lower:
            target_location = "River Aqueduct"
            beat_id = "challenge_sequence"
            suggested_challenge = "puzzle_sequence_guardian"
            active_challenge = "puzzle_sequence_guardian"
            objective = "Assemble the ordered sequence of movement commands to guide the guardian."

        elif "gear" in action_lower or "cogs" in action_lower:
            target_location = "River Aqueduct"
            beat_id = "examine_gears"
            objective = "Inspect the seized waterwheel gears."

        elif "ancient grove" in action_lower or "grove" in action_lower:
            target_location = "Ancient Grove"
            beat_id = "grove_arrival"
            objective = "Seek audience with Sylvan the Forest Spirit."

        elif "portal" in action_lower or "conditional" in action_lower:
            target_location = "Ancient Grove"
            beat_id = "challenge_conditions"
            suggested_challenge = "puzzle_conditional_door"
            active_challenge = "puzzle_conditional_door"
            objective = "Evaluate the condition required to unseal the Sylvan gateway."

        elif "ruins" in action_lower or "subterranean" in action_lower or "tile" in action_lower:
            target_location = "Clockwork Ruins"
            beat_id = "ruins_arrival"
            objective = "Explore the subterranean energy vault."

        elif "return to whispering village" in action_lower or "return_village" in action_lower:
            target_location = "Whispering Village"
            beat_id = "village_return"
            objective = "Return to Whispering Village square."

        proposed_state_changes["current_location"] = target_location

        proposal = {
            "proposed_next_event": f"Beat '{beat_id}' at {target_location}: {objective}",
            "beat_id": beat_id,
            "action_id": a_id,
            "narrative_objective": objective,
            "target_location": target_location,
            "active_challenge": active_challenge,
            "suggested_challenge_category": suggested_challenge,
            "proposed_state_changes": proposed_state_changes,
            "rationale": f"Player action (id='{a_id}', text='{player_action}') routed to beat '{beat_id}' at {target_location}."
        }

        logger.info(f"Director planned beat '{beat_id}' at {target_location} (action_id={a_id})")
        return proposal
