"""
Player models and adaptive trait structures for MythCode.
Expanded to support expressive character customization, companions, and magical affinities.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List
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
    pronouns: str = "they/them"
    role: str = "Rune Engineer"
    appearance: str = "Inquisitive scholar with brass-tinted goggles"
    hair_style: str = "Braided crown"
    hair_color: str = "Auburn"
    outfit: str = "Leather scholar coat with enchanted rune pockets"
    magical_affinity: str = "Arcane"  # Nature, Light, Water, Fire, Wind, Arcane
    personality: str = "Curious & Patient"
    companion: str = "Clockwork Owl"  # Clockwork Owl, Sylvan Sprite, Runestone Fox, Ember Salamander, Zephyr Finch
    learning_style: str = "Hands-on Experimentation"
    keepsake: str = "Brass Chrono-Gear"  # Brass Chrono-Gear, Star-Blossom, River Prism, Carved Rune-Tablet
    adventure_style: str = "Analytical"
    xp: int = 0
    level: int = 1
    inventory: List[str] = field(default_factory=lambda: ["Explorer's Journal", "Brass Chrono-Gear"])
    traits: AdaptiveTraits = field(default_factory=AdaptiveTraits)
    current_quest_id: str = "quest_water_crisis"
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "pronouns": self.pronouns,
            "role": self.role,
            "appearance": self.appearance,
            "hair_style": self.hair_style,
            "hair_color": self.hair_color,
            "outfit": self.outfit,
            "magical_affinity": self.magical_affinity,
            "personality": self.personality,
            "companion": self.companion,
            "learning_style": self.learning_style,
            "keepsake": self.keepsake,
            "adventure_style": self.adventure_style,
            "xp": self.xp,
            "level": self.level,
            "inventory": list(self.inventory),
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
            pronouns=data.get("pronouns", "they/them"),
            role=data.get("role", "Rune Engineer"),
            appearance=data.get("appearance", "Inquisitive scholar with brass-tinted goggles"),
            hair_style=data.get("hair_style", "Braided crown"),
            hair_color=data.get("hair_color", "Auburn"),
            outfit=data.get("outfit", "Leather scholar coat with enchanted rune pockets"),
            magical_affinity=data.get("magical_affinity", "Arcane"),
            personality=data.get("personality", "Curious & Patient"),
            companion=data.get("companion", "Clockwork Owl"),
            learning_style=data.get("learning_style", "Hands-on Experimentation"),
            keepsake=data.get("keepsake", "Brass Chrono-Gear"),
            adventure_style=data.get("adventure_style", "Analytical"),
            xp=int(data.get("xp", 0)),
            level=int(data.get("level", 1)),
            inventory=list(data.get("inventory", ["Explorer's Journal", "Brass Chrono-Gear"])),
            traits=traits,
            current_quest_id=data.get("current_quest_id", "quest_water_crisis"),
            created_at=data.get("created_at", time.time()),
        )
