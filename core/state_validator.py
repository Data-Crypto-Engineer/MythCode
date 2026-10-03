"""
Deterministic state validation engine.
Ensures world invariants, prevents impossible transitions, and preserves state integrity.
"""
from typing import Dict, Any, Tuple, List
from models.world import WorldState
from utils.validators import validate_stat_bounds

class StateValidator:
    """Validates world state updates proposed by agents or user interactions."""

    VALID_WATER_STATES = {"damaged", "investigating", "restoring", "restored"}
    VALID_GUARDIAN_STATES = {"inactive", "awakening", "operational", "repaired"}
    ALLOWED_LOCATIONS = {
        "Whispering Village",
        "Ancient Grove",
        "River Aqueduct",
        "Clockwork Ruins"
    }

    @classmethod
    def validate_transition(
        cls,
        current_state: WorldState,
        proposed_updates: Dict[str, Any]
    ) -> Tuple[bool, List[str], WorldState]:
        """
        Validates proposed updates against current state.
        Returns:
            is_valid (bool): Whether all proposed updates are legitimate.
            issues (List[str]): Explanations for any rejected fields.
            cloned_state (WorldState): A sanitized copy with validated changes applied.
        """
        issues = []
        # Clone current state
        new_data = current_state.to_dict()

        # 1. Location validation
        if "current_location" in proposed_updates:
            target_loc = proposed_updates["current_location"]
            if target_loc not in cls.ALLOWED_LOCATIONS:
                issues.append(f"Rejected unknown location '{target_loc}'.")
            else:
                new_data["current_location"] = target_loc
                if target_loc not in new_data["discovered_locations"]:
                    new_data["discovered_locations"].append(target_loc)

        # 2. Water supply validation
        if "water_supply" in proposed_updates:
            proposed_water = proposed_updates["water_supply"]
            if proposed_water not in cls.VALID_WATER_STATES:
                issues.append(f"Invalid water supply status '{proposed_water}'.")
            else:
                new_data["water_supply"] = proposed_water

        # 3. Guardian status
        if "clockwork_guardian" in proposed_updates:
            proposed_guard = proposed_updates["clockwork_guardian"]
            if proposed_guard not in cls.VALID_GUARDIAN_STATES:
                issues.append(f"Invalid clockwork guardian status '{proposed_guard}'.")
            else:
                new_data["clockwork_guardian"] = proposed_guard

        # 4. Numeric bounds (Village Morale 0-100, Trust -10 to +10)
        if "village_morale" in proposed_updates:
            raw_morale = proposed_updates["village_morale"]
            try:
                new_data["village_morale"] = validate_stat_bounds(raw_morale, 0, 100)
            except (ValueError, TypeError):
                issues.append(f"Rejected non-numeric morale value '{raw_morale}'.")

        if "forest_spirit_trust" in proposed_updates:
            raw_trust = proposed_updates["forest_spirit_trust"]
            try:
                new_data["forest_spirit_trust"] = validate_stat_bounds(raw_trust, -10, 10)
            except (ValueError, TypeError):
                issues.append(f"Rejected non-numeric trust value '{raw_trust}'.")

        # 5. Completed Quests - prevent duplicates
        if "completed_quests" in proposed_updates:
            for q in proposed_updates["completed_quests"]:
                if q not in new_data["completed_quests"]:
                    new_data["completed_quests"].append(q)

        # 6. Important Choices - append only
        if "important_choices" in proposed_updates:
            for c in proposed_updates["important_choices"]:
                if c not in new_data["important_choices"]:
                    new_data["important_choices"].append(c)

        # 7. NPC Relationships - merge without contradiction
        if "npc_relationships" in proposed_updates and isinstance(proposed_updates["npc_relationships"], dict):
            if "npc_relationships" not in new_data:
                new_data["npc_relationships"] = {}
            new_data["npc_relationships"].update(proposed_updates["npc_relationships"])

        # 8. Persistent Memories - keyed replacement to maintain continuity
        if "persistent_memories" in proposed_updates and isinstance(proposed_updates["persistent_memories"], list):
            if "persistent_memories" not in new_data:
                new_data["persistent_memories"] = []
            for pm in proposed_updates["persistent_memories"]:
                pm_key = pm.get("key")
                if pm_key:
                    new_data["persistent_memories"] = [m for m in new_data["persistent_memories"] if m.get("key") != pm_key]
                new_data["persistent_memories"].append(pm)

        is_valid = len(issues) == 0
        validated_state = WorldState.from_dict(new_data)
        return is_valid, issues, validated_state
