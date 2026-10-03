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
                    director_plan["proposed_state_changes"]["village_morale"] = world_state.village_morale + 15
                    player_profile.xp += 50
                    self.storage.add_character_memory(
                        player_id=player_id,
                        npc_name="Mira",
                        event_summary="Player solved the sequence alignment and awakened the Clockwork Guardian!",
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
