"""
High-level Game Engine uniting state managers, CrewAI multi-agent pipeline, and deterministic rules.
"""
from typing import Dict, Any, Optional
from database.storage import get_storage
from core.state_manager import StateManager
from core.learning_engine import LearningEngine
from core.quest_manager import QuestManager
from agents.mythweaver_crew import MythWeaverCrew
from utils.logger import setup_logger

logger = setup_logger("GameEngine")

class GameEngine:
    """Primary application interface coordinating persistent game sessions."""

    def __init__(self, player_id: str = "player_default", db_path: str = "mythcode_storage.db"):
        self.player_id = player_id
        self.db_path = db_path
        self.state_mgr = StateManager(db_path, player_id)
        self.quest_mgr = QuestManager()
        self.learning_engine = LearningEngine()
        self.crew = MythWeaverCrew(db_path)

    def initialize_session(self, **kwargs):
        """Initializes or loads a persistent session for the player."""
        profile = self.state_mgr.load_or_init_player(**kwargs)
        world = self.state_mgr.load_or_init_world()
        learning = self.state_mgr.load_or_init_learning()
        logger.info(f"Initialized session for '{profile.name}' ({profile.role}) in {world.kingdom}")
        return {
            "player": profile.to_dict(),
            "world": world.to_dict(),
            "learning": learning.to_dict(),
            "quests": [q.to_dict() for q in self.quest_mgr.get_all_quests()]
        }

    def export_backup(self) -> str:
        """Returns JSON backup of game state."""
        return self.state_mgr.storage.export_backup_json(self.player_id)

    def import_backup(self, json_data: str) -> bool:
        """Imports and restores game state from JSON backup."""
        return self.state_mgr.storage.import_backup_json(self.player_id, json_data)

    def execute_action(self, action_text: str, action_type: str = "exploration", action_id: Optional[str] = None) -> Dict[str, Any]:
        """Dispatches an exploratory or narrative action through the multi-agent pipeline."""
        return self.crew.process_player_action(
            player_id=self.player_id,
            action_text=action_text,
            action_type=action_type,
            action_id=action_id
        )

    def solve_challenge(self, puzzle_id: str, submission: Any) -> Dict[str, Any]:
        """Submits a computational puzzle solution to the Logic & Learning pipeline."""
        return self.crew.process_player_action(
            player_id=self.player_id,
            action_text=f"Attempted challenge '{puzzle_id}'",
            action_type="puzzle",
            puzzle_submission=submission,
            puzzle_id=puzzle_id
        )

    def get_hint(self, puzzle_id: str) -> Dict[str, Any]:
        """Requests an in-character pedagogical hint from the learning engine."""
        learning = self.state_mgr.load_or_init_learning()
        hint, updated_progress = self.learning_engine.request_hint(puzzle_id, learning)
        self.state_mgr.commit_learning(updated_progress)
        return {"hint": hint, "hint_uses": updated_progress.hint_uses.get(puzzle_id, 0)}

    def reset_game(self):
        """Clears all session data and resets world state cleanly."""
        self.state_mgr.reset_all()
        logger.info(f"Session '{self.player_id}' has been reset.")
