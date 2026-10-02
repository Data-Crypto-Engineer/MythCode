"""
State Manager coordinates active gameplay state with persistent SQLite storage.
Supports rollback and validated transaction checkpoints.
"""
from typing import Dict, Any, Optional
import json
import os
from models.player import PlayerProfile
from models.world import WorldState
from models.learning import LearningProgress
from database.storage import SQLiteStorage, get_storage
from utils.logger import setup_logger

logger = setup_logger("StateManager")

class StateManager:
    """Provides atomic state loading, saving, and rollback."""

    def __init__(self, db_path: str = "mythcode_storage.db", player_id: str = "player_default"):
        self.storage = get_storage(db_path)
        self.player_id = player_id
        self._last_valid_world: Optional[WorldState] = None

    def load_or_init_world(self, initial_world_path: str = "data/initial_world.json") -> WorldState:
        saved = self.storage.get_world_state(self.player_id)
        if saved:
            world = WorldState.from_dict(saved)
        else:
            if os.path.exists(initial_world_path):
                with open(initial_world_path, "r", encoding="utf-8") as f:
                    init_data = json.load(f)
                    world = WorldState.from_dict(init_data)
            else:
                world = WorldState()
            self.storage.save_world_state(self.player_id, world.to_dict())

        self._last_valid_world = world
        return world

    def load_or_init_player(self, name: str = "Aria", role: str = "Clockwork Scholar", style: str = "Analytical") -> PlayerProfile:
        saved = self.storage.get_player_profile(self.player_id)
        if saved:
            return PlayerProfile.from_dict(saved)
        profile = PlayerProfile(id=self.player_id, name=name, role=role, adventure_style=style)
        self.storage.save_player_profile(profile.to_dict())
        return profile

    def load_or_init_learning(self) -> LearningProgress:
        saved = self.storage.get_learning_progress(self.player_id)
        if saved:
            return LearningProgress.from_dict(saved)
        progress = LearningProgress()
        self.storage.save_learning_progress(self.player_id, progress.to_dict())
        return progress

    def commit_world(self, world: WorldState):
        self._last_valid_world = world
        self.storage.save_world_state(self.player_id, world.to_dict())

    def commit_player(self, profile: PlayerProfile):
        self.storage.save_player_profile(profile.to_dict())

    def commit_learning(self, progress: LearningProgress):
        self.storage.save_learning_progress(self.player_id, progress.to_dict())

    def rollback_world(self) -> WorldState:
        """Restores the last known valid world state in case of validation or AI failure."""
        logger.warning(f"Rolling back world state for player {self.player_id}")
        if self._last_valid_world:
            return self._last_valid_world
        return self.load_or_init_world()

    def reset_all(self):
        """Purges stored state for clean new game."""
        self.storage.reset_session(self.player_id)
        self._last_valid_world = None
