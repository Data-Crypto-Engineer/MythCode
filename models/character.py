"""
Character models and persistent NPC memories.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

@dataclass
class CharacterMemory:
    id: str
    npc_name: str
    player_id: str
    event_summary: str
    sentiment: str  # "positive", "neutral", "skeptical"
    timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class NPCState:
    name: str
    role: str
    current_location: str
    relationship_level: int = 0
    dialogue_history: List[str] = field(default_factory=list)
    known_facts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NPCState":
        return cls(
            name=data.get("name", "Unknown"),
            role=data.get("role", "Citizen"),
            current_location=data.get("current_location", "Whispering Village"),
            relationship_level=int(data.get("relationship_level", 0)),
            dialogue_history=list(data.get("dialogue_history", [])),
            known_facts=list(data.get("known_facts", []))
        )
