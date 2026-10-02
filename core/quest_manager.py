"""
Quest Manager for handling mission progression, pathways, and discoveries.
"""
from typing import Dict, Any, List, Optional
import json
import os
from models.quest import Quest, QuestPathway

class QuestManager:
    """Tracks active missions, branches, and outcomes."""

    def __init__(self, quests_file: str = "data/quests.json"):
        self.quests: Dict[str, Quest] = {}
        self._load_quests(quests_file)

    def _load_quests(self, path: str):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data.get("quests", []):
                q = Quest.from_dict(item)
                self.quests[q.id] = q

    def get_quest(self, quest_id: str) -> Optional[Quest]:
        return self.quests.get(quest_id)

    def get_all_quests(self) -> List[Quest]:
        return list(self.quests.values())

    def update_quest_stage(self, quest_id: str, new_stage: str, outcome: Optional[str] = None):
        quest = self.get_quest(quest_id)
        if quest:
            quest.stage = new_stage
            if outcome:
                quest.outcome = outcome
            if new_stage in ("completed", "resolved"):
                quest.completed = True

    def check_crisis_resolution(self, water_supply: str, completed_puzzles: List[str]) -> bool:
        """Determines if the main village water crisis has been solved."""
        has_solved_enough = len(completed_puzzles) >= 2 or water_supply == "restored"
        return has_solved_enough
