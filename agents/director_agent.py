"""
Director Agent (Agent 1).
Central experience coordinator proposing narrative transitions and pacing.
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

        # Determine suggested challenge & agent focus
        suggested_challenge = None
        target_location = location
        proposed_state_changes = {}

        if "aqueduct" in action_lower or "waterwheel" in action_lower or "river" in action_lower:
            target_location = "River Aqueduct"
            suggested_challenge = "puzzle_sequence_guardian"
            required_agents = ["StoryWeaver", "WorldKeeper", "LogicLearning"]
            objective = "Reach the seized sluice gates and restore mechanical flow."

        elif "grove" in action_lower or "forest" in action_lower or "spirit" in action_lower:
            target_location = "Ancient Grove"
            suggested_challenge = "puzzle_conditional_door"
            required_agents = ["StoryWeaver", "ContinuitySafety"]
            objective = "Commune with Sylvan the Forest Spirit and evaluate the runic seals."

        elif "ruins" in action_lower or "vault" in action_lower or "subterranean" in action_lower or "tile" in action_lower:
            target_location = "Clockwork Ruins"
            suggested_challenge = "puzzle_loop_tiles"
            required_agents = ["StoryWeaver", "LogicLearning"]
            objective = "Energize the ancient subterranean resonance conduits using iterative loops."

        elif "village" in action_lower or "return" in action_lower:
            target_location = "Whispering Village"
            required_agents = ["StoryWeaver", "WorldKeeper"]
            objective = "Converse with elders and check village morale."

        else:
            required_agents = ["StoryWeaver", "PlayerInsight"]
            objective = "Explore the surroundings and discover new pathways."

        proposed_state_changes["current_location"] = target_location

        proposal = {
            "proposed_next_event": f"Transition to {target_location} to pursue '{objective}'",
            "narrative_objective": objective,
            "required_agent_contributions": required_agents,
            "suggested_challenge_category": suggested_challenge,
            "proposed_state_changes": proposed_state_changes,
            "rationale": (
                f"Player indicated intent '{player_action}'. Given preference profile "
                f"(Puzzle: {traits.get('puzzle_preference', 0.5):.2f}, Exploration: {traits.get('exploration_preference', 0.5):.2f}), "
                f"routing to {target_location} optimizes narrative engagement."
            )
        }

        logger.info(f"Director planned: {proposal['proposed_next_event']}")
        return proposal
