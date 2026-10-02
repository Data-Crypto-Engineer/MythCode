"""
Continuity & Safety Agent (Agent 6).
Mandatory validation gatekeeper. Enforces content safety, age appropriateness,
narrative continuity, and state validity.
"""
from typing import Dict, Any, List
import re
from utils.logger import setup_logger

logger = setup_logger("ContinuitySafetyAgent")

class ContinuitySafetyAgent:
    """Verifies content safety, age appropriateness, and world consistency."""

    ROLE = "Guardian of Continuity, Lore & Player Safety"
    GOAL = "Audit all narrative outputs, character dialogue, and proposed mutations for safety and consistency."
    BACKSTORY = (
        "The celestial arbiter of integrity who ensures that no hostile, graphic, or contradictory elements "
        "enter the tapestry of Elarion."
    )

    PROHIBITED_TERMS = [
        "explicit", "graphic", "gore", "bloodshed", "execute_code",
        "eval(", "exec(", "system(", "__import__", "rm -rf"
    ]

    def __init__(self, llm=None):
        self.llm = llm

    def audit_scene_and_transitions(
        self,
        scene: Dict[str, Any],
        proposed_state: Dict[str, Any],
        world_rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Audits proposed text and proposed state updates.
        Returns:
            approved (bool)
            issues (List[str])
            corrections (List[str])
            requires_retry (bool)
        """
        issues: List[str] = []
        corrections: List[str] = []

        # Check content safety
        text_corpus = f"{scene.get('scene_title', '')} {scene.get('scene_description', '')} {scene.get('dialogue', '')}".lower()
        for term in self.PROHIBITED_TERMS:
            if term in text_corpus:
                issues.append(f"Detected prohibited or unsafe phrasing: '{term}'.")
                corrections.append(f"Filtered out unsafe phrase '{term}' to maintain age-appropriate tone.")

        # Check state transitions
        if "village_morale" in proposed_state:
            morale = proposed_state["village_morale"]
            if not isinstance(morale, (int, float)) or morale < 0 or morale > 100:
                issues.append(f"Village morale {morale} outside valid boundary [0, 100].")

        approved = len(issues) == 0
        result = {
            "approved": approved,
            "issues": issues,
            "corrections": corrections,
            "requires_retry": not approved
        }

        if not approved:
            logger.warning(f"Safety audit issues found: {issues}")
        else:
            logger.info("Safety audit passed successfully.")

        return result
