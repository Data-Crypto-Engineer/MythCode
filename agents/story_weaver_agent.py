"""
Story Weaver Agent (Agent 3).
Generates evolving fantasy narratives, dialogue, and choices grounded in world state and memory.
Specialized for Chapter I: The Silence of the Springs with rich storybook prose and explicit choice IDs.
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

        # 1. Base Story Beats Library for Chapter I & Beyond
        beats = {
            # --- Whispering Village Beats ---
            "inspect_fountain": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Investigating the Fountain's Dried Springs",
                "description": (
                    f"You kneel beside the great fountain with your {companion} perched alertly upon the granite rim. "
                    f"Scraping away dried mineral crusts, your fingers trace intricate runic conduits etched into the stone. "
                    f"Your {affinity} affinity detects a faint magical vibration pulsing through the bedrock: the springs have not "
                    f"naturally evaporated. Downstream, the main waterwheel sluice gates at the River Aqueduct have been locked shut!"
                ),
                "speaker": "Elder Thorne",
                "dialogue": f"{hero_name}, your {affinity.lower()} perception is acute. The sluice gates downstream are shut tight, and Mira has been working relentlessly on the clockwork sentinel. Will you confer with her, or march directly to the aqueduct?",
                "choices": [
                    {"id": "speak_mira", "text": "Walk over to Mira's workshop to ask about the seized sluice gates."},
                    {"id": "follow_aqueduct", "text": "Follow the dry stone aqueduct trail downstream toward the River Gorge."},
                    {"id": "speak_thorne", "text": "Ask Elder Thorne about the history of the ancient waterwheel."}
                ]
            },
            "dialogue_mira": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Mira's Workshop in the Village",
                "description": (
                    f"Sparks scatter across Mira's workbench as she tightens a brass caliper. Her eyes widen as she notices your {keepsake}. "
                    f"\"By the gears of Elarion—a {hero_role}!\" she exclaims, unrolling an inked parchment schematic. "
                    f"\"The silence of the springs began yesterday. The giant waterwheel at the river gorge is sound, but its clutch is locked. "
                    f"The ancient Clockwork Sentinel that operates the clutch is frozen on the stone dais, awaiting instructions. "
                    f"If you can arrange its movement sequence correctly, it will step to the altar and unlock the mountain waters!\""
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"{hero_name}, the sentinel has no intuition—it executes movement instructions line-by-line, in exact order. Step one mistake, and the gears jam! Will you accompany me to the aqueduct?",
                "choices": [
                    {"id": "follow_aqueduct", "text": "Accompany Mira downstream to the River Aqueduct."},
                    {"id": "help_mira_prep", "text": "Offer to help Mira inspect and calibrate her blueprints first."},
                    {"id": "ask_mira_clues", "text": "Ask Mira how the sentinel's command dais works before leaving."},
                    {"id": "inspect_fountain", "text": "Double-check the village fountain pipes first."}
                ]
            },
            "dialogue_mira_triumph": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Mira's Workshop — Waters Unleashed",
                "description": (
                    f"Water gurgles merrily through the copper cooling pipes of Mira's workshop. Polished brass gauges spin in steady rhythm. "
                    f"Mira pushes her welding goggles up onto her forehead, wiping away a smear of machine grease with the back of her glove as she sees you enter with your {companion}."
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"\"{hero_name}! Listen to that sound—the river waterwheel is turning like clockwork! Every conduit in the village is flowing again because of that sequence you aligned. You didn't just save my workshop; you saved Whispering Village!\"",
                "choices": [
                    {"id": "confer_mira_grove", "text": "Ask Mira what she knows about the disturbances reported in the Ancient Grove."},
                    {"id": "inspect_mira_inventions", "text": "Ask Mira about her experimental clockwork prototypes on the workbench."},
                    {"id": "return_village", "text": "Head back to the village square."}
                ]
            },
            "help_mira_prep": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Calibrating Blueprints at the Workshop",
                "description": (
                    f"You lean over the workbench beside Mira, using your {hero_role} eye to examine the gear ratios and friction tolerances on the parchment. "
                    f"Together, you and Mira refine the movement plan for the Clockwork Sentinel. Your {companion} trills approvingly as Mira inks in the final calibrations."
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"\"Brilliant calculation, {hero_name}! These compensations ensure the sentinel won't skid on the damp river flags. With this sequence verified, we're ready for the gorge dais!\"",
                "choices": [
                    {"id": "follow_aqueduct", "text": "March together to the River Aqueduct to awaken the sentinel."},
                    {"id": "ask_mira_clues", "text": "Review the exact movement rune order once more."},
                    {"id": "inspect_fountain", "text": "Take a quick glance at the village fountain before leaving."}
                ]
            },
            "confer_mira_grove": {
                "chapter": "Chapter II: The Sylvan Gateway",
                "title": "Consulting Mira on the Ancient Grove",
                "description": (
                    f"Mira unrolls a broader map of Elarion, tracing the aqueduct's upstream sources into the emerald canopy of the Ancient Grove. "
                    f"Your {companion} hops closer to inspect the inked boundary lines."
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"\"The water reaches our valley from the Grove, but the forest spirit Sylvan guards the upper threshold with conditional runic gates. To pass, you'll need more than a simple sequence—you'll have to evaluate truth conditions! Be careful up there, {hero_name}.\"",
                "choices": [
                    {"id": "goto_grove", "text": "Set out for the misty canopy of the Ancient Grove."},
                    {"id": "return_village", "text": "Return to Whispering Village square."}
                ]
            },
            "inspect_mira_inventions": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Mira's Clockwork Workshop Wonders",
                "description": (
                    f"Rows of brass pendulums, clockwork songbirds, and steam-driven micro-pumps line the shelves. "
                    f"Mira beams with pride as she tinkers with a miniature harmonic resonator beside your {companion}."
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"\"With running water powering my lathe again, I can finally finish these prototypes! As a token of our partnership, whenever you need mechanical advice, my doors are open, {hero_name}.\"",
                "choices": [
                    {"id": "confer_mira_grove", "text": "Ask about the Ancient Grove to the north."},
                    {"id": "return_village", "text": "Step back outside into the village square."}
                ]
            },
            "ask_mira_clues": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Deciphering the Sentinel Dais",
                "description": (
                    f"Mira traces a 3x3 checkered grid in the stone dust with a brass rod while your {companion} watches closely. "
                    f"\"The sentinel starts facing north at the edge of the chasm,\" she explains. \"The clutch pedestal sits two paces forward "
                    f"and one pace to the right. To reach it safely across the tiles without tumbling into the empty sluice trench, you must queue: "
                    f"FORWARD, FORWARD, TURN RIGHT, and FORWARD. Order is everything—actions arranged in a sequence dictate its exact path!\""
                ),
                "speaker": "Mira the Inventor",
                "dialogue": "Remember, the runes execute in the exact order you slot them into the dais. Ready to awaken the mechanism?",
                "choices": [
                    {"id": "follow_aqueduct", "text": "Proceed to the River Aqueduct to awaken the sentinel."},
                    {"id": "inspect_fountain", "text": "Return to the village fountain."}
                ]
            },
            "dialogue_thorne": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Council with Elder Thorne",
                "description": (
                    f"Elder Thorne leans heavily against his wooden staff near the empty irrigation channels. "
                    f"\"The kingdom of Elarion flourished because the ancients bound logic and magic together,\" he murmurs. "
                    f"\"When the waters flow, the heart of our realm beats true. If the aqueduct cannot be restored, the grove "
                    f"and ruins will surely wither next.\""
                ),
                "speaker": "Elder Thorne",
                "dialogue": f"As a {hero_role}, your hands carry the craft of our ancestors, {hero_name}. Guide Mira and awaken the mechanism.",
                "choices": [
                    {"id": "speak_mira", "text": "Speak with Mira at her workshop."},
                    {"id": "follow_aqueduct", "text": "Head straight to the River Aqueduct downstream."}
                ]
            },

            # --- River Aqueduct Beats ---
            "aqueduct_arrival": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "The Seized Waterwheel at the Aqueduct",
                "description": (
                    f"The roar of the river is reduced to a hollow drip. Towering oak and brass cogs hang suspended across the gorge. "
                    f"Upon a raised checkered flagstone platform stands the bronze Clockwork Sentinel. Its chest-plate displays three "
                    f"dormant crystalline runes, and its mechanical joints are poised in silence before the empty sluice clutch."
                ),
                "speaker": "Mira the Inventor",
                "dialogue": f"Here it is, {hero_name}! The command altar stands before the sentinel. Arrange the movement sequence so it traverses the tiles and unlocks the clutch!",
                "choices": [
                    {"id": "interact_sentinel", "text": "Step up to the command dais to arrange the movement runes (Sequence Puzzle)."},
                    {"id": "examine_gears", "text": "Examine the massive waterwheel teeth and chasm stones."},
                    {"id": "return_village", "text": "Walk back to Whispering Village."}
                ]
            },
            "examine_gears": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Inspecting the Clockwork Waterwheel",
                "description": (
                    f"You peer through the massive brass spokes of the waterwheel. The clutch teeth are fully intact, but held rigidly "
                    f"by a spring-loaded locking bar. A mechanical linkage leads directly from the locking bar to the pedestal at the end "
                    f"of the checkered stone platform. Only when the sentinel steps onto the final pressure plate will the clutch release."
                ),
                "speaker": "Mira the Inventor",
                "dialogue": "The mechanism is structurally sound! It only needs the sentinel's weight on the activation plate. Step to the dais!",
                "choices": [
                    {"id": "interact_sentinel", "text": "Step up to the command dais to arrange the movement runes."},
                    {"id": "return_village", "text": "Return to Whispering Village."}
                ]
            },
            "challenge_sequence": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Control Altar: The Sentinel's Movement Program",
                "description": (
                    f"The brass pedestal before you pulses with soft amber light. Four rune sockets await your commands: "
                    f"Forward strides and directional pivots. Below, the Clockwork Sentinel stands balanced, its copper gears humming "
                    f"as it awaits the sequence of instructions."
                ),
                "speaker": "Sentinel Dais Inscription",
                "dialogue": "Awaiting sequential rune arrangement. Actions will execute chronologically from first slot to last.",
                "choices": [
                    {"id": "interact_sentinel", "text": "Queue movement runes on the control dais."},
                    {"id": "examine_gears", "text": "Step back to review the waterwheel chasm."},
                    {"id": "return_village", "text": "Step back to the trail."}
                ]
            },

            # --- Village Triumph Beat (Post-Sequence Solve) ---
            "village_return_triumph": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "The Springs Awaken in Whispering Village",
                "description": (
                    f"You return to the village square to the joyous sound of rushing water! Crystal-clear mountain springs surge "
                    f"into the central fountain, splashing over carved granite rims and filling the village irrigation canals. "
                    f"Villagers gather in celebration, cheering for {hero_name} the {hero_role} and their faithful {companion}."
                ),
                "speaker": "Elder Thorne",
                "dialogue": f"The silence has broken! The springs sing once more, all thanks to your mastery of sequence. You have proven yourself a true protector of Elarion, {hero_name}!",
                "choices": [
                    {"id": "speak_mira", "text": "Speak with Mira about the next regional disturbance."},
                    {"id": "goto_grove", "text": "Venture north toward the Ancient Grove to investigate reports of agitated forest spirits."},
                    {"id": "goto_ruins", "text": "Delve into the subterranean Clockwork Ruins."}
                ]
            },
            "village_return": {
                "chapter": "Chapter I: The Silence of the Springs",
                "title": "Whispering Village Square",
                "description": (
                    f"You return to the cobblestone square of Whispering Village. The morning breeze rustles through the eaves. "
                    f"Elder Thorne gazes down the valley, awaiting news of the waterwheel."
                ),
                "speaker": "Elder Thorne",
                "dialogue": f"Welcome back, {hero_name}. Have you uncovered the truth behind the seized waterwheel at the gorge?",
                "choices": [
                    {"id": "follow_aqueduct", "text": "Return downstream to the River Aqueduct."},
                    {"id": "speak_mira", "text": "Speak with Mira at her workshop."},
                    {"id": "inspect_fountain", "text": "Examine the fountain once more."}
                ]
            },

            # --- Ancient Grove Beats ---
            "grove_arrival": {
                "chapter": "Chapter II: The Sylvan Gateway",
                "title": "The Misty Canopy of the Ancient Grove",
                "description": (
                    f"Silver mist coils among massive willow boughs glowing with emerald moss. In the clearing rises an ancient "
                    f"runic stone gateway. Sylvan, the Forest Spirit, manifests in a swirl of shimmering leaves."
                ),
                "speaker": "Sylvan the Forest Spirit",
                "dialogue": f"Mortals seek water with iron tools. But our sacred springs heed only those who understand conditionality. The gateway tests whether your condition is True or False.",
                "choices": [
                    {"id": "solve_door_puzzle", "text": "Approach the runic portal and evaluate the opening condition (Conditional Puzzle)."},
                    {"id": "return_village", "text": "Return to Whispering Village."}
                ]
            },
            "challenge_conditions": {
                "chapter": "Chapter II: The Sylvan Gateway",
                "title": "The Sylvan Runic Gateway Test",
                "description": (
                    f"The moss-covered doorway displays glowing script: 'IF the traveler carries the Emerald Seal of Concord, "
                    f"unseal the archway; ELSE remain dormant stone.' Three choices lie before you."
                ),
                "speaker": "Sylvan the Forest Spirit",
                "dialogue": "Evaluate the condition with true logic, traveler. An if/else branch never wavers from mathematical truth.",
                "choices": [
                    {"id": "solve_door_puzzle", "text": "Select your condition evaluation for the gateway."},
                    {"id": "return_village", "text": "Step back to Whispering Village."}
                ]
            },

            # --- Clockwork Ruins Beats ---
            "ruins_arrival": {
                "chapter": "Chapter III: Resonating Conduits",
                "title": "The Subterranean Conduit Chamber",
                "description": (
                    f"Descending ancient spiral stairs carved into bedrock, you enter a vast cavern beneath the reservoir. "
                    f"Five crystalline resonance tiles stretch across the floor, leading to a massive hydraulic pump core."
                ),
                "speaker": "Resonant Altar Echo",
                "dialogue": "A single pulse will fade before reaching the cisterns. Only a sustained iterative loop across all five conduits will awaken the subterranean pumps.",
                "choices": [
                    {"id": "solve_loop_puzzle", "text": "Harmonize the five energy tiles using a repetitive cycle (Loop Puzzle)."},
                    {"id": "return_village", "text": "Ascend back to the surface."}
                ]
            },
            "challenge_loops": {
                "chapter": "Chapter III: Resonating Conduits",
                "title": "The Resonating Conduit of Five",
                "description": (
                    f"Five crystalline tiles gleam before you. Instead of chanting five separate manual commands, your {hero_role} "
                    f"training allows you to channel an iterative loop that counts from 0 through 4."
                ),
                "speaker": "Resonant Altar Echo",
                "dialogue": "Channel the loop spell. In programming and runecraft, loops conquer repetition.",
                "choices": [
                    {"id": "solve_loop_puzzle", "text": "Activate the 5-step conduit loop."},
                    {"id": "return_village", "text": "Step back to the surface."}
                ]
            }
        }

        # Select base beat or fallback
        scene_data = beats.get(beat_id)
        if not scene_data:
            if location == "River Aqueduct":
                scene_data = beats["aqueduct_arrival"]
            elif location == "Ancient Grove":
                scene_data = beats["grove_arrival"]
            elif location == "Clockwork Ruins":
                scene_data = beats["ruins_arrival"]
            else:
                scene_data = beats["inspect_fountain"]

        base_scene = {
            "chapter": scene_data.get("chapter", "Chapter I: The Silence of the Springs"),
            "scene_title": scene_data["title"],
            "scene_description": scene_data["description"],
            "speaker": scene_data["speaker"],
            "dialogue": scene_data["dialogue"],
            "choices": scene_data["choices"],
            "location": location,
            "event_category": "narrative_encounter",
            "active_challenge": active_challenge
        }

        # Natural narrative memory and relationship weaving
        npc_name = base_scene["speaker"]
        npc_simple = npc_name.split()[0] if npc_name else ""
        npc_relationships = world_state.get("npc_relationships", {})
        npc_rel = npc_relationships.get(npc_simple, "neutral")
        is_water_restored = (world_state.get("water_supply") == "restored" or world_state.get("clockwork_guardian") in ("operational", "repaired"))

        # 1. Mira memory & relationship continuity
        if npc_simple == "Mira":
            if is_water_restored or npc_rel in ("helped", "allied"):
                # If water is restored or Mira was helped, use triumphant dialogue
                if beat_id in ("dialogue_mira", "dialogue_mira_triumph"):
                    base_scene["scene_title"] = "Mira's Workshop — Waters Unleashed"
                    base_scene["scene_description"] = (
                        f"Water gurgles merrily through the copper cooling pipes of Mira's workshop. Polished brass gauges spin in steady rhythm. "
                        f"Mira pushes her welding goggles up onto her forehead, wiping away machine grease as she sees you enter with your {companion}."
                    )
                    base_scene["dialogue"] = (
                        f"\"{hero_name}! Listen to that sound—the river waterwheel is turning like clockwork! Every conduit in the village is flowing again "
                        f"because of that sequence you aligned. You didn't just save my workshop; you saved Whispering Village!\""
                    )
                    base_scene["choices"] = [
                        {"id": "confer_mira_grove", "text": "Ask Mira what she knows about disturbances in the Ancient Grove."},
                        {"id": "inspect_mira_inventions", "text": "Ask Mira about her experimental clockwork prototypes."},
                        {"id": "return_village", "text": "Head back to the village square."}
                    ]
            elif npc_rel == "helped_prep" and beat_id == "dialogue_mira":
                base_scene["dialogue"] = (
                    f"\"Welcome back, {hero_name}! Those friction calibrations we calculated on the blueprints earlier are ready. "
                    f"The Clockwork Sentinel awaits our command at the gorge! Ready to head down?\""
                )
            elif npc_rel == "bypassed" and beat_id == "dialogue_mira":
                base_scene["dialogue"] = (
                    f"\"Ah, {hero_name}! I saw you marching straight down to the aqueduct earlier. Did you inspect the seized sentinel dais? "
                    f"Its commands must be sequenced with mathematical precision!\""
                )
            elif npc_rel in ("consulted", "met") and beat_id == "dialogue_mira":
                base_scene["dialogue"] = (
                    f"\"Welcome back to the workshop, {hero_name}! Remember the 4-step sequence on the dais: Forward, Forward, Turn Right, Forward. "
                    f"Order is everything—the sentinel follows instructions line-by-line!\""
                )

        # 2. Elder Thorne memory & relationship continuity
        elif npc_simple == "Elder":
            if is_water_restored:
                if beat_id == "inspect_fountain":
                    base_scene["scene_title"] = "The Singing Springs of Whispering Village"
                    base_scene["scene_description"] = (
                        f"Crystal-clear mountain water cascades through the carved runic channels of the village fountain, churning "
                        f"into the deep stone basin with a joyful roar. Your {companion} bathes its feathers at the water's edge. "
                        f"Villagers fill clay amphorae with laughter, celebrating the end of the drought."
                    )
                    base_scene["dialogue"] = f"\"{hero_name}, look upon the fruits of your labor! The ancient conduits hum with life once more. The village will never forget your deed.\""
                    base_scene["choices"] = [
                        {"id": "speak_mira", "text": "Visit Mira at her workshop."},
                        {"id": "goto_grove", "text": "Travel north toward the Ancient Grove to investigate reports of agitated spirits."},
                        {"id": "goto_ruins", "text": "Explore the subterranean Clockwork Ruins beneath the valley."}
                    ]
                elif beat_id not in ("village_return_triumph",):
                    base_scene["dialogue"] = f"\"{hero_name}, our hearts overflow just as the cisterns do. You brought back the lifeblood of Whispering Village. Walk with honor throughout Elarion.\""

        # 3. River Aqueduct World State Overrides
        if world_state.get("clockwork_guardian") in ("operational", "repaired") and location == "River Aqueduct":
            base_scene["scene_description"] += " The Clockwork Guardian hums quietly, its crystalline core spinning in smooth rhythm."

        if is_water_restored and location == "River Aqueduct":
            base_scene["scene_description"] += " Below in the gorge, the giant waterwheel spins with immense hydraulic power, splashing foaming spray against the mossy cliffs."

        # Enrich with Gemini Storyteller if available (narrative prose strictly grounded in structured facts)
        enriched_scene = self.gemini.enrich_scene(
            base_scene=base_scene,
            player_profile=player_profile,
            world_state=world_state,
            character_memories=character_memories,
            recent_action=player_action
        )

        return enriched_scene
