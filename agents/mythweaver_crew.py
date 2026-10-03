"""
CrewAI Orchestration Layer for MythCode.
Coordinates the 6 specialized agents with conditional execution and fallback safety.
Designed for cost-conscious, single-pass narrative cycles.
"""
from typing import Dict, Any, List, Optional
import time
from utils.logger import setup_logger
from utils.config import get_app_config
from utils.error_handler import handle_exception, fallback_narrative_scene
from models.world import WorldState
from models.player import PlayerProfile
from models.learning import LearningProgress
from core.state_validator import StateValidator
from core.player_model import PlayerModelEngine
from core.learning_engine import LearningEngine
from database.storage import get_storage

from .director_agent import DirectorAgent
from .player_insight_agent import PlayerInsightAgent
from .story_weaver_agent import StoryWeaverAgent
from .world_keeper_agent import WorldKeeperAgent
from .logic_learning_agent import LogicLearningAgent
from .continuity_safety_agent import ContinuitySafetyAgent

logger = setup_logger("MythWeaverCrew")

# Check if CrewAI is available in the Python runtime
HAS_CREWAI = False
try:
    import crewai  # type: ignore
    HAS_CREWAI = True
except Exception as e:
    HAS_CREWAI = False
    logger.warning(f"CrewAI import unavailable (fallback to native deterministic orchestration): {e}")

