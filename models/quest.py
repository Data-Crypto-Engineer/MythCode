"""
Quest models and progression tracking.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class QuestPathway:
    id: str
    title: str
    description: str
    location: str
    recommended_agent: str
    associated_concept: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Quest:
    id: str
    title: str
    description: str
    stage: str
    pathways: List[QuestPathway] = field(default_factory=list)
    completed: bool = False
    outcome: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "stage": self.stage,
            "pathways": [p.to_dict() if isinstance(p, QuestPathway) else p for p in self.pathways],
            "completed": self.completed,
            "outcome": self.outcome,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Quest":
        raw_pathways = data.get("pathways", [])
        pathways = [
            QuestPathway(**p) if isinstance(p, dict) else p
            for p in raw_pathways
        ]
        return cls(
            id=data.get("id", "quest_water_crisis"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            stage=data.get("stage", "investigation"),
            pathways=pathways,
            completed=data.get("completed", False),
            outcome=data.get("outcome")
        )
