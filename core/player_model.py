"""
Adaptive Player Model Engine.
Calculates evidence-based, bounded updates to player preferences and computational mastery.
"""
from typing import Dict, Any
from models.player import PlayerProfile, AdaptiveTraits
from utils.validators import validate_preference_bounds

class PlayerModelEngine:
    """Manages continuous player modeling with smooth bounded deltas."""

    DELTA_STEP = 0.05  # Gentle update step per interaction

    @classmethod
    def record_action(
        cls,
        profile: PlayerProfile,
        action_category: str,
        challenge_success: bool = False,
        concept: str = ""
    ) -> PlayerProfile:
        """
        Updates player traits based on behavioral evidence.
        Categories: 'exploration', 'dialogue', 'puzzle', 'building'
        """
        traits = profile.traits

        # Bounded updates for play style preferences
        if action_category == "exploration":
            traits.exploration_preference = validate_preference_bounds(traits.exploration_preference + cls.DELTA_STEP)
            # Reversible balancing: slight dampening of other extremes
            traits.dialogue_preference = validate_preference_bounds(traits.dialogue_preference - (cls.DELTA_STEP * 0.2))

        elif action_category == "dialogue":
            traits.dialogue_preference = validate_preference_bounds(traits.dialogue_preference + cls.DELTA_STEP)
            traits.puzzle_preference = validate_preference_bounds(traits.puzzle_preference - (cls.DELTA_STEP * 0.2))

        elif action_category == "puzzle":
            traits.puzzle_preference = validate_preference_bounds(traits.puzzle_preference + cls.DELTA_STEP)
            traits.building_preference = validate_preference_bounds(traits.building_preference + (cls.DELTA_STEP * 0.3))

        elif action_category == "building":
            traits.building_preference = validate_preference_bounds(traits.building_preference + cls.DELTA_STEP)

        # Concept mastery updates (strictly based on validated puzzle performance)
        if concept and concept in traits.concept_mastery:
            current_mastery = traits.concept_mastery[concept]
            if challenge_success:
                # Substantial boost on success
                new_mastery = min(1.0, round(current_mastery + 0.35, 2))
            else:
                # Small experience gain for trying, never regression to 0
                new_mastery = min(1.0, round(current_mastery + 0.05, 2))
            traits.concept_mastery[concept] = new_mastery

        # Adapt challenge level based on overall mastery
        avg_mastery = sum(traits.concept_mastery.values()) / max(1, len(traits.concept_mastery))
        if avg_mastery >= 0.70:
            traits.challenge_level = 3
        elif avg_mastery >= 0.30:
            traits.challenge_level = 2
        else:
            traits.challenge_level = 1

        profile.traits = traits
        return profile