class MythWeaverCrew:
    """Orchestrates multi-agent execution pipeline for MythCode."""

    def __init__(self, db_path: str = "mythcode_storage.db"):
        self.config = get_app_config()
        self.storage = get_storage(db_path)
        self.learning_engine = LearningEngine()

        # Initialize the 6 agents
        self.director = DirectorAgent()
        self.player_insight = PlayerInsightAgent()
        self.story_weaver = StoryWeaverAgent()
        self.world_keeper = WorldKeeperAgent()
        self.logic_learning = LogicLearningAgent(self.learning_engine)
        self.continuity_safety = ContinuitySafetyAgent()

    def process_player_action(
        self,
        player_id: str,
        action_text: str,
        action_type: str = "exploration",
        puzzle_submission: Optional[Any] = None,
        puzzle_id: Optional[str] = None,
        action_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Coordinates full multi-agent gameplay cycle:
        1. Action interpretation
        2. Director Planning
        3. Player Insight update
        4. Story Weaving with Character Memory
        5. Computational Learning check (if puzzle)
        6. Continuity & Safety Audit
        7. Deterministic State Validation & Commit
        """
        start_time = time.time()
        telemetry: List[Dict[str, Any]] = []

        try:
            # 1. Fetch current persistence state
            player_dict = self.storage.get_player_profile(player_id) or {}
            player_profile = PlayerProfile.from_dict(player_dict)

            world_dict = self.storage.get_world_state(player_id) or {}
            world_state = WorldState.from_dict(world_dict)

            memories = self.storage.get_character_memories(player_id)
            learning_dict = self.storage.get_learning_progress(player_id) or {}
            learning_progress = LearningProgress.from_dict(learning_dict)

            # 2. Agent 1: Director planning
            director_plan = self.director.plan_next_beat(
                player_action=action_text,
                world_state=world_state.to_dict(),
                player_profile=player_profile.to_dict(),
                quest_state={},
                learning_progress=learning_progress.to_dict(),
                action_id=action_id
            )
            telemetry.append({
                "agent": "DirectorAgent",
                "output": director_plan["proposed_next_event"],
                "rationale": director_plan["rationale"]
            })

            # 3. Agent 2: Player Insight update
            challenge_result = None
            concept_name = ""
            puzzle_feedback = ""
            revealed_code = None

            # 4. Agent 5: Logic & Learning (conditional execution if puzzle submitted)
            if puzzle_id and puzzle_submission is not None:
                eval_res = self.logic_learning.evaluate_submission(
                    puzzle_id=puzzle_id,
                    user_input=puzzle_submission,
                    progress=learning_progress
                )
                challenge_result = eval_res["is_correct"]
                puzzle_feedback = eval_res["feedback"]
                revealed_code = eval_res["reveal"]
                learning_progress = eval_res["updated_progress"]
                concept_name = self.learning_engine.get_puzzle(puzzle_id).concept if self.learning_engine.get_puzzle(puzzle_id) else ""

                telemetry.append({
                    "agent": "LogicLearningAgent",
                    "output": f"Evaluated '{puzzle_id}': Success={challenge_result}",
                    "details": puzzle_feedback
                })

                # If guardian puzzle solved, mark guardian as operational!
                if puzzle_id == "puzzle_sequence_guardian" and challenge_result:
                    director_plan["proposed_state_changes"]["clockwork_guardian"] = "operational"
                    director_plan["proposed_state_changes"]["water_supply"] = "restored"
                    director_plan["proposed_state_changes"]["village_morale"] = min(100, world_state.village_morale + 20)
                    if "npc_relationships" not in director_plan["proposed_state_changes"]:
                        director_plan["proposed_state_changes"]["npc_relationships"] = {}
                    director_plan["proposed_state_changes"]["npc_relationships"]["Mira"] = "helped"
                    if "persistent_memories" not in director_plan["proposed_state_changes"]:
                        director_plan["proposed_state_changes"]["persistent_memories"] = []
                    director_plan["proposed_state_changes"]["persistent_memories"].append({
                        "key": "mira_sentinel_helped",
                        "summary": f"{player_profile.name} arranged the sequential movement runes, awakening the Clockwork Guardian and restoring mountain water to Mira's workshop and Whispering Village.",
                        "event_type": "puzzle_victory",
                        "timestamp": time.time()
                    })
                    player_profile.xp += 50
                    self.storage.add_character_memory(
                        player_id=player_id,
                        npc_name="Mira",
                        event_summary=f"{player_profile.name} solved the sequence alignment and awakened the Clockwork Guardian, saving Mira's workshop and the village springs!",
                        sentiment="positive"
                    )
                    # Add to Codex of Becoming (PART 9)
                    learning_progress.codex_entries.append({
                        "category": "mastery",
                        "concept": "Sequence",
                        "title": "Mastery of Sequential Flow",
                        "fantasy_lore": "Ordered incantations dictate physical motion. One misstep alters destination.",
                        "programming_concept": "Instructions execute line-by-line in exact chronological order.",
                        "code_example": "move_forward()\nmove_forward()\nturn_right()\nmove_forward()",
                        "mastery_status": "Mastered"
                    })

                # If conditional door solved, increase spirit trust
                elif puzzle_id == "puzzle_conditional_door" and challenge_result:
                    director_plan["proposed_state_changes"]["forest_spirit_trust"] = min(10, world_state.forest_spirit_trust + 4)
                    player_profile.xp += 50
                    self.storage.add_character_memory(
                        player_id=player_id,
                        npc_name="Sylvan",
                        event_summary="Player understood conditional evaluation and respected the runic seal.",
                        sentiment="positive"
                    )
                    # Add to Codex of Becoming (PART 9)
                    learning_progress.codex_entries.append({
                        "category": "mastery",
                        "concept": "Conditions",
                        "title": "Mastery of Conditional Gates",
                        "fantasy_lore": "Magical portals evaluate boolean reality: truth permits passage; falsehood seals the gate.",
                        "programming_concept": "if/else branches choose pathways based on boolean condition truth.",
                        "code_example": "if has_emerald_seal:\n    open_portal()\nelse:\n    search_for_seal()",
                        "mastery_status": "Mastered"
                    })

                # If loop puzzle solved, restore water supply!
                elif puzzle_id == "puzzle_loop_tiles" and challenge_result:
                    director_plan["proposed_state_changes"]["water_supply"] = "restored"
                    director_plan["proposed_state_changes"]["village_morale"] = min(100, world_state.village_morale + 25)
                    player_profile.xp += 100
                    self.storage.add_character_memory(
                        player_id=player_id,
                        npc_name="Elder Thorne",
                        event_summary="Player channeled the loop resonance and fully restored water to Whispering Village!",
                        sentiment="positive"
                    )
                    # Add to Codex of Becoming (PART 9)
                    learning_progress.codex_entries.append({
                        "category": "mastery",
                        "concept": "Loops",
                        "title": "Mastery of Iterative Resonance",
                        "fantasy_lore": "Energy channeled in loops repeats across multiple conduits without redundant effort.",
                        "programming_concept": "for loops repeat execution blocks across sequences or ranges.",
                        "code_example": "for step in range(5):\n    energize_tile(step)",
                        "mastery_status": "Mastered"
                    })

            # Calculate Player Level from XP
            player_profile.level = 1 + (player_profile.xp // 75)

            # Update player insight
            insight_res = self.player_insight.analyze_interaction(
                current_traits=player_profile.traits.to_dict(),
                player_action=action_text,
                challenge_result=challenge_result,
                concept=concept_name
            )
            player_profile.traits = player_profile.traits.from_dict(insight_res["updated_traits"])
            telemetry.append({
                "agent": "PlayerInsightAgent",
                "output": f"Challenge Level: {player_profile.traits.challenge_level}, Puzzle Pref: {player_profile.traits.puzzle_preference:.2f}",
                "insights": insight_res["insights"]
            })

            # Handle narrative consequences and persistent memories for explicit choices
            if action_id:
                if "npc_relationships" not in director_plan["proposed_state_changes"]:
                    director_plan["proposed_state_changes"]["npc_relationships"] = {}
                if "persistent_memories" not in director_plan["proposed_state_changes"]:
                    director_plan["proposed_state_changes"]["persistent_memories"] = []
                if "important_choices" not in director_plan["proposed_state_changes"]:
                    director_plan["proposed_state_changes"]["important_choices"] = []

                choice_meta = {
                    "help_mira_prep": (
                        "Helped Mira calibrate blueprint tolerances",
                        {"Mira": "helped_prep"},
                        "mira_prep",
                        f"{player_profile.name} helped Mira calibrate the Clockwork Sentinel's movement tolerances in her workshop."
                    ),
                    "ask_mira_clues": (
                        "Asked Mira for movement sequence advice",
                        {"Mira": "consulted"},
                        "mira_clues",
                        f"Mira instructed {player_profile.name} on the 4-step sequence (Forward, Forward, Turn Right, Forward)."
                    ),
                    "speak_mira": (
                        "Visited Mira at her workshop",
                        {"Mira": "met"} if world_state.get_npc_relationship("Mira") == "unmet" else {},
                        "mira_visit",
                        f"{player_profile.name} visited Mira's workshop in Whispering Village."
                    ),
                    "bypass_mira": (
                        "Bypassed Mira's workshop toward River Gorge",
                        {"Mira": "bypassed"} if world_state.get_npc_relationship("Mira") not in ("helped", "helped_prep") else {},
                        "mira_bypassed",
                        f"{player_profile.name} marched directly to the River Aqueduct without conferring with Mira."
                    ),
                    "speak_thorne": (
                        "Conferred with Elder Thorne",
                        {"Elder Thorne": "consulted"},
                        "thorne_consulted",
                        f"{player_profile.name} conferred with Elder Thorne about the village history."
                    ),
                    "return_village_triumph": (
                        "Celebrated water restoration in village square",
                        {"Elder Thorne": "reverent", "Mira": "helped"},
                        "village_triumph",
                        f"Whispering Village held a celebration for {player_profile.name} as mountain springs returned."
                    )
                }

                if action_id in choice_meta:
                    conseq_text, rel_dict, mem_key, mem_summary = choice_meta[action_id]
                    if rel_dict:
                        for k, v in rel_dict.items():
                            if world_state.get_npc_relationship(k) != "helped":
                                director_plan["proposed_state_changes"]["npc_relationships"][k] = v
                    director_plan["proposed_state_changes"]["persistent_memories"].append({
                        "key": mem_key,
                        "summary": mem_summary,
                        "event_type": "player_choice",
                        "timestamp": time.time()
                    })
                    director_plan["proposed_state_changes"]["important_choices"].append({
                        "choice_id": action_id,
                        "action_text": action_text,
                        "consequence": conseq_text,
                        "timestamp": time.time()
                    })

            # 5. Agent 4: World Keeper evaluation
            world_eval = self.world_keeper.evaluate_world_mutation(
                current_world=world_state,
                proposed_changes=director_plan["proposed_state_changes"],
                player_action=action_text
            )
            new_world_state = world_eval["validated_state"]
            telemetry.append({
                "agent": "WorldKeeperAgent",
                "output": "World transition verified." if world_eval["is_valid"] else "Rejected invalid transition.",
                "notes": world_eval["keeper_notes"]
            })

            # 6. Agent 3: Story Weaver scene generation
            scene = self.story_weaver.generate_scene(
                director_proposal=director_plan,
                world_state=new_world_state.to_dict(),
                player_profile=player_profile.to_dict(),
                character_memories=memories,
                learning_progress=learning_progress.to_dict(),
                player_action=action_text
            )
            telemetry.append({
                "agent": "StoryWeaverAgent",
                "output": f"Scene: '{scene['scene_title']}' at {scene['location']}",
                "speaker": scene["speaker"]
            })

            # 7. Agent 6: Continuity & Safety audit
            safety_res = self.continuity_safety.audit_scene_and_transitions(
                scene=scene,
                proposed_state=new_world_state.to_dict(),
                world_rules={}
            )
            telemetry.append({
                "agent": "ContinuitySafetyAgent",
                "output": "Approved" if safety_res["approved"] else "Requires Revision",
                "issues": safety_res["issues"]
            })

            # 8. Deterministic Commit to SQLite Persistence
            self.storage.save_player_profile(player_profile.to_dict())
            self.storage.save_world_state(player_id, new_world_state.to_dict())
            self.storage.save_learning_progress(player_id, learning_progress.to_dict())
            self.storage.record_interaction(player_id, action_text, new_world_state.current_location, scene["scene_title"])

            elapsed_ms = int((time.time() - start_time) * 1000)

            return {
                "success": True,
                "scene": scene,
                "world_state": new_world_state.to_dict(),
                "player_profile": player_profile.to_dict(),
                "learning_progress": learning_progress.to_dict(),
                "puzzle_feedback": puzzle_feedback,
                "puzzle_correct": challenge_result,
                "revealed_code": revealed_code,
                "active_challenge": director_plan.get("active_challenge"),
                "telemetry": telemetry,
                "execution_ms": elapsed_ms,
                "using_crewai": HAS_CREWAI
            }

        except Exception as e:
            err_report = handle_exception(e, f"MythWeaverCrew execution for action: {action_text}")
            fallback_scene = fallback_narrative_scene(world_state.current_location if 'world_state' in locals() else "Whispering Village", action_text)
            return {
                "success": False,
                "error": err_report,
                "scene": fallback_scene,
                "world_state": world_state.to_dict() if 'world_state' in locals() else {},
                "player_profile": player_profile.to_dict() if 'player_profile' in locals() else {},
                "learning_progress": learning_progress.to_dict() if 'learning_progress' in locals() else {},
                "telemetry": telemetry,
                "execution_ms": int((time.time() - start_time) * 1000),
                "using_crewai": False
            }
