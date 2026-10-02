"""
Player Insight Agent (Agent 2).
Maintains continuously updated, evidence-based player adaptation models.
Uses bounded updates and avoids permanent stereotypes.
"""
from typing import Dict, Any, Optional
from utils.logger import setup_logger
from utils.validators import validate_preference_bounds

logger = setup_logger("PlayerInsightAgent")

class PlayerInsightAgent:
    """Monitors player behavior and refines difficulty and narrative pacing."""

    ROLE = "Adaptive Cognitive & Gameplay Analyst"
    GOAL = "Observe player choices and calibrate narrative complexity and instructional pacing."
    BACKSTORY = (
        "An empathetic scholar of mortal decision-making who measures curiosity, persistence, "
        "and algorithmic comprehension without imposing rigid labels."
    )

    def __init__(self, llm=None):
        self.llm = llm

    def analyze_interaction(
        self,
        current_traits: Dict[str, Any],
        player_action: str,
        challenge_result: Optional[bool] = None,
        concept: str = ""
    ) -> Dict[str, Any]:
        """
        Produces updated trait estimates and qualitative insights.
        """
        traits = dict(current_traits)
        action_lower = player_action.lower()

        insights = []

        if any(w in action_lower for w in ["explore", "examine", "look", "travel", "head to"]):
            traits["exploration_preference"] = validate_preference_bounds(
                traits.get("exploration_preference", 0.5) + 0.05
            )
            insights.append("Player exhibits high environmental curiosity.")

        if any(w in action_lower for w in ["talk", "speak", "ask", "plead", "dialogue", "converse"]):
            traits["dialogue_preference"] = validate_preference_bounds(
                traits.get("dialogue_preference", 0.5) + 0.05
            )
            insights.append("Player actively seeks narrative context and character rapport.")

        if any(w in action_lower for w in ["solve", "puzzle", "code", "guide", "loop", "condition", "sequence"]):
            traits["puzzle_preference"] = validate_preference_bounds(
                traits.get("puzzle_preference", 0.5) + 0.05
            )
            insights.append("Player demonstrates enthusiasm for computational mechanics.")

        if challenge_result is not None and concept:
            mastery = dict(traits.get("concept_mastery", {}))
            curr = mastery.get(concept, 0.0)
            if challenge_result:
                mastery[concept] = min(1.0, round(curr + 0.35, 2))
                insights.append(f"Demonstrated mastery milestone in '{concept}'.")
            else:
                mastery[concept] = min(1.0, round(curr + 0.05, 2))
                insights.append(f"Gained diagnostic experience in '{concept}'.")
            traits["concept_mastery"] = mastery

        return {
            "updated_traits": traits,
            "insights": insights,
            "recommended_guidance": "Encourage structured experimentation" if traits.get("puzzle_preference", 0.5) > 0.6 else "Support through immersive storytelling"
        }
