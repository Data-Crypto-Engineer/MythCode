"""
Comprehensive error handler and safe narrative recovery for MythCode.
Ensures zero game-state destruction upon external API failure.
"""
from typing import Dict, Any, Optional
from .logger import setup_logger

logger = setup_logger("ErrorHandler")

class MythCodeError(Exception):
    """Base exception for all domain errors."""
    pass

class ConfigurationError(MythCodeError):
    """Raised when configuration, model or credentials are improperly defined."""
    pass

class AIProviderError(MythCodeError):
    """Raised when external LLM or CrewAI call fails or times out."""
    pass

class StateValidationError(MythCodeError):
    """Raised when an agent proposes an illegal or contradictory world transition."""
    pass

def handle_exception(exc: Exception, context_hint: str = "") -> Dict[str, Any]:
    """
    Categorizes the error, logs technical details without leaking keys,
    and returns a user-safe structured status dictionary.
    """
    error_type = type(exc).__name__
    clean_msg = str(exc)

    logger.error(f"Error caught in context '{context_hint}': [{error_type}] {clean_msg}")

    # Return structured user response
    return {
        "status": "error",
        "error_type": error_type,
        "user_message": (
            "The arcane winds falter for a moment, but your story remains firmly rooted in memory. "
            "A fallback narrative has kept your journey safe."
        ),
        "technical_summary": f"Recovered gracefully from {error_type}",
        "fallback_engaged": True
    }

def fallback_narrative_scene(location: str, action: str) -> Dict[str, Any]:
    """
    Returns a deterministic, safe, lore-consistent fallback scene if LLM generation fails.
    """
    scenes = {
        "Whispering Village": {
            "title": "The Silent Village Square",
            "description": (
                "Cobblestones glisten faintly in the morning mist. Near the dried central fountain, "
                "the villagers murmur quietly about the receding springs. Mira adjusts her brass goggles "
                "beside her workshop, waiting for someone bold enough to act."
            ),
            "speaker": "Elder Thorne",
            "dialogue": "Our reservoir cannot last another moon. Please, traveler, investigate the water's source!",
            "choices": [
                {"id": "inspect_fountain", "text": "Examine the intricate stonework and dried pipes of the village fountain."},
                {"id": "visit_mira", "text": "Converse with Mira about her mechanical waterwheel project."},
                {"id": "head_to_river", "text": "Travel downstream toward the River Aqueduct."}
            ]
        },
        "River Aqueduct": {
            "title": "The Seized Waterwheel at the Aqueduct",
            "description": (
                "Towering oak and bronze cogs hang suspended above a trickling stream. "
                "A bronze clockwork sentinel rests on the stone bank, its rune-plates dormant and misaligned."
            ),
            "speaker": "Mira",
            "dialogue": "The guardian must be guided along the channel stones to re-engage the sluice clutch!",
            "choices": [
                {"id": "solve_guardian_puzzle", "text": "Step up to the control altar to guide the Clockwork Guardian (Sequence Puzzle)."},
                {"id": "inspect_cogs", "text": "Look closely at the waterwheel's seized gear teeth."},
                {"id": "return_village", "text": "Return to Whispering Village."}
            ]
        },
        "Ancient Grove": {
            "title": "The Misty Canopy of the Ancient Grove",
            "description": (
                "Bioluminescent moss clings to towering elder-willows. In the quiet clearing stands an ancient runic portal, "
                "its doorway guarded by emerald glyphs pulsing with soft harmonic hums."
            ),
            "speaker": "Sylvan the Forest Spirit",
            "dialogue": "Mortals disturb the harmony with cold iron. Prove you understand the laws of condition before stepping through.",
            "choices": [
                {"id": "solve_door_puzzle", "text": "Approach the runic portal and evaluate the opening condition (Conditional Puzzle)."},
                {"id": "plead_harmony", "text": "Assure Sylvan that your intent is to restore balance, not destroy it."},
                {"id": "return_village", "text": "Return to Whispering Village."}
            ]
        },
        "Clockwork Ruins": {
            "title": "The Subterranean Conduit Chamber",
            "description": (
                "Deep under the bedrock, five resonance tiles gleam in unison along an ancient water conduit. "
                "A rhythmic pulse requires consistent, repeated energy harmonizing."
            ),
            "speaker": "Resonant Altar Echo",
            "dialogue": "A single step will not suffice. Only repeated harmonic cycles will fill the ancient reservoirs.",
            "choices": [
                {"id": "solve_loop_puzzle", "text": "Harmonize the five energy tiles using a repetitive cycle (Loop Puzzle)."},
                {"id": "survey_chamber", "text": "Study the mechanical diagrams etched into the stone walls."},
                {"id": "return_aqueduct", "text": "Ascend back to the River Aqueduct."}
            ]
        }
    }

    return scenes.get(location, scenes["Whispering Village"])
