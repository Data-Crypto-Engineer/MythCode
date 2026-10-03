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
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

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
        Enriches narrative prose and dialogue using Gemini strictly grounded in structured facts.
        Gemini receives structured world & player facts and creates narrative around them.
        The deterministic game state is authoritative — Gemini never invents state or changes reality.
        """
        if not self.is_available:
            return base_scene

        speaker = base_scene.get('speaker', 'Narrator')
        speaker_simple = speaker.split()[0] if speaker else "Narrator"
        npc_relationships = world_state.get('npc_relationships', {})
        speaker_rel = npc_relationships.get(speaker_simple, "neutral")

        # Format persistent memories (bullet points)
        p_mems = world_state.get('persistent_memories', [])
        persistent_mems_summary = [m.get("summary") for m in p_mems[-4:]] if p_mems else []
        if not persistent_mems_summary and character_memories:
            persistent_mems_summary = [m.get("event_summary") for m in character_memories[:3]]

        prompt = f"""You are the narrative stylist for MythCode, an enchanted fantasy adventure.
Your role is to craft atmospheric wording and dialogue around the following AUTHORITATIVE FACTS.
The deterministic facts below are absolute law. You MUST NOT contradict them or invent persistent state, items, or quests.

[STRUCTURED FACTS]
PLAYER:
* name = {player_profile.get('name', 'Aria')} ({player_profile.get('pronouns', 'they/them')})
* role = {player_profile.get('role', 'Rune Engineer')}
* companion = {player_profile.get('companion', 'Clockwork Owl')}
* affinity = {player_profile.get('magical_affinity', 'Arcane')}
* keepsake = {player_profile.get('keepsake', 'Brass Chrono-Gear')}
* personality = {player_profile.get('personality', 'Curious & Patient')}

WORLD:
* current location = {world_state.get('current_location', 'Whispering Village')}
* water supply = {world_state.get('water_supply', 'damaged')} (springs restored: {world_state.get('water_supply') == 'restored'})
* clockwork guardian = {world_state.get('clockwork_guardian', 'inactive')}
* village morale = {world_state.get('village_morale', 60)}%
* forest spirit trust = {world_state.get('forest_spirit_trust', 0)}/10
* persistent memories = {persistent_mems_summary}

NPC CONTEXT:
* speaker = {speaker}
* relationship = {speaker_rel}

SHORT-TERM CONTEXT:
* recent action = "{recent_action}"
* scene beat = "{base_scene.get('scene_title')}"

RULES:
1. Ground your dialogue strictly in the relationship and memory. If relationship='helped', the NPC MUST acknowledge that the player helped them.
2. If water is restored, the environment MUST be vibrant with flowing springs; do not describe dry fountains.
3. Keep scene description to 2-3 atmospheric, storybook sentences.
4. Keep dialogue to 1-2 authentic character sentences addressing the player.
5. Do NOT invent new items, skills, or quest completions not listed in the facts.

Respond ONLY with valid JSON:
{{
  "scene_description": "2-3 sentences of atmospheric prose reflecting the established facts",
  "dialogue": "1-2 sentences of authentic dialogue from {speaker} reflecting relationship and memories"
}}"""

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
