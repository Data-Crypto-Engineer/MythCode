"""
Story Weaver Agent (Agent 3).
Generates evolving fantasy narratives, dialogue, and choices grounded in world state and memory.
Enriched with Gemini AI storytelling (PART 6) and responsive deterministic beat templates.
"""
from typing import Dict, Any, List, Optional
from utils.logger import setup_logger
from utils.gemini_storyteller import GeminiStoryteller

logger = setup_logger("StoryWeaverAgent")

class StoryWeaverAgent:
    """Crafts rich story scenes and character interactions reflecting past player deeds."""

    ROLE = "Mythic Bard & World Chronicler"
    GOAL = "Compose vivid, atmospheric scenes and character dialogue that weave computational thinking into high fantasy."
    BACKSTORY = (
        "A weaver of living legends in Elarion, skilled in turning gears, runic conditions, and magical repetitions "
        "into emotional, high-stakes folklore."
    )

    def __init__(self, llm=None):
        self.llm = llm
        self.gemini = GeminiStoryteller()

    def generate_scene(
        self,
        director_proposal: Dict[str, Any],
        world_state: Dict[str, Any],
        player_profile: Dict[str, Any],
        character_memories: List[Dict[str, Any]],
        learning_progress: Dict[str, Any],
        player_action: str = ""
    ) -> Dict[str, Any]:
        """
        Synthesizes a structured, highly responsive scene based on the Director's planned beat.
        """
        beat_id = director_proposal.get("beat_id", "general_exploration")
        location = director_proposal.get("target_location", world_state.get("current_location", "Whispering Village"))
        active_challenge = director_proposal.get("active_challenge")

        hero_name = player_profile.get("name", "Aria")
        hero_role = player_profile.get("role", "Rune Engineer")
        companion = player_profile.get("companion", "Clockwork Owl")
        affinity = player_profile.get("magical_affinity", "Arcane")
        keepsake = player_profile.get("keepsake", "Brass Chrono-Gear")

        # 1. Base Story Beats Library
        beats = {
            # --- Whispering Village Beats ---
            "inspect_fountain": {
                "title": "Investigating the Fountain's Dry Reservoir",
                "description": (
                    f"You kneel beside the intricately carved granite fountain with your {companion} peering closely. "
                    f"Scraping away dried sediment, your fingers trace ancient runic conduit veins. They lead directly downstream "
                    f"toward the River Aqueduct, with a secondary harmonic channel veering off toward the Ancient Grove. "
                    f"The problem isn't a natural drought—someone or something has deliberately seized the sluice regulators!"
                ),
                "speaker": "Elder Thorne",
                "dialogue": f"{hero_name}, your {affinity.lower()} senses don't deceive you. The old aqueduct gears downstream have seized, and the forest spirits upstream have turned cold. Where will you direct your steps?",
                "choices": [
                    {"id": "visit_mira", "text": "Walk over to Mira's workshop to ask about the aqueduct gears."},
                    {"id": "head_to_river", "text": "Travel downstream toward the River Aqueduct."},
                    {"id": "goto_grove", "text": "Venture into the misty canopy of the Ancient Grove."}
                ]
            },
            "dialogue_mira": {
                "title": "Mira's Clockwork Workshop",
                "description": (
                    f"Sparks flutter from Mira's workbench as she tightens a brass cog. Her eyes widen as she spots your {keepsake}. "
                    f"\"A fellow practitioner of mechanical craft!\" she beams. She unrolls a parchment schematic of the River Aqueduct. "
                    f"\"The main waterwheel sluice is blocked by our dormant Clockwork Sentinel. If you can command it through the proper "
                    f"step-by-step sequence of motions, it can reach the activation altar and release the clutch!\""
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"Take this advice, {hero_name}: sentinels execute instructions sequentially, line-by-line. Order is everything! Will you come with me to the Aqueduct?",
                "choices": [
                    {"id": "head_to_river", "text": "Travel downstream toward the River Aqueduct with Mira."},
                    {"id": "inspect_fountain", "text": "Double-check the village fountain pipes first."},
                    {"id": "goto_grove", "text": "Ask about the forest spirits in the Ancient Grove instead."}
                ]
            },
            "dialogue_thorne": {
                "title": "Council with Elder Thorne",
                "description": (
                    f"Elder Thorne leans heavily against his wooden staff near the town hall. Villagers nod respectfully as you and your "
                    f"{companion} approach. \"The kingdom's elders have charted three pathways to restore our waters: mechanical repair at the Aqueduct, "
                    f"spiritual harmony in the Grove, or channeling the subterranean conduits in the old ruins.\""
                ),
                "speaker": "Elder Thorne",
                "dialogue": f"As a {hero_role}, your wisdom is our greatest hope, {hero_name}. Which path calls to your instincts?",
                "choices": [
                    {"id": "head_to_river", "text": "Head to the River Aqueduct to inspect the machinery."},
                    {"id": "goto_grove", "text": "Venture into the Ancient Grove to petition Sylvan the Forest Spirit."},
                    {"id": "goto_ruins", "text": "Delve into the subterranean Clockwork Ruins."}
                ]
            },

            # --- River Aqueduct Beats ---
            "aqueduct_arrival": {
                "title": "The Seized Waterwheel at the Aqueduct",
                "description": (
                    f"You arrive at the roaring gorge where towering oak and brass gears hang suspended over dry river flagstones. "
                    f"A dormant Clockwork Sentinel rests on a raised stone platform. Before it lies a 3x3 checkered stone pathway "
                    f"leading to the crystal activation pedestal."
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"{hero_name}, the guardian is ready for instructions! Input the exact step-by-step movement program so it advances forward and turns right to the altar.",
                "choices": [
                    {"id": "solve_guardian_puzzle", "text": "Step up to the control altar to guide the Clockwork Guardian (Sequence Puzzle)."},
                    {"id": "inspect_cogs", "text": "Examine the seized teeth of the massive waterwheel."},
                    {"id": "return_village", "text": "Return to Whispering Village."}
                ]
            },
            "challenge_sequence": {
                "title": "Control Altar: Guiding the Clockwork Sentinel",
                "description": (
                    f"The brass pedestal before you pulses with glowing runic glyphs. Four command slots await your instructions: "
                    f"Forward movements and turns. Below, the Clockwork Guardian awaits your program."
                ),
                "speaker": "Sentinel Control Interface",
                "dialogue": "Awaiting sequential execution queue. Instruction order determines the sentinel's spatial destination.",
                "choices": [
                    {"id": "solve_guardian_puzzle", "text": "Enter and execute the movement sequence on the altar."},
                    {"id": "consult_hint", "text": "Consult the Arcane Archives for a sequence hint."},
                    {"id": "step_back_aqueduct", "text": "Step back to survey the aqueduct."}
                ]
            },

            # --- Ancient Grove Beats ---
            "grove_arrival": {
                "title": "The Misty Canopy of the Ancient Grove",
                "description": (
                    f"Silver mist coils among massive willow boughs glowing with emerald moss. In the clearing rises an ancient "
                    f"runic stone gateway. Sylvan, the Forest Spirit, manifests in a swirl of shimmering leaves."
                ),
                "speaker": "Sylvan the Forest Spirit",
                "dialogue": f"Mortals come seeking water with iron tools. But our sacred springs heed only those who understand conditionality. The gateway tests whether your condition is True or False.",
                "choices": [
                    {"id": "solve_door_puzzle", "text": "Approach the runic portal and evaluate the opening condition (Conditional Puzzle)."},
                    {"id": "plead_harmony", "text": f"Present your {affinity} affinity and assure Sylvan of your peaceful intent."},
                    {"id": "return_village", "text": "Return to Whispering Village."}
                ]
            },
            "challenge_conditions": {
                "title": "The Sylvan Runic Gateway Test",
                "description": (
                    f"The moss-covered doorway displays ancient glowing script: 'IF the traveler carries the Emerald Seal of Concord, "
                    f"unseal the archway; ELSE remain dormant stone.' Three choices lie before you."
                ),
                "speaker": "Sylvan the Forest Spirit",
                "dialogue": "Evaluate the condition with true logic, traveler. An if/else branch never wavers from mathematical truth.",
                "choices": [
                    {"id": "solve_door_puzzle", "text": "Select your condition evaluation for the gateway."},
                    {"id": "consult_hint", "text": "Request an arcane hint from Sylvan."},
                    {"id": "step_back_grove", "text": "Step back to inspect the grove clearing."}
                ]
            },

            # --- Clockwork Ruins Beats ---
            "ruins_arrival": {
                "title": "The Subterranean Conduit Chamber",
                "description": (
                    f"Descending ancient spiral stairs carved into bedrock, you enter a vast cavern beneath the reservoir. "
                    f"Five crystalline resonance tiles stretch across the floor, leading to a massive hydraulic pump core."
                ),
                "speaker": "Resonant Altar Echo",
                "dialogue": "A single pulse will fade before reaching the cisterns. Only a sustained iterative loop across all five conduits will awaken the subterranean pumps.",
                "choices": [
                    {"id": "solve_loop_puzzle", "text": "Harmonize the five energy tiles using a repetitive cycle (Loop Puzzle)."},
                    {"id": "survey_chamber", "text": "Examine the crystalline conduits running through the walls."},
                    {"id": "return_aqueduct", "text": "Ascend back to the River Aqueduct."}
                ]
            },
            "challenge_loops": {
                "title": "The Resonating Conduit of Five",
                "description": (
                    f"Five crystalline tiles gleam before you. Instead of chanting five separate manual commands, your {hero_role} "
                    f"training allows you to channel an iterative loop that counts from 0 through 4."
                ),
                "speaker": "Resonant Altar Echo",
                "dialogue": "Channel the loop spell. In programming and runecraft, loops conquer repetition.",
                "choices": [
                    {"id": "solve_loop_puzzle", "text": "Activate the 5-step conduit loop."},
                    {"id": "consult_hint", "text": "Seek a hint on loop syntax."},
                    {"id": "step_back_ruins", "text": "Step back to examine the cavern."}
                ]
            },

            # --- Village Return ---
            "village_return": {
                "title": "Back at the Village Square",
                "description": (
                    f"You return to Whispering Village. The air is tense with anticipation. Villagers look to you eagerly "
                    f"as your {companion} perches on the edge of the dried fountain."
                ),
                "speaker": "Elder Thorne",
                "dialogue": f"Welcome back, {hero_name}. Have you uncovered news from the Aqueduct or the Grove?",
                "choices": [
                    {"id": "visit_mira", "text": "Speak with Mira at her workshop."},
                    {"id": "head_to_river", "text": "Head back out to the River Aqueduct."},
                    {"id": "goto_grove", "text": "Journey into the Ancient Grove."}
                ]
            }
        }

        # Select base beat or fallback to location default
        scene_data = beats.get(beat_id)
        if not scene_data:
            # Fallback to general location
            if location == "River Aqueduct":
                scene_data = beats["aqueduct_arrival"]
            elif location == "Ancient Grove":
                scene_data = beats["grove_arrival"]
            elif location == "Clockwork Ruins":
                scene_data = beats["ruins_arrival"]
            else:
                scene_data = beats["dialogue_thorne"]

        base_scene = {
            "scene_title": scene_data["title"],
            "scene_description": scene_data["description"],
            "speaker": scene_data["speaker"],
            "dialogue": scene_data["dialogue"],
            "choices": scene_data["choices"],
            "location": location,
            "event_category": "narrative_encounter",
            "active_challenge": active_challenge
        }

        # Personalize dialogue with character memories
        npc_name = base_scene["speaker"]
        relevant_mems = [m for m in character_memories if m.get("npc_name") == npc_name or npc_name in m.get("npc_name", "")]
        if relevant_mems:
            mem_summary = relevant_mems[0]["event_summary"]
            base_scene["dialogue"] = f"(Remembering: '{mem_summary}') " + base_scene["dialogue"]

        # World state overrides: Guardian awakened or Water restored
        if world_state.get("clockwork_guardian") in ("operational", "repaired") and location == "River Aqueduct":
            base_scene["scene_description"] += " The Clockwork Guardian hums quietly, its crystalline core spinning in smooth rhythm."

        if world_state.get("water_supply") == "restored":
            base_scene["scene_description"] += " Crystal-clear water cascades once again through the channels of Elarion!"
            if base_scene["speaker"] == "Elder Thorne":
                base_scene["dialogue"] = f"Praise the stars, {hero_name}! The fountains are filled and our kingdom is saved!"

        # 2. Enrich with Gemini Storyteller if available (PART 6)
        enriched_scene = self.gemini.enrich_scene(
            base_scene=base_scene,
            player_profile=player_profile,
            world_state=world_state,
            character_memories=character_memories,
            recent_action=player_action
        )

        return enriched_scene
