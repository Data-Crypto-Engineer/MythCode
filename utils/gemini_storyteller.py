"""
Gemini Storyteller Integration for MythCode (PART 6).
Provides optional narrative enrichment and contextual NPC dialogue.
Uses standard library urllib for zero-dependency resilience across all Python environments.
Never controls puzzle validation, state clamping, or database integrity.
"""
import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List
from utils.logger import setup_logger
from utils.config import get_app_config

logger = setup_logger("GeminiStoryteller")

class GeminiStoryteller:
    """Optional generative AI layer for personalized atmospheric prose and NPC dialogue."""

    def __init__(self):
        self.config = get_app_config()
        self.api_key = self.config.get("api_key") or os.getenv("GEMINI_API_KEY", "")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    @property
    def is_available(self) -> bool:
        placeholders = {"YOUR_API_KEY_HERE", "MY_GEMINI_API_KEY", "YOUR_GEMINI_API_KEY", ""}
        return bool(self.api_key and self.api_key not in placeholders)

    def enrich_scene(
        self,
        base_scene: Dict[str, Any],
        player_profile: Dict[str, Any],
        world_state: Dict[str, Any],
        character_memories: List[Dict[str, Any]],
        recent_action: str
    ) -> Dict[str, Any]:
        """
        Attempts to enrich the scene description and dialogue using Gemini.
        Returns base_scene untouched if API is missing or fails.
        """
        if not self.is_available:
            return base_scene

        prompt = f"""You are the master narrator and character voice of MythCode, an enchanted fantasy adventure in the realm of Elarion.
The player has just taken the following action: "{recent_action}".

Player Context:
- Name: {player_profile.get('name', 'Aria')} ({player_profile.get('pronouns', 'they/them')})
- Fantasy Calling: {player_profile.get('role', 'Rune Engineer')}
- Appearance: {player_profile.get('appearance', 'Inquisitive scholar')}
- Hair: {player_profile.get('hair_style', 'Braided crown')} in {player_profile.get('hair_color', 'Auburn')}
- Attire: {player_profile.get('outfit', 'Leather scholar coat')}
- Personality: {player_profile.get('personality', 'Curious & Patient')}
- Magical Affinity: {player_profile.get('magical_affinity', 'Arcane')}
- Companion Familiar: {player_profile.get('companion', 'Clockwork Owl')}
- Keepsake: {player_profile.get('keepsake', 'Brass Chrono-Gear')}
- Learning Approach: {player_profile.get('learning_style', 'Hands-on Experimentation')}

World Context:
- Location: {world_state.get('current_location', 'Whispering Village')}
- Water Supply: {world_state.get('water_supply', 'damaged')}
- Clockwork Guardian: {world_state.get('clockwork_guardian', 'inactive')}
- Forest Spirit Trust: {world_state.get('forest_spirit_trust', 0)}/10
- Village Morale: {world_state.get('village_morale', 60)}%

Speaker: {base_scene.get('speaker', 'Elder Thorne')}
Relevant Character Memories: {[m.get('event_summary') for m in character_memories[:2]]}

Please provide an enriched response in valid JSON matching this schema:
{{
  "scene_description": "2-3 sentences of atmospheric, storybook description reflecting their action and affinity",
  "dialogue": "In-character dialogue from the speaker addressing the player and mentioning their companion or keepsake when fitting"
}}

Respond ONLY with valid JSON. Do not include markdown codeblocks or extra text."""

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 300,
                    "responseMimeType": "application/json"
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=4.0) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    clean_text = raw_text.strip()
                    if clean_text.startswith("```json"):
                        clean_text = clean_text[7:]
                    if clean_text.endswith("```"):
                        clean_text = clean_text[:-3]
                    parsed = json.loads(clean_text.strip())

                    cloned = dict(base_scene)
                    if parsed.get("scene_description"):
                        cloned["scene_description"] = parsed["scene_description"]
                    if parsed.get("dialogue"):
                        cloned["dialogue"] = parsed["dialogue"]
                    logger.info("Successfully enriched scene using Gemini API.")
                    return cloned
        except Exception as e:
            logger.warning(f"Gemini enrichment failed gracefully (fallback to deterministic scene): {e}")

        return base_scene
