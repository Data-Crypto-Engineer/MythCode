"""
World state models and validation boundaries.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any

@dataclass
class WorldState:
    kingdom: str = "Elarion"
    current_location: str = "Whispering Village"
    water_supply: str = "damaged"
    forest_spirit_trust: int = 0
    clockwork_guardian: str = "inactive"
    village_morale: int = 60
    completed_quests: List[str] = field(default_factory=list)
    discovered_locations: List[str] = field(default_factory=lambda: ["Whispering Village"])
    available_locations: List[str] = field(default_factory=lambda: ["Whispering Village", "Ancient Grove", "River Aqueduct"])
    important_choices: List[Dict[str, Any]] = field(default_factory=list)
    unresolved_conflicts: List[str] = field(default_factory=lambda: [
        "The village water reservoir is bone-dry and crops are withering.",
        "A dormant clockwork sentinel blocks the ancient conduit."
    ])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldState":
        if not data:
            return cls()
        return cls(
            kingdom=data.get("kingdom", "Elarion"),
            current_location=data.get("current_location", "Whispering Village"),
            water_supply=data.get("water_supply", "damaged"),
            forest_spirit_trust=int(data.get("forest_spirit_trust", 0)),
            clockwork_guardian=data.get("clockwork_guardian", "inactive"),
            village_morale=int(data.get("village_morale", 60)),
            completed_quests=list(data.get("completed_quests", [])),
            discovered_locations=list(data.get("discovered_locations", ["Whispering Village"])),
            available_locations=list(data.get("available_locations", ["Whispering Village", "Ancient Grove", "River Aqueduct"])),
            important_choices=list(data.get("important_choices", [])),
            unresolved_conflicts=list(data.get("unresolved_conflicts", []))
        )
