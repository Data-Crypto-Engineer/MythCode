"""
Learning models, puzzle specifications, and code reveal structures.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

@dataclass
class PythonConceptReveal:
    concept_name: str
    explanation: str
    code_snippet: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class PuzzleChallenge:
    id: str
    concept: str
    title: str
    description: str
    hint: str
    python_reveal: PythonConceptReveal
    grid_size: Optional[List[int]] = None
    start_position: Optional[List[int]] = None
    goal_position: Optional[List[int]] = None
    required_steps: Optional[List[str]] = None
    available_options: Optional[List[Dict[str, Any]]] = None
    target_count: Optional[int] = None
    correct_action: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if isinstance(self.python_reveal, PythonConceptReveal):
            d["python_reveal"] = self.python_reveal.to_dict()
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PuzzleChallenge":
        reveal_data = data.get("python_reveal", {})
        if isinstance(reveal_data, dict):
            reveal = PythonConceptReveal(**reveal_data)
        else:
            reveal = reveal_data
        return cls(
            id=data.get("id", ""),
            concept=data.get("concept", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            hint=data.get("hint", ""),
            python_reveal=reveal,
            grid_size=data.get("grid_size"),
            start_position=data.get("start_position"),
            goal_position=data.get("goal_position"),
            required_steps=data.get("required_steps"),
            available_options=data.get("available_options"),
            target_count=data.get("target_count"),
            correct_action=data.get("correct_action"),
        )

@dataclass
class LearningProgress:
    concepts_encountered: List[str] = field(default_factory=list)
    completed_puzzles: List[str] = field(default_factory=list)
    unlocked_reveals: List[Dict[str, Any]] = field(default_factory=list)
    attempts: Dict[str, int] = field(default_factory=dict)
    hint_uses: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LearningProgress":
        if not data:
            return cls()
        return cls(
            concepts_encountered=list(data.get("concepts_encountered", [])),
            completed_puzzles=list(data.get("completed_puzzles", [])),
            unlocked_reveals=list(data.get("unlocked_reveals", [])),
            attempts=dict(data.get("attempts", {})),
            hint_uses=dict(data.get("hint_uses", {}))
        )
