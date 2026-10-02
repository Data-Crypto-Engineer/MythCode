"""
SQLite storage engine for persistent sessions, character memory, and learning progress.
Handles connection lifecycles, schema migrations, and JSON serialization.
"""
import sqlite3
import json
import os
import time
from typing import Optional, Dict, Any, List
from utils.logger import setup_logger

logger = setup_logger("Storage")

class SQLiteStorage:
    def __init__(self, db_path: str = "mythcode_storage.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self):
        self._init_db()

    def _init_db(self):
        """Initializes tables for game sessions, world state, memories, and learning progress."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Player profiles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_profiles (
                    player_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    adventure_style TEXT,
                    traits_json TEXT NOT NULL,
                    current_quest_id TEXT,
                    updated_at REAL
                )
            """)

            # World states
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS world_states (
                    player_id TEXT PRIMARY KEY,
                    kingdom TEXT NOT NULL,
                    current_location TEXT NOT NULL,
                    water_supply TEXT NOT NULL,
                    forest_spirit_trust INTEGER,
                    clockwork_guardian TEXT,
                    village_morale INTEGER,
                    completed_quests_json TEXT,
                    discovered_locations_json TEXT,
                    important_choices_json TEXT,
                    unresolved_conflicts_json TEXT,
                    updated_at REAL
                )
            """)

            # Character memories
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS character_memories (
                    id TEXT PRIMARY KEY,
                    player_id TEXT NOT NULL,
                    npc_name TEXT NOT NULL,
                    event_summary TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    created_at REAL
                )
            """)

            # Learning progress
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_progress (
                    player_id TEXT PRIMARY KEY,
                    concepts_json TEXT,
                    completed_puzzles_json TEXT,
                    unlocked_reveals_json TEXT,
                    attempts_json TEXT,
                    hint_uses_json TEXT,
                    updated_at REAL
                )
            """)

            # Interaction history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interaction_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    location TEXT NOT NULL,
                    scene_title TEXT,
                    created_at REAL
                )
            """)
            conn.commit()
            logger.info(f"Initialized SQLite storage at '{self.db_path}'")

    # --- Profile Operations ---
    def save_player_profile(self, profile_dict: Dict[str, Any]):
        player_id = profile_dict.get("id", "player_default")
        traits = json.dumps(profile_dict.get("traits", {}))
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO player_profiles
                (player_id, name, role, adventure_style, traits_json, current_quest_id, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id,
                profile_dict.get("name", "Aria"),
                profile_dict.get("role", "Clockwork Scholar"),
                profile_dict.get("adventure_style", "Analytical"),
                traits,
                profile_dict.get("current_quest_id", "quest_water_crisis"),
                time.time()
            ))
            conn.commit()

    def get_player_profile(self, player_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM player_profiles WHERE player_id = ?", (player_id,)).fetchone()
            if not row:
                return None
            return {
                "id": row["player_id"],
                "name": row["name"],
                "role": row["role"],
                "adventure_style": row["adventure_style"],
                "traits": json.loads(row["traits_json"]) if row["traits_json"] else {},
                "current_quest_id": row["current_quest_id"],
                "created_at": row["updated_at"]
            }

    # --- World State Operations ---
    def save_world_state(self, player_id: str, state_dict: Dict[str, Any]):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO world_states
                (player_id, kingdom, current_location, water_supply, forest_spirit_trust,
                 clockwork_guardian, village_morale, completed_quests_json,
                 discovered_locations_json, important_choices_json, unresolved_conflicts_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id,
                state_dict.get("kingdom", "Elarion"),
                state_dict.get("current_location", "Whispering Village"),
                state_dict.get("water_supply", "damaged"),
                int(state_dict.get("forest_spirit_trust", 0)),
                state_dict.get("clockwork_guardian", "inactive"),
                int(state_dict.get("village_morale", 60)),
                json.dumps(state_dict.get("completed_quests", [])),
                json.dumps(state_dict.get("discovered_locations", ["Whispering Village"])),
                json.dumps(state_dict.get("important_choices", [])),
                json.dumps(state_dict.get("unresolved_conflicts", [])),
                time.time()
            ))
            conn.commit()

    def get_world_state(self, player_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM world_states WHERE player_id = ?", (player_id,)).fetchone()
            if not row:
                return None
            return {
                "kingdom": row["kingdom"],
                "current_location": row["current_location"],
                "water_supply": row["water_supply"],
                "forest_spirit_trust": row["forest_spirit_trust"],
                "clockwork_guardian": row["clockwork_guardian"],
                "village_morale": row["village_morale"],
                "completed_quests": json.loads(row["completed_quests_json"] or "[]"),
                "discovered_locations": json.loads(row["discovered_locations_json"] or "[]"),
                "important_choices": json.loads(row["important_choices_json"] or "[]"),
                "unresolved_conflicts": json.loads(row["unresolved_conflicts_json"] or "[]")
            }

    # --- Character Memory Operations ---
    def add_character_memory(self, player_id: str, npc_name: str, event_summary: str, sentiment: str = "neutral"):
        mem_id = f"mem_{int(time.time() * 1000)}"
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO character_memories (id, player_id, npc_name, event_summary, sentiment, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (mem_id, player_id, npc_name, event_summary, sentiment, time.time()))
            conn.commit()

    def get_character_memories(self, player_id: str, npc_name: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            if npc_name:
                rows = conn.execute(
                    "SELECT * FROM character_memories WHERE player_id = ? AND npc_name = ? ORDER BY created_at DESC",
                    (player_id, npc_name)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM character_memories WHERE player_id = ? ORDER BY created_at DESC",
                    (player_id,)
                ).fetchall()
            return [
                {
                    "id": r["id"],
                    "npc_name": r["npc_name"],
                    "event_summary": r["event_summary"],
                    "sentiment": r["sentiment"],
                    "created_at": r["created_at"]
                }
                for r in rows
            ]

    # --- Learning Progress ---
    def save_learning_progress(self, player_id: str, progress_dict: Dict[str, Any]):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO learning_progress
                (player_id, concepts_json, completed_puzzles_json, unlocked_reveals_json, attempts_json, hint_uses_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                player_id,
                json.dumps(progress_dict.get("concepts_encountered", [])),
                json.dumps(progress_dict.get("completed_puzzles", [])),
                json.dumps(progress_dict.get("unlocked_reveals", [])),
                json.dumps(progress_dict.get("attempts", {})),
                json.dumps(progress_dict.get("hint_uses", {})),
                time.time()
            ))
            conn.commit()

    def get_learning_progress(self, player_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM learning_progress WHERE player_id = ?", (player_id,)).fetchone()
            if not row:
                return None
            return {
                "concepts_encountered": json.loads(row["concepts_json"] or "[]"),
                "completed_puzzles": json.loads(row["completed_puzzles_json"] or "[]"),
                "unlocked_reveals": json.loads(row["unlocked_reveals_json"] or "[]"),
                "attempts": json.loads(row["attempts_json"] or "{}"),
                "hint_uses": json.loads(row["hint_uses_json"] or "{}")
            }

    # --- Interaction History ---
    def record_interaction(self, player_id: str, action: str, location: str, scene_title: str):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO interaction_history (player_id, action, location, scene_title, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (player_id, action, location, scene_title, time.time()))
            conn.commit()

    def get_recent_interactions(self, player_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM interaction_history
                WHERE player_id = ?
                ORDER BY created_at DESC LIMIT ?
            """, (player_id, limit)).fetchall()
            return [
                {
                    "action": r["action"],
                    "location": r["location"],
                    "scene_title": r["scene_title"],
                    "created_at": r["created_at"]
                }
                for r in reversed(rows)
            ]

    # --- Session Reset ---
    def reset_session(self, player_id: str):
        """Purges saved session data safely for the specified player_id."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM player_profiles WHERE player_id = ?", (player_id,))
            conn.execute("DELETE FROM world_states WHERE player_id = ?", (player_id,))
            conn.execute("DELETE FROM character_memories WHERE player_id = ?", (player_id,))
            conn.execute("DELETE FROM learning_progress WHERE player_id = ?", (player_id,))
            conn.execute("DELETE FROM interaction_history WHERE player_id = ?", (player_id,))
            conn.commit()
            logger.info(f"Reset session for player '{player_id}'")

_storage_instance: Optional[SQLiteStorage] = None

def get_storage(db_path: str = "mythcode_storage.db") -> SQLiteStorage:
    global _storage_instance
    if _storage_instance is None or _storage_instance.db_path != db_path:
        _storage_instance = SQLiteStorage(db_path)
    return _storage_instance
