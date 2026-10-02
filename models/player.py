"""
Player models and adaptive trait structures.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any
import time

@dataclass
class AdaptiveTraits:
    exploration_preference: float = 0.50
    dialogue_preference: float = 0.50
    puzzle_preference: float = 0.50
    building_preference: float = 0.50
    challenge_level: int = 1
    concept_mastery: Dict[str, float] = field(default_factory=lambda: {
        "sequence": 0.0,
        "conditions": 0.0,
        "loops": 0.0
    })

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdaptiveTraits":
        if not data:
            return cls()
        mastery = data.get("concept_mastery", {"sequence": 0.0, "conditions": 0.0, "loops": 0.0})
        return cls(
            exploration_preference=float(data.get("exploration_preference", 0.50)),
            dialogue_preference=float(data.get("dialogue_preference", 0.50)),
            puzzle_preference=float(data.get("puzzle_preference", 0.50)),
            building_preference=float(data.get("building_preference", 0.50)),
            challenge_level=int(data.get("challenge_level", 1)),
            concept_mastery=mastery
        )

@dataclass
class PlayerProfile:
    id: str = "player_default"
    name: str = "Aria"
    role: str = "Clockwork Scholar"
    adventure_style: str = "Analytical"
    traits: AdaptiveTraits = field(default_factory=AdaptiveTraits)
    current_quest_id: str = "quest_water_crisis"
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "adventure_style": self.adventure_style,
            "traits": self.traits.to_dict(),
            "current_quest_id": self.current_quest_id,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerProfile":
        traits_data = data.get("traits", {})
        traits = AdaptiveTraits.from_dict(traits_data)
        return cls(
            id=data.get("id", "player_default"),
            name=data.get("name", "Aria"),
            role=data.get("role", "Clockwork Scholar"),
            adventure_style=data.get("adventure_style", "Analytical"),
            traits=traits,
            current_quest_id=data.get("current_quest_id", "quest_water_crisis"),
            created_at=data.get("created_at", time.time()),
        )
